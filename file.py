
import os
import yaml

dir_path = os.path.dirname(os.path.realpath(__file__)) + '/data.yaml'

class File:
    def read_file():
        with open(r''+dir_path) as file:
            documents = yaml.full_load(file)

        return documents
        
    def write_file(documents, dict_file):
        with open(r''+dir_path, 'w') as file:
            documents = yaml.dump(dict_file, file)

    def get_host():
        path = os.path.dirname(os.path.realpath(__file__)) + '/config.yaml'
        with open(r''+path) as file:
            documents = yaml.full_load(file)
        
        return documents['thingsboard']['THINGSBOARD_HOST']

    def get_token():
        path = os.path.dirname(os.path.realpath(__file__)) + '/config.yaml'
        with open(r''+path) as file:
            documents = yaml.full_load(file)
        
        return documents['thingsboard']['ACCESS_TOKEN']

