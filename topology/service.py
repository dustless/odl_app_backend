from topology.models import *
from basics.odl_http import odl_http_get
from basics.req_res import *

from datetime import datetime
import time
import traceback
import string, random

#from odl_app_backend.virtual_network import VirtualNetwork
from odl_app_backend.settings import MININET_AVAILABLE, MININET_NEED_INIT, mini_network

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
        if MININET_NEED_INIT and not mini_network.initialized:
            mini_network.init_topo()
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
                    if node_dic['node-id'] == 'openflow:1':
                        loc = '35 -250'
                    elif node_dic['node-id'] == 'openflow:2':
                        loc = '-81 -120'
                    elif node_dic['node-id'] == 'openflow:3':
                        loc = '152 -120'
                    else:
                        loc = str(random.randint(-200, 100)) + ' ' + str(random.randint(-50, 20))
                    node = Node.objects.create(node_id=node_dic['node-id'], node_name=name, category=category, loc=loc)

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
                        link = Link.objects.filter(link_id__icontains=node_connector['id'])
                        if link:
                            link = link[0]
                        else:
                            continue
                        link_load, created = LinkLoad.objects.get_or_create(link=link)

                        cur_s2d_bytes = node_connector['opendaylight-port-statistics:flow-capable-node-connector-statistics']['bytes']['transmitted']
                        cur_d2s_bytes = node_connector['opendaylight-port-statistics:flow-capable-node-connector-statistics']['bytes']['received']

                        if not created:
                            link.load_s2d = (cur_s2d_bytes - link_load.bytes_s2d)*8.0/(time.time()-link_load.update_time)/1000.0
                            link.load_d2s = (cur_d2s_bytes - link_load.bytes_d2s)*8.0/(time.time()-link_load.update_time)/1000.0
                            link.save()
                        link_load.bytes_s2d = cur_s2d_bytes
                        link_load.bytes_d2s = cur_d2s_bytes
                        link_load.update_time = time.time()
                        link_load.save()
                    except:
                        #print traceback.print_exc()
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
    if MININET_AVAILABLE and MININET_NEED_INIT:
        if MININET_NEED_INIT and not mini_network.initialized:
            mini_network.init_topo()
        if not MiniNode.objects.all().exists():
            s1 = MiniNode.objects.create(node_name='s1', category='switch', loc='35 -250')
            s2 = MiniNode.objects.create(node_name='s2', category='switch', loc='-81 -120')
            s3 = MiniNode.objects.create(node_name='s3', category='switch', loc='152 -120')
            h1 = MiniNode.objects.create(node_name='h1', category='host', loc='-167 -10')
            h2 = MiniNode.objects.create(node_name='h2', category='host', loc='-30 -10')
            h3 = MiniNode.objects.create(node_name='h3', category='host', loc='75 -10')
            h4 = MiniNode.objects.create(node_name='h4', category='host', loc='260 -10')
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

def make_graph(topology, load_weight):
    graph = {}
    for node_dic in topology['nodeDataArray']:
        graph[node_dic['id']] = {}
    for link_dic in topology['linkDataArray']:
        if link_dic['source_node_id'] in graph and link_dic['dest_node_id'] in graph:
            graph[link_dic['source_node_id']][link_dic['dest_node_id']] = \
                link_dic['cost']*(1 - load_weight) + float(link_dic['load_s2d'].split(' ')[0])/100.0*load_weight
            graph[link_dic['dest_node_id']][link_dic['source_node_id']] = \
                link_dic['cost']*(1 - load_weight) + float(link_dic['load_d2s'].split(' ')[0])/100.0*load_weight

    return graph


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


def add_optimal_path(topology, load_weight, source, dest):
    graph = make_graph(topology, load_weight)
    dist, pre = bellman_ford(graph, source)
    path = []
    while dest:
        path.append((pre[dest], dest))
        dest = pre[dest]
    for link_dic in topology['linkDataArray']:
        if (link_dic['source_node_id'], link_dic['dest_node_id']) in path:
            link_dic['category'] = 'bestPath'
        elif (link_dic['dest_node_id'], link_dic['source_node_id']) in path:
            link_dic['category'] = 'bestPath'
            link_dic['source_node_id'], link_dic['dest_node_id'] = link_dic['dest_node_id'], link_dic['source_node_id']

    return topology


if __name__ == '__main__':
    topology = get_controller_topology()
    add_optimal_path(topology, 0, 4, 7)