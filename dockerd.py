import re

import docker

class DockerClient(object):
    def __init__(self):
        self.client = docker.from_env()

    def get_rancher_url_from_existing_agent(self):

        try:
            existing_node_agents = self.client.containers.list(all=True,filters={'name':'k8s_agent_cattle-node-agent'})
        except docker.errors.APIError as err:
            raise Exception('Failed to list existing containers: {}'.format(err))
        else:
            if len(existing_node_agents) == 0:
                raise Exception('No existing node-agent containers located.')
            else:
                agent = existing_node_agents[0]
                if 'Config' not in agent.attrs.keys():
                    raise Exception('Config block not found on container {} object'.format(agent.name))
                elif 'Env' not in agent.attrs['Config'].keys():
                    raise Exception('Env block not found on container {} object'.format(agent.name))
                else:
                    for env in agent.attrs['Config']['Env']:
                        match = re.search('^CATTLE_SERVER=', env)
                        if match != None:
                            server = env[match.span()[1]:]
                            return server
                    raise Exception('No CATTLE_SERVER environment variable found on container {} object'.format(agent.name))

    def get_etc_kubernetes_path_from_kubelet(self):

        try:
            kubelet = self.client.containers.get('kubelet')
        except docker.errors.NotFound as err:
            raise Exception("kubelet container not found.")
        except docker.errors.APIError as err:
            raise Exception('Failed to get kubelet container: {}'.format(err))
        else:
            if 'Mounts' not in kubelet.attrs.keys():
                raise Exception('Mounts block not found on kubelet container object')
            else:
                for mount in kubelet.attrs['Mounts']:
                    if 'Destination' in mount.keys() and mount['Destination'] == '/etc/kubernetes':
                        if 'Source' not in mount.keys():
                            raise Exception('No source found for mount /etc/kubernetes in kubelet container object mounts')
                        else:
                            return mount['Source']
                raise Exception('No mount with destination /etc/kubernetes found in kubelet container object')
