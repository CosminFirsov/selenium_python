# Load libraries
import datetime

from selenium.webdriver.chrome.options import Options

from runner.Runner import Runner


def random_string(string_length=10):
    import random
    import string
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(string_length))


runner = Runner()
options = Options()
mobile_emulation = {"deviceName": "Nexus 5"}
# options.add_argument('--start-maximized')
options.add_argument('window-size=1920,1080')
options.add_argument('--lang=en-GB')
options.add_experimental_option("mobileEmulation", mobile_emulation)
runner.set_runner('lib/chromedriver', options)
