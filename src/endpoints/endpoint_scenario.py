from dataclasses import dataclass

@dataclass
class EndpointScenario(object):
    """Endpoint Scenario
        
        Calibration scenario for an endpoint.
        The class contains the endpoint parameters values as well as the Quality of user Experience (QoE) defined in the 
        configuration file provided to the module
    """

    parameters_values: dict
    qoe: int