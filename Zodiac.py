import logging, sys

logging.basicConfig(stream=sys.stderr,
                    level=logging.CRITICAL)  # use logging.DEBUG for testing, logging.CRITICAL for runtime
# https://docs.python.org/3/library/logging.html#levels

import csv
import datetime
from collections import defaultdict

people_by_months_dict = defaultdict(list)

zodiac_symbols = {
    "Capricorn": "Sea-Goat (Goat-Fish hybrid)",
    "Aquarius": "Water-bearer",
    "Pisces": "Fish",
    "Aries": "Ram",
    "Taurus": "Bull",
    "Gemini": "Twins",
    "Cancer": "Crab",
    "Leo": "Lion",
    "Virgo": "Maiden",
    "Libra": "Scales",
    "Scorpio": "Scorpion",
    "Sagittarius": "Archer"
}

zodiac_elements = {
    "Water": ["Cancer", "Scorpio", "Pisces"],
    "Fire": ["Aries", "Leo", "Sagittarius"],
    "Earth": ["Taurus", "Virgo", "Capricorn"],
    "Air": ["Gemini", "Libra", "Aquarius"]
}

zodiac_element_descriptions = {
    "Water": "Water signs are exceptionally emotional and ultra-sensitive. They are highly intuitive and they can be as mysterious as the ocean itself. Water signs love profound conversations and intimacy. They rarely do anything openly and are always there to support their loved ones. The Water Signs are: Cancer, Scorpio and Pisces.",
    "Fire": "Fire signs tend to be passionate, dynamic, and temperamental. They get angry quickly, but they also forgive easily. They are adventurers with immense energy. They are physically very strong and are a source of inspiration for others. Fire signs are intelligent, self-aware, creative and idealistic people, always ready for action. The Fire Signs are: Aries, Leo and Sagittarius.",
    "Earth": "Earth signs are “grounded” and the ones that bring us down to earth. They are mostly conservative and realistic, but they can also be very emotional. They are connected to our material reality and can be turned to material goods. They are practical, loyal and stable and they stick by their people through hard times. The Earth Signs are: Taurus, Virgo and Capricorn.",
    "Air": "Air signs are rational, social, and love communication and relationships with other people. They are thinkers, friendly, intellectual, communicative and analytical. They love philosophical discussions, social gatherings and good books. They enjoy giving advice, but they can also be very superficial. The Air Signs are: Gemini, Libra and Aquarius."
}

zodiac_qualities = {
    "Cardinal": ["Aries", "Cancer", "Libra", "Capricorn"],
    "Mutable": ["Gemini", "Virgo", "Sagittarius", "Pisces"],
    "Fixed": ["Taurus", "Leo", "Scorpio", "Aquarius"]
}

zodiac_gay_position = {
    "Capricorn": "kinky top",
    "Aquarius": "soft bottom",
    "Pisces": "soft switch",
    "Aries": "power top",
    "Taurus": "power bottom",
    "Gemini": "kinky switch",
    "Cancer": "kinky bottom",
    "Leo": "power top",
    "Virgo": "power switch",
    "Libra": "soft switch",
    "Scorpio": "kinky top",
    "Sagittarius": "soft top"
}

zodiac_descriptions = {
    "Capricorn": "-Strengths: Responsible, disciplined, self-control, good managers"
                 "\nWeaknesses: Know-it-all, unforgiving, condescending, expecting the worst"
                 "\nCapricorn likes: Family, tradition, music, understated status, quality craftsmanship"
                 "\nCapricorn dislikes: Almost everything at some point"
                 "\nDescription: Capricorn is a sign that represents time and responsibility, and its representatives are traditional and often very serious by nature. These individuals possess an inner state of independence that enables significant progress both in their personal and professional lives. They are masters of self-control and have the ability to lead the way, make solid and realistic plans, and manage many people who work for them at any time. They will learn from their mistakes and get to the top based solely on their experience and expertise.",
    "Aquarius": "-Strengths: Progressive, original, independent, humanitarian"
                "\nWeaknesses: Runs from emotional expression, temperamental, uncompromising, aloof"
                "\nAquarius likes: Fun with friends, helping others, fighting for causes, intellectual conversation, a good listener"
                "\nAquarius dislikes: Limitations, broken promises, being lonely, dull or boring situations, people who disagree with them"
                "\nAquarius-born are shy and quiet, but on the other hand they can be eccentric and energetic. However, in both cases, they are deep thinkers and highly intellectual people who love helping others. They are able to see without prejudice, on both sides, which makes them people who can easily solve problems."
                "\nDescription: Although they can easily adapt to the energy that surrounds them, Aquarius-born have a deep need to be some time alone and away from everything, in order to restore power. People born under the Aquarius sign, look at the world as a place full of possibilities.",
    "Pisces": "-Strengths: Compassionate, artistic, intuitive, gentle, wise, musical"
              "\nWeaknesses: Fearful, overly trusting, sad, desire to escape reality, can be a victim or a martyr"
              "\nPisces likes: Being alone, sleeping, music, romance, visual media, swimming, spiritual themes"
              "\nPisces dislikes: Know-it-all, being criticized, the past coming back to haunt, cruelty of any kind"
              "\nDescription: Pisces are very friendly, so they often find themselves in a company of very different people. Pisces are selfless, they are always willing to help others, without hoping to get anything back.",
    "Aries": "-Strengths: Courageous, determined, confident, enthusiastic, optimistic, honest, passionate"
             "\nWeaknesses: Impatient, moody, short-tempered, impulsive, aggressive"
             "\nAries likes: Comfortable clothes, taking on leadership roles, physical challenges, individual sports"
             "\nAries dislikes: Inactivity, delays, work that does not use one's talents"
             "\nDescription: As the first sign in the zodiac, the presence of Aries always marks the beginning of something energetic and turbulent. They are continuously looking for dynamic, speed and competition, always being the first in everything - from work to social gatherings. Thanks to its ruling planet Mars and the fact it belongs to the element of Fire (just like Leo and Sagittarius), Aries is one of the most active zodiac signs. It is in their nature to take action, sometimes before they think about it well.",
    "Taurus": "-Strengths: Reliable, patient, practical, devoted, responsible, stable"
              "\nWeaknesses: Stubborn, possessive, uncompromising"
              "\nTaurus likes: Gardening, cooking, music, romance, high quality clothes, working with hands"
              "\nTaurus dislikes: Sudden changes, complications, insecurity of any kind, synthetic fabrics"
              "\nDescription: Practical and well-grounded, Taurus is the sign that harvests the fruits of labor. They feel the need to always be surrounded by love and beauty, turned to the material world, hedonism, and physical pleasures. People born with their Sun in Taurus are sensual and tactile, considering touch and taste the most important of all senses. Stable and conservative, this is one of the most reliable signs of the zodiac, ready to endure and stick to their choices until they reach the point of personal satisfaction.",
    "Gemini": "-Strengths: Gentle, affectionate, curious, adaptable, ability to learn quickly and exchange ideas"
              "\nWeaknesses: Nervous, inconsistent, indecisive"
              "\nGemini likes: Music, books, magazines, chats with nearly anyone, short trips around the town"
              "\nGemini dislikes: Being alone, being confined, repetition and routine"
              "\nDescription: Expressive and quick-witted, Gemini represents two different personalities in one and you will never be sure which one you will face. They are sociable, communicative and ready for fun, with a tendency to suddenly get serious, thoughtful and restless. They are fascinated with the world itself, extremely curious, with a constant feeling that there is not enough time to experience everything they want to see.",
    "Cancer": "Strengths: Tenacious, highly imaginative, loyal, emotional, sympathetic, persuasive"
              "\nWeaknesses: Moody, pessimistic, suspicious, manipulative, insecure"
              "\nCancer likes: Art, home-based hobbies, relaxing near or in water, helping loved ones, a good meal with friends"
              "\nCancer dislikes: Strangers, any criticism of Mom, revealing of personal life"
              "\nDescription: Deeply intuitive and sentimental, Cancer can be one of the most challenging zodiac signs to get to know. They are very emotional and sensitive, and care deeply about matters of the family and their home. Cancer is sympathetic and attached to people they keep close. Those born with their Sun in Cancer are very loyal and able to empathize with other people's pain and suffering.",
    "Leo": "Strengths: Creative, passionate, generous, warm-hearted, cheerful, humorous"
           "\nWeaknesses: Arrogant, stubborn, self-centered, lazy, inflexible"
           "\nLeo likes: Theater, taking holidays, being admired, expensive things, bright colors, fun with friends"
           "\nLeo dislikes: Being ignored, facing difficult reality, not being treated like a king or queen"
           "\nDescription: People born under the sign of Leo are natural born leaders. They are dramatic, creative, self-confident, dominant and extremely difficult to resist, able to achieve anything they want to in any area of life they commit to. There is a specific strength to a Leo and their \"king of the jungle\" status. Leo often has many friends for they are generous and loyal. Self-confident and attractive, this is a Sun sign capable of uniting different groups of people and leading them as one towards a shared cause, and their healthy sense of humor makes collaboration with other people even easier.",
    "Virgo": "-Strengths: Loyal, analytical, kind, hardworking, practical"
             "\nWeaknesses: Shyness, worry, overly critical of self and others, all work and no play"
             "\nVirgo likes: Animals, healthy food, books, nature, cleanliness"
             "\nVirgo dislikes: Rudeness, asking for help, taking center stage"
             "\nDescription: Virgos are always paying attention to the smallest details and their deep sense of humanity makes them one of the most careful signs of the zodiac. Their methodical approach to life ensures that nothing is left to chance, and although they are often tender, their heart might be closed for the outer world. This is a sign often misunderstood, not because they lack the ability to express, but because they won’t accept their feelings as valid, true, or even relevant when opposed to reason. The symbolism behind the name speaks well of their nature, born with a feeling they are experiencing everything for the first time.",
    "Libra": "-Strengths: Cooperative, diplomatic, gracious, fair-minded, social"
             "\nWeaknesses: Indecisive, avoids confrontations, will carry a grudge, self-pity"
             "\nLibra likes: Harmony, gentleness, sharing with others, the outdoors"
             "\nLibra dislikes: Violence, injustice, loudmouths, conformity"
             "\nDescription: People born under the sign of Libra are peaceful, fair, and they hate being alone. Partnership is very important for them, as their mirror and someone giving them the ability to be the mirror themselves. These individuals are fascinated by balance and symmetry, they are in a constant chase for justice and equality, realizing through life that the only thing that should be truly important to themselves in their own inner core of personality. This is someone ready to do nearly anything to avoid conflict, keeping the peace whenever possible",
    "Scorpio": "Strengths: Resourceful, brave, passionate, stubborn, a true friend"
               "\nWeaknesses: Distrusting, jealous, secretive, violent"
               "\nScorpio likes: Truth, facts, being right, longtime friends, teasing, a grand passion"
               "\nScorpio dislikes: Dishonesty, revealing secrets, passive people"
               "\nDescrption: Scorpio-born are passionate and assertive people. They are determined and decisive, and will research until they find out the truth. Scorpio is a great leader, always aware of the situation and also features prominently in resourcefulness.",
    "Sagittarius": "-Strengths: Generous, idealistic, great sense of humor"
                   "\nWeaknesses: Promises more than can deliver, very impatient, will say anything no matter how undiplomatic"
                   "\nSagittarius likes: Freedom, travel, philosophy, being outdoors"
                   "\nSagittarius dislikes: Clingy people, being constrained, off-the-wall theories, details"
                   "\nDescription: Curious and energetic, Sagittarius is one of the biggest travelers among all zodiac signs. Their open mind and philosophical view motivates them to wander around the world in search of the meaning of life. Sagittarius is extrovert, optimistic and enthusiastic, and likes changes. "
                   "\nSagittarius-born are able to transform their thoughts into concrete actions and they will do anything to achieve their goals."
}


def main():
    # Initialize people data
    init_people_from_csv()

    while True:
        user_input = get_int_input(
            "1. Look up a person."
            "\n2. Add a new person."
            "\n3. Look up a sign, symbol, date, or element."
            "\n4. Play a guessing game for signs and dates."
            "\n0. Exit."
            "\nPick an option:")
        if user_input == 1:
            person_found = False
            # Look up a person
            user_input = input("Enter a name and I will search the database for them: ").strip()
            for key, val in people_by_months_dict.items():
                logging.debug("Searching in key (month): " + str(key))
                for zodiac_person in val:
                    logging.debug("Comparing to person: " + zodiac_person.name)
                    if zodiac_person.name == user_input:
                        person_found = True
                        if zodiac_person.president == True:
                            print("NAME: President " + zodiac_person.name)
                        else:
                            print("NAME: " + zodiac_person.name)
                        print("Birthday: " + zodiac_person.birthday.strftime("%d %B, %Y (%A)"))
                        if zodiac_person.political:
                            print("This person is political.")
                        else:
                            print("This person is not political.")
                        # TODO: Continue here
                        """
                        self.sign = get_sign(self.birthday)
                        self.elment = get_element(self.sign[0])
                        self.quality = get_quality(self.sign[0])
                        self.gay_position = zodiac_gay_position[self.sign[0]]
                        """
                        break
                    if person_found:
                        break
            if not person_found:
                print("That person is not in my database")
        elif user_input == 2:
            # TODO: Continue here.
            pass
        elif user_input == 3:
            pass
        elif user_input == 4:
            pass
        elif user_input == 0:
            break
        else:
            pass


def init_people_from_csv():
    with open("people.csv", 'r', newline='') as f:
        reader = csv.DictReader(f)
        # fieldnames_for_csv = next(reader)  # Skip over headers
        for row in reader:
            people_by_months_dict[row["Month"]].append(ZodiacPerson(row["Name"],
                                                                    datetime.date(int(row["Year"]),
                                                                                  month_to_int(row["Month"]),
                                                                                  int(row["Day"])),
                                                                    bool(row["Political"]),
                                                                    bool(row["Hottie"]),
                                                                    bool(row["President"])
                                                                    ))
            # people_by_months_dict[row["Name"]] = date(int(row["Year"]), month_to_int(row["Month"]), int(row["Day"]))


def yield_dates_in_range(date1, date2):
    """
    Yields data objects within a range.
    :param date1: Date object of the starting date
    :param date2: Date object of the ending date
    :return: None, yields date objects within this range
    """
    for n in range(int((date2 - date1).days) + 1):
        yield date1 + timedelta(n)


def month_to_int(month):
    if month == "January":
        return 1
    elif month == "February":
        return 2
    elif month == "March":
        return 3
    elif month == "April":
        return 4
    elif month == "May":
        return 5
    elif month == "June":
        return 6
    elif month == "July":
        return 7
    elif month == "August":
        return 8
    elif month == "September":
        return 9
    elif month == "October":
        return 10
    elif month == "November":
        return 11
    elif month == "December":
        return 12
    else:
        raise Exception(str(month) + " is not a valid month.")


def get_sign(date_obj):
    """
    Takes an input date and returns the sign as a tuple of (sign, cusp).
    :param date: The date of the sign
    :return: (sign, cusp) tuple. Cusp may be None.
    """
    sign = None
    cusp = None

    # non-cusp
    if (date_obj.month == 12 and date_obj.day >= 22) or (date_obj.month == 1 and date_obj.day <= 20):
        sign = "Capricorn"
    elif (date_obj.month == 1 and date_obj.day >= 21) or (date_obj.month == 2 and date_obj.day <= 19):
        sign = "Aquarius"
    elif (date_obj.month == 2 and date_obj.day >= 20) or (date_obj.month == 3 and date_obj.day <= 20):
        sign = "Pisces"
    elif (date_obj.month == 3 and date_obj.day >= 21) or (date_obj.month == 4 and date_obj.day <= 20):
        sign = "Aries"
    elif (date_obj.month == 4 and date_obj.day >= 21) or (date_obj.month == 5 and date_obj.day <= 20):
        sign = "Taurus"
    elif (date_obj.month == 5 and date_obj.day >= 21) or (date_obj.month == 6 and date_obj.day <= 21):
        sign = "Gemini"
    elif (date_obj.month == 6 and date_obj.day >= 22) or (date_obj.month == 7 and date_obj.day <= 22):
        sign = "Cancer"
    elif (date_obj.month == 7 and date_obj.day >= 23) or (date_obj.month == 8 and date_obj.day <= 23):
        sign = "Leo"
    elif (date_obj.month == 8 and date_obj.day >= 24) or (date_obj.month == 9 and date_obj.day <= 22):
        sign = "Virgo"
    elif (date_obj.month == 9 and date_obj.day >= 23) or (date_obj.month == 10 and date_obj.day <= 22):
        sign = "Libra"
    elif (date_obj.month == 10 and date_obj.day >= 23) or (date_obj.month == 11 and date_obj.day <= 22):
        sign = "Scorpio"
    elif (date_obj.month == 11 and date_obj.day >= 23) or (date_obj.month == 12 and date_obj.day <= 21):
        sign = "Sagittarius"
    else:
        raise Exception("No sign was assigned in get_sign()")

    # cusps
    if (date_obj.month == 1 and date_obj.day >= 16) or (date_obj.month == 1 and date_obj.day <= 23):
        cusp = "Capricorn/Aquarius"
    elif (date_obj.month == 2 and date_obj.day >= 15) or (date_obj.month == 2 and date_obj.day <= 21):
        cusp = "Aquarius/Pisces"
    elif (date_obj.month == 3 and date_obj.day >= 17) or (date_obj.month == 3 and date_obj.day <= 23):
        cusp = "Pisces/Aries"
    elif (date_obj.month == 4 and date_obj.day >= 16) or (date_obj.month == 4 and date_obj.day <= 22):
        cusp = "Aries/Taurus"
    elif (date_obj.month == 5 and date_obj.day >= 17) or (date_obj.month == 5 and date_obj.day <= 23):
        cusp = "Taurus/Gemini"
    elif (date_obj.month == 6 and date_obj.day >= 17) or (date_obj.month == 6 and date_obj.day <= 23):
        cusp = "Gemini/Cancer"
    elif (date_obj.month == 7 and date_obj.day >= 19) or (date_obj.month == 7 and date_obj.day <= 25):
        cusp = "Cancer/Leo"
    elif (date_obj.month == 8 and date_obj.day >= 19) or (date_obj.month == 8 and date_obj.day <= 25):
        cusp = "Leo/Virgo"
    elif (date_obj.month == 9 and date_obj.day >= 19) or (date_obj.month == 9 and date_obj.day <= 25):
        cusp = "Virgo/Libra"
    elif (date_obj.month == 10 and date_obj.day >= 19) or (date_obj.month == 10 and date_obj.day <= 25):
        cusp = "Libra/Scorpio"
    elif (date_obj.month == 11 and date_obj.day >= 18) or (date_obj.month == 11 and date_obj.day <= 24):
        cusp = "Scorpio/Sagittarius"
    elif (date_obj.month == 12 and date_obj.day >= 18) or (date_obj.month == 12 and date_obj.day <= 24):
        cusp = "Sagittarius/Capricorn"
    else:
        pass  # No cusp detected

    tup = (sign, cusp)
    return tup


def get_quality(sign):
    """
    Helper method to get a quality for a Zodiac sign.
    :param sign: The sign we want the quality for.
    :return: The quality
    """
    for key, val in zodiac_qualities.items():
        if val == sign:
            return key


def get_element(sign):
    """
    Helper method to get a element for a Zodiac sign.
    :param sign: The sign we want the element for.
    :return: The element
    """
    for key, val in zodiac_elements.items():
        if val == sign:
            return key


def get_int_input(query_str):
    """
    Prompt the user for an integer input and only continue once they've given a valid input.
    :param query_str:   The prompt to the user.
    :return:    An integer type that the user has entered.
    """
    while True:
        try:
            return int(input(query_str))
        except ValueError:
            print("That didn't work. Try again.")


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
        self.political = bool(political)
        self.hottie = bool(hottie)
        self.president = bool(president)
        self.sign = get_sign(self.birthday)
        self.elment = get_element(self.sign[0])
        self.quality = get_quality(self.sign[0])
        self.gay_position = zodiac_gay_position[self.sign[0]]


if __name__ == "__main__":
    main()
