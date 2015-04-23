# -*- coding: utf-8 -*-
#from django.shortcuts import render
import traceback

from django.views.decorators.csrf import csrf_exempt

from basics.req_res import *
from topology.service import *

# Create your views here.

_url_topology = '{config}/network-topology:network-topology/'
_url_topology_node = _url_topology + '/node/{node-id}'


@csrf_exempt
def mininet_add_node(request):
    try:
        mini_network = get_mini_network()
        if isinstance(mini_network, HttpResponse):
            return mini_network
        node, created = MiniNode.objects.get_or_create(node_name=request.REQUEST['node_name'])
        if not created:
            return wrap_error_response(400, "Node name already exists.")
        do_update_node(request, node)
        try:
            if node.category == 'switch':
                mini_network.add_switch(node.node_name)
            else:
                mini_network.add_host(node.node_name)
        except:
            node.delete()
            return wrap_error_response(500, "Add node failed.Try again.")
        return wrap_success_response(get_mininet_topology())
    except Exception as e:
        print traceback.print_exc()
        return wrap_error_response(500, str(e))


@csrf_exempt
def mininet_update_node(request):
    try:
        try:
            node = MiniNode.objects.get(id=request.REQUEST['id'])
        except:
            return wrap_error_response(400, "Node does not exist.")
        do_update_node(request, node)
        return wrap_success_response(get_mininet_topology())
    except Exception as e:
        print traceback.print_exc()
        return wrap_error_response(500, str(e))


@csrf_exempt
def mininet_delete_node(request):
    try:
        mini_network = get_mini_network()
        if isinstance(mini_network, HttpResponse):
            return mini_network
        try:
            node = MiniNode.objects.get(id=request.REQUEST['id'])
            mini_network
            return wrap_error_response(500, 'Not available now.')
        except:
            return wrap_error_response(400, "Update failed.Maybe node does not exists")
    except Exception as e:
        print traceback.print_exc()
        return wrap_error_response(500, str(e))


@csrf_exempt
def mininet_add_link(request):
    try:
        mini_network = get_mini_network()
        if isinstance(mini_network, HttpResponse):
            return mini_network
        source_node = MiniNode.objects.get(id=request.REQUEST["source_node_id"])
        dest_node = MiniNode.objects.get(id=request.REQUEST["dest_node_id"])
        curve = request.REQUEST.get('curve', 0.0)

        try:
            link = MiniLink.objects.get(source_node=source_node, dest_node=dest_node)
            link = MiniLink.objects.get(source_node=dest_node, dest_node=source_node)
            return wrap_error_response(400, "Link already exists.")
        except:
            link_id = str(source_node.id) + ':' + str(dest_node.id)
            MiniLink.objects.create(link_id, source_node=source_node, dest_node=dest_node, curve=curve)
            return wrap_success_response(get_mininet_topology())
    except Exception as e:
        print traceback.print_exc()
        return wrap_error_response(500, str(e))


@csrf_exempt
def mininet_update_link(request):
    try:
        try:
            link = MiniLink.objects.get(id=request.REQUEST['id'])
        except:
            return wrap_error_response(400, "Node does not exist.")
        if "curve" in request.REQUEST and request.REQUEST["curve"]:
            link.curve = float(request.REQUEST["curve"])
        link.save()
        return wrap_success_response(get_mininet_topology())
    except Exception as e:
        print traceback.print_exc()
        return wrap_error_response(500, str(e))


@csrf_exempt
def mininet_delete_link(request):
    try:
        return wrap_error_response(500, 'Not available now.')
    except Exception as e:
        print traceback.print_exc()
        return wrap_error_response(500, str(e))


@csrf_exempt
def get_mininet_topology_data(request):
    try:
        return wrap_success_response(get_mininet_topology())
    except Exception as e:
        print traceback.print_exc()
        return wrap_error_response(500, str(e))


@csrf_exempt
def get_controller_topology_data(request):
    try:
        topology = get_topology()
        nodes = get_and_update_nodes(topology)
        links = get_links_with_load(topology)
        dic = {
            "nodeDataArray": nodes,
            "linkDataArray": links
        }
        return wrap_success_response(dic)
    except Exception as e:
        print traceback.print_exc()
        return wrap_error_response(500, str(e))


if __name__ == '__main__':
    print get_inventory_nodes()
    print get_inventory_node('openflow:1')