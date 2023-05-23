from fastapi import FastAPI
from .db import database


app = FastAPI(title='Bewise test task 1')


@app.get('/')
async def root():
    return 'Hello world'


@app.on_event('startup')
async def startup():
    if not database.is_connected:
        await database.connect()


@app.on_event('shutdown')
async def shutdown():
    if database.is_connected:
        await database.disconnect()