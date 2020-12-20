import dockerd

def main():
    docker_client = dockerd.DockerClient()
    try:
        server = docker_client.get_rancher_url_from_existing_agent()
    except Exception as err:
        print("Error attempting to get Rancher URL from existing agent: {}".format(err))
        exit(1)
    print(server)

if __name__ == '__main__':
    main()
