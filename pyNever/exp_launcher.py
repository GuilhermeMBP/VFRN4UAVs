import csv
import logging
import os
import signal
import sys
import time
from contextlib import contextmanager

import pynever.strategies.conversion as conv
from pynever.strategies.conversion import ONNXConverter, ONNXNetwork
from pynever.strategies.verification import NeVerProperty, NeverVerification

pynever_setting = [#['Over-approx.', 'overapprox', [0]],
                   #['Mixed1', 'mixed', [1]],
                   ['Complete', 'complete', [10000]]]

logger_stream = logging.getLogger("pynever.strategies.verification")
logger_file = logging.getLogger("log_file")

logger_stream.addHandler(logging.StreamHandler())
logger_file.addHandler(logging.FileHandler('/app/VFRN4UAVs/pyNever/logs/experiments_quadrants_436.csv'))

logger_stream.setLevel(logging.INFO)
logger_file.setLevel(logging.INFO)

logger_ver = logging.getLogger("pynever.strategies.abstraction.layers")
logger_ver.setLevel(logging.INFO)


class TimeoutException(Exception):
    """
    Exception class for timeout

    """

    pass


@contextmanager
def time_limit(seconds: int):
    def signal_handler(signum, frame):
        raise TimeoutException('Timeout')

    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(seconds)

    try:
        yield
    finally:
        signal.alarm(0)


def exec_instance(network_path: str, property_path: str, property_id: str, timeout_seconds: int):
    network_instance = conv.load_network_path(network_path)
    onnx_net = None
    if isinstance(network_instance, ONNXNetwork):
        onnx_net = ONNXConverter().to_neural_network(network_instance)

    property_instance = NeVerProperty()
    property_instance.from_smt_file(property_path)

    inst_name = f"[{network_instance.identifier} - {property_id}]"
    part_string = f'{inst_name},'

    for setting in pynever_setting:
        logger_stream.info(f"Benchmark: {inst_name}")
        logger_stream.info(f"PyNeVer setting: {setting[0]}")

        try:
            with time_limit(timeout_seconds):
                strategy = NeverVerification(setting[1], setting[2])
                time_start = time.perf_counter()
                safe = not strategy.verify(onnx_net, property_instance)
                time_end = time.perf_counter()
                part_string += f"{safe},{time_end - time_start},"
        except TimeoutException:
            part_string += f"---,---,"
            break

    logger_file.info(part_string[:-1])

if __name__ == '__main__':
    '''
    Usage: python exp_launcher.py 1 100 
    for running all tests with 100 seconds timeout
    
    '''

    TEST_DRONES = True if sys.argv[1] == '1' else False
    TIMEOUT = int(sys.argv[2])

    logger_file.info('Benchmark,Over-approx.,,Complete,,')
    logger_file.info(',Result,Time,Result,Time')

    # Drones launcher
    if TEST_DRONES:
        with open('/app/VFRN4UAVs/discrete/datasets/dataset_20.08.2024/final/vnnlibs_0.01_quadrants/vnnlib_files_continue.csv') as instances:
            csv_reader = csv.reader(instances)

            for instance in csv_reader:
                exec_instance(f"/app/VFRN4UAVs/discrete/models/sac_kin_discrete2d_complex_wo_tanh_436reward.onnx",
                              f"/app/VFRN4UAVs/discrete/datasets/dataset_20.08.2024/final/vnnlibs_0.01_quadrants/{instance[0]}",
                              instance[0], TIMEOUT)



