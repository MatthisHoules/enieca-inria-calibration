# External Imports
import argparse
from typing import List, Dict

# Internal Imports
from src.io.utils import read_configuration_file, write_output_yaml_file
from src.calibration import Kepler
from src.calibration.calibrate import calibrate

if __name__ == '__main__':

    arg_parser = argparse.ArgumentParser(description='Application endpoints consumtion estimation module')
    arg_parser.add_argument('-a', '--app_addr', required=True, help='Address of the application to calibrate', type=str)
    arg_parser.add_argument('-c', '--configuration_path', required=True, help='application configuration json file path', type=str)
    arg_parser.add_argument('-k', '--kepler_addr', required=True, help='Kepler exporter address', type=str)
    arg_parser.add_argument('-p', '--app_container_name', required=True, help='Application Kuberneted Pod Name', type=str)
    arg_parser.add_argument('-o', '--output_path', required=True, help='Output path, could be a file path or a dir path', type=str)
    arg_parser.add_argument('-n', '--user_load', required=True, help='number of users for the calibration', type=int)
    arg_parser.add_argument('-i', '--calibration_iterations', required=True, help='number of iteration to calibration each scenario', type=int)

    args = arg_parser.parse_args()

    endpoints_to_calibrate: List = read_configuration_file(args.configuration_path)
    kepler: Kepler = Kepler(args.kepler_addr)


    calibrated_endpoints: Dict = calibrate(
        host=args.app_addr,
        app_container_name=args.app_container_name,
        list_endpoints=endpoints_to_calibrate,
        num_users=args.user_load,
        kepler=kepler,
        n_calibration=args.calibration_iterations
    )
    write_output_yaml_file(calibrated_endpoints, args.output_path)





