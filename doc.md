#URL prefix: http://192.168.255.7:8000/
## 1 modify topology for Mininet
### 1.1 add node
**Description**: 

	URL		mininet/add/node/
	Method	GET
	Params			
	{
	    "category":
	    "node_name": 
	    "loc":
	}
	Result
	{
        "code":200
        "msg":"success"
        "nodeDataArray": [
            {"id": 1, "category":"server", "loc":"143 -130", "node_name":"xxx"}
        ],
		"linkDataArray": [
			{"link_id":"link", "source_node_id":1, "source_node_name":"xxx", "dest_node_id":2, "dest_node_name":"xxx", "curve":0}
		]
	}

### 1.2 modify node
**Description**: 

	URL		mininet/update/node/
	Method	POST/GET
	Params			
	{
	    "id":
	    
	    "loc":
	}
	Result
	{
        "code":200
        "msg":"success"
        "nodeDataArray": [
            {"id": 1, "category":"server", "loc":"143 -130", "node_name":"xxx"}
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
	    "id":
	}
	Result
	{
        "code":200
        "msg":"success"
        "nodeDataArray": [
            {"id": 1, "category":"server", "loc":"143 -130", "node_name":"xxx"}
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
            {"id": 1, "category":"server", "loc":"143 -130", "node_name":"xxx"}
        ],
		"linkDataArray": [
			{"link_id":"link", "source_node_id":1, "source_node_name":"xxx", "dest_node_id":2, "dest_node_name":"xxx", "curve":0}
		]
	}

### 1.5 update link
**Description**:

    URL		mininet/update/link/
	Method	POST/GET
	Params			
	{
	    "id":
	    
	    "curve":
	}
	Result
	{
        "code":200
        "msg":"success"
        "nodeDataArray": [
            {"id": 1, "category":"server", "loc":"143 -130", "node_name":"xxx"}
        ],
		"linkDataArray": [
			{"link_id":"link", "source_node_id":1, "source_node_name":"xxx", "dest_node_id":2, "dest_node_name":"xxx", "curve":0}
		]
	}

### 1.6 delete link
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
            {"id": 1, "category":"server", "loc":"143 -130", "node_name":"xxx"}
        ],
		"linkDataArray": [
			{"link_id":"link", "source_node_id":1, "source_node_name":"xxx", "dest_node_id":2, "dest_node_name":"xxx", "curve":0}
		]
	}

## 2 modify topology for ODL view

### 2.1 modify node node_name or loc
**Description**: 

	URL		opendaylight/update/node/
	Method	POST/GET
	Params			
	{
	    "id":
	    
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

### 2.2 modify link curve or cost
**Description**: 

	URL		opendaylight/update/link/
	Method	POST/GET
	Params			
	{
	    "id":
	    
	    "curve":
	    "cost":
	}
	Result
	{
        "code":200
        "msg":"success"
        "nodeDataArray": [
            {"id": 1, "category":"server", "loc":"143 -130", "node_id":"server1", "node_name":"xxx"}
        ],
		"linkDataArray": [
			{"link_id":"link", "cost": 1.0, "source_node_id":1, "source_node_name":"xxx", "dest_node_id":2, "dest_node_name":"xxx", "curve":0}
		]
	}


## 3 get topology from controller
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
            {
                "id": 1,
                "category":"switch",
                "loc":"143 -130",
                "node_id":"openflow:1",
                "node_name":"s_1"
            },
            ...
        ],
		"linkDataArray": [
			{
			    "id":
			    "link_id":"link",
			    "cost": 1.0,
			    "source_node_id":1,
			    "source_node_name":"xxx",
			    "dest_node_id":2,
			    "dest_node_name":"xxx",
			    "load_s2d":"10Mbps",
			    "load_d2s":"1Mbps",
			    "color":"#01DF01",
			    "curve":0
			},
			...
		]

	}


## 4 get topology from mininet
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
            {
                "id": 1,
                "category":"switch",
                "loc":"143 -130",
                "node_name":"s_1"
            },
            ...
        ],
		"linkDataArray": [
			{
			    "id":
			    "link_id":"link",
			    "source_node_id":1,
			    "source_node_name":"xxx",
			    "dest_node_id":2,
			    "dest_node_name":"xxx",
			    "curve":0
			},
			...
		]
	}


## 5 get optimal path
**Description**: 

	URL		opendaylight/get/optimal/path/
	Method	POST/GET
	Params			
	{
	    "loadWeight":
	    "source_node_id":
	    "dest_node_id":
	}
	Result
	{
        "code":200
        "msg":"success"
        "nodeDataArray": [
            {
                "id": 1,
                "category":"switch",
                "loc":"143 -130",
                "node_id":"openflow:1",
                "node_name":"s_1"
            },
            ...
        ],
		"linkDataArray": [
			{
			    "id":
			    
			    "category": "bestPath",  // if this link is in the optimal path
			    
			    "link_id":"link",
			    "cost": 1.0,
			    "source_node_id":1,
			    "source_node_name":"xxx",
			    "dest_node_id":2,
			    "dest_node_name":"xxx",
			    "load_s2d":"10Mbps",
			    "load_d2s":"1Mbps",
			    "color":"#01DF01",
			    "curve":0
			},
			...
		]

	}