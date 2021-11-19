import operator as op
import pandas as pd
import re

# Input
surname = str(input("Enter your surname: "))
name = str(input("Enter your name: "))
birth_date = str(input("Enter your birth date (DD/MM/YYYY): "))
sex = str(input("Enter your sex (F/M): "))
city = str(input("Enter your birth place: "))


def get_vowels(string):
    """
    :param string: input string
    :return: a list of vowels
    """
    return re.findall(r"(?i)[aeiou]", string)


def get_consonants(string):
    """
    :param string: input string
    :return: a list of consonants
    """
    return re.findall(r"(?i)[^aeiou ]", string)


def manageSurname():
    """
    :return: surname part of fiscal code
    """
    vowels = get_vowels(surname)
    consonants = get_consonants(surname)
    num_vowels = len(vowels)
    num_consonants = len(consonants)
    ret_val = None

    if num_consonants >= 3:
        ret_val = consonants[:3]
    elif num_consonants == 2:
        ret_val = consonants[:] + vowels[0]
    elif num_consonants == 1 and num_vowels == 2:
        ret_val = consonants[0] + vowels[:]
    elif num_consonants == 1 and num_vowels == 1:
        ret_val = consonants[0] + num_vowels[0] + "X"

    return "".join(ret_val)


def manage_name():
    """
    :return: name part of fiscal code
    """
    vowels = get_vowels(name)
    consonants = get_consonants(name)
    num_vowels = len(vowels)
    num_consonants = len(consonants)
    ret_val = None

    if num_consonants >= 4:
        ret_val = op.itemgetter(0, 2, 3)(consonants)
    elif num_consonants == 3:
        ret_val = consonants[:3]
    elif num_consonants == 2:
        ret_val = consonants[:] + vowels[0]
    elif num_consonants == 1 and num_vowels == 2:
        ret_val = consonants[0] + vowels[:]
    elif num_consonants == 1 and num_vowels == 1:
        ret_val = consonants[0] + num_vowels[0] + "X"
    elif num_consonants == 0 and num_vowels == 2:
        ret_val = vowels + "X"

    return "".join(ret_val)


def manage_birth_date_and_sex():
    """
    :return: birth date and sex part of fiscal code
    """
    birth_date_split = birth_date.split("/")
    year = birth_date_split[2][2:4]
    month = int(birth_date_split[1]) - 1
    day = birth_date_split[0]

    months = [chr(c) for c in range(ord("A"), ord("T") + 1) if chr(c) not in ["F", "G", "I", "J", "K", "N", "O", "Q"]]
    month = months[month]

    if sex == "F":
        day = int(day)
        day += 30

    day = "{:>02}".format(str(day))

    return year + month + day


def manage_municipality():
    """
    :return: municipality of fiscal code
    """
    data = pd.read_csv("municipalities.csv", sep=";", encoding="ISO-8859-1")
    columns_to_drop = [data.columns[0], *data.columns[2:6].tolist(), *data.columns[7:].tolist()]
    data.drop(columns=columns_to_drop, axis=1, inplace=True)
    code = data[data.iloc[:, 0] == city].iloc[0, 1]

    return code


def manage_cin():
    """"
    :return: Control Internal Number of fiscal code
    """
    partial_fiscal_code = manageSurname() + manage_name() + manage_birth_date_and_sex() + manage_municipality()
    evens = partial_fiscal_code[1::2]
    odds = partial_fiscal_code[0::2]
    odds_table = [1, 0, 5, 7, 9, 13, 15, 17, 19, 21, 2, 4, 18, 20, 11, 3, 6, 8, 12, 14, 16, 10, 22, 25, 24, 23]
    sum_evens = 0
    sum_odds = 0
    sum_total = 0
    cin = ""

    for i in range(len(odds_table)):
        odds_table[i] = [odds_table[i], (i, chr(65 + i))]

    for c in evens:
        sum_evens += (ord(c) - 65) if c.isalpha() else int(c)

    for c in odds:
        c = int(c) if c.isdigit() else c
        for arr in odds_table:
            if c in arr[1]:
                sum_odds += arr[0]

    sum_total = sum_evens + sum_odds

    cin = chr((sum_total % 26) + 65)

    return cin


def calculate_fiscal_code():
    """
    :return: fiscal code
    """
    return manageSurname() + manage_name() + manage_birth_date_and_sex() + manage_municipality() + manage_cin()


# Output
print(calculate_fiscal_code())
