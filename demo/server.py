from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from src.utils.convert import convert_diet_result

import sys
import os

sys.path.append(os.getcwd())

from src.models.wrapper import DIETClassifierWrapper

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


@app.get("/detect")
async def detect(input: str):
    output = wrapper.predict([input])[0]

    del output["intent_ranking"]

    response = jsonable_encoder(output)
    # response = convert_diet_result(response)
    return JSONResponse(response)
