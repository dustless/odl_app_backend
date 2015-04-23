from topology.models import *
from basics.odl_http import odl_http_get
from basics.req_res import *

from datetime import datetime
import time
import traceback
import string, random

from odl_app_backend.virtual_network import VirtualNetwork
from odl_app_backend.settings import MININET_AVAILABLE, MININET_INIT, mini_network

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
    if MININET_AVAILABLE:
        return mini_network
    else:
        return wrap_error_response(500, "Mininet is not available.")


def do_update_node(request, node):
    #category = request.REQUEST.get("category", None)
    node_name = request.REQUEST.get("node_name", None)
    loc = request.REQUEST.get("loc", None)
    if loc:
        node.loc = loc
    if node_name and isinstance(node, Node):
        node.node_name = node_name
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
    if MININET_AVAILABLE and MININET_INIT:
        if not MiniNode.objects.all().exists():
            s1 = MiniNode.objects.create(node_name='s1', category='switch', loc='0 100')
            s2 = MiniNode.objects.create(node_name='s2', category='switch', loc='-20 60')
            s3 = MiniNode.objects.create(node_name='s3', category='switch', loc='20 60')
            h1 = MiniNode.objects.create(node_name='h1', category='host', loc='-50 20')
            h2 = MiniNode.objects.create(node_name='h2', category='host', loc='-25 20')
            h3 = MiniNode.objects.create(node_name='h3', category='host', loc='25 20')
            h4 = MiniNode.objects.create(node_name='h4', category='host', loc='50 20')
            MiniLink.objects.create(link_id='1:2', source_node=s1, dest_node=s2)
            MiniLink.objects.create(link_id='1:3', source_node=s1, dest_node=s3)
            MiniLink.objects.create(link_id='2:4', source_node=s2, dest_node=h1)
            MiniLink.objects.create(link_id='2:5', source_node=s2, dest_node=h2)
            MiniLink.objects.create(link_id='3:6', source_node=s3, dest_node=h3)
            MiniLink.objects.create(link_id='3:7', source_node=s3, dest_node=h4)
    nodes = get_mininet_nodes()
    links = get_mininet_links()
    dic = {
        "nodeDataArray": nodes,
        "linkDataArray": links
    }
    return dic

def get_controller_topology():
    topology = get_topology()
    nodes = get_and_update_nodes(topology)
    links = get_links_with_load(topology)
    dic = {
        "nodeDataArray": nodes,
        "linkDataArray": links
    }
    return dic


### path calculate
### use bellman-ford


def relax(node, neighbour, graph, d, p):
    if d[neighbour] > d[node] + graph[node][neighbour]:
        d[neighbour] = d[node] + graph[node][neighbour]
        p[neighbour] = node


def bellman_ford(graph, source):
    dist = {}
    pre = {}
    for node in graph:
        dist[node] = float('Inf')
        pre[node] = None
    dist[source] = 0
    for i in range(len(graph)-1):
        for u in graph:
            for v in graph[u]:
                relax(u, v, graph, dist, pre)

    # check for negative-weight cycles
    for u in graph:
        for v in graph[u]:
            assert dist[v] <= dist[u] + graph[u][v]

    return dist, pre


def test():
    graph = {
        'a': {'b': -1, 'c':  4},
        'b': {'c':  3, 'd':  2, 'e':  2},
        'c': {},
        'd': {'b':  1, 'c':  5},
        'e': {'d': -3}
        }

    d, p = bellman_ford(graph, 'a')

    assert d == {
        'a':  0,
        'b': -1,
        'c':  2,
        'd': -2,
        'e':  1
        }

    assert p == {
        'a': None,
        'b': 'a',
        'c': 'b',
        'd': 'e',
        'e': 'b'
        }

if __name__ == '__main__': test()