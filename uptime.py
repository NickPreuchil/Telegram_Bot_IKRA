import datetime

startup_time = datetime.datetime.now()


def uptime() -> datetime.datetime:
    """
    Returns the current uptime of the program.
    :return: datetime.datetime
    """
    return datetime.datetime.now() - startup_time