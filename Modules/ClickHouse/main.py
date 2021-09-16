from infi.clickhouse_orm import Database
from infi.clickhouse_orm import Model,Float32Field,UInt32Field, Int32Field, StringField, DateField, DateTimeField , Float64Field, MergeTree, ReplacingMergeTree, UInt16Field, MergeTree, UInt64Field, NullableField,UInt8Field



class ClickHouse:

    def clickHouseConnection():
        return Database(
            'analytics',
            db_url='http://mfc-tf01.dl.wb.ru:8125' ,
            username='default',
            password=''
        )

    class DeliveryOverdue(Model):

        app = StringField(default='')
        user_id = Int32Field(default=0)
        chrt = UInt64Field(default=0)
        supplierId = Int32Field(default=0)
        position_name = StringField(default='')
        text = StringField(default='')
        delivery_date = DateTimeField()
        delivery_overdue = Int32Field()
        date = DateField(materialized='toDate(delivery_date)')

        engine = MergeTree(partition_key=['date'], order_by=('delivery_date', ))

        @classmethod
        def table_name(cls):
            return 'delivery_overdue'

    clickHouse = clickHouseConnection() #
    clickHouse.create_table(DeliveryOverdue)

    class Positions(Model):
        dt = DateTimeField()
        message = StringField(default='')
        rid = UInt64Field(default=0)
        user_id = UInt64Field(default=0)
        order_id = UInt64Field(default=0)
        chrt_id = UInt64Field(default=0)
        create_dt = DateTimeField()


        engine = MergeTree(partition_key=['toYYYYMM(dt)'], order_by=('user_id', 'message', 'rid'))

        @classmethod
        def table_name(cls):
            return 'positions'

    def clickHousePositionConnection():
        return Database(
            'cc_dwh',
            db_url='http://mfc-ch1.dl.wb.ru:8123' ,
            username='cc_backend2',
            password='b18004161b1b11eaa791C7f35185331c'
        )

    positionDB = clickHousePositionConnection()