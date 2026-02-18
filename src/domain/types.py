from enum import Enum
from typing import Literal

WeekdayOption = Literal["Monday", "Tuesday", "Wednesday", "Thursday", "Saturday", "Sunday"]
class Weekday(Enum):
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6
    SUNDAY = 7

    @classmethod
    def from_weekday_option(cls, day: WeekdayOption) -> "Weekday":
        return cls[day.upper()]




PeriodOption = Literal["Overnight", "Early Morning", "AM Peak", "Midday", "Early Afternoon", "PM Peak", "Evening"]
class Period(Enum):
    OVERNIGHT = 1
    EARLY_MORNING = 2
    AM_PEAK = 3
    MIDDAY = 4
    EARLY_AFTERNOON = 5
    PM_PEAK = 6
    EVENING = 7

    @classmethod
    def from_period_option(cls, value: PeriodOption) -> "Period":
        normalized = value.upper().replace(" ", "_")
        period_code = cls[normalized]
        if period_code is None:
            raise Exception(f"Invalid period {normalized}")
        return period_code


