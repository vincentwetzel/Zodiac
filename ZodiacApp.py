#! /usr/bin/env python3

# TODO: Fully upgrade all function annotations

from Zodiac import Zodiac
from ZodiacPerson import ZodiacPerson
import logging
import sys
import pandas
import datetime
import calendar
from collections import defaultdict
import shutil
import os
import tkinter
import tkinter.filedialog
from win32com.client import Dispatch

# TODO: Create a web scraper to pull Zodac intimacy data from astrology-zodiac-signs.com

# NOTE TO USER: use logging.DEBUG for testing, logging.CRITICAL for runtime
logging.basicConfig(stream=sys.stderr,
                    level=logging.DEBUG)


class ZodiacApp:
    def __init__(self):
        # TODO: Annotate all of these class variables

        self.people_by_sign_dict = defaultdict(list)
        """{ Month: ZodiacPerson }"""

        # Init save file
        self.root_tk = tkinter.Tk()

        save_file = None
        try:
            save_file = open("settings.ini", 'r').readline().strip().split("save_file=")[1]
            if save_file == "":
                raise FileNotFoundError()
        except (FileNotFoundError, IndexError):
            save_file = tkinter.filedialog.asksaveasfilename(title="Choose a name for your Zodiac database",
                                                             defaultextension='xlsx',
                                                             filetypes=[("Excel Workbook", ".xlsx")])

            with open('settings.ini', 'w') as settings_file:
                settings_file.write("save_file=" + save_file)
            if not os.path.exists(save_file):
                column_names = ["Name", "Day", "Month", "Year", "Sign", "Element", "Quality", "Gay", "Position",
                                "Political", "Hottie", "President"]
                df = pandas.DataFrame(columns=column_names)
                df.to_excel(save_file, index=False, freeze_panes=(1, 0))

                # Autosize the columns of the output file
                excel = Dispatch('Excel.Application')
                wb = excel.Workbooks.Open(save_file)
                excel.Worksheets(1).Activate()
                excel.ActiveSheet.Columns.AutoFit()
                wb.Save()
                wb.Close()

        self.init_people_database(os.path.realpath(save_file))

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
                print(self.get_person_info_from_db(
                    input("Enter a name and I will search the database for them: ").strip()))
            elif user_input == 2:
                # 2. Add a new person
                self.add_new_person_to_zodiac_database()
            elif user_input == 3:
                # 3. Print statistics about the database
                print(self.get_stats_about_database())
            elif user_input == 4:
                # 4. Look up a sign's information"
                print(format_section(Zodiac.get_sign_info(input(
                    "The signs of the Zodiac are Capricorn, Aquarius, Pisces, Aries, Taurus, Gemini, "
                    "Cancer, Leo, Virgo, Libra, Scorpio, Sagittarius."
                    "\nEnter the sign that you would like to know more about: "))), "*")
            elif user_input == 5:
                # 5. Look up a symbol
                print(format_section(Zodiac.get_symbol_info(input(
                    "Enter a Zodiac sign and I will give you its symbol."
                    "\nYour options are:"
                    "\nCapricorn, Aquarius, Pisces, Aries, Taurus, Gemini, "
                    "Cancer, Leo, Virgo, Libra, Scorpio, Sagittarius: "))), "*")
            elif user_input == 6:
                # 6. Look up an element.
                print(format_section(Zodiac.get_element_info(input(
                    "Enter a Zodiac element and I will give you information about it."
                    "\nYour options are:"
                    "\nAir, Fire, Earth, and Water: "))), "*")
            elif user_input == 7:
                # 7. Look up a date.
                print(format_section(Zodiac.get_sign_for_date_str(
                    input("Enter a day of the year and I will give you its Zodiac information (e.g. January 1): "))),
                    "*")
            elif user_input == 8:
                # 8. Play a guessing game for signs and dates.
                pass
                # TODO: Make a game
            elif user_input == 0:
                # 0. Exit.
                break
            else:
                print("That is not an option. Try again.")

        self.root_tk.mainloop()
        # --- Script End ---

    def init_people_database(self, excel_file) -> None:
        """
        Initializes Zodiac data from a CSV file.
        :param excel_file:
        :return: None
        """
        df = pandas.read_excel(excel_file)
        for idx, row in df.iterrows():
            person = ZodiacPerson(row["Name"],
                                  datetime.date(int(row["Year"]),
                                                Zodiac.month_to_int(row["Month"]),
                                                int(row["Day"])),
                                  row["Political"] in ["True", "TRUE"],
                                  row["Hottie"] in ["True", "TRUE"],
                                  row["President"] in ["True", "TRUE"]
                                  )
            self.people_by_sign_dict[row["Sign"]].append(person)

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

    def add_new_person_to_zodiac_database(self):
        # TODO: This method is incomplete.
        """
        Add a new person to the CSV database.
        :return: None
        """
        # Create a backup of the current data
        now = datetime.datetime.now()
        shutil.copyfile("zodiac_people.csv", "people backup from " + now.strftime("%d-%m-%Y %H.%M.%S") + ".csv")

        # Prepare current data IN ORDER
        people_in_order = x = [[] for i in range(13)]  # List of 13 lists, leave bucket 0 unused
        for zodiac_person in self.people_by_sign_dict.values():
            month = zodiac_person.birthday.month
            # TODO: Continue finishing this method.

    def get_stats_about_database(self):
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
        for sign in self.people_by_sign_dict:
            output += "\n" + sign + ": " + str(len(self.people_by_sign_dict[sign]))
            for zodiac_person in self.people_by_sign_dict[sign]:
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
        output += self.get_str_for_dict_of_lists(people_by_sign_dict)

        output += format_section("POLITICAL PEOPLE BY SIGN", "*")
        output += self.get_str_for_dict_of_lists(political_by_sign_dict)

        output += format_section("HOTTIES BY SIGN", "*")
        output += self.get_str_for_dict_of_lists(hottie_by_sign_dict)

        output += format_section("PRESIDENTS BY SIGN", "*")
        output += self.get_str_for_dict_of_lists(presidents_by_sign_dict)

        output += format_section("PEOPLE BY ELEMENT", "*")
        output += self.get_str_for_dict_of_lists(people_by_elements_dict)

        output += format_section("PEOPLE BY QUALITY", "*")
        output += self.get_str_for_dict_of_lists(people_by_qualities_dict)

        output += format_section("PEOPLE BY GAY POSITION", "*")
        output += self.get_str_for_dict_of_lists(people_by_gay_positions_dict)

        return output

    def get_person_info_from_db(self, person_name):
        """
        Gets a string containing information about a specific person.
        :param person_name: The name of the person to retrieve data about.
        :return: A str containing Zodiac information about that person.
        """
        output = ""
        person_found = False
        for sign, people in self.people_by_sign_dict.items():
            logging.debug("Searching in key (sign): " + str(sign))
            for zodiac_person in people:
                logging.debug("Comparing to person: " + zodiac_person.name)
                if zodiac_person.name == person_name:
                    person_found = True
                    if zodiac_person.president:
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

    def order_list_by_birthday(self, list_of_zodiac_people):
        ordered_list = []
        logging.debug(
            "***UNFORMATTED LIST AT START: " + self.format_print_of_list_of_zodiac_people(list_of_zodiac_people))
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
                logging.debug("Running list: " + self.format_print_of_list_of_zodiac_people(ordered_list))
        return ordered_list

    def get_str_for_dict_of_lists(self, d):
        # TODO: d is the worst name for a dict ever. Fix this!
        # TODO: Also, doc this better so it is clear why it belongs in ZodiacApp
        """
        Prints info about a dictionary of Zodiac people.
        :param d: Dictionary in the form { Category: [ZodiacPerson1, ZodiacPerson2, ...] }
        :return: A string with information about this dictionary
        """
        output = ""
        for key in d:
            output += "\n" + key + "(" + str(len(d[key])) + ", " + "%0.2f" % (100 * len(
                d[key]) / sum(len(x) for x in d.values())) + "%): "
            ordered_list = self.order_list_by_birthday(d[key])
            output += self.format_print_of_list_of_zodiac_people(ordered_list)
            output += "\nTOTAL: " + str(sum(len(x) for x in d.values())) + "\n"

        return output

    def format_print_of_list_of_zodiac_people(self, ls):
        # TODO: So you know how 'd' was a terrible name for a dict? ls is a HORRIBLE name for a list. Fix this.
        # TODO: Give this function a better name too.
        output = ""
        for person in ls:
            output += person.name + " (" + person.birthday.strftime("%B %d") + "), "
        if not ls == []:
            output = output[:-2]  # Remove the last comma
        return output


def get_int_input(query_str) -> int:
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


def format_section(section_title, symbol) -> str:
    """
    A helper method to print our output to the console in a pretty fashion

    :param section_title:   The name of the section we are printing.
    :param symbol:      The symbol to repetetively print to box in our output. This will usually be a '*'.
    :return:    None
    """
    return "\n" + (symbol * 50) + "\n" + section_title + "\n" + (symbol * 50) + "\n"


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
    # TODO: Finish method
    result = list()
    for key in dict_to_order.keys():
        for val in result:
            if result == []:
                result.insert(0, val)
                break
            # TODO: continue here...


if __name__ == "__main__":
    ZodiacApp()
