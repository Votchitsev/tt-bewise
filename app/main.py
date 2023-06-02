from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from .db import database
from .questionsAPI import QuestionsAPI
from .interface import QuestionsQuery


app = FastAPI(title='Bewise test task 1')

questions_api = QuestionsAPI('https://jservice.io/api/random')

templates = Jinja2Templates(directory='app/templates')


@app.get('/', response_class=HTMLResponse)
def root(request: Request):
    return templates.TemplateResponse('index.html', context={'request': request})


@app.post('/')
async def questions(query: QuestionsQuery):
    questions_count = query.questions_num

    prev_questions = await questions_api.get_questions(questions_count)

    return prev_questions


@app.on_event('startup')
async def startup():
    if not database.is_connected:
        await database.connect()


@app.on_event('shutdown')
async def shutdown():
    if database.is_connected:
        await database.disconnect()
