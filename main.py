import dockerd

def main():
    docker_client = dockerd.DockerClient()
    try:
        server = docker_client.get_rancher_url_from_existing_agent()
    except Exception as err:
        print("Error attempting to get Rancher URL from existing agent: {}".format(err))
        exit(1)
    print(server)

    try:
        etc_kubernetes_path = docker_client.get_etc_kubernetes_path_from_kubelet()
    except Exception as err:
        print("Error attempting to get host /etc/kubernetes path from kubelet: {}".format(err))
        exit(1)
    print(etc_kubernetes_path)

if __name__ == '__main__':
    main()
