#!/shebang

from typing import Optional

from httpx import AsyncClient
from os import path
from fastapi import FastAPI, Header
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse


client, app = AsyncClient(), FastAPI()
templates = Jinja2Templates(directory="boilerplates")


async def frame(url, user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36 Edg/96.0.1054.29'):
    resp = await client.get(url, headers={'User-Agent': user_agent}, follow_redirects=True)
    resp.headers['X-Frame-Options'] = 'Allow'
    return resp.content.decode()


@app.get('/')
async def root():
    return {'message': 'Please refer to /docs path.'}


@app.get('/frame', response_class=HTMLResponse)
async def return_frame(url: str, user_agent: Optional[str] = Header(None)):
    resp = await frame(url, user_agent=user_agent)
    return resp


@app.get('/uniframe')
async def uniframe(url: Optional[str]):
    return templates.TemplateResponse("frame_basic_boilerplate.html", {"request": request, "url": f'/frame?url={url}'})


@app.get('/{path}')
def path(path):
    return {'path': path}
