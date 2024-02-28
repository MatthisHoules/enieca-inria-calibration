# External Imports
from typing import List, Dict
import yaml
import json
import os

# Internal Imports
from src.endpoints.endpoint import Endpoint
from src.endpoints.endpoint_scenario import EndpointScenario



def read_configuration_file(file_path: str) -> List[Endpoint]:
    """read_configuration_file
        
        Params: 
            file_path: str: configuration path
    """

    with open(file_path) as infile:
        configuration: dict = json.load(infile)

    list_endpoints: List[Endpoint] = []    
    for endpoint_name, endpoint_configuration in configuration.items():
        e = Endpoint(endpoint_name, endpoint_configuration['url'], endpoint_configuration['parameters'])

        for scenario in endpoint_configuration['scenarios']:
            e.add_scenario(EndpointScenario(
                scenario['parameters_values'],
                scenario['qoe']
            ))

        list_endpoints.append(e)

    return list_endpoints



def write_output_yaml_file(data: Dict, file_path: str) -> None:
    """write_output_yaml_file
        
        Params:
            data: Dict: data to write in a yml file
            file_path: str, dir or file path of the output yaml file. If path is a dir, the file name is set to 'output.yml'
    """

    if os.path.isdir(file_path):
        file_path = os.path.join(file_path, 'output.yml')

    with open(file_path, 'w') as file:
        yaml.dump(data, file, sort_keys=False)


