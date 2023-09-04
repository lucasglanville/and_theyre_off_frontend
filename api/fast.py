import pandas as pd
import numpy as np
import requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

#uvicorn fast:app --reload

app = FastAPI()

@app.get("/api-test")
def api_test():
  return {"This API" : "is working"}

@app.get("/hello-name")
def hello(name: str, surname: str):
  return {'Hello ' : f'{name} {surname}!'}

@app.get("/my-sum")
def my_sum(num1: int, num2: int, num3: int):
    res = sum([num1, num2, num3])
    return {"The Sum is" : res}



# @app.get("/predict")
# def predict():

#     # from our_module_1 import load_model
#     # from our_module_2 import preprocess_features

#     ### PREPROCESS DATA ###
#     processed_data = preprocess_features(data)

#     ### LOAD MODEL & MAKE PREDICTION ON PROCESSED DATA
#     model = load_model()
#     predicted_probs = round(float(model.predict(processed_data)),4)

#     ### COMPARE PREDICTED PROBABILITIES,
#     ### RETURN MINIMUM ODDS REQUIRED TO BET FOR EVERY HORSE

#     threshold = 0.1
#     required_odds = [1/(x-threshold) for x in predicted_probs]

#     #RETURN IN DICTIONARY FORMAT FOR API
#     return {'odds': predicted_probs,
#             'required odds to bet': required_odds}
