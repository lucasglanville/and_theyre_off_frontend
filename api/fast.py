import pandas as pd
import numpy as np
import requests
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json

class Prediction(BaseModel):
    df: str

#uvicorn fast:app --reload

app = FastAPI()

# @app.get("/api-test")
# def api_test():
#   return {"This API" : "is working"}

# @app.get("/hello-name")
# def hello(name: str, surname: str):
#   return {'Hello ' : f'{name} {surname}!'}

# @app.get("/my-sum")
# def my_sum(num1: int, num2: int, num3: int):
#     res = sum([num1, num2, num3])
#     return {"The Sum is" : res}


@app.get("/predict")
def predict():

    # from our_module_1 import load_model
    # from our_module_2 import preprocess_features

    ### PREPROCESS DATA ###
    processed_data = preprocess_features_v2()

    ### LOAD MODEL & MAKE PREDICTION ON PROCESSED DATA

    model
    predicted_probs = round(float(model.predict(processed_data)),4)

    ### COMPARE PREDICTED PROBABILITIES,
    ### RETURN MINIMUM ODDS REQUIRED TO BET FOR EVERY HORSE


