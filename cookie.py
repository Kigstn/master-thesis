import uuid

from starlette.responses import RedirectResponse


# This gives each user a unique ID and saves it in a cookie
def set_cookie(redirect_path: str) -> RedirectResponse:
    response = RedirectResponse(redirect_path, status_code=303)

    # generate a uuid for the user which will be used to identify them in this experiment. Needed for all following steps
    user_id = str(uuid.uuid4())

    # overwrite the cookie, if exists
    response.set_cookie(key="user_id", value=user_id)

    return response
