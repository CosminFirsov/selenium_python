from selenium import webdriver
import configparser
from utils import User
from singleton_decorator import singleton
from pymongo import MongoClient
#from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import pyautogui
import threading

#class Singleton(type):
#    """There can and will be only one instance of the class that extends a Singleton
#    """
#    def __init__(self, name, bases, mmbs):
#        super(Singleton, self).__init__(name, bases, mmbs)
#        self._instance = super(Singleton, self).__call__()

#    def __call__(self, *args, **kw):
#        return self._instance

#from functools import wraps
#__instances = {}
#def singleton(cls):
#    @wraps(cls)
#    def getInstance(*args, **kwargs):
#        instance = __instances.get(cls, None)
#        if not instance:
#            instance = cls(*args, **kwargs)
#            __instances[cls] = instance
#        return instance
#    return getInstance  

@singleton
class Runner():
    #Read .ini file
    config = configparser.ConfigParser()
    config.read('resources/application_properties.ini')
    
    #Driver
    Driver = webdriver.Chrome(executable_path = config['DEFAULT']['chromedriver_path'])
    
    def __init__(self):
        print('#########Runner##########')
        self.Driver.get(self.config['URLs']['INICIO'])