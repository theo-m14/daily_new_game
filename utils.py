from datetime import datetime


def has_numbers(inputString):
    return any(char.isdigit() for char in inputString)

def get_month_in_string() -> str:
    month_converter_tab = ['janvier','février', 'mars', 'avril', 'mai' , 'juin', 'juillet', 'aout', 'septembre', 'octobre', 'novembre', 'décembre']
    month = datetime.now().month

    if(month == 1):
        return month_converter_tab[11]
    else:
        return month_converter_tab[month-1]