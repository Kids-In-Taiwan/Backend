from .manager import SQLManager
from config.config import get_yaml_config
import pymssql


class AccountSQLManager(SQLManager):
    def __init__(self, asdict=False):
        self.conn = None
        self.cursor = None
        self.connect(asdict)

    def connect(self, asdict):
        config = get_yaml_config('mssql')

        self.conn = pymssql.connect(host=config['host'],
                                    user=config['user'],
                                    password=config['password'],
                                    database=config['database'])
        self.cursor = self.conn.cursor(as_dict=asdict)

    def add_account(self, username: str, hash_in: str, email: str, name: str, identity: str, phone: str, organization: str, relation: int):
        insert_op = 'INSERT INTO dbo.account (account_name, nickname, password, email, name, identity_num, phone, organization, relation) VALUES (%(username)s, %(nickname)s, %(email)s, %(password)s, %(name)s, %(identity)s, %(phone)s, %(organization)s, %(relation)s)'
        print(insert_op)
        self.cursor.execute(
            insert_op, {
                'username': username,
                'nickname': username,
                'password': hash_in,
                'email': email,
                'name': name,
                'identity': identity,
                'phone': phone,
                'organization': organization,
                'relation': relation
            })
        self.conn.commit()

    def change_password(self, username: str, hash_new: str):
        change_op = 'UPDATE dbo.account SET password=%(new_password)s WHERE account_name=%(username)s'
        self.cursor.execute(change_op, {
            'username': username,
            'new_password': hash_new
        })
        self.conn.commit()

    def change_nickname(self, username: str, nickname: str):
        change_op = 'UPDATE dbo.account SET nickname=%(nickname)s WHERE account_name=%(username)s'
        self.cursor.execute(change_op, {
            'username': username,
            'nickname': nickname
        })
        self.conn.commit()

    def change_name(self, username: str, name: str):
        change_op = 'UPDATE dbo.account SET name=%(name)s WHERE account_name=%(username)s'
        self.cursor.execute(change_op, {
            'username': username,
            'name': name
        })
        self.conn.commit()

    def change_phone(self, username: str, phone: str):
        change_op = 'UPDATE dbo.account SET phone=%(phone)s WHERE account_name=%(username)s'
        self.cursor.execute(change_op, {
            'username': username,
            'phone': phone
        })
        self.conn.commit()

    def change_organization(self, username: str, organization: str):
        change_op = 'UPDATE dbo.account SET organization=%(organization)s WHERE account_name=%(username)s'
        self.cursor.execute(change_op, {
            'username': username,
            'organization': organization
        })
        self.conn.commit()

    def change_relation(self, username: str, relation: int):
        change_op = 'UPDATE dbo.account SET relation=%(relation)s WHERE account_name=%(username)s'
        self.cursor.execute(change_op, {
            'username': username,
            'relation': relation
        })
        self.conn.commit()

    def loadinfo(self, username: str):
        search_op = 'SELECT account_name, nickname, email, auth, name, phone, organization, relation FROM dbo.account WHERE account_name=%(username)s'
        try:
            self.cursor.execute(search_op, {
                'username': username,
            })
        except:
            return None
        data = self.cursor.fetchone()
        return data

    def get_by_username(self, username: str):
        search_op = 'SELECT * FROM dbo.account WHERE account_name=%(username)s'
        try:
            self.cursor.execute(search_op, {'username': username})
        except:
            return None
        data = self.cursor.fetchone()
        return data

    def get_by_email(self, email: str):
        search_op = 'SELECT * FROM dbo.account WHERE email=%(email)s'
        try:
            self.cursor.execute(search_op, {'email': email})
        except:
            return None
        data = self.cursor.fetchone()
        return data
