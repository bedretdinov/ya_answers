import rpyc


class DynamicPlayer:
    host = 'mfc-tf01.dl.wb.ru'
    port = 9933
    connector = False

    @classmethod
    def connect(cls):
        if (cls.connector == False):
            return rpyc.classic.connect(
                host=cls.host,
                port=cls.port
            )
        return cls.connector

    @classmethod
    def import_(cls, module):
        return cls.connect().modules[module]

