from enum import IntEnum

class TriggerStatus(IntEnum):
    START = 0
    SUCCESS = 1
    FAILURE = 2
    UNKNOWN = 99


class TriggerType(IntEnum):
    MANUAL = 0
    DAILY_AUTOMATION = 1
    CI_CD = 3