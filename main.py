from typing import Optional

import pandas as pd
import uvicorn
from fastapi import FastAPI
from autoload import Modules
import traceback
import sys
import sqlite3
import datetime

logdb = sqlite3.connect('log.sqlite', check_same_thread=False)
app = FastAPI()

@app.get("/api/v1/send/")
def detect_and_send( user_id:int, text: Optional[str] = None,  app: Optional[str] = None):

    try:

        overdue_delivery = Modules.Delivery.check(user_id)

        if(overdue_delivery=={}):
            return {"status": False}
        else:

            Modules.Telebot.sentDeliveryInfo(user_id, text, app, overdue_delivery)

            return {"status":True,"items":overdue_delivery}

    except:
        etype, value, tb = sys.exc_info()
        error = ''.join(traceback.format_exception(etype, value, tb, 100))

        log = pd.DataFrame([
            {'error':error, 'date':datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        ])
        log.to_sql('delivery_logs', if_exists='append',con=logdb)

        return {"status": "error",'msg':error}







if __name__ == '__main__':
    uvicorn.run(app, port=4001, host='0.0.0.0')