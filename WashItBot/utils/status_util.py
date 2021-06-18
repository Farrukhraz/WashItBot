from WashItBot.main import WASHING_MACHINES_MONITORING_UTIL as MU
from WashItBot.utils.monitoring_util import WashingProcess

STATUS_MESSAGE_TEMPLATE = """
Стиральная машина №{}
{}

Стиральная машина №2
{}

Стиральная машина №3
{}

Стиральная машина №4
{}

Сушилка №1              
{}

Сушилка №2
{}                

Сушилка №3              
{}                

Сушилка №4
{}"""


wash_machine_temp = "Стиральная машина №{}\n{}"
dry_machine_temp = "Сушилка №{}\n{}"



def get_all_machines_status():
    washing_machines_ids = [f"Стиральная машина:{i}" for i in range(1, 5)]
    drying_machines_ids = [f"Сушилка:{i}" for i in range(1, 5)]
    machines = []
    for _id in washing_machines_ids + drying_machines_ids:
        machine = MU.get_machine(_id)
        if _id.lower().startswith('ст'):
            text = f"Стиральная машина №{_id.split(':')[1]}\n"
        else:
            text = f"Сушилка №{_id.split(':')[1]}\n"
        if not machine or (machine and machine.get_remaining_time() == 0):
            machines.append("✅ " + text + "Cвободна")
        else:
            machines.append("❌ " + text + __get_machine_remaining_time(machine))
    return "\n\n".join(machines)


def __get_machine_remaining_time(machine: WashingProcess) -> str:
    _time = machine.get_remaining_time()    # get time in seconds
    mins, secs = divmod(int(_time), 60)
    return f"До конца осталось: {'%02.f' % mins} мин. {'%02.f' % secs} сек."
