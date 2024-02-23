# External Imports
from typing import List
import requests

# Internal Imports
from src.endpoints.endpoint_scenario import EndpointScenario


class Endpoint(object):
    """Endpoint

        Class that contains the information for an application endpoint, with the different scenarios to calibrate
    """

    def __init__(self, name: str, endpoint_url: str, parameters: List) -> None:
        """__init__

            params:
                name: str: name of the endpoint
                endpoint_url: url of the endpoint
                parameters: list[dict]: parameters of the the endpoints, they contains both types (path, url...) and names
        """

        self.name: str = name
        self.endpoint_url: str  = endpoint_url
        self.parameters: List = parameters

        self.scenarios: List[EndpointScenario] = []

        self.__process_endpoint_url()



    def __process_endpoint_url(self) -> None:
        """__process_endpoint_url
            
            private class that parsed the endpoint url into a format where it is possible to add the path parameters values
        """

        split_url: List[str] = self.endpoint_url.split('/')

        # Todo just replace char < to { in conf ?
        formatted_url: str = ''
        for s in split_url:
            if len(s) == 0: continue

            if s[0] == '{':
                # Url parameter
                formatted_url += '/' + s.replace(':', '')
            else:
                # Regular
                formatted_url += f"/{s}"

        self.formatted_url: str = formatted_url



    def process_endpoint(self):
        """process_endpoint
            
            Return a generator of the different scenarios for the endpoint.
            each generator's item contains the url, the user experience, the the parameters name & value 
        """

        print(self.formatted_url)

        for scenario in self.scenarios:
            yield {
                "url": self.formatted_url.format(**scenario.parameters_values),
                "qoe": scenario.qoe,
                "parameters": [{'name': name, 'value': value} for name, value in scenario.parameters_values.items()]
            }



    def add_scenario(self, s: EndpointScenario) -> None:
        """add_scenario
            
            add a scenario to the scenarios list
            
            params: 
                s: EndpointScenario: endpoint scenario to add.
            
        """

        self.scenarios.append(s)