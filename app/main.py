import datetime
from typing import Optional

from fastapi import Request, Cookie, FastAPI, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from starlette.responses import RedirectResponse
from starlette.staticfiles import StaticFiles
from urllib.parse import urlencode

from app.cookie import set_cookie
from app.errors import http_exceptions_handler, request_validation_error_handler
from app.database import get_db, Database
from app.config import use_case_dict, limesurvey_use_case_evaluation, limesurvey_user_info_url, emotions_dict, \
    limesurvey_interface_evaluation, experiment_steps

db: Database = None

# mount the webserver to /static
app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.mount("/dist", StaticFiles(directory="app/dist"), name="dist")

# load templates
templates = Jinja2Templates(directory="app/templates")

# add error handlers
app.add_exception_handler(HTTPException, http_exceptions_handler)
app.add_exception_handler(RequestValidationError, request_validation_error_handler)


# This middleware makes sure there always is a cookie with a unique user ID
@app.middleware("http")
async def check_for_cookie(request: Request, call_next):
    user_id = request.cookies.get("user_id")

    # check if cookie is set. If not set it and redirect to same page
    if not user_id:
        return set_cookie(request.base_url.path)

    # execute normal call
    response = await call_next(request)
    return response


# root
@app.get('/', response_class=HTMLResponse)
async def root(request: Request, user_id: Optional[str] = Cookie(None)):
    # get a random use case to show the user
    use_case_info = await db.get_use_case(user_id)

    # if not more use cases are to be done
    if await db.user_is_done(user_id):
        return RedirectResponse("/thanks", status_code=303)
    # if user has done step two
    elif not use_case_info:
        use_case_info = await db.get_in_progress_use_case(user_id)
        params = {
            "use_case_id": use_case_info["use_case_id"],
            "use_case_step": use_case_info["use_case_step"],
            "progress_saved": False
        }
        redirect_url = f"/afterusecaseemotion?{urlencode(params)}"
        return RedirectResponse(redirect_url, status_code=303)

    # check if the user is new (has not completed a single use case step)
    if await db.user_is_new(user_id):
        url = "/guide"
    else:
        url = "/usecase"

    # build continue button url
    params = {
        "use_case_id": use_case_info["use_case_id"],
        "use_case_step": use_case_info["use_case_step"]
    }
    continue_button_url = f"{url}?{urlencode(params)}"

    return templates.TemplateResponse("root.html", {
        "request": request,
        "user_id": user_id,
        "use_case_count": experiment_steps,
        "use_case_count_current": await db.get_number_of_completed_use_cases(user_id),
        "continue_button_url": continue_button_url,
    })


# show the user a guide on how to use the site
@app.get('/guide')
async def guide(request: Request, use_case_id: int, use_case_step: int, user_id: str = Cookie(None)):
    estimate_time_needed = 999999

    # define params needed to build the link to the limesurvey user data collection
    params = {
        "userid": user_id,
        "usecaseid": use_case_id,
        "usecasestep": use_case_step,
    }

    return templates.TemplateResponse("guide.html", {
        "request": request,
        "user_id": user_id,
        "use_case_count": experiment_steps,
        "use_case_count_current": await db.get_number_of_completed_use_cases(user_id),
        "use_case_url": f"{limesurvey_user_info_url}?{urlencode(params)}",
        "estimate_time_needed": estimate_time_needed,
    })


# show the user a use case
@app.get('/usecase')
async def use_case(request: Request, use_case_id: int, use_case_step: int, progress_saved: bool = False, from_limesurvey_user_data_collection: bool = False, user_id: str = Cookie(None)):
    # if user comes from the user data collection aka limesurvey, save their id in the DB with use_case_id = 0
    if from_limesurvey_user_data_collection:
        await db.update_db_user(
            user_id=user_id,
            use_case_id=0,
            use_case_step=0,
            time=datetime.datetime.now(tz=datetime.timezone.utc),
        )

    return templates.TemplateResponse("use_case.html", {
        "request": request,
        "user_id": user_id,
        "use_case_count": experiment_steps,
        "use_case_count_current": await db.get_number_of_completed_use_cases(user_id),
        "use_case_text": use_case_dict[use_case_id],
        "usecaseid": use_case_id,
        "usecasestep": use_case_step,
        "saved": bool(progress_saved or from_limesurvey_user_data_collection),
        "emotions": emotions_dict
    })


# handle the form in /usecase
@app.post('/usecaseuseremotion')
async def use_case_user_emotion(use_case_id: int, use_case_step: int, user_emotion: str = Form(...), user_emotion_reason: str = Form(...), user_id: str = Cookie(None)):
    # build the dict which holds the emotion info from the form and is passed to limesurvey
    user_emotion_dict = {
        "user_emotion": user_emotion,
        "user_emotion_reason": user_emotion_reason,
    }

    # todo get response
    use_case_response = "abc"

    # define params needed to build the limesurvey link
    limesurvey_params = {
        "newtest": "Y",
        "lang": "de",
        "userid": user_id,
        "usecaseid": use_case_id,
        "usecasestep": use_case_step,
        "usecaseresponse": use_case_response,
        "useremotion": '|'.join([f"{i}:{j}" for i, j in user_emotion_dict.items()]),     # convert the dict into a pure string because limesurvey doesnt like "{" in strings
    }
    return RedirectResponse(f"{limesurvey_use_case_evaluation}?{urlencode(limesurvey_params)}", status_code=303)


# use this url to redirect the limesurvey results from the use case evaluation
@app.get('/limesurveyusecase', response_class=HTMLResponse)
async def limesurvey_use_case(user_id: str, use_case_id: int, use_case_step: int, user_emotion: str):
    # convert user emotion back to a dict, since it is encoded
    user_emotion = {j[0]: j[1] for j in [i.split(":") for i in user_emotion.split("|")]}

    # save progress in DB
    await db.update_db_user(
        user_id=user_id,
        use_case_id=use_case_id,
        use_case_step=use_case_step,
        time=datetime.datetime.now(tz=datetime.timezone.utc),
        user_emotion_before_response=user_emotion["user_emotion"],
        user_emotion_reason_before_response=user_emotion["user_emotion_reason"],
    )

    # redirect user to ask for their emotion after use case response
    params = {
        "use_case_id": use_case_id,
        "use_case_step": use_case_step,
    }
    redirect_path = f"/afterusecaseemotion?{urlencode(params)}"
    return RedirectResponse(redirect_path, status_code=303)


# ask the user for their emotion again
@app.get('/afterusecaseemotion')
async def after_use_case_emotion(request: Request, use_case_id: int, use_case_step: int, progress_saved: bool = True, user_id: str = Cookie(None)):
    return templates.TemplateResponse("after_use_case_emotion.html", {
        "request": request,
        "user_id": user_id,
        "use_case_count": experiment_steps,
        "use_case_count_current": await db.get_number_of_completed_use_cases(user_id),
        "usecaseid": use_case_id,
        "usecasestep": use_case_step,
        "emotions": emotions_dict,
        "saved": progress_saved,
    })


# redirect to limesurvey
@app.post('/afterusecaseemotiontolimsurvey')
async def after_use_case_emotion_to_limsurvey(use_case_id: int, use_case_step: int, user_emotion: str = Form(...), user_id: str = Cookie(None)):
    # save the new emotion in the DB in the entry for the use case
    await db.update_db_user(
        user_id=user_id,
        use_case_id=use_case_id,
        use_case_step=use_case_step,
        time=datetime.datetime.now(tz=datetime.timezone.utc),
        user_emotion_after_response=user_emotion,
    )

    # define params needed to build the limesurvey link
    limesurvey_params = {
        "newtest": "Y",
        "lang": "de",
        "userid": user_id,
    }
    return RedirectResponse(f"{limesurvey_interface_evaluation}?{urlencode(limesurvey_params)}", status_code=303)


# use this url to redirect the limesurvey results from the interface evaluation
@app.get('/limesurveyinterface', response_class=HTMLResponse)
async def limesurvey_interface(user_id: str):
    # save progress in DB
    await db.update_db_user(
        user_id=user_id,
        use_case_id=-1,
        use_case_step=-1,
        time=datetime.datetime.now(tz=datetime.timezone.utc),
    )

    # redirect user to thanks page
    return RedirectResponse("/thanks", status_code=303)


# set a new cookie with a new ID and redirects to home. Mostly used for testing
@app.get('/thanks', response_class=HTMLResponse)
async def thanks(request: Request, user_id: str = Cookie(None), email_saved: bool = False, comment_saved: bool = False):
    return templates.TemplateResponse("thanks.html", {
        "request": request,
        "user_id": user_id,
        "use_case_count": experiment_steps,
        "use_case_count_current": await db.get_number_of_completed_use_cases(user_id),
        "email_saved": email_saved,
        "comment_saved": comment_saved,
    })


# saves / update the users giveaway email and returns them to the thanks you site with a toast
@app.post('/giveawayemail')
async def save_email(email: str = Form(...), user_id: str = Cookie(None)):
    # update email
    await db.update_email(user_id, email)

    # direct them back
    params = {
        "email_saved": True,
    }
    redirect_path = f"/thanks?{urlencode(params)}"
    return RedirectResponse(redirect_path, status_code=303)


# saves / update if the users had a comment
@app.post('/comment')
async def user_comment(comment: str = Form(...), user_id: str = Cookie(None)):
    # update comment
    await db.update_comment(user_id, comment)

    # direct them back
    params = {
        "comment_saved": True,
    }
    redirect_path = f"/thanks?{urlencode(params)}"
    return RedirectResponse(redirect_path, status_code=303)


# set a new cookie with a new ID and redirects to home. Mostly used for testing
@app.get('/newcookie', response_class=HTMLResponse)
async def new_cookie():
    return set_cookie("/")


# open DB connection on startup
@app.on_event("startup")
async def startup_event():
    global db

    # connect to the DB
    db = await get_db()


# close DB on shutdown
@app.on_event("shutdown")
async def shutdown_event():
    await db.close()
