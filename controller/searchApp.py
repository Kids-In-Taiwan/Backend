from flask import Blueprint, request
from flask_login import login_required, current_user
from service.search import Search
from .utils.response import HTTPResponse, HTTPError
from .utils.request import Request
from .utils.auth_required import auth_required, AuthLevel

__all__ = ['searchApp_api']

searchApp_api = Blueprint('searchApp_api', __name__)


def conv_req_list(params_str):
    str_list = request.args.getlist(params_str)
    return list(map(int, str_list))


#get waves from selected age and survey type
@searchApp_api.route('/searchWave', methods=['GET'])
@login_required
@auth_required(AuthLevel.REGULAR)
def searchWave():
    try:
        ageType = conv_req_list("ageType")
        surveyType = conv_req_list('surveyType')
        wave = Search.search_wave(ageType, surveyType)
    except:
        return HTTPError('unknown error', 406)

    return HTTPResponse('ok', data={"wave": wave})


#get problems from selected age, survey, wave
@searchApp_api.route('/searchInfo', methods=['GET'])
@login_required
@auth_required(AuthLevel.REGULAR)
def searchInfo():
    try:
        Info = Search.search_info(current_user.id)
    except:
        return HTTPError('unknown error', 406)

    return HTTPResponse('ok', data={"info": Info})


#get user's last search info: age, survey type
@searchApp_api.route('/getSearchInfo', methods=['GET'])
@login_required
@auth_required(AuthLevel.REGULAR)
def getSearchInfo():
    try:
        Info = Search.get_search_info(current_user.id)
    except:
        return HTTPError('unknown error', 406)

    return HTTPResponse('ok', data={"info": Info})


#store user's last search info: age, survey type
@searchApp_api.route('/storeSearchInfo', methods=['POST'])
@login_required
@auth_required(AuthLevel.REGULAR)
@Request.json('info: dict')
def storeSearchInfo(info):
    try:
        res = Search.store_search_info(current_user.id, info)
    except:
        return HTTPError('unknown error', 406)

    return HTTPResponse('ok')


#delete user's search info: age, survey type
@searchApp_api.route('/delSearchInfo', methods=['DELETE'])
@login_required
@auth_required(AuthLevel.REGULAR)
def delSearchInfo():
    try:
        res = Search.del_search_info(current_user.id)
    except:
        return HTTPError('unknown error', 406)

    return HTTPResponse('ok')


#store user's selected probelm to shop_cart
@searchApp_api.route('/storeInfo', methods=['POST'])
@login_required
@auth_required(AuthLevel.REGULAR)
@Request.json('problemList: list')
def storeInfo(problemList):
    try:
        res = Search.store_info(current_user.id, problemList)
    except:
        return HTTPError('unknown error', 406)
    return HTTPResponse('ok')


#get user's shop_cart
@searchApp_api.route('/getInfo', methods=['GET'])
@login_required
@auth_required(AuthLevel.REGULAR)
def getInfo():
    try:
        problem_list = Search.get_info(current_user.id)
        # if problem_id == 'failed':
        #     return HTTPError('Failed to fetch info', 403)
    except:
        return HTTPError('unknown error', 406)
    return HTTPResponse('ok', data={"problemList": problem_list})


#delete user's shop_cart
@searchApp_api.route('/delInfo', methods=['DELETE'])
@login_required
@auth_required(AuthLevel.REGULAR)
def delInfo():
    try:
        '''delete user info'''
        res = Search.del_info(current_user.id)
    except:
        return HTTPError('unknown error', 406)
    return HTTPResponse('ok')