# External Imports
import invokust
from locust import HttpUser, task, constant
from locust.log import setup_logging
from typing import Tuple, List, Dict
import time
from statistics import median, mean

# Internal Imports
from src.calibration.kepler import Kepler
from src.endpoints.endpoint import Endpoint




def calibrate(host: str, app_container_name: str, list_endpoints: List[Endpoint], num_users, kepler: Kepler, calibration_duration: str = '30s', n_calibration: int = 5):
    """calibrate

        Calibrate the different endpoints

        Params:
            host: str: application Host
            list_endpoints: List[Endpoint]: list of the application endpoints to be calibrated
            num_users: int: charge of the calibration
            calibration_duration: str: duration: duration of the calibration for each endpoint
            n_calibration: number of calibration for each endpoint scenario
    """

    endpoints_calibrated: dict = {"endpoints": []}

    for endpoint in list_endpoints:
        
        e: dict = {
            'name': endpoint.name,
            'redirect': endpoint.endpoint_url,
            'parameters': endpoint.parameters,
            'benchmark': []
        }

        for scenario in endpoint.process_endpoint():            
            list_req_s: List = []
            list_consumption_per_request: List = []

            for i in range(n_calibration):
                before_calibration_energy: Tuple[float] = kepler.get_container_consumption(app_container_name)

                class WebsiteUser(HttpUser):
                    wait_time = constant(1)

                    @task()
                    def get_home_page(self):
                        self.client.get(scenario['url'])

                settings = invokust.create_settings(
                    classes=[WebsiteUser],
                    host=host,
                    num_users=num_users,
                    spawn_rate=num_users,
                    run_time=calibration_duration,
                    reset_stats=True
                )

                loadtest = invokust.LocustLoadTest(settings)
                loadtest.run()    
                stats_loadtest: Dict = loadtest.stats()
                
                import json
                with open("sample.json", "w") as outfile: 
                    json.dump(stats_loadtest, outfile, indent=4) 

                del loadtest

                after_calibration_energy: Tuple[float] = kepler.get_container_consumption(app_container_name)
                
                list_req_s.append(stats_loadtest['num_requests']/30)
                list_consumption_per_request.append(round((after_calibration_energy[0] - before_calibration_energy[0]) / stats_loadtest['num_requests'], 5))
                
                # 50s delay to avoid overload (could lead to refused requests)
                time.sleep(60)
            
            e['benchmark'].append({
                'qoe': scenario['qoe'],
                
                'meanRps': mean(list_req_s),
                'medianRps': median(list_req_s),
                'minRps': min(list_req_s),
                'maxRps': max(list_req_s),
                'meanJoulesPerRequest': mean(list_consumption_per_request),
                'medianJoulesPerRequest': median(list_consumption_per_request),
                'maxJoulesPerRequest': max(list_consumption_per_request),
                'minJoulesPerRequest': min(list_consumption_per_request),

                'parameters': scenario['parameters']
            })

        endpoints_calibrated['endpoints'].append(e)

    return endpoints_calibrated