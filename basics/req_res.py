from django.http import HttpResponse
import json


def wrap_error_response(code, error):
    dic = {}
    dic['code'] = code
    dic['msg'] = error
    return HttpResponse(json.dumps(dic), content_type='application/json')


def wrap_success_response(dict = {}):
    # mzhu: for debug only.  Please don't comment it out as it's important to trace/debug what was returned
    # to disable the logging, simply fix the LOGGING level in salon/settings.py
    # system_logger.debug(dict.values())
    return wrap_response(200, 'success', dict)


def wrap_response(code, msg, dict):
    dict['code'] = code
    dict['msg'] = msg
    return HttpResponse(json.dumps(dict), content_type='application/json')