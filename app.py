import uvicorn
import uuid

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse



# mount the webserver to /static
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

# load templates
templates = Jinja2Templates(directory="templates")


@app.get('/', response_class=HTMLResponse)
async def root(request: Request):
    # generate a uuid for the user which will be used to identify them though this experiment
    user_id = str(uuid.uuid4())

    return templates.TemplateResponse("root.html", {"request": request, "user_id": user_id})


@app.get('/test')
async def root(request: Request):
    print(request)
    return "Hi"


# start the server
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
