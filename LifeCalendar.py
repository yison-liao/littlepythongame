import datetime


def LifeCalendar(birthday: str, expected_life: int):
    time_spend = chr(9632)
    time_left = chr(9633)
    time_sleep = chr(9679)
    time_sick = chr(9675)
    THIS_TIME = chr(9788)
    DAYS_PER_YEAR = 365
    WEEK_DAY = 7
    SLEEP_HOURS_PER_DAY = 7
    RETIRED_AGE = 65

    now = datetime.datetime.now()
    birthday_parse = datetime.datetime.strptime(birthday, "%Y/%m/%d")
    weeks_lives = (now - birthday_parse).days // WEEK_DAY
    this_week = weeks_lives + 1
    retire_week = RETIRED_AGE * DAYS_PER_YEAR // WEEK_DAY
    sleep_week = int((retire_week - weeks_lives) * (SLEEP_HOURS_PER_DAY / 24))

    header = r"y\w,"
    for i in range(1, DAYS_PER_YEAR // WEEK_DAY + 1):
        header += str(i)
        if i != 52:
            header += ","

    life = ""
    week = 0
    expected_life_week = expected_life * DAYS_PER_YEAR // WEEK_DAY
    year_idx = 1
    while week <= expected_life_week:
        for i in range(0, DAYS_PER_YEAR // WEEK_DAY + 1):
            if i == 0:
                life += str(year_idx)
                life += ","
                continue
            elif week <= weeks_lives:
                life += time_spend
            elif week == this_week:
                life += THIS_TIME
            elif (retire_week - sleep_week) <= week < retire_week:
                life += time_sleep
            elif week >= retire_week:
                life += time_sick
            else:
                life += time_left
            week += 1
            if i != 52:
                life += ","
        life += "\n"
        year_idx += 1

    return header + "\n" + life


if __name__ == "__main__":
    print(LifeCalendar("1992/12/21", 70))
