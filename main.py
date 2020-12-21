import os
import re

import yaml

import dockerd
import kube
import rancher

def parse_kube_config(etc_kubernetes_path):
    kube_config_path = '/host' + etc_kubernetes_path + '/ssl/kubecfg-kube-node.yaml'
    if not os.path.isfile(kube_config_path):
        raise Exception('kubeconfig file does not exist at {}'.format(kube_config_path))
    try:
        with open(kube_config_path, 'r') as kube_config_file:
            try:
                kube_config_yaml = kube_config_file.read()
                kube_config_yaml = re.sub(etc_kubernetes_path,'/host'+etc_kubernetes_path, kube_config_yaml)
                kube_config = yaml.safe_load(kube_config_yaml)
            except yaml.YAMLError as err:
                raise Exception('Error attempting to parse YAML {}: {}'.format(kube_config_path,err))
            else:
                return kube_config
    except EnvironmentError as err:
        raise Exception('Error opening {}: {}'.format(kube_config_path, err))

def main():
    docker_client = dockerd.DockerClient()
    try:
        server = docker_client.get_rancher_url_from_existing_agent()
    except Exception as err:
        print('Error attempting to get Rancher URL from existing agent: {}'.format(err))
        exit(1)
    print(server)

    try:
        etc_kubernetes_path = docker_client.get_etc_kubernetes_path_from_kubelet()
    except Exception as err:
        print('Error attempting to get host /etc/kubernetes path from kubelet: {}'.format(err))
        exit(1)
    print(etc_kubernetes_path)

    try:
        kube_config = parse_kube_config(etc_kubernetes_path)
    except Exception as err:
        print('Error attempting to parse node kubeconfig file: {}'.format(err))
        exit(1)
    print(kube_config)

    kube.test_k8s(kube_config)

    client = rancher.Client(url=server+'/v3',token='token-lnghs:f7sbnxc5956krqg24hx6j5rvb8q6zszldw7gt9vx4j5dh7l6pd4xlh',verify=False)

    token = client.by_id_cluster_registration_token('c-4xcmb'+':system')

    print(token['insecureCommand'])

if __name__ == '__main__':
    main()
