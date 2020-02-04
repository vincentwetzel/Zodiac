import logging
import sys
import pandas
import datetime
import calendar
from collections import defaultdict
import shutil
import os

# TODO: Create a web scraper to pull Zodac intimacy data from astrology-zodiac-signs.com
# TODO: COnvert this to an OOP design

# NOTE TO USER: use logging.DEBUG for testing, logging.CRITICAL for runtime
logging.basicConfig(stream=sys.stderr,
                    level=logging.CRITICAL)

zodiac_sign_descriptions = {
    "Capricorn": "-Strengths: Responsible, disciplined, self-control, good managers"
                 "\n-Weaknesses: Know-it-all, unforgiving, condescending, expecting the worst"
                 "\n-Capricorn likes: Family, tradition, music, understated status, quality craftsmanship"
                 "\n-Capricorn dislikes: Almost everything at some point"
                 "\n-Description: Capricorn is a sign that represents time and responsibility, and its representatives are traditional and often very serious by nature."
                 "\nThese individuals possess an inner state of independence that enables significant progress both in their personal and professional lives."
                 "\nThey are masters of self-control and have the ability to lead the way, make solid and realistic plans, and manage many people who work for them at any time."
                 "\nThey will learn from their mistakes and get to the top based solely on their experience and expertise.",
    "Aquarius": "-Strengths: Progressive, original, independent, humanitarian"
                "\n-Weaknesses: Runs from emotional expression, temperamental, uncompromising, aloof"
                "\n-Aquarius likes: Fun with friends, helping others, fighting for causes, intellectual conversation, a good listener"
                "\n-Aquarius dislikes: Limitations, broken promises, being lonely, dull or boring situations, people who disagree with them"
                "\n-Description: Aquarius-born are shy and quiet, but on the other hand they can be eccentric and energetic."
                "\nHowever, in both cases, they are deep thinkers and highly intellectual people who love helping others."
                "\nThey are able to see without prejudice, on both sides, which makes them people who can easily solve problems."
                "\nAlthough they can easily adapt to the energy that surrounds them, Aquarius-born have a deep need to be some time alone and away from everything, in order to restore power."
                "\nPeople born under the Aquarius sign, look at the world as a place full of possibilities.",
    "Pisces": "-Strengths: Compassionate, artistic, intuitive, gentle, wise, musical"
              "\n-Weaknesses: Fearful, overly trusting, sad, desire to escape reality, can be a victim or a martyr"
              "\n-Pisces likes: Being alone, sleeping, music, romance, visual media, swimming, spiritual themes"
              "\n-Pisces dislikes: Know-it-all, being criticized, the past coming back to haunt, cruelty of any kind"
              "\n-Description: Pisces are very friendly, so they often find themselves in a company of very different people."
              "\nPisces are selfless, they are always willing to help others, without hoping to get anything back.",
    "Aries": "-Strengths: Courageous, determined, confident, enthusiastic, optimistic, honest, passionate"
             "\n-Weaknesses: Impatient, moody, short-tempered, impulsive, aggressive"
             "\n-Aries likes: Comfortable clothes, taking on leadership roles, physical challenges, individual sports"
             "\n-Aries dislikes: Inactivity, delays, work that does not use one's talents"
             "\n-Description: As the first sign in the zodiac, the presence of Aries always marks the beginning of something energetic and turbulent."
             "\nThey are continuously looking for dynamic, speed and competition, always being the first in everything - from work to social gatherings."
             "\nThanks to its ruling planet Mars and the fact it belongs to the element of Fire (just like Leo and Sagittarius), Aries is one of the most active zodiac signs."
             "\nIt is in their nature to take action, sometimes before they think about it well.",
    "Taurus": "-Strengths: Reliable, patient, practical, devoted, responsible, stable"
              "\n-Weaknesses: Stubborn, possessive, uncompromising"
              "\n-Taurus likes: Gardening, cooking, music, romance, high quality clothes, working with hands"
              "\n-Taurus dislikes: Sudden changes, complications, insecurity of any kind, synthetic fabrics"
              "\n-Description: Practical and well-grounded, Taurus is the sign that harvests the fruits of labor."
              "\nThey feel the need to always be surrounded by love and beauty, turned to the material world, hedonism, and physical pleasures."
              "\nPeople born with their Sun in Taurus are sensual and tactile, considering touch and taste the most important of all senses."
              "\nStable and conservative, this is one of the most reliable signs of the zodiac, ready to endure and stick to their choices until they reach the point of personal satisfaction.",
    "Gemini": "-Strengths: Gentle, affectionate, curious, adaptable, ability to learn quickly and exchange ideas"
              "\n-Weaknesses: Nervous, inconsistent, indecisive"
              "\n-Gemini likes: Music, books, magazines, chats with nearly anyone, short trips around the town"
              "\n-Gemini dislikes: Being alone, being confined, repetition and routine"
              "\n-Description: Expressive and quick-witted, Gemini represents two different personalities in one and you will never be sure which one you will face."
              "\nThey are sociable, communicative and ready for fun, with a tendency to suddenly get serious, thoughtful and restless."
              "\nThey are fascinated with the world itself, extremely curious, with a constant feeling that there is not enough time to experience everything they want to see.",
    "Cancer": "-Strengths: Tenacious, highly imaginative, loyal, emotional, sympathetic, persuasive"
              "\n-Weaknesses: Moody, pessimistic, suspicious, manipulative, insecure"
              "\n-Cancer likes: Art, home-based hobbies, relaxing near or in water, helping loved ones, a good meal with friends"
              "\n-Cancer dislikes: Strangers, any criticism of Mom, revealing of personal life"
              "\n-Description: Deeply intuitive and sentimental, Cancer can be one of the most challenging zodiac signs to get to know."
              "\nThey are very emotional and sensitive, and care deeply about matters of the family and their home."
              "\nCancer is sympathetic and attached to people they keep close."
              "\nThose born with their Sun in Cancer are very loyal and able to empathize with other people's pain and suffering.",
    "Leo": "-Strengths: Creative, passionate, generous, warm-hearted, cheerful, humorous"
           "\n-Weaknesses: Arrogant, stubborn, self-centered, lazy, inflexible"
           "\n-Leo likes: Theater, taking holidays, being admired, expensive things, bright colors, fun with friends"
           "\n-Leo dislikes: Being ignored, facing difficult reality, not being treated like a king or queen"
           "\n-Description: People born under the sign of Leo are natural born leaders."
           "\nThey are dramatic, creative, self-confident, dominant and extremely difficult to resist, able to achieve anything they want to in any area of life they commit to."
           "\nThere is a specific strength to a Leo and their \"king of the jungle\" status."
           "\nLeo often has many friends for they are generous and loyal."
           "\nSelf-confident and attractive, this is a Sun sign capable of uniting different groups of people and leading them as one towards a shared cause, and their healthy sense of humor makes collaboration with other people even easier.",
    "Virgo": "-Strengths: Loyal, analytical, kind, hardworking, practical"
             "\n-Weaknesses: Shyness, worry, overly critical of self and others, all work and no play"
             "\n-Virgo likes: Animals, healthy food, books, nature, cleanliness"
             "\n-Virgo dislikes: Rudeness, asking for help, taking center stage"
             "\n-Description: Virgos are always paying attention to the smallest details and their deep sense of humanity makes them one of the most careful signs of the zodiac."
             "\nTheir methodical approach to life ensures that nothing is left to chance, and although they are often tender, their heart might be closed for the outer world."
             "\nThis is a sign often misunderstood, not because they lack the ability to express, but because they won’t accept their feelings as valid, true, or even relevant when opposed to reason."
             "\nThe symbolism behind the name speaks well of their nature, born with a feeling they are experiencing everything for the first time.",
    "Libra": "-Strengths: Cooperative, diplomatic, gracious, fair-minded, social"
             "\n-Weaknesses: Indecisive, avoids confrontations, will carry a grudge, self-pity"
             "\n-Libra likes: Harmony, gentleness, sharing with others, the outdoors"
             "\n-Libra dislikes: Violence, injustice, loudmouths, conformity"
             "\n-Description: People born under the sign of Libra are peaceful, fair, and they hate being alone."
             "\nPartnership is very important for them, as their mirror and someone giving them the ability to be the mirror themselves."
             "\nThese individuals are fascinated by balance and symmetry, they are in a constant chase for justice and equality, realizing through life that the only thing that should be truly important to themselves in their own inner core of personality."
             "\nThis is someone ready to do nearly anything to avoid conflict, keeping the peace whenever possible",
    "Scorpio": "-Strengths: Resourceful, brave, passionate, stubborn, a true friend"
               "\n-Weaknesses: Distrusting, jealous, secretive, violent"
               "\n-Scorpio likes: Truth, facts, being right, longtime friends, teasing, a grand passion"
               "\n-Scorpio dislikes: Dishonesty, revealing secrets, passive people"
               "\n-Descrption: Scorpio-born are passionate and assertive people."
               "\nThey are determined and decisive, and will research until they find out the truth."
               "\nScorpio is a great leader, always aware of the situation and also features prominently in resourcefulness.",
    "Sagittarius": "-Strengths: Generous, idealistic, great sense of humor"
                   "\n-Weaknesses: Promises more than can deliver, very impatient, will say anything no matter how undiplomatic"
                   "\n-Sagittarius likes: Freedom, travel, philosophy, being outdoors"
                   "\n-Sagittarius dislikes: Clingy people, being constrained, off-the-wall theories, details"
                   "\n-Description: Curious and energetic, Sagittarius is one of the biggest travelers among all zodiac signs."
                   "\nTheir open mind and philosophical view motivates them to wander around the world in search of the meaning of life."
                   "\nSagittarius is extrovert, optimistic and enthusiastic, and likes changes."
                   "\nSagittarius-born are able to transform their thoughts into concrete actions and they will do anything to achieve their goals."
}
"""{ Sign: Description }"""

zodiac_symbols = {
    "Capricorn": "Sea-Goat (Goat-Fish hybrid)",
    "Capricorn/Aquarius": "Sea-Goat (Goat-Fish hybrid)/Water-bearer",
    "Aquarius": "Water-bearer",
    "Aquarius/Pisces": "Water-bearer/Fish",
    "Pisces": "Fish",
    "Pisces/Aries": "Fish/Ram",
    "Aries": "Ram",
    "Aries/Taurus": "Ram/Bull",
    "Taurus": "Bull",
    "Taurus/Gemini": "Bull/Twins",
    "Gemini": "Twins",
    "Gemini/Cancer": "Twins/Crab",
    "Cancer": "Crab",
    "Cancer/Leo": "Crab/Lion",
    "Leo": "Lion",
    "Leo/Virgo": "Lion/Maiden",
    "Virgo": "Maiden",
    "Virgo/Libra": "Maiden/Scales",
    "Libra": "Scales",
    "Libra/Scorpio": "Scales/Scorpio",
    "Scorpio": "Scorpion",
    "Scorpio/Sagittarius": "Scorpion/Archer",
    "Sagittarius": "Archer",
    "Sagittarius/Capricorn": "Archer/Sea-Goat (Goat-Fish hybrid)"
}
"""{ Sign: Symbol }"""

zodiac_elements = {
    "Water": ["Cancer", "Scorpio", "Pisces"],
    "Fire": ["Aries", "Leo", "Sagittarius"],
    "Earth": ["Taurus", "Virgo", "Capricorn"],
    "Air": ["Gemini", "Libra", "Aquarius"],
    "Earth/Air": ["Capricorn/Aquarius", "Taurus/Gemini", "Virgo/Libra"],
    "Air/Water": ["Aquarius/Pisces", "Gemini/Cancer", "Libra/Scorpio"],
    "Water/Fire": ["Pisces/Aries", "Cancer/Leo", "Scorpio/Sagittarius"],
    "Fire/Earth": ["Aries/Taurus", "Leo/Virgo", "Sagittarius/Capricorn"],
}
"""{ Element: Zodiac Sign }"""

zodiac_element_descriptions = {
    "Water": "The Water Signs are Cancer, Scorpio and Pisces."
             "\nWater signs are exceptionally emotional and ultra-sensitive."
             "\nThey are highly intuitive and they can be as mysterious as the ocean itself."
             "\nWater signs love profound conversations and intimacy."
             "\nThey rarely do anything openly and are always there to support their loved ones.",
    "Fire": "The Fire Signs are Aries, Leo and Sagittarius."
            "\nFire signs tend to be passionate, dynamic, and temperamental."
            "\nThey get angry quickly, but they also forgive easily."
            "\nThey are adventurers with immense energy."
            "\nThey are physically very strong and are a source of inspiration for others."
            "\nFire signs are intelligent, self-aware, creative and idealistic people, always ready for action.",
    "Earth": "The Earth Signs are Taurus, Virgo and Capricorn."
             "\nEarth signs are “grounded” and the ones that bring us down to earth."
             "\nThey are mostly conservative and realistic, but they can also be very emotional."
             "\nThey are connected to our material reality and can be turned to material goods."
             "\nThey are practical, loyal and stable and they stick by their people through hard times.",
    "Air": "The Air Signs are Gemini, Libra and Aquarius."
           "\nAir signs are rational, social, and love communication and relationships with other people."
           "\nThey are thinkers, friendly, intellectual, communicative and analytical."
           "\nThey love philosophical discussions, social gatherings and good books."
           "\nThey enjoy giving advice, but they can also be very superficial."
}
"""{ Element: Description }"""

zodiac_qualities = {
    "Cardinal": ["Capricorn", "Aries", "Cancer", "Libra"],
    "Fixed": ["Aquarius", "Taurus", "Leo", "Scorpio"],
    "Mutable": ["Pisces", "Gemini", "Virgo", "Sagittarius"],
    "Cardinal/Fixed": ["Capricorn/Aquarius", "Aries/Taurus", "Cancer/Leo", "Libra/Scorpio"],
    "Fixed/Mutable": ["Aquarius/Pisces", "Taurus/Gemini", "Leo/Virgo", "Scorpio/Sagittarius"],
    "Mutable/Cardinal": ["Pisces/Aries", "Gemini/Cancer", "Virgo/Libra", "Sagittarius/Capricorn"]
}
"""{ Quality: Sign }"""

zodiac_quality_descriptions = {
    "Cardinal": "The cardinal signs are Capricorn, Aries, Cancer, and Libra."
                "\nCardinal Signs are the initiators of the zodiac."
                "\nThey are also found at key jumping-off points on the chart wheel, specifically the Ascendant, Medium Coeli (M.C. or Midheaven), Descendant and Imum Coeli (I.C.)."
                "\nIndividuals possessing a Cardinal Quality like to get things going."
                "\nThey are active, quick and ambitious."
                "\nMany projects get started, thanks to Cardinal initiative, although a good deal of them are never finished."
                "\nThat’s because Cardinal folks are much fonder of starting things than finishing them."
                "\n\nYou won’t find a Cardinal person slacking off."
                "\nThese people are full of vim and vigor and possess a drive and ambition that is unmistakable."
                "\nEnthusiasm and a zest for life fill the Cardinal individual."
                "\nSome might perceive this rampant energy as domineering, and, at times, it can be."
                "\nCardinal people can easily forget about the rest of the pack when they are busily focusing on their own endeavors."
                "\nEven so, their energetic spirit often wins the day."
                "\n\nCardinal folks are clever and want to win."
                "\nThey love to start things, and whether they finish them or not, there’s always a lot going on."
                "\nNaysayers who find them to be too self-centered will simply have to watch (and marvel) as they speed by!",
    "Mutable": "The mutable signs are Pisces, Gemini, Virgo, and Sagittarius."
               "\nMutable Signs know how to go with the flow."
               "\nThey are adaptable and flexible and can change their form of expression to whatever a situation requires."
               "\nStanding their ground is of little import to Mutable folks."
               "\nThese people would much rather conform to the norm, so long as their doing so will help the greater good."
               "\nLuckily, Mutable individuals are versatile and find it quite easy to change."
               "\nConsider them the chameleons of the zodiac, since they can take on varied personae."
               "\n\nMutable people are blessed with a tremendous resourcefulness."
               "\nTalk about making lemonade out of lemons!"
               "\nThey know how to squeeze that last drop of juice and make things better in the process."
               "\nThose influenced by a Mutable Quality in their horoscope also enjoy learning, play fair and are diplomatic and well-liked by others."
               "\nTo their further credit, they are sharp, sympathetic and can see (via a sixth sense?) the essential elements of a situation."
               "\nAt times, however, their desire to please everyone can get them into hot water."
               "\nThey may come across as wishy-washy, inconsistent and downright duplicitous."
               "\nAll this in the name of aiming to please!"
               "\n\nThe beauty of mutability is that those possessing it are flexible, versatile and highly resourceful."
               "\nThese folks are quick to help others and are selfless in the process."
               "\nWhile they may occasionally stretch themselves to the breaking point, they know how to bounce back.",
    "Fixed": "The fixed signs are Aquarius, Taurus, Leo, and Scorpio."
             "\nFixed Signs understand that steadiness is the key."
             "\nThose influenced by this Quality are happy to forge ahead with their projects, calmly working away until they have achieved their objectives."
             "\nThis is no struggle for Fixed folks, rather it’s what makes them tick."
             "\nThese individuals are stable, determined and resolute."
             "\nThey want to get to the finish line and have the persistence and ability to concentrate, characteristics which will get them there."
             "\n\nThere is no lack of confidence in Fixed individuals."
             "\nSelf-reliance could be a Fixed person’s middle name."
             "\nThose possessed of a Fixed nature are powerful, yet purposeful."
             "\nThere are no wasted motions here: Fixed folks move patiently and steadily toward their goals."
             "\nThey are also steady and reliable and always remember those who helped them out."
             "\nConversely, those born under a Fixed sign can at times be stubborn, my-way-or-the-highway folks."
             "\nThey may have a tendency to get stuck in their ways and to believe that they are always right."
             "\n\nThose influenced by a Fixed Quality are determined, reliable and persistent."
             "They have great strength, and strength of purpose, and love to get the job done."
             "So what if they refuse to budge? They get results."
}
"""{ Sign: Description }"""

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
    "Sagittarius": "soft top",
    "Capricorn/Aquarius": "kinky top/soft bottom",
    "Aquarius/Pisces": "soft bottom/soft switch",
    "Pisces/Aries": "soft switch/power top",
    "Aries/Taurus": "power top/power bottom",
    "Taurus/Gemini": "power bottom/kinky switch",
    "Gemini/Cancer": "kinky switch/kinky bottom",
    "Cancer/Leo": "kinky bottom/power top",
    "Leo/Virgo": "power top/power switch",
    "Virgo/Libra": "power switch/soft switch",
    "Libra/Scorpio": "soft switch/kinky top",
    "Scorpio/Sagittarius": "kinky top/soft top",
    "Sagittarius/Capricorn": "soft top/kinky top"
}
"""{ Sign: Gay sex position }"""

people_by_sign_dict = defaultdict(list)
"""{ Month: ZodiacPerson }"""


def main():
    # Initialize people data
    init_people_database(os.path.realpath("E:\Google Drive (vincentwetzel3@gmail.com)\zodiac\zodiac_people.xlsx"))

    while True:
        user_input = get_int_input(
            "\nChoose an option:"
            "\n1. Look up a person."
            "\n2. Add a new person."
            "\n3. Print statistics about the database"
            "\n4. Look up a sign's information"
            "\n5. Look up a symbol"
            "\n6. Look up an element."
            "\n7. Look up a date."
            "\n8. Play a guessing game for signs and dates."
            "\n0. Exit."
            "\nPick an option:")
        if user_input == 1:
            # 1. Look up a person
            print(get_person_info(input("Enter a name and I will search the database for them: ").strip()))
        elif user_input == 2:
            # 2. Add a new person
            add_new_person_to_zodiac_database()
        elif user_input == 3:
            # 3. Print statistics about the database
            print(get_stats_about_database())
        elif user_input == 4:
            # 4. Look up a sign's information"
            print(get_sign_info(input(
                "The signs of the Zodiac are Capricorn, Aquarius, Pisces, Aries, Taurus, Gemini, "
                "Cancer, Leo, Virgo, Libra, Scorpio, Sagittarius."
                "\nEnter the sign that you would like to know more about: ")))
        elif user_input == 5:
            # 5. Look up a symbol
            print(get_symbol_info(input(
                "Enter a Zodiac sign and I will give you its symbol."
                "\nYour options are:"
                "\nCapricorn, Aquarius, Pisces, Aries, Taurus, Gemini, "
                "Cancer, Leo, Virgo, Libra, Scorpio, Sagittarius: ")))
        elif user_input == 6:
            # 6. Look up an element.
            print(get_element_info(input(
                "Enter a Zodiac element and I will give you information about it."
                "\nYour options are:"
                "\nAir, Fire, Earth, and Water: ")))
        elif user_input == 7:
            # 7. Look up a date.
            print(get_sign_for_date(
                input("Enter a day of the year and I will give you its Zodiac information (e.g. January 1): ")))
        elif user_input == 8:
            # 8. Play a guessing game for signs and dates.
            pass
            # TODO: Make a game
        elif user_input == 0:
            # 0. Exit.
            break
        else:
            print("That is not an option. Try again.")
    # --- Script End ---


def init_people_database(excel_file):
    """
    Initializes Zodiac data from a CSV file.
    :return: None
    """
    global people_by_sign_dict
    df = pandas.read_excel(excel_file)
    for idx, row in df.iterrows():
        person = ZodiacPerson(row["Name"],
                              datetime.date(int(row["Year"]),
                                            month_to_int(row["Month"]),
                                            int(row["Day"])),
                              row["Political"] in ["True", "TRUE"],
                              row["Hottie"] in ["True", "TRUE"],
                              row["President"] in ["True", "TRUE"]
                              )
        people_by_sign_dict[row["Sign"]].append(person)

        # Verify that the original data which is being read in from the file is correct
        if not (row["Sign"] == person.sign):
            raise Exception(
                "Person: " + person.name + " has caused an error during initialization. Their sign in the database is: " +
                row["Sign"] + " whereas it should be: " + person.sign)
        if not row["Element"] == person.element:
            raise Exception(
                "Person: " + person.name + " has caused an error during initialization. Their element in the database is: " +
                row["Element"] + " whereas it should be: " + person.element)
        if not row["Quality"] == person.quality:
            raise Exception(
                "Person: " + person.name + " has caused an error during initialization. Their element in the database is: " +
                row["Quality"] + " whereas it should be: " + person.quality)
        if not row["Gay Position"] == person.gay_position:
            raise Exception(
                "Person: " + person.name + " has caused an error during initialization. Their element in the database is: " +
                row["Gay Position"] + " whereas it sho`uld be: " + person.gay_position)


def add_new_person_to_zodiac_database():
    """
    Add a new person to the CSV database.
    :return: None
    """
    # Create a backup of the current data
    now = datetime.datetime.now()
    shutil.copyfile("zodiac_people.csv", "people backup from " + now.strftime("%d-%m-%Y %H.%M.%S") + ".csv")

    # Prepare current data IN ORDER
    people_in_order = x = [[] for i in range(13)]  # List of 13 lists, leave bucket 0 unused
    global people_by_sign_dict
    for zodiac_person in people_by_sign_dict.values():
        month = zodiac_person.birthday.month
        # TODO: Add a new person to the database


def get_stats_about_database():
    """
    Gets statistics about the Zodiac database.
    :return: A str with info about the database
    """
    political_by_sign_dict = defaultdict(list)
    hottie_by_sign_dict = defaultdict(list)
    presidents_by_sign_dict = defaultdict(list)
    people_by_elements_dict = defaultdict(list)
    people_by_qualities_dict = defaultdict(list)
    people_by_gay_positions_dict = defaultdict(list)

    output = format_section("TOTAL PEOPLE PER SIGN IN DATABASE", "*")
    global people_by_sign_dict
    for sign in people_by_sign_dict:
        output += "\n" + sign + ": " + str(len(people_by_sign_dict[sign]))
        for zodiac_person in people_by_sign_dict[sign]:
            if zodiac_person.political:
                political_by_sign_dict[sign].append(zodiac_person)
            if zodiac_person.hottie:
                hottie_by_sign_dict[sign].append(zodiac_person)
            if zodiac_person.president:
                presidents_by_sign_dict[sign].append(zodiac_person)
            people_by_elements_dict[zodiac_person.element].append(zodiac_person)
            people_by_qualities_dict[zodiac_person.element].append(zodiac_person)
            people_by_gay_positions_dict[zodiac_person.gay_position].append(zodiac_person)
    output += "\n"

    output += format_section("PEOPLE BY SIGN", "*")
    output += get_str_for_dict_of_lists(people_by_sign_dict)

    output += format_section("POLITICAL PEOPLE BY SIGN", "*")
    output += get_str_for_dict_of_lists(political_by_sign_dict)

    output += format_section("HOTTIES BY SIGN", "*")
    output += get_str_for_dict_of_lists(hottie_by_sign_dict)

    output += format_section("PRESIDENTS BY SIGN", "*")
    output += get_str_for_dict_of_lists(presidents_by_sign_dict)

    output += format_section("PEOPLE BY ELEMENT", "*")
    output += get_str_for_dict_of_lists(people_by_elements_dict)

    output += format_section("PEOPLE BY QUALITY", "*")
    output += get_str_for_dict_of_lists(people_by_qualities_dict)

    output += format_section("PEOPLE BY GAY POSITION", "*")
    output += get_str_for_dict_of_lists(people_by_gay_positions_dict)

    return output


def get_person_info(person_name):
    """
    Gets a string containing information about a specific person.
    :param person_name: The name of the person to retrieve data about.
    :return: A str containing Zodiac information about that person.
    """
    output = ""
    person_found = False
    global people_by_sign_dict
    for sign, people in people_by_sign_dict.items():
        logging.debug("Searching in key (sign): " + str(sign))
        for zodiac_person in people:
            logging.debug("Comparing to person: " + zodiac_person.name)
            if zodiac_person.name == person_name:
                person_found = True
                if zodiac_person.president == True:
                    output += "NAME: President " + zodiac_person.name
                else:
                    output += "\nNAME: " + zodiac_person.name
                output += "\nBIRTHDAY: " + zodiac_person.birthday.strftime(
                    "%d %B, %Y (%A)") + ". This person is " + str(
                    diff_between_two_dates(zodiac_person.birthday, datetime.date.today())[0]) + " years old."
                output += "\nSIGN: " + zodiac_person.sign
                output += "\nELEMENT: " + zodiac_person.element
                output += "\nQUALITY: " + zodiac_person.quality
                output += "\nGAY POSITION: " + zodiac_person.gay_position
                break
            if person_found:
                break
        if person_found:
            break
    if not person_found:
        return "That person is not in my database"

    return output


def get_sign_info(zodiac_sign):
    """
    Gets information about a Zodiac sign.
    :param zodiac_sign: The sign to get information about.
    :return: A str containing information about that sign.
    """
    output = ""
    if zodiac_sign in zodiac_symbols:
        global people_by_sign_dict
        output += format_section(zodiac_sign + ", the " + zodiac_symbols[zodiac_sign], "*")
        output += zodiac_sign_descriptions[zodiac_sign]
        output += "\n\nELEMENT: " + get_element(zodiac_sign)
        output += "\n" + zodiac_element_descriptions[get_element(zodiac_sign)]
        output += "\n\nQUALITY: " + get_quality(zodiac_sign)
        output += "\n" + zodiac_quality_descriptions[get_quality(zodiac_sign)]
        output += "\n\nGAY POSITION: " + zodiac_gay_position[zodiac_sign]
        output += "\n\nPEOPLE: "
        for person in people_by_sign_dict[zodiac_sign]:
            output += person.name + " (" + person.birthday.strftime("%B %d") + "), "
        if people_by_sign_dict[zodiac_sign]:
            output = output[:-2].strip()  # Remove the last comma

        return output
    else:
        return "That is not a valid Zodiac sign. "


def get_symbol_info(zodiac_sign):
    """
    Gets information about a Zodiac symbol.
    :param zodiac_sign: The sign to get info about.
    :return: A str of info about the input sign.
    """
    if zodiac_sign in zodiac_symbols:
        return "SIGN: " + zodiac_sign + "\nSYMBOL: the " + zodiac_symbols[zodiac_sign]
    else:
        return "That is not a valid Zodiac sign."


def get_element_info(zodiac_element):
    """
    Gets information about a Zodiac element.
    :param zodiac_element: A Zodiac element to get info for.
    :return: A str containing information about the Element associated with the input Zodiac sign.
    """
    if zodiac_element in zodiac_elements:
        return format_section(zodiac_element, "*") + zodiac_element_descriptions[zodiac_element]
    else:
        return "That is not a valid Zodiac sign."


def get_sign_for_date(date):
    # TODO: Rename this function to be less similar to get_sign()
    """
    Given a date, return the Zodiac sign for this date.
    :param date: A string of a date in the form "January 1"
    :return: The sign for this date
    """
    try:
        # split date
        month = date.split(" ")[0]
        day = int(date.split(" ")[1])

        try:
            month = month_to_int(month)
        except Exception as e:
            logging.debug("There was an issue when calling month_to_int in get_sign_for_date().")
            logging.debug(e)
            return "That is not a valid month."

        try:
            date_obj = datetime.date(2001, month, day)
        except Exception as e:
            return "This date is invalid because that month doesn't have that many days."

        sign = get_sign(date_obj)

        return "The sign for " + date_obj.strftime("%B %d") + " is " + sign
    except Exception as e:
        logging.debug("There was an issue with splitting the date in get_info_for_date()")
        logging.debug(e)
        return "That is not a valid date."


def yield_dates_in_range(date1, date2):
    """
    Yields data objects within a range.
    :param date1: Date object of the starting date
    :param date2: Date object of the ending date
    :return: None, yields date objects within this range
    """
    for n in range(int((date2 - date1).days) + 1):
        yield date1 + datetime.timedelta(n)


def diff_between_two_dates(starting_date, ending_date):
    """
    Finds the number of days between one day and another
    :param starting_date: Starting Date object
    :param ending_date: Ending Date object
    :return: A tuple of the difference in the form (years, months, days)
    """
    if (ending_date - starting_date).days < 0:
        raise Exception("The starting date must be before  the ending date")

    # Calculate days
    if ending_date.day >= starting_date.day:
        days = ending_date.day - starting_date.day
    else:
        days_in_month = calendar.monthrange(starting_date.year, starting_date.month)[1]
        date_temp = starting_date + datetime.timedelta(
            days=days_in_month)  # calendar.monthrange(starting_date.year, starting_date.month)[1]
        days = (ending_date - date_temp).days

    # Calculate months
    if ending_date.month >= starting_date.month:
        months = ending_date.month - starting_date.month
    else:
        months = (ending_date.month + 12) - starting_date.month
        if ending_date.day < starting_date.day:
            months = months - 1

    # Calculate years
    years = ending_date.year - starting_date.year
    if ending_date.month < starting_date.month:
        years = years - 1

    return (years, months, days)


def dict_keys_ordered_by_size_of_values_list(dict_to_order):
    result = list()
    for key in dict_to_order.keys():
        for val in result:
            if result == []:
                result.insert(0, val)
                break
            # TODO: continue here...


def order_list_by_birthday(list_of_zodiac_people):
    ordered_list = []
    logging.debug("***UNFORMATTED LIST AT START: " + format_print_of_list_of_zodiac_people(list_of_zodiac_people))
    for person in list_of_zodiac_people:
        logging.debug("Inserting " + person.name + " with birthday " + str(person.birthday) + " into ordered_list")
        if ordered_list == []:
            ordered_list.insert(0, person)
        else:
            for count, current_ordered_person in enumerate(ordered_list):
                if ordered_list[count].birthday.month == person.birthday.month:
                    # Normal case for insertion
                    if ordered_list[count].birthday.day > person.birthday.day:
                        ordered_list.insert(count, person)
                        break
                if ordered_list[count].birthday.month - 1 == person.birthday.month:
                    # e.g. I only have February birthdays then I encounter a January birthday (Aquarius)
                    ordered_list.insert(count, person)
                    break
                if person.birthday.month == 12 and ordered_list[count].birthday.month == 1:
                    # Handle December/January cases differently for Capricorns
                    ordered_list.insert(count, person)
                    break
                if count == len(ordered_list) - 1:
                    # Reached end of list, insert the new element at the end.
                    ordered_list.insert(count + 1, person)
                    break
            logging.debug("Running list: " + format_print_of_list_of_zodiac_people(ordered_list))
    return ordered_list


def get_str_for_dict_of_lists(d):
    """
    Prints info about a dictionary of Zodiac people.
    :param d: Dictionary in the form { Category: [ZodiacPerson1, ZodiacPerson2, ...] }
    :return: A string with information about this dictionary
    """
    output = ""
    for key in d:
        output += "\n" + key + "(" + str(len(d[key])) + ", " + "%0.2f" % (100 * len(
            d[key]) / sum(len(x) for x in d.values())) + "%): "
        ordered_list = order_list_by_birthday(d[key])
        output += format_print_of_list_of_zodiac_people(ordered_list)
        output += "\nTOTAL: " + str(sum(len(x) for x in d.values())) + "\n"

    return output


def format_print_of_list_of_zodiac_people(ls):
    output = ""
    for person in ls:
        output += person.name + " (" + person.birthday.strftime("%B %d") + "), "
    if not ls == []:
        output = output[:-2]  # Remove the last comma
    return output


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
    :return: The sign, possibly as a "sign1/sign2" in the case of a cusp
    """

    # non-cusp
    if (date_obj.month == 12 and date_obj.day >= 25) or (date_obj.month == 1 and date_obj.day <= 15):
        return "Capricorn"
    elif (date_obj.month == 1 and date_obj.day >= 16) and (date_obj.month == 1 and date_obj.day <= 23):
        return "Capricorn/Aquarius"
    elif (date_obj.month == 1 and date_obj.day >= 24) or (date_obj.month == 2 and date_obj.day <= 14):
        return "Aquarius"
    elif (date_obj.month == 2 and date_obj.day >= 15) and (date_obj.month == 2 and date_obj.day <= 21):
        return "Aquarius/Pisces"
    elif (date_obj.month == 2 and date_obj.day >= 22) or (date_obj.month == 3 and date_obj.day <= 16):
        return "Pisces"
    elif (date_obj.month == 3 and date_obj.day >= 17) and (date_obj.month == 3 and date_obj.day <= 23):
        return "Pisces/Aries"
    elif (date_obj.month == 3 and date_obj.day >= 24) or (date_obj.month == 4 and date_obj.day <= 15):
        return "Aries"
    elif (date_obj.month == 4 and date_obj.day >= 16) and (date_obj.month == 4 and date_obj.day <= 22):
        return "Aries/Taurus"
    elif (date_obj.month == 4 and date_obj.day >= 23) or (date_obj.month == 5 and date_obj.day <= 16):
        return "Taurus"
    elif (date_obj.month == 5 and date_obj.day >= 17) and (date_obj.month == 5 and date_obj.day <= 23):
        return "Taurus/Gemini"
    elif (date_obj.month == 5 and date_obj.day >= 24) or (date_obj.month == 6 and date_obj.day <= 16):
        return "Gemini"
    elif (date_obj.month == 6 and date_obj.day >= 17) and (date_obj.month == 6 and date_obj.day <= 23):
        return "Gemini/Cancer"
    elif (date_obj.month == 6 and date_obj.day >= 24) or (date_obj.month == 7 and date_obj.day <= 18):
        return "Cancer"
    elif (date_obj.month == 7 and date_obj.day >= 19) and (date_obj.month == 7 and date_obj.day <= 25):
        return "Cancer/Leo"
    elif (date_obj.month == 7 and date_obj.day >= 26) or (date_obj.month == 8 and date_obj.day <= 18):
        return "Leo"
    elif (date_obj.month == 8 and date_obj.day >= 19) and (date_obj.month == 8 and date_obj.day <= 25):
        return "Leo/Virgo"
    elif (date_obj.month == 8 and date_obj.day >= 26) or (date_obj.month == 9 and date_obj.day <= 18):
        return "Virgo"
    elif (date_obj.month == 9 and date_obj.day >= 19) and (date_obj.month == 9 and date_obj.day <= 25):
        return "Virgo/Libra"
    elif (date_obj.month == 9 and date_obj.day >= 26) or (date_obj.month == 10 and date_obj.day <= 18):
        return "Libra"
    elif (date_obj.month == 10 and date_obj.day >= 19) and (date_obj.month == 10 and date_obj.day <= 25):
        return "Libra/Scorpio"
    elif (date_obj.month == 10 and date_obj.day >= 26) or (date_obj.month == 11 and date_obj.day <= 17):
        return "Scorpio"
    elif (date_obj.month == 11 and date_obj.day >= 18) and (date_obj.month == 11 and date_obj.day <= 24):
        return "Scorpio/Sagittarius"
    elif (date_obj.month == 11 and date_obj.day >= 25) or (date_obj.month == 12 and date_obj.day <= 17):
        return "Sagittarius"
    elif (date_obj.month == 12 and date_obj.day >= 18) and (date_obj.month == 12 and date_obj.day <= 24):
        return "Sagittarius/Capricorn"
    else:
        raise Exception("No sign was assigned in get_sign()")


def get_quality(sign):
    """
    Helper method to get a quality for a Zodiac sign.
    :param sign: The sign we want the quality for.
    :return: The quality
    """
    for quality in zodiac_qualities:
        for zodiac_sign in zodiac_qualities[quality]:
            if zodiac_sign == sign:
                return quality
    raise Exception("No quality was found for " + str(sign))


def get_element(sign):
    """
    Helper method to get a element for a Zodiac sign.
    :param sign: The sign we want the element for.
    :return: The element
    """
    for element in zodiac_elements:
        for zodiac_sign in zodiac_elements[element]:
            if zodiac_sign == sign:
                return element
    raise Exception("No element was found for " + str(sign))


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


def format_section(section_title, symbol):
    """
    A helper method to print our output to the console in a pretty fashion

    :param section_title:   The name of the section we are printing.
    :param symbol:      The symbol to repetetively print to box in our output. This will usually be a '*'.
    :return:    None
    """
    return "\n" + (symbol * 50) + "\n" + section_title + "\n" + (symbol * 50) + "\n"


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
        self.sign = get_sign(self.birthday)
        self.symbol = zodiac_symbols[self.sign]
        self.element = get_element(self.sign)
        self.quality = get_quality(self.sign)
        self.gay_position = zodiac_gay_position[self.sign]


if __name__ == "__main__":
    main()
