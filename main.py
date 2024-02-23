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

    args = arg_parser.parse_args()

    # -c './tests/conf_v1.json'
    # -k ecotype-44.nantes.grid5000.fr:9102
    # -a http://ecotype-44.nantes.grid5000.fr:5900/
    # -p fibonicci-app'

    endpoints_to_calibrate: List = read_configuration_file(args.configuration_path)
    kepler: Kepler = Kepler(args.kepler_addr)

    calibrated_endpoints: Dict = calibrate(
        args.app_addr,
        args.app_container_name,
        endpoints_to_calibrate,
        256,
        kepler
    )
    write_output_yaml_file(calibrated_endpoints, args.output_path)





