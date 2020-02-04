import logging
import datetime


class Zodiac:
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

    def __init__(self):
        pass

    @staticmethod
    def get_sign_info(zodiac_sign):
        # TODO: Previously this function also printed the people who are associated with this Zodiac sign.
        #  That was nice. Find a way to do that again.
        """
        Gets information about a Zodiac sign.
        :param zodiac_sign: The sign to get information about.
        :return: A str containing information about that sign.
        """
        output = ""
        if zodiac_sign in Zodiac.zodiac_symbols:
            output += zodiac_sign + ", the " + Zodiac.zodiac_symbols[zodiac_sign]
            output += Zodiac.zodiac_sign_descriptions[zodiac_sign]
            output += "\n\nELEMENT: " + Zodiac.get_element(zodiac_sign)
            output += "\n" + Zodiac.zodiac_element_descriptions[Zodiac.get_element(zodiac_sign)]
            output += "\n\nQUALITY: " + Zodiac.get_quality(zodiac_sign)
            output += "\n" + Zodiac.zodiac_quality_descriptions[Zodiac.get_quality(zodiac_sign)]
            output += "\n\nGAY POSITION: " + Zodiac.zodiac_gay_position[zodiac_sign]
            output += "\n\nPEOPLE: "

            return output
        else:
            return "That is not a valid Zodiac sign. "

    @staticmethod
    def get_symbol_info(zodiac_sign):
        """
        Gets information about a Zodiac symbol.
        :param zodiac_sign: The sign to get info about.
        :return: A str of info about the input sign.
        """
        if zodiac_sign in Zodiac.zodiac_symbols:
            return "SIGN: " + zodiac_sign + "\nSYMBOL: the " + Zodiac.zodiac_symbols[zodiac_sign]
        else:
            return "That is not a valid Zodiac sign."

    @staticmethod
    def get_element_info(zodiac_element):
        """
        Gets information about a Zodiac element.
        :param zodiac_element: A Zodiac element to get info for.
        :return: A str containing information about the Element associated with the input Zodiac sign.
        """
        if zodiac_element in Zodiac.zodiac_elements:
            return Zodiac.zodiac_element_descriptions[zodiac_element]
        else:
            return "That is not a valid Zodiac sign."

    @staticmethod
    def get_sign_for_date_str(date_str) -> str:
        """
        Given a date, return the Zodiac sign for this date.
        :param date_str: A string of a date in the form "January 1"
        :return: The sign for this date
        """
        try:
            # split date
            month = date_str.split(" ")[0]
            day = int(date_str.split(" ")[1])

            try:
                month = Zodiac.month_to_int(month)
            except Exception as e:
                logging.debug("There was an issue when calling month_to_int in get_sign_for_date().")
                logging.debug(e)
                return "That is not a valid month."

            try:
                date_obj = datetime.date(2001, month, day)
            except ValueError:
                return "This date is invalid because that month doesn't have that many days."
            sign = Zodiac.get_sign_for_date_obj(date_obj)

            return "The sign for " + date_obj.strftime("%B %d") + " is " + sign
        except Exception as e:
            logging.debug("There was an issue with splitting the date in get_info_for_date()")
            logging.debug(e)
            return "That is not a valid date."

    @staticmethod
    def get_sign_for_date_obj(date_obj: datetime.date) -> str:
        """
        The sign, possibly as a "sign1/sign2" in the case of a cusp
        :param date_obj: The date of the sign
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

    @staticmethod
    def get_quality(sign) -> str:
        """
        Helper method to get a quality for a Zodiac sign.
        :param sign: The sign we want the quality for.
        :return: The quality as a str.
        """
        for quality in Zodiac.zodiac_qualities:
            for zodiac_sign in Zodiac.zodiac_qualities[quality]:
                if zodiac_sign == sign:
                    return quality
        raise Exception("No quality was found for " + str(sign))

    @staticmethod
    def get_element(sign) -> str:
        """
        Helper method to get a element for a Zodiac sign.
        :param sign: The sign we want the element for.
        :return: The element
        """
        for element in Zodiac.zodiac_elements:
            for zodiac_sign in Zodiac.zodiac_elements[element]:
                if zodiac_sign == sign:
                    return element
        raise Exception("No element was found for " + str(sign))

    @staticmethod
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
