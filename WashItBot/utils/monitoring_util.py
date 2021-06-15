import logging
import threading

from time import time, sleep
from typing import Dict


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


class WashingProcess(threading.Thread):

    def __init__(self, user_id: str, machine_id: str, _time: int, *args, **kwargs) -> None:
        super().__init__(name=machine_id)
        self.user_id = user_id
        self.machine_id = machine_id
        self.__stop = False
        self.end_time = round(time() + self.__validate_time(_time))

    def is_busy(self) -> bool:
        return not self.__stop

    def create(self) -> None:
        self.start()

    def run(self):
        while not self.__stop and time() < self.end_time:
            sleep(1)
        self.__stop = True

    def get_remaining_time(self) -> int:
        """ Get remaining time of this machine in seconds """
        remaining_time = round(self.end_time - time())
        return remaining_time if remaining_time > 0 else 0

    def stop(self):
        self.__stop = True

    def __validate_time(self, _time: int) -> int:
        if not isinstance(_time, int):
            raise ValueError(f"Time must be instance of 'int' but instance of '{type(_time)}' is given instead")
        if _time < 1:
            raise ValueError(f"Time must be Natural number in range [1, +inf) but '{_time}' is given instead")
        return _time


class MonitoringUtil:

    def __init__(self):
        self.busy_machines: Dict[str, WashingProcess] = dict()

    def get_status(self) -> list:
        """ Returns free and busy washing machines with all necessary info

        :return: List[Tuple[str, int]]
            [(machine_id, remaining_time), (..., ...), ...]
        """
        result = []
        for machine_id in self.busy_machines:
            result.append((machine_id, self.get_remaining_time(machine_id), ))
        return result

    def get_remaining_time(self, machine_id: str) -> int:
        """ Return remaining time of the busy machine (in seconds)

        :param machine_id: str
            id of the machine
        :return: int
            -1  if machine hasn't been used before
            0   if machine is not busy
            >1  if machine is busy
        """
        machine = self.busy_machines.get(machine_id)
        if machine:
            return machine.get_remaining_time()
        return -1

    def is_machine_busy(self, machine_id: str) -> bool:
        """ True if machine is busy else False """
        machine = self.busy_machines.get(machine_id)
        if machine:
            return machine.is_busy()
        return False

    def take_machine(self, user_id: str, machine_id: str, _time: int) -> None:
        """ Take machine """
        if not self.is_machine_busy(machine_id):
            self.busy_machines[machine_id] = WashingProcess(user_id, machine_id, _time)
        else:
            logger.warning(f"id='{machine_id}' can't be taken 'cause it is busy")

