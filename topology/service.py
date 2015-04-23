from topology.models import *
from basics.odl_http import odl_http_get
from basics.req_res import *

from datetime import datetime
import time
import traceback
import string, random

from odl_app_backend.settings import mini_network

_url_topology = '{config}/network-topology:network-topology/'
_url_inventory_nodes = '{config}/opendaylight-inventory:nodes'
_url_inventory_node = _url_inventory_nodes + '/node/{node-id}/'


def get_cur_utc_timestamp():
    return long(time.mktime(datetime.utcnow().timetuple()))


LINK_COLOR = ("#00FF00", "#0000CD", "#D2691E", "FF0000")
def get_color(load):
    if load < 10:
        return LINK_COLOR[0]
    elif load < 50:
        return LINK_COLOR[1]
    elif load < 80:
        return LINK_COLOR[2]
    else:
        return LINK_COLOR[3]


def make_random_digits(length=9):
    letters = string.digits # alphanumeric
    return ''.join([random.choice(letters) for _ in range(length)])


def get_mini_network():
    if mini_network:
        return mini_network
    else:
        return wrap_error_response(500, "Mininet is not available.")


def do_update_node(request, node):
    #category = request.REQUEST.get("category", None)
    #node_name = request.REQUEST.get("node_name", None)
    loc = request.REQUEST.get("loc", None)
    if loc:
        node.loc = loc
    node.save()


def get_topology():
    response = odl_http_get(_url_topology.format(**{'config': 'operational'}),
                            'application/json').json()
    topology = response['network-topology']['topology'][0]
    return topology


def get_inventory_nodes():
    response = odl_http_get(_url_inventory_nodes.format(**{'config': 'operational'}),
                            'application/json').json()
    return response['nodes']['node']

def get_inventory_node(node_id):
    response = odl_http_get(_url_inventory_node.format(**{'config': 'operational',
                                                          'node-id': node_id}),
                            'application/json').json()
    return response['node']

def get_and_update_nodes(topology):
    nodes = []
    if 'node' in topology:
        for node_dic in topology['node']:
            try:
                try:
                    node = Node.objects.get(node_id=node_dic['node-id'])
                except:
                    if 'host' in node_dic['node-id']:
                        name = 'h_' + make_random_digits(4)
                        while Node.objects.filter(node_name=name).exists():
                            name = 'h_' + make_random_digits(4)
                        category = 'server'
                    else:
                        name = 's_' + make_random_digits(4)
                        while Node.objects.filter(node_name=name).exists():
                            name = 's_' + make_random_digits(4)
                        category = 'switch'
                    node = Node.objects.create(node_id=node_dic['node-id'], node_name=name, category=category)
                dic = node.get_dict()
                nodes.append(dic)
            except:
                print traceback.print_exc()
                continue
    return nodes

def get_links(topology):
    links = []
    handled = []
    if 'link' in topology:
        for link_dic in topology['link']:
            try:
                if '/' in link_dic['link-id']:
                    reversed_link_id = '/'.join(link_dic['link-id'].split('/')[::-1])
                else:
                    reversed_link_id = link_dic['destination']['dest-tp']

                if reversed_link_id in handled:
                    continue
                handled.append(link_dic['link-id'])
                try:
                    link = Link.objects.get(link_id=link_dic['link-id'])
                except:
                    source_node_id = link_dic['source']['source-node']
                    dest_node_id = link_dic['destination']['dest-node']
                    source_node = Node.objects.get(node_id=source_node_id)
                    dest_node = Node.objects.get(node_id=dest_node_id)
                    link = Link.objects.create(
                        link_id=link_dic['link-id'],
                        source_node=source_node,
                        dest_node=dest_node
                    )
                    Link.objects.create(
                        link_id=reversed_link_id,
                        source_node=dest_node,
                        dest_node=source_node
                    )
                dic = link.get_dict()
                dic['color'] = get_color(max(link.load_s2d, link.load_d2s))
                links.append(dic)
            except:
                continue
    return links


def handle_links_with_topology(topology):
    handled = []
    if 'link' in topology:
        for link_dic in topology['link']:
            try:
                if '/' in link_dic['link-id']:
                    reversed_link_id = '/'.join(link_dic['link-id'].split('/')[::-1])
                else:
                    reversed_link_id = link_dic['destination']['dest-tp']

                if reversed_link_id in handled:
                    continue
                handled.append(link_dic['link-id'])
                try:
                    link = Link.objects.get(link_id=link_dic['link-id'])
                except:
                    source_node_id = link_dic['source']['source-node']
                    dest_node_id = link_dic['destination']['dest-node']
                    source_node = Node.objects.get(node_id=source_node_id)
                    dest_node = Node.objects.get(node_id=dest_node_id)
                    link = Link.objects.create(
                        link_id=link_dic['link-id'],
                        source_node=source_node,
                        dest_node=dest_node
                    )
                    Link.objects.create(
                        link_id=reversed_link_id,
                        source_node=dest_node,
                        dest_node=source_node
                    )
            except:
                continue


def update_links_load(topology):
    nodes = get_inventory_nodes()

    handle_links_with_topology(topology)

    for node_dic in nodes:
        if 'node-connector' in node_dic:
            for node_connector in node_dic['node-connector']:
                if 'LOCAL' not in node_connector['id']:
                    try:
                        link = Link.objects.get(link_id=node_connector['id'])
                        link_load, created = LinkLoad.objects.get_or_create(link=link)
                        if not created:
                            link.load_s2d = (link_load.bytes_s2d - int(node_connector['opendaylight-port-statistics:flow-capable-node-connector-statistics']['bytes']['transmitted']))\
                                            *8/(get_cur_utc_timestamp()-link_load.update_time)/1000000.0
                            link.load_d2s = (link_load.bytes_d2s - int(node_connector['opendaylight-port-statistics:flow-capable-node-connector-statistics']['bytes']['received']))\
                                            *8/(get_cur_utc_timestamp()-link_load.update_time)/1000000.0
                            link.save()
                        link_load.bytes_s2d = node_connector['opendaylight-port-statistics:flow-capable-node-connector-statistics']['bytes']['transmitted']
                        link_load.bytes_d2s = node_connector['opendaylight-port-statistics:flow-capable-node-connector-statistics']['bytes']['received']
                        link_load.update_time = get_cur_utc_timestamp()
                        link_load.save()
                    except:
                        continue


def get_links_with_load(topology):
    update_links_load(topology)
    return get_links(topology)


def get_mininet_nodes():
    nodes = []
    for node in MiniNode.objects.all():
        dic = node.get_dict()
        nodes.append(dic)
    return nodes


def get_mininet_links():
    links = []
    for link in MiniLink.objects.all():
        dic = link.get_dict()
        links.append(dic)
    return links


def get_mininet_topology():
    nodes = get_mininet_nodes()
    links = get_mininet_links()
    dic = {
        "nodeDataArray": nodes,
        "linkDataArray": links
    }
    return dic