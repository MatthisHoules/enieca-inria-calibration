# External Imports
import requests
import re
from re import Pattern
from typing import Tuple



class Kepler(object):
    """Kepler

        Kepler wrapper class.
    """

    def __init__(self, address: str):
        """constructor

            Params:
                address: str: Kepler address and port
        """

        self.address: str = address



    def get_container_consumption(self, container_name: str) -> Tuple[float]:
        """get_container_consumption
            
            Returns the dynamic and the idle consumption of a container_name

            Params:
                container_name: str: name of the container to retrieve the energy consumption
        """

        response = requests.get(f"http://{self.address}/metrics")
        metrics_data: str = response.text               

        pattern_dynamic: Pattern = re.compile(r'kepler_container_joules_total.*container_name="'+container_name+r'".*,mode="dynamic",.*} (\d+\.\d+)')
        match = pattern_dynamic.search(metrics_data)
        dynamic_consumption: float = float(match.group(1)) if match else None 
        
        pattern_idle: Pattern = re.compile(r'kepler_container_joules_total.*container_name="'+container_name+r'".*,mode="idle",.*} (\d+\.\d+)')
        match = pattern_idle.search(metrics_data)
        idle_consumption: float = float(match.group(1)) if match else None

        return (dynamic_consumption, idle_consumption)
