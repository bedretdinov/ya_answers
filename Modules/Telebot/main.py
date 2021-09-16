import telegram
from datetime import datetime, timedelta
import traceback
import sys
import jinja2
from autoload import Modules


class Telebot:

    bot = telegram.Bot("1958242398:AAFlGDqfpoQYpPao-dFTCd3AC0tkaTGrK68")
    channel_id = -1001518892025
    templateLoader = jinja2.FileSystemLoader(searchpath="./templates")
    templateEnv = jinja2.Environment(loader=templateLoader)
    template = templateEnv.get_template("delivery.html")

    @classmethod
    def sentMessage(cls,text):
        cls.bot.sendMessage(chat_id=cls.channel_id, text=text, parse_mode='HTML')

    @classmethod
    def sentDeliveryInfo(cls, user_id, text, app,overdue_delivery):


        insert_db = []
        for row in overdue_delivery:
            message = cls.template.render(
                user_id=user_id,
                text=text,
                app=app,
                chrt=row['chrt'],
                delivery_overdue=row['delivery_overdue'],
                delivery_date=row['delivery_date'],
                delivery_date_end=row['delivery_date_end'],
                product=row['product'],
            )
            cls.sentMessage(message)

            insert_db.append(Modules.ClickHouse.DeliveryOverdue(
                app=app,
                user_id = user_id,
                text = text,
                chrt = row['chrt'],
                supplierId = row['product'].get('supplierId',0),
                position_name = row['product'].get('name',''),
                delivery_date = row['delivery_date'],
                delivery_overdue = row['delivery_overdue']
            ))



        Modules.ClickHouse.clickHouse.insert(insert_db)