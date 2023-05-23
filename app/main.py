from pydantic import BaseModel

from fastapi import FastAPI
from .db import database
from .questionsAPI import QuestionsAPI


class QuestionsQuery(BaseModel):
    questions_num: int


app = FastAPI(title='Bewise test task 1')

questions_api = QuestionsAPI('https://jservice.io/api/random')


@app.get('/')
async def root():
    return 'Hello world'


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
