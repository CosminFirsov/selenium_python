import configparser

from selenium.webdriver.chrome.options import Options

from runner import Runner
import time as Time
Runner = Runner.Runner()


def after_step(context, step):
    """
    It will repeat after every step. If the step is marked as failed, it will take a screenshot and stored it
    with the current timestamp as name
    :param context:
    :param step:
    :return:
    """
    if step.status == 'failed':
        from datetime import datetime
        Time.sleep(3)
        now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        Runner.Driver.save_screenshot('./reports/screenshot/screenshot-{}-{}.png'.format(now, str(step)))


def before_tag(context, tag):
    """
    It will repeat for every scenario and every tag
    :param context: behave context object
    :param tag: a dict with the tags of the current feature
    :return: None
    """
    # Read .ini file
    config = configparser.ConfigParser()
    config.read('resources/application_properties.ini')

    # Responsive
    mobile_emulation = {"deviceName": "Nexus 5"}

    # Driver path
    Runner.executable_path = config['DEFAULT']['chromedriver_path']

    # headless browser options
    options = Options()
    # options.add_argument("--disable-notifications")
    # options.add_argument('--no-sandbox')
    # options.add_argument('--verbose')
    # options.add_argument('--disable-gpu')
    # options.add_argument('--disable-software-rasterizer')
    # options.add_argument('--headless')

    options.add_argument('window-size=1920,1080')
    options.add_argument('--lang=en-GB')
    Runner.set_option(options)

    if tag == "mobile":   # Responsive
        options.add_experimental_option("mobileEmulation", mobile_emulation)
        Runner.set_option(options)
        Runner.set_runner(config['DEFAULT']['chromedriver_path'], options)
    elif tag == "web":  # Desktop
        Runner.set_runner(config['DEFAULT']['chromedriver_path'], options)


def after_scenario(context, tag):
    print('test')
    # Runner.Driver.quit()
