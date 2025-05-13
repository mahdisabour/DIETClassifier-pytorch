import sys
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from prometheus_fastapi_instrumentator import Instrumentator
from logger import LogClass

from src.utils.convert import convert_diet_result
from src.models.wrapper import DIETClassifierWrapper


sys.path.append(os.getcwd())
log = LogClass.get_logger(name="main")

CONFIG_FILE = "src/config.yml"

wrapper = DIETClassifierWrapper(CONFIG_FILE)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Instrumentator().instrument(app).expose(app)

@app.get("/detect")
async def detect(input: str):
    output = wrapper.predict([input])[0]

    del output["intent_ranking"]

    response = jsonable_encoder(output)
    response = convert_diet_result(response)
    return JSONResponse(response)
