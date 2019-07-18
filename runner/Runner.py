from selenium import webdriver
import configparser

from selenium.webdriver.chrome.options import Options

from singleton_decorator import singleton

executable_path = None
desired_capabilities = None


@singleton
class Runner:
    # Read .ini file
    config = configparser.ConfigParser()
    config.read('resources/application_properties.ini')

    options = Options()

    Driver = None

    def __init__(self):
        print('#########Runner##########')

    def set_runner(self, path, chrome):
        self.Driver = webdriver.Chrome(executable_path=path, chrome_options=chrome)

    def set_option(self, value):
        self.options = value
