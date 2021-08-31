from repo.admin import AdminSQLManager

__all__ = ['Admin']


class Admin():
    @classmethod
    def user_management(cls, Identity):
        dict = {
            'All_superadmin': '1',
            'admin': '1',
            'member': '2',
            'blacklist': '3'
        }
        if Identity in dict:
            Identity = dict[Identity]

            manager = AdminSQLManager()
            user = manager.user_management(Identity)
        else:
            raise ValueError
        return user

    @classmethod
    def change_auth(cls, user, userlevel):
        manager = AdminSQLManager()
        manager.change_auth(user, userlevel)
        return 'ok'

    @classmethod
    def search_by_auth(cls, auth):
        dict = {
            'All_data': '1 | release = 0',
            'release': '1',
            'unreleased': '0'
        }
        if auth in dict:
            auth = dict[auth]
            manager = AdminSQLManager()
            user = manager.search_by_auth(auth)
        else:
            raise ValueError
        return user

    @classmethod
    def search_by_month(cls, month):
        dict = {'Month_all': 'all', 'Month_small': 'small', 'Month_big': 'big'}
        if month in dict:
            month = dict[month]
            manager = AdminSQLManager()
            list = manager.search_by_month(month)
        else:
            raise ValueError
        return list

    @classmethod
    def search_by_wave(cls, wave):
        if 'Wave' in wave:
            manager = AdminSQLManager()
            list = manager.search_by_wave(wave)
        else:
            raise ValueError
        return list

    @classmethod
    def search_by_type(cls, type):
        dict = {
            'Allpeople': 'all',
            'Teachers': '1',
            'Parent': '2',
            'Relatives': '3'
        }
        if type in dict:
            manager = AdminSQLManager()
            list = manager.search_by_type(type)
        else:
            return ValueError
        return list

    @classmethod
    def search_by_keyword(cls, keyword):
        list = []
        '''
        sql search by keywords
        '''
        return list
