import sys,os
import pandas as pd

import certifi
ca=certifi.where()

from dotenv import load_dotenv
load_dotenv()
MONGO_DB_URL=os.getenv("MONGO_DB_URL")
print(MONGO_DB_URL)

import pymongo
from Network_security.exception.exception import NetworkSecurityexception
from Network_security.logging.logger import logging
from Network_security.pipeline.training_pipeline import TrainingPipeline

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile, Request 
from uvicorn import run as app_run
from fastapi.responses import Response
from starlette.responses import RedirectResponse

from Network_security.utils.main_utils.utils import load_object
from Network_security.utils.ml_utils.model.estimator import Networkmodel

client=pymongo.MongoClient(MONGO_DB_URL,tlsCAFile=ca) 

from Network_security.constant.training_pipeline import DATA_INGESTION_COLLECTION_NAME
from Network_security.constant.training_pipeline import DATA_INGESTION_DATABASE_NAME

database=client[DATA_INGESTION_DATABASE_NAME]
collection=client[DATA_INGESTION_COLLECTION_NAME]

app=FastAPI()
origins=["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi.templating import Jinja2Templates 
templates=Jinja2Templates(directory="./templates")

@app.get("/",tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")

@app.get('/train')
async def train_route():
    try:
        training_pipeline=TrainingPipeline()
        training_pipeline.run_pipeline()
        return Response("Training is successful") 
    except Exception as e:
        raise NetworkSecurityexception(e,sys)

@app.post('/predict')
async def predict_route(request:Request,file: UploadFile=File(...)):
    try:
        df=pd.read_csv(file.file)
        
        preprocessor=load_object("final_model/preprocessor.pkl")
        model=load_object("final_model/model.pkl")
        network_model=Networkmodel(preprocessor=preprocessor,model=model)
        print(df.iloc[0])
        y_pred=network_model.predict(df)
        print(y_pred)
        df['predicted_col']=y_pred
        print(df["predicted_col"])
        #df['predicted_column'].replace(-1, 0)
        #return df.to_json()
        df.to_csv("prediction_output/output.csv")  #after adding predicted column.. 
        table_html=df.to_html(classes="table table-striped")
        #print(table_html)
        return templates.TemplateResponse("table.html",{"request": request,"table": table_html})         

    except Exception as e:
        raise NetworkSecurityexception(e,sys)
    
if __name__=="__main__":
    app_run(app,host="localhost",port=8000)  