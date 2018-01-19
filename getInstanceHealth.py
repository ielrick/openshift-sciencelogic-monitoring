import json
import sys
import ssl
import urllib2

print('Version 0.1.whoa')

""" From original Python code by Andy Watkins... SL h4x0r by Iain Elrick """

theurl = self.cred_details['cred_host']
#token = self.cred_details['cred_pwd']
# field in sciencelogic is not long enough so have to hard code for now...
token = "REDACTED"
instanceName = self.cred_details['cred_user']
port = self.cred_details['cred_port']
endpoint = theurl + ":" + str(port)

def get_all_nodes(endpoint, token, insecure=False):
    """
    Fetch the nodes data from the endpoint, using the /api/v1/nodes API

    Equivalent of:
      curl -k -H "Authorization: Bearer $token" -H 'Accept: application/json' \
      $endpoint/api/v1/nodes

    :param endpoint: the Openshift URL. Usually starts with "https://ocp."
        and ends with ":8443"
    :param token: security token for accessing this API
    :param insecure: set this to true for insecure SSL
        (the equivalent of curl's "-k" option.)
    :return:
    """
    request = urllib2.Request(endpoint + "/api/v1/nodes")
    request.add_header('Authorization', 'Bearer ' + token)
    request.add_header('Accept', 'application/json')
    ssl_context = None
    if insecure:
        ssl_context = ssl._create_unverified_context()
    result = urllib2.urlopen(request, context=ssl_context)
    return result.read()


def get_status_from_node(data_item):
    """ Extract the status conditions from the data
    Returns: a dict combining the hostname and the status conditions.
    """
    addresses = data_item['status']['addresses']
    address = None
    for addr in addresses:
        if addr['type'] == 'Hostname':
            address = addr['address']
    assert address is not None  # There is always a hostname.
    return {'hostname': address,
            'conditions': data_item['status']['conditions']}


def get_conditions(endpoint, token):
    """ The main entry point.
    Returns:
        a dict of the results.
    """
    all_nodes = json.loads(get_all_nodes(endpoint, token, insecure=True))
    data_out = []
    for node in all_nodes['items']:
        node_out = get_status_from_node(node)
        data_out.append(node_out)
    return data_out

nodeName={}
nodeStatus={}

def find_faults(cond_data):
    """ find faults in status condition data
    """
    nodeNum = 1
    for node in cond_data:
        hostname = node['hostname']
        nodeName[nodeNum] = hostname
        state = 'Green'        
        for cond in node['conditions']:
            if cond['status'] != "False" and cond['type'] != "Ready":
                nodeStatus[nodeNum] = 'Red'
                # print("FAULT: {}".format(cond['message']))
            elif cond['status'] != "True" and cond['type'] == "Ready":
                nodeStatus[nodeNum] = 'Red'
                # print("FAULT: {}".format(cond['message']))
            else:
                nodeStatus[nodeNum] = 'Green'
        nodeNum +=1

dd = get_conditions(endpoint, token)
find_faults(dd)

print(instanceName)
print(nodeName[1])
print(nodeName[2])
print(nodeName[3])
print(nodeName[4])
print(nodeName[5])
print(nodeStatus[1])
print(nodeStatus[2])
print(nodeStatus[3])
print(nodeStatus[4])
print(nodeStatus[5])

result_handler['instanceName'] = [(0, str(instanceName))]
result_handler['node1Name'] = [(0, str(nodeName[1]))]
result_handler['node2Name'] = [(0, str(nodeName[2]))]
result_handler['node3Name'] = [(0, str(nodeName[3]))]
result_handler['node4Name'] = [(0, str(nodeName[4]))]
result_handler['node5Name'] = [(0, str(nodeName[5]))]
result_handler['node1Status'] = [(0, str(nodeStatus[1]))]
result_handler['node2Status'] = [(0, str(nodeStatus[2]))]
result_handler['node3Status'] = [(0, str(nodeStatus[3]))]
result_handler['node4Status'] = [(0, str(nodeStatus[4]))]
result_handler['node5Status'] = [(0, str(nodeStatus[5]))]
