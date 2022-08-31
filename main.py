from typing import Optional
import pandas as pd
import uvicorn
from fastapi import Request, FastAPI,Form, Body
import traceback
import sys
import sqlite3
import datetime
import json
from transliterate import slugify
from sqlalchemy import create_engine
import pymysql


app = FastAPI()

@app.post("/api/v1/answers/save/")
async def get_body(form_data : dict = Body()):
    form_data['answers'] = json.loads(form_data['answers'])
    df = pd.json_normalize(form_data)

    engine = create_engine('mysql+pymysql://dev:dev777@answersdb:3306/ya_answers', echo=False)
    connection = engine.connect()

    rename = {}
    for c in df.columns:
        if(slugify(c)!=None):
            rename[c] = slugify(c).replace('-','_').replace('answers','answers_')
    df.rename(columns=rename , inplace=True)
    df.to_sql('form_answers', con=engine, if_exists = 'append', index=False)

    connection.close()

if __name__ == '__main__':
    uvicorn.run(app, port=8888, host='0.0.0.0')