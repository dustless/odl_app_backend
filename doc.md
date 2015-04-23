#URL prefix: http://127.0.0.1:8000/
## 1 modify topology for Mininet
### 1.1 add node
**Description**: 

	URL		mininet/add/node/
	Method	GET
	Params			
	{
	    "category":
	    "node_id": for Mininet
	    "node_name": for show
	    "loc":
	}
	Result
	{
        "code":200
        "msg":"success"
        "nodeDataArray": [
            {"id": 1, "category":"server", "loc":"143 -130", "node_id":"server1", "node_name":"xxx"}
        ],
		"linkDataArray": [
			{"link_id":"link", "source_node_id":1, "source_node_name":"xxx", "dest_node_id":2, "dest_node_name":"xxx", "curve":0}
		]
	}

### 1.2 modify node name
**Description**: 

	URL		mininet/update/node/
	Method	POST/GET
	Params			
	{
	    "node_id":
	    
	    "node_name":
	    "loc":
	}
	Result
	{
        "code":200
        "msg":"success"
        "nodeDataArray": [
            {"id": 1, "category":"server", "loc":"143 -130", "node_id":"server1", "node_name":"xxx"}
        ],
		"linkDataArray": [
			{"link_id":"link", "source_node_id":1, "source_node_name":"xxx", "dest_node_id":2, "dest_node_name":"xxx", "curve":0}
		]
	}

### 1.3 delete node
**Description**: 

	URL		mininet/delete/node/
	Method	POST/GET
	Params			
	{
	    "node_id":
	}
	Result
	{
        "code":200
        "msg":"success"
        "nodeDataArray": [
            {"id": 1, "category":"server", "loc":"143 -130", "node_id":"server1", "node_name":"xxx"}
        ],
		"linkDataArray": [
			{"link_id":"link", "source_node_id":1, "source_node_name":"xxx", "dest_node_id":2, "dest_node_name":"xxx", "curve":0}
		]
	}

### 1.4 add link
**Description**: 

	URL		mininet/add/link/
	Method	POST/GET
	Params			
	{
	    "source_node_id":
	    "dest_node_id":
	    "curve":
	}
	Result
	{
        "code":200
        "msg":"success"
        "nodeDataArray": [
            {"id": 1, "category":"server", "loc":"143 -130", "node_id":"server1", "node_name":"xxx"}
        ],
		"linkDataArray": [
			{"link_id":"link", "source_node_id":1, "source_node_name":"xxx", "dest_node_id":2, "dest_node_name":"xxx", "curve":0}
		]
	}

### 1.5 delete link
**Description**: 

	URL		mininet/delete/link/
	Method	POST/GET
	Params			
	{
	    "id":
	}
	Result
	{
        "code":200
        "msg":"success"
        "nodeDataArray": [
            {"id": 1, "category":"server", "loc":"143 -130", "node_id":"server1", "node_name":"xxx"}
        ],
		"linkDataArray": [
			{"link_id":"link", "source_node_id":1, "source_node_name":"xxx", "dest_node_id":2, "dest_node_name":"xxx", "curve":0}
		]
	}

## 2 get topology from controller
**Description**: 

	URL		opendaylight/get/topology/
	Method	POST/GET
	Params			
	{
	}
	Result
	{
        "code":200
        "msg":"success"
        "nodeDataArray": [
            {"id": 1, "category":"server", "loc":"143 -130", "node_id":"server1", "node_name":"xxx"}
        ],
		"linkDataArray": [
			{"link_id":"link", "source_node_id":1, "source_node_name":"xxx", "dest_node_id":2, "dest_node_name":"xxx", "load_s2d":"10Mbps", "load_d2s":"1Mbps", "color":"#01DF01", "curve":0}
		]

	}


## 3 get topology from mininet
**Description**: 

	URL		mininet/get/topology/
	Method	POST/GET
	Params			
	{
	}
	Result
	{
        "code":200
        "msg":"success"
        "nodeDataArray": [
            {"id": 1, "category":"server", "loc":"143 -130", "node_id":"server1", "node_name":"xxx"}
        ],
		"linkDataArray": [
			{"link_id":"link", "source_node_id":1, "source_node_name":"xxx", "dest_node_id":2, "dest_node_name":"xxx", "curve":0}
		]
	}
