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
