from .manager import SQLManager
from config.config import get_yaml_config
import pymssql


class AdminSQLManager(SQLManager):
    def connect(self):
        config = get_yaml_config('mssql')

        self.conn = pymssql.connect(host=config['host'],
                                    user=config['user'],
                                    password=config['password'],
                                    database=config['database'],
                                    as_dict=True)
        self.cursor = self.conn.cursor()

    def _get_allsurvey(self):
        search_op = "SELECT * FROM dbo.survey"
        self.cursor.execute(search_op)
        data = self.conn.fetchall()
        return data

    def user_management(self, Identity: str):
        search_op = "SELECT account_name, email, auth FROM dbo.account WHERE auth=%(Identity)d"
        self.cursor.execute(search_op, {'Identity': Identity})
        data = self.cursor.fetchall()
        return data

    def change_auth(self, user: str, userlevel: int):
        change_op = "UPDATE dbo.account SET auth=%(userlevel)d WHERE account_name=%(user)d"
        self.cursor.execute(change_op, {'user': user, 'userlevel': userlevel})
        self.conn.commit()

    def search_by_auth(self, auth: str):
        search_op = "SELECT * FROM dbo.survey WHERE release=%(auth)d"
        self.cursor.execute(search_op, {'auth': auth})
        data = self.cursor.fetchall()
        return data

    def search_by_month(self, month: str):
        if month == 'all':
            return self._get_allsurvey()
        else:
            search_op = "SELECT * FROM dbo.survey WHERE age_type=%(month)d"
            self.cursor.execute(search_op, {'month': month})
        data = self.cursor.fetchall()
        return data

    def search_by_wave(self, wave: str):
        if wave == 'Wave_all':
            return self._get_allsurvey()
        else:
            search_op = "SELECT * FROM dbo.survey WHERE wave=%(wave)d"
            self.cursor.execute(search_op, {'wave': wave})
        data = self.cursor.fetchall()
        return data

    def search_by_type(self, type: str):
        if type == 'all':
            return self._get_allsurvey()
        else:
            search_op = "SELECT * FROM dbo.survey WHERE survey_type=%(type)d"
            self.cursor.execute(search_op, {'type': type})
        data = self.cursor.fetchall()
        return data