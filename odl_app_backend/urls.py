from django.conf.urls import patterns, include, url

import xadmin
xadmin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'odl_app_backend.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'xadmin/', include(xadmin.site.urls)),
    url(r'mininet/add/node/', 'topology.views.mininet_add_node'),
    url(r'mininet/update/node/', 'topology.views.mininet_update_node'),
    url(r'mininet/delete/node/', 'topology.views.mininet_delete_node'),
    url(r'mininet/add/link/', 'topology.views.mininet_add_link'),
    url(r'mininet/update/link/', 'topology.views.mininet_update_link'),
    url(r'mininet/delete/link/', 'topology.views.mininet_delete_link'),
    url(r'mininet/get/topology/', 'topology.views.get_mininet_topology_data'),

    url(r'mininet/ping/all/', 'topology.views.mininet_ping_all'),
    url(r'mininet/ping/between/hosts/', 'topology.views.mininet_ping_between_hosts'),

    url(r'opendaylight/update/node/', 'topology.views.opendaylight_update_node'),
    url(r'opendaylight/update/link/', 'topology.views.opendaylight_update_link'),
    url(r'opendaylight/get/topology/', 'topology.views.get_controller_topology_data'),
    url(r'opendaylight/get/optimal/path/', 'topology.views.get_optimal_path'),
)
