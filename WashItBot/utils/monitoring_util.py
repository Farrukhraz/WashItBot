

class MonitoringUtil:

    def status(self) -> list:
        """ Returns free and busy washing machines with all necessary info """
        pass

    def get_remaining_time(self, _id: str) -> int:
        """ Return remaining time of the machine (in seconds) if it is or 0 if machine is free """
        pass

    def create_event(self, *args, **kwargs) -> None:
        """ Create event if machine is being taken """
        pass

