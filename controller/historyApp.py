from flask import Blueprint
from flask_login import current_user, login_required
from service.history import NotEnoughParams, History, WrongParamType
from .utils.response import HTTPResponse, HTTPError
from .utils.request import Request
from .utils.auth_required import AuthLevel, auth_required

__all__ = ['historyApp_api']

historyApp_api = Blueprint('historyApp_api', __name__)

@historyApp_api.route('/surveyDownloadCount', methods=['GET'])
@login_required
@auth_required(AuthLevel.ADMIN)
@Request.args('surveyId', 'startDate', 'endDate')
def getDownloadCount(surveyId, startDate, endDate):
	try:
		count = History.get_count(surveyId, startDate, endDate)
	except NotEnoughParams:
		return HTTPError('Not enough params', 405)
	except WrongParamType:
		return HTTPError('Wrong Param Type', 405)
	except:
		return HTTPError('unknown error', 406)
	return HTTPResponse('ok', data={"downloadCount": count})