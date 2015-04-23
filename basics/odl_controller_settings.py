REMOTE_CONTROLLER = True

if REMOTE_CONTROLLER:
    CONTROLLER_IP = '192.168.255.7'
else:
    CONTROLLER_IP = '127.0.0.1'

odl_server = {
    'address': CONTROLLER_IP,
    'port': 8181,
    'username': 'admin',
    'password': 'admin'
}