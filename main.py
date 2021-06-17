import datetime
from typing import Optional

import uvicorn
import sqlite3
import os

from fastapi import Request, Cookie, FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from starlette.responses import RedirectResponse
from starlette.staticfiles import StaticFiles
from urllib.parse import urlencode, unquote, quote

from cookie import set_cookie
from errors import http_exceptions_handler, request_validation_error_handler
from database import get_use_case, use_case_dict, update_db_user, get_number_of_completed_use_cases

# create and load the DB. Using sqlite3 since that's the easiest IMO
db_name = 'user_data.db'
first_start = not os.path.isfile(db_name)
con = sqlite3.connect(db_name)

# add table to db if first start
if first_start:
    con.execute("""
        CREATE TABLE
            use_cases
            (user_id TEXT, use_case_id SMALLINT, use_case_step SMALLINT, user_emotion JSON, datetime TIMESTAMP WITH TIME ZONE, PRIMARY KEY (user_id, use_case_id, use_case_step));
    """)

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

    return templates.TemplateResponse("root.html", {
        "request": request,
        "user_id": user_id,
        "use_case_count": len(use_case_dict),
        "use_case_count_current": get_number_of_completed_use_cases(con, user_id),
        "use_case_id": use_case_info["use_case_id"],
        "use_case_step": use_case_info["use_case_step"]
    })


# show the user a use case
@app.get('/usecase')
async def use_case(request: Request, use_case_id: int, use_case_step: int, progress_saved: bool = False,
                   user_id: str = Cookie(None)):
    # todo make cool popup that results were saved
    if progress_saved:
        pass

    # todo get the user emotion if not specified

    # todo special behaviour is the seond use case step is given

    use_case_response = "abc"
    user_emotion = {}

    return templates.TemplateResponse("use_case.html", {
        "request": request,
        "user_id": user_id,
        "use_case_count": len(use_case_dict),
        "use_case_count_current": a,
        "use_case_text": use_case_dict[use_case_id],
        "use_case_id": use_case_id,
        "use_case_step": use_case_step,
        "use_case_response": use_case_response,
        "user_emotion": user_emotion,
        "saved": progress_saved
    })

    # todo call limesurvey twice. First with emotion based response, sencond without
    # todo for that, first call limesurvey, then call a redirect url, that redirect back to limesurvey if the use_case_step is 1

    # todo set cookie with id and overview which usecases are still missing

    # https://limesurvey.rz.tu-bs.de/index.php/742517?newtest=Y&lang=de&userid=asdsbxdfsdf&usecaseid=1&usecasestep=1&usecaseresponse=asghdgasldhgaszhjdg&nextresponse=jasdhjasöd


# use this url to redirect the limesurvey results
@app.get('/limesurvey', response_class=HTMLResponse)
async def limesurvey(user_id: str, use_case_id: int, use_case_step: int, user_emotion: str, next_response: str):
    # convert user emotion back to a dict, since it is urlencoded
    user_emotion = eval(unquote(user_emotion))

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
            "useremotion": quote(str(user_emotion)),
            "nextresponse": None,
        }
        redirect_path = f"https://limesurvey.rz.tu-bs.de/index.php/742517?{urlencode(params)}"

    # if yes, get a new use case and start over
    else:
        use_case_info = get_use_case(con, user_id)

        params = {
            "use_case_id": use_case_info["use_case_id"],
            "use_case_step": use_case_info["use_case_step"],
            "progress_saved": True,
        }
        redirect_path = f"/usecase?{urlencode(params)}"

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
