from ZodiacInfo import ZodiacInfo


class ZodiacPerson:
    """
    A class to hold data about an individual and their ZodiacInfo info.
    """

    def __init__(self, name, birthday_date, political=False, hottie=False, president=False):
        """
        Initializes a ZodiacInfo Object.
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
        self.sign = ZodiacInfo.get_sign_for_date_obj(self.birthday)
        self.symbol = ZodiacInfo.zodiac_symbols[self.sign]
        self.element = ZodiacInfo.get_element(self.sign)
        self.quality = ZodiacInfo.get_quality(self.sign)
        self.gay_position = ZodiacInfo.zodiac_sex_position[self.sign]
