from autoload import Modules
import pandas as pd
import pickle
import datetime


class Delivery:

    @classmethod
    def dateParse(cls, time_in_secs):
        return datetime.datetime.fromtimestamp(float(time_in_secs))

    @classmethod
    def check(cls, user_id):

        payment_positions = Modules.ClickHouse.Positions.objects_in(Modules.ClickHouse.positionDB).filter(
            (Modules.ClickHouse.Positions.user_id == user_id)
            & (Modules.ClickHouse.Positions.message == 'positions.payment_complete')
        )

        positions_arrived = Modules.ClickHouse.Positions.objects_in(Modules.ClickHouse.positionDB).filter(
            (Modules.ClickHouse.Positions.user_id == user_id)
            & (Modules.ClickHouse.Positions.message == 'positions.arrived')
        )

        payment_positions = set(row.rid for row in payment_positions)
        positions_arrived = set(row.rid for row in positions_arrived)

        delivery = Modules.DynamicPlayer.import_('librarry.delivery.main')
        position = Modules.DynamicPlayer.import_('librarry.position.main')

        positionObj = position.Position()
        deliveryInfo = delivery.DeliveryInfo()

        res = pickle.loads(deliveryInfo.getActiveDeliveryPcl(user_id))
        delivery_info = pd.DataFrame(res)
        if (delivery_info.empty):
            return {}

        delivery_info = delivery_info[delivery_info['rid'].isin(payment_positions)]
        delivery_info = delivery_info[~delivery_info['rid'].isin(positions_arrived)]
        delivery_info = delivery_info[delivery_info['delivery_date']!=0]
        delivery_info['delivery_date'] = delivery_info['delivery_date'].map(Delivery.dateParse)

        delivery_info['delivery_date_end'] = (
                delivery_info['delivery_date'] + pd.Timedelta(days=2)
        )

        delivery_info['delivery_overdue'] = (
                pd.Timestamp("today") - pd.to_datetime(delivery_info['delivery_date_end'])
        ).dt.days



        delivery_info = delivery_info.query('delivery_overdue>=1 and delivery_overdue<1000')

        if(not delivery_info.empty):
            res = delivery_info[['delivery_overdue', 'delivery_date','delivery_date_end','chrt']]
            res['product'] = res['chrt'].map(lambda x: pickle.loads(positionObj.getByChrtPcl(x)))
            res['user_id'] = user_id
            return res.to_dict('records')

        return {}