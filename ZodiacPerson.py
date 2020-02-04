from Zodiac import Zodiac


class ZodiacPerson:
    """
    A class to hold data about an individual and their Zodiac info.
    """

    def __init__(self, name, birthday_date, political=False, hottie=False, president=False):
        """
        Initializes a Zodiac Object.
        :param name: The name of the person.
        :param birthday_date: Their birthday as a Date Object.
        :param political: Whether or not this person is politically involved.
        :param hottie: Whether or not this person is a hottie.
        :param president: Whether or not this person is a president.
        """
        self.name = name
        self.birthday = birthday_date
        """stored as a date object"""
        self.political = bool(political)
        self.hottie = bool(hottie)
        self.president = bool(president)
        self.sign = Zodiac.get_sign_for_date_obj(self.birthday)
        self.symbol = Zodiac.zodiac_symbols[self.sign]
        self.element = Zodiac.get_element(self.sign)
        self.quality = Zodiac.get_quality(self.sign)
        self.gay_position = Zodiac.zodiac_gay_position[self.sign]
