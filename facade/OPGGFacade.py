from selenium.common.exceptions import WebDriverException

from screen.opgg import HomeScreen
import configparser

# Read .ini file
config = configparser.ConfigParser()
config.read('resources/application_properties.ini')

home = HomeScreen.HomeScreen()


# region HOME

def wait_to_load():
    pass


def search_for(option):
    home.input_search(option)
    home.click_search()


# endregion
