import random
from typing import Optional


class BirthdayGen:
    """
    Randomly generate birthday, to test "Birthday paradox"
    """

    def __init__(self) -> None:
        self.MAX_BIRTHDAYS = 100
        self.MONTH = {
            "abbr_month": (
                "Jan",
                "Feb",
                "Mar",
                "Apr",
                "May",
                "Jun",
                "July",
                "Aug",
                "Sep",
                "Oct",
                "Nov",
                "Dec",
            ),
            "month": (
                "January",
                "February",
                "March",
                "April",
                "May",
                "June",
                "July",
                "August",
                "September",
                "October",
                "November",
                "December",
            ),
        }
        self.days = {30: [4, 6, 9, 11], 31: [1, 3, 5, 7, 8, 10, 12], 29: [2]}
        self.simulation = []

    def getBirthday(self, abbr: bool = True) -> str:
        month = self.MONTH["abbr_month"] if abbr else self.MONTH["month"]

        random_month = random.randint(0, 11)
        for key, val in self.days.items():
            if (random_month + 1) in val:
                day_seed = key
                break
        random_day = random.randint(1, day_seed)

        return f"{month[random_month]} {random_day}"

    def matchBirthday(self, birthdays: list) -> bool:
        birthdays_set = set(birthdays)
        if len(birthdays) == len(birthdays_set):
            return False
        return True

    def countMatchBirthday(self, birthdays: list) -> Optional[dict]:
        """
        Match a list of birthdays and return the numbers of birthdays in dict
        """
        if self.matchBirthday(birthdays):
            return None

        counts = {}
        for date in set(birthdays):
            counts[date] = 0
            len_before = len(birthdays)
            birthdays = list(filter(lambda x: x != date, birthdays))
            len_after = len(birthdays)
            counts[date] = len_before - len_after

        return counts

    def massGenerate(self, birthday_num: int):
        if 0 > birthday_num and birthday_num > self.MAX_BIRTHDAYS:
            return None

        return [self.getBirthday() for _ in range(birthday_num)]

    def paradoxAnalysis(self, num_experiment: int, num_birthdays: int):
        if 0 > num_experiment or (
            0 > num_birthdays and num_birthdays > self.MAX_BIRTHDAYS
        ):
            return None
        try:
            for i in range(num_experiment):
                birthdays = self.massGenerate(num_birthdays)
                if birthdays is None:
                    return
                self.simulation.append(1 if self.matchBirthday(birthdays) else 0)
                if (i + 1) % 1000 == 0:
                    print(f"{i+1} times gen")
            odd_match_birthdays = (
                round(sum(self.simulation) / len(self.simulation), 4) * 100
            )
            conclusion = f"""***************************************************************
Within {num_experiment} samples, 
we calculated the odds of match birthdays at a {num_birthdays} people group, 
the result is {odd_match_birthdays}%.
****************************************************************
"""

            return conclusion
        except Exception:
            raise Exception("paradoxAnalysis goes wrong")


if __name__ == "__main__":
    main = BirthdayGen()
    print(main.paradoxAnalysis(100000, 23))
