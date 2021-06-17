import datetime
from typing import Optional

import uvicorn
import sqlite3
import os

from fastapi import Request, Cookie, FastAPI, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from starlette.responses import RedirectResponse
from starlette.staticfiles import StaticFiles
from urllib.parse import urlencode

from cookie import set_cookie
from errors import http_exceptions_handler, request_validation_error_handler
from database import get_use_case, update_db_user, get_number_of_completed_use_cases, user_is_new, create_db_tables, \
    update_email
from config import use_case_dict, limesurvey_url, limesurvey_user_info_url

# create and load the DB. Using sqlite3 since that's the easiest IMO
db_name = 'user_data.db'
first_start = not os.path.isfile(db_name)
con = sqlite3.connect(db_name)

# add table to db if first start
if first_start:
    create_db_tables(con)

# mount the webserver to /static
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

# load templates
templates = Jinja2Templates(directory="templates")

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
    use_case_info = get_use_case(con, user_id)

    # if not more use cases are to be done
    if not use_case_info:
        return RedirectResponse("/thanks", status_code=303)

    # check if the user is new (has not completed a single use case step)
    if user_is_new(con, user_id):
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
        "use_case_count": len(use_case_dict),
        "use_case_count_current": get_number_of_completed_use_cases(con, user_id),
        "continue_button_url": continue_button_url,
    })


# show the user a guide on how to use the site
@app.get('/guide')
async def guide(request: Request, use_case_id: int, use_case_step: int, user_id: str = Cookie(None)):
    # todo guide how this works if the user is new. Maybe with carousel?
    # https://getbootstrap.com/docs/5.0/components/carousel/

    guide_text = "temp"

    # define params needed to build the link to the limesurvey user data collection
    params = {
        "userid": user_id,
        "usecaseid": use_case_id,
        "usecasestep": use_case_step,
    }

    return templates.TemplateResponse("guide.html", {
        "request": request,
        "user_id": user_id,
        "use_case_count": len(use_case_dict),
        "use_case_count_current": get_number_of_completed_use_cases(con, user_id),
        "guide_text": guide_text,
        "use_case_url": f"{limesurvey_user_info_url}?{urlencode(params)}",
    })


# show the user a use case
@app.get('/usecase')
async def use_case(request: Request, use_case_id: int, use_case_step: int, progress_saved: bool = False, from_limesurvey_user_data_collection: bool = False, user_id: str = Cookie(None)):
    # if user comes from the user data collection aka limesurvey, save their id in the DB with use_case_id = 0
    if from_limesurvey_user_data_collection:
        update_db_user(con, user_id, 0, None, None, datetime.datetime.now(tz=datetime.timezone.utc))

    # todo get the user emotion if not specified

    # todo special behaviour is the seond use case step is given

    use_case_response = "abc"
    next_response = "def"
    user_emotion = {1: 2, "asidajsd": "asdipojäasd"}

    # define params needed to build the limesurvey link later
    limesurvey_params = {
        "newtest": "Y",
        "lang": "de",
        "userid": user_id,
        "usecaseid": use_case_id,
        "usecasestep": use_case_step,
        "usecaseresponse": use_case_response,
        "useremotion": '|'.join([f"{i}:{j}" for i, j in user_emotion.items()]),     # convert the dict into a pure string because limesurvey doesnt like "{" in strings
        "nextresponse": next_response,
    }

    return templates.TemplateResponse("use_case.html", {
        "request": request,
        "user_id": user_id,
        "use_case_count": len(use_case_dict),
        "use_case_count_current": get_number_of_completed_use_cases(con, user_id),
        "use_case_text": use_case_dict[use_case_id],
        "limesurvey_url": f"{limesurvey_url}?{urlencode(limesurvey_params)}",
        "saved": bool(progress_saved or from_limesurvey_user_data_collection),
    })


# use this url to redirect the limesurvey results
@app.get('/limesurvey', response_class=HTMLResponse)
async def limesurvey(user_id: str, use_case_id: int, use_case_step: int, user_emotion: str, next_response: str):
    # convert user emotion back to a dict, since it is encoded
    user_emotion = {j[0]: j[1] for j in [i.split(":") for i in user_emotion.split("|")]}

    # save progress in DB
    update_db_user(con, user_id, use_case_id, use_case_step, user_emotion, datetime.datetime.now(tz=datetime.timezone.utc))

    # check if the user has filled out both parts
    # if no, redirect them back to limesurvey
    if use_case_step == 1:
        params = {
            "lang": "de",
            "newtest": "Y",
            "userid": user_id,
            "usecaseid": use_case_id,
            "usecasestep": 2,
            "usecaseresponse": next_response,
            "useremotion": '|'.join([f"{i}:{j}" for i, j in user_emotion.items()]),     # convert the dict into a pure string because limesurvey doesnt like "{" in strings
            "nextresponse": None,
        }
        redirect_path = f"{limesurvey_url}?{urlencode(params)}"

    # if yes, get a new use case and start over
    else:
        use_case_info = get_use_case(con, user_id)

        # if not more use cases are to be done
        if not use_case_info:
            return RedirectResponse("/thanks", status_code=303)

        params = {
            "use_case_id": use_case_info["use_case_id"],
            "use_case_step": use_case_info["use_case_step"],
            "progress_saved": True,
        }
        redirect_path = f"/usecase?{urlencode(params)}"

    return RedirectResponse(redirect_path, status_code=303)


# set a new cookie with a new ID and redirects to home. Mostly used for testing
@app.get('/thanks', response_class=HTMLResponse)
async def thanks(request: Request, user_id: str = Cookie(None), email_saved: bool = False):
    # todo if there are no more use cases, redirect to thank you site
    # todo maybe ask for mail to participate in giveaway or sth
    return templates.TemplateResponse("thanks.html", {
        "request": request,
        "user_id": user_id,
        "use_case_count": len(use_case_dict),
        "use_case_count_current": get_number_of_completed_use_cases(con, user_id),
        "email_saved": email_saved,
    })


# saves / update the users giveaway email and returns them to the thanks you site with a toast
@app.post('/giveawayemail')
async def save_email(email: str = Form(...), user_id: str = Cookie(None)):
    # update email
    update_email(con, user_id, email)

    # direct them back
    params = {
        "email_saved": True,
    }
    redirect_path = f"/thanks?{urlencode(params)}"
    return RedirectResponse(redirect_path, status_code=303)


# set a new cookie with a new ID and redirects to home. Mostly used for testing
@app.get('/newcookie', response_class=HTMLResponse)
async def new_cookie():
    return set_cookie("/")


# close DB on shutdown
@app.on_event("shutdown")
async def shutdown_event():
    con.close()


# start the server
uvicorn.run(app, host="0.0.0.0", port=8000)
