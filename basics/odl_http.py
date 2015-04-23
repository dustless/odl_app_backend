# Copyright 2014 Cisco Systems, Inc.
# 
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
# 
# http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
# an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.
from __future__ import print_function as _print_function
from odl_controller_settings import odl_server
# odl_server = {
#     'address': '192.168.255.7',
#     'port': 8181,
#     'username': 'admin',
#     'password': 'admin'
# }
try:
    import Queue as queue
except ImportError:
    import queue
from requests import request

from threading import Lock


_url_template = 'http://%s:%d/restconf/%s'

_http_history = queue.Queue(20)
_http_history_lock = Lock()

def http_history_append(http):
    '''Append one HTTP request to the historical record.
    
    If the historical record reaches capacity the oldest HTTP request is removed and discarded.
    '''
    _http_history_lock.acquire()
    try:
        if _http_history.full():
            # discard oldest.             
            _http_history.get_nowait()
        _http_history.put_nowait(http)
        # print(_http_history.qsize())
    finally:
        _http_history_lock.release()

    
def http_history():
    '''Remove all HTTP requests from the historical record and return them.
    
    Result is a list of zero or more HTTP requests.
    Order of list is chronological. Oldest in element zero.
    '''
    popped = []
    _http_history_lock.acquire()
    try:
        while not _http_history.empty():
            popped.append(_http_history.get_nowait())
    finally:
        _http_history_lock.release()
    return popped

def http_history_clear():
    '''Remove all HTTP requests from the historical record and discard them.'''
    _http_history_lock.acquire()
    try:
        while not _http_history.empty():
            _http_history.get_nowait()
    finally:
        _http_history_lock.release()

def odl_http_request(
    method,
    url_suffix,
    contentType,
    content,
    accept,
    expected_status_code
):
    'Request a response from the ODL server.'
    url = _url_template % (odl_server['address'], odl_server['port'], url_suffix)
    headers = {}
    if accept != None:
        headers['Accept'] = accept
    if contentType != None:
        headers['Content-Type'] = contentType
    if content != None:
        headers['Content-Length'] = len(content)
    response = request(method, url, headers=headers, data=content, auth=(odl_server['username'], odl_server['password']))
    http_history_append(response)
    status_code_ok = response.status_code in expected_status_code \
        if isinstance(expected_status_code, (list, tuple)) \
        else  response.status_code == expected_status_code
    if not status_code_ok:
        msg = 'Expected HTTP status code %s, got %d, response: %s' % (expected_status_code, response.status_code, response.text)
        raise Exception(msg)
    else:
        return response
#     if accept == 'xml':
#         return etree.parse(StringIO(response.text))
#     elif accept == 'json':
#         return json.loads(response.text)
#     else:
#         return response.text

def odl_http_get(
    url_suffix,
    accept='text/plain',
    expected_status_code=200,
    contentType=None,
    content=None
):
    'Get a response from the ODL server.'
    return odl_http_request('get', url_suffix, contentType, content, accept, expected_status_code)

def odl_http_post(
    url_suffix,
    contentType,
    content,
    accept=None,
    expected_status_code=204
):
    'Request a post to the ODL server.'
    return odl_http_request('post', url_suffix, contentType, content, accept, expected_status_code)

def odl_http_put(
    url_suffix,
    contentType,
    content,
    accept=None,
    expected_status_code=204
):
    'Request a put into the ODL server.'
    return odl_http_request('put', url_suffix, contentType, content, accept, expected_status_code)

def odl_http_delete(
    url_suffix,
    accept=None,
    expected_status_code=204,
    contentType=None,
    content=None
):
    'Request a delete on the ODL server.'
    return odl_http_request('delete', url_suffix, contentType, content, accept, expected_status_code)
