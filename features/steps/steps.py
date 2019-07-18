from facade import Facade, OPGGFacade
from runner import Runner
from behave import Given, When, Then
import configparser
from behave import register_type
from parse_type import TypeBuilder
import parse

# ----------------------------------------------------------------------------
# run with behave
# ----------------------------------------------------------------------------
Runner = Runner.Runner()

facade = Facade.Facade()

# ----------------------------------------------------------------------------
# Read .ini file:
# ----------------------------------------------------------------------------
config = configparser.ConfigParser()
config.read('resources/application_properties.ini')


def screenshot(context):
    from datetime import datetime
    now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    Runner.Driver.save_screenshot('./reports/screenshot/screenshot-{}-{}.png'.format(now, str(context.step)))


# ----------------------------------------------------------------------------
# STEPS:
# ----------------------------------------------------------------------------
@Given(u'I go back')
def go_back_in_browser(context):
    Runner.Driver.back()


@Given(u'I wait {seg} seconds')
def step_wait(context, seg):
    """
    Waits -seg- seconds
    :param context: obligatory parameter from 'behave'
    :param seg: how many seconds the application will wait
    :return: nothing
    """
    print('step I wait ' + seg + ' seconds')
    facade.wait(seg=seg)


@Given(u'I open the main {main} page')
def step_open_main_page(context, main):
    """
    Reads the .ini file and goes to -MAIN- page from file
    :param context: obligatory parameter from 'behave'
    :param MAIN: parameter from application_properties.ini
    :return: nothing
    """
    print('step I open the main ' + config['URLs'][main] + ' page')
    Runner.Driver.get(config['URLs'][main])
    Facade.accept_cookies()


@Then(u'the {main} page loaded successfully')
def check_page_loaded(context, main):
    """
    Calls every wait_to_load page from current screen
    :param context: obligatory parameter from 'behave'
    :param MAIN: page where you check if the browser is currently on
    :return: nothing
    """
    print('step the ' + main + ' page loaded successfully')
    facade.wait(url=config['URLs'][main], seg=1)


@Then(u'I close the browser')
def close_browser(context):
    """
    It ill close the browser and quit the session
    :param context: obligatory parameter from 'behave'
    :return: nothing
    """
    print('step I close the browser')
    Runner.Driver.quit()


@Given(u'I take a screenshot')
def take_screenshot(context):
    from datetime import datetime
    now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    Runner.Driver.save_screenshot('./reports/screenshot/{}-{}.png'.format(now, str(context.scenario)))


@Given(u'I take a screenshot with name {name}')
def take_screenshot_with_name(context, name):
    from datetime import datetime
    now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    Runner.Driver.save_screenshot('./reports/screenshot/{}-{}.png'.format(now, str(name)))
