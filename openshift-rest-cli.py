import json
import requests
import yaml


class OpenShiftRest(object):

    def __init__(self, env):
        self.env = env
        self.__get_conf()

    def __get_conf(self):
        with open('openshift.yml', 'r') as conf_file:
            try:
                self.conf = yaml.load(conf_file)
            except yaml.YAMLError as exc:
                print exc

    def __get(self, uri, api='api'):
        response = requests.get("{}/{}/v1/{}".format(self.conf[self.env]['url'], api, uri),
                                headers={"Authorization": "Bearer {}".format(self.conf[self.env]['token'])},
                                timeout=3)
        return json.loads(response.text)

    def get_namespaces(self, dict_output=False):
        results = self.__get('namespaces')
        namespaces = []
        if not dict_output:
            for result in results['items']:
                namespaces.append(result['metadata']['name'])
        else:
            namespaces = results
        return namespaces

    def get_pods(self, namespaces, dict_output=False):
        pods = {}
        for namespace in namespaces:
            results = self.__get('namespaces/{}/pods'.format(namespace))
            if not dict_output:
                for result in results['items']:
                    if namespace in pods:
                        pods[namespace].append(result['metadata']['name'])
                    else:
                        pods[namespace] = [result['metadata']['name']]
            else:
                pods[namespace] = results
        return pods

    def get_all_pods(self, dict_output=False):
        results = self.get_pods(self.get_namespaces(), dict_output)
        return results

    def get_dc(self, namespaces, dict_output=False):
        dcs = {}
        for namespace in namespaces:
            results = self.__get('namespaces/{}/deplymentconfigs'.format(namespace), 'oapi')
            print results
            exit()
            if not dict_output:
                for result in results['items']:
                    if namespace in dcs:
                        dcs[namespace].append(result['metadata']['name'])
                    else:
                        dcs[namespace] = [result['metadata']['name']]
            else:
                dcs[namespace] = results
        return dcs

oc = OpenShiftRest('dev')
# print oc.get_namespaces()
# print oc.get_pods(['tools-dev'])
# print oc.get_all_pods()
print oc.get_dc(['tools-dev'])
