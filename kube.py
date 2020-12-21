import urllib3
from kubernetes import client, config

urllib3.disable_warnings()

def test_k8s(kube_config):
    configuration = client.Configuration()
    configuration.host = kube_config['clusters'][0]['cluster']['server']
    configuration.verify_ssl = False
    configuration.cert_file = kube_config['users'][0]['user']['client-certificate']
    configuration.key_file = kube_config['users'][0]['user']['client-key']



    with client.ApiClient(configuration) as api_client:
        v1 = client.CoreV1Api(api_client)
        print("Listing pods with their IPs:")
        ret = v1.list_pod_for_all_namespaces(watch=False)
        for i in ret.items:
            print("%s\t%s\t%s" % (i.status.pod_ip, i.metadata.namespace, i.metadata.name))
