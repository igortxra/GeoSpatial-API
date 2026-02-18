from enum import Enum


class Weekday(Enum):
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6
    SUNDAY = 7

    @classmethod
    def from_string(cls, day: str):
        return cls[day.upper()].value


class Period(Enum):
    OVERNIGHT = 1
    EARLY_MORNING = 2
    AM_PEAK = 3
    MIDDAY = 4
    EARLY_AFTERNOON = 5
    PM_PEAK = 6
    EVENING = 7

    @classmethod
    def from_string(cls, value: str):
        normalized = value.upper().replace(" ", "_")
        period_code = cls[normalized]
        if period_code is None:
            raise Exception(f"Invalid period {normalized}")
        return period_code.value
