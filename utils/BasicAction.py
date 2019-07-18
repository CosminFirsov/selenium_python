from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement

from runner import Runner
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time as Time
from selenium.common.exceptions import WebDriverException, StaleElementReferenceException
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import Select

Runner = Runner.Runner()


class BasicAction:
    """
    Here you do all the actions over the driver like click a button, wait for it to be in a desired state, get text,
    check if an element contains a text, select from a drop down, etc...
    """

    def wait(self, seg=1, url=None, timeout=500):
        """
        Wait 1 seconds by default. Check if the current page has a body with a size. If the url is set, check every
        -seg- seconds for the it and compares it with the one from the browser (browser has to contain a part of the
        url). It will do -timeout- times
        :param seg: the seconds it will sleep the current thread before checking again. It rounds up the value then
        convert it to an integer
        :param url: the url the browser has to contain
        :param timeout: how many time will do the checkout
        :return: Nothing
        """
        import math
        seg = int(math.ceil(float(seg)))
        Time.sleep(seg)
        size_main_content = 0
        try:
            size_main_content = self.wait_to_be_present_and_get_size(xpath='//body')
        except StaleElementReferenceException:
            self.wait(self, seg=seg, url=url, timeout=timeout)
        if size_main_content['height'] <= 0 or size_main_content['width'] <= 0:
            print('body has no size')
            Time.sleep(seg)
        if url is not None:
            import re

            http = re.search("http([s])?://", url)
            http_browser = re.search("http([s])?://", self.get_current_page())
            contador = 0
            expected_url = url[http.end():]
            while contador != int(timeout):
                current_url = self.get_current_page()[http_browser.end():]
                if expected_url in current_url or self.similar(expected_url, current_url) > 0.75:
                    break
                Time.sleep(seg)
                contador += 1
            if contador == int(timeout):
                raise Exception(
                    'Timeout exceeded. \tUrl expected: \t{} \tUrl from browser \t{}'.format(url[http.end():],
                                                                                            self.get_current_page()))

    def similar(self, a, b):
        """
        This code was made because sometime you can be on the same ulr but on different language. Only /en/ will change
        . If you compare with in operator, it will return false.
        :param a: first string element
        :param b: second string element
        :return: float[0, 1]
        """
        from difflib import SequenceMatcher
        return SequenceMatcher(None, a, b).ratio()

    def go_back(self):
        """
        Clicks go back into browser history
        :return:
        """
        Runner.Driver.back()

    def wait_to_be_clickable_clear_text_and_input_new_text(self, text, element=None, **paths):
        """
        Wait for the element from the current screen to be in a clickable state, clear all text and input new text
        :param text: the text you want to input
        :param element: the web_element o a dict with the name, id, xpath, class_name, tag_name, text, href, type_name,
        src, and html_tag
        :param paths: the name, id, xpath, class_name, tag_name, text, href, type_name, src, and html_tag as parameters
        :return: the web_element generated
        """
        return self.wait_and_perform_action(self.wait_to_be_clickable, self.clear_text_and_input_new_text,
                                            element=element, value=text, **paths)

    def wait_to_be_selected_clear_text_and_input_new_text(self, text, **paths):
        """
        Wait for the element from the current screen to be in a selected state, clear all text and input new text
        :param text: the text you want to input
        :param element: the web_element o a dict with the name, id, xpath, class_name, tag_name, text, href, type_name,
        src, and html_tag
        :param paths: the name, id, xpath, class_name, tag_name, text, href, type_name, src, and html_tag as parameters
        :return: the web_element generated
        """
        return self.wait_and_perform_action(self.wait_to_be_selected, self.clear_text_and_input_new_text, value=text,
                                            **paths)

    def wait_to_be_clickable_and_click_it(self, element=None, **paths):
        """
        Wait for the element from the current screen to be in a clickable state then clicks the web_element generated
        :param element: the web_element o a dict with the name, id, xpath, class_name, tag_name, text, href, type_name,
        src, and html_tag
        :param paths: the name, id, xpath, class_name, tag_name, text, href, type_name, src, and html_tag as parameters
        :return: the web_element generated
        """
        return self.wait_and_perform_action(self.wait_to_be_clickable, self.click, element=element, **paths)

    def wait_to_be_present_and_clicks_it(self, element=None, **paths):
        """
        Wait for the element from the current screen to be present in the DOM then clicks the web_element generated
        :param element: the web_element o a dict with the name, id, xpath, class_name, tag_name, text, href, type_name,
        src, and html_tag
        :param paths: the name, id, xpath, class_name, tag_name, text, href, type_name, src, and html_tag as parameters
        :return: the web_element generated
        """
        return self.wait_and_perform_action(self.wait_to_be_present, self.click, element=element, **paths)

    def wait_to_be_present_and_select_value_from_select(self, value, element=None, **paths):
        """
        Wait for the element from the current screen to be present in the DOM then select the value wanted from that
        html element
        :param value: the value option you want to select
        :param element: the web_element o a dict with the name, id, xpath, class_name, tag_name, text, href, type_name,
        src, and html_tag
        :param paths: the name, id, xpath, class_name, tag_name, text, href, type_name, src, and html_tag as parameters
        :return: the web_element generated
        """
        return self.wait_and_perform_action(self.wait_to_be_present, self.select, element=element, value=value, **paths)

    def wait_to_be_present_and_get_location(self, element=None, **paths):
        """
        Wait for the element from the current screen to be present in the DOM then returns a dict with its location. It
        will have x and y attributes
        :param element: the web_element o a dict with the name, id, xpath, class_name, tag_name, text, href, type_name,
        src, and html_tag
        :param paths: the name, id, xpath, class_name, tag_name, text, href, type_name, src, and html_tag as parameters
        :return: A dict with x and y as attribute. Location is based on pixels
        """
        return self.wait_and_perform_action(self.wait_to_be_present, self.get_location, element=element, **paths)

    def wait_to_be_present_and_get_element(self, element=None, **paths):
        """
        Wait for the element from the current screen to be present in the DOM then returns the web_element generated
        :param element: the web_element o a dict with the name, id, xpath, class_name, tag_name, text, href, type_name,
        src, and html_tag
        :param paths: the name, id, xpath, class_name, tag_name, text, href, type_name, src, and html_tag as parameters
        :return: the web_element generated
        """
        return self.wait_and_perform_action(self.wait_to_be_present, self.get_element, element=element, **paths)

    def wait_to_be_clickable_move_mouse_over_it_and_clicks_it(self, element=None, **paths):
        """
        Wait for the element from the current screen to be in a clickable state, performs an action of moving the mouse
        over the center of the element, then clicks the web_element generated
        :param element: the web_element o a dict with the name, id, xpath, class_name, tag_name, text, href, type_name,
        src, and html_tag
        :param paths: the name, id, xpath, class_name, tag_name, text, href, type_name, src, and html_tag as parameters
        :return: the web_element generated
        """
        return self.wait_and_perform_action(self.wait_to_be_clickable, self.move_mouse_over_it_and_left_click_it,
                                            element=element, **paths)

    def wait_to_be_clickable_and_move_mouse_over(self, element=None, **paths):
        """
        Wait for the element from the current screen to be in a clickable state and performs an action of moving the mouse
        over the center of the element
        :param element: the web_element o a dict with the name, id, xpath, class_name, tag_name, text, href, type_name,
        src, and html_tag
        :param paths: the name, id, xpath, class_name, tag_name, text, href, type_name, src, and html_tag as parameters
        :return: the web_element generated
        """
        return self.wait_and_perform_action(self.wait_to_be_clickable, self.move_mouse_over, element=element, **paths)

    def wait_to_be_clickable_and_send_home_key(self, element=None, **paths):
        """
        Wait for the element from the current screen to be in a clickable state, then sends the HOME key to that element
        :param element: the web_element o a dict with the name, id, xpath, class_name, tag_name, text, href, type_name,
        src, and html_tag
        :param paths: the name, id, xpath, class_name, tag_name, text, href, type_name, src, and html_tag as parameters
        :return: the web_element generated
        """
        return self.wait_and_perform_action(self.wait_to_be_clickable, self.send_home_key_to, element=element, **paths)

    def wait_to_be_clickable_and_send_page_down_key(self, element=None, **paths):
        """
        Wait for the element from the current screen to be in a clickable state, then sends the PgDn key to that element
        :param element: the web_element o a dict with the name, id, xpath, class_name, tag_name, text, href, type_name,
        src, and html_tag
        :param paths: the name, id, xpath, class_name, tag_name, text, href, type_name, src, and html_tag as parameters
        :return: the web_element generated
        """
        return self.wait_and_perform_action(self.wait_to_be_clickable, self.send_down_key_to, element=element, **paths)

    def wait_to_be_clickable_and_send_end_key(self, element=None, **paths):
        """
        Wait for the element from the current screen to be in a clickable state, then sends the END key to that element
        :param element: the web_element o a dict with the name, id, xpath, class_name, tag_name, text, href, type_name,
        src, and html_tag
        :param paths: the name, id, xpath, class_name, tag_name, text, href, type_name, src, and html_tag as parameters
        :return: the web_element generated
        """
        return self.wait_and_perform_action(self.wait_to_be_clickable, self.send_end_key_to, element=element
                                            , **paths)

    def wait_to_be_clickable_and_send_page_up_key(self, element=None, **paths):
        """
        Wait for the element from the current screen to be in a clickable state, then sends the PgUp key to that element
        :param element: the web_element o a dict with the name, id, xpath, class_name, tag_name, text, href, type_name,
        src, and html_tag
        :param paths: the name, id, xpath, class_name, tag_name, text, href, type_name, src, and html_tag as parameters
        :return: the web_element generated
        """
        return self.wait_and_perform_action(self.wait_to_be_clickable, self.send_down_key_to, element=element, **paths)

    def wait_to_be_clickable_and_send_enter_key(self, element=None, **paths):
        """
        Wait for the element from the current screen to be in a clickable state, then sends the ENTER key to that element
        :param element: the web_element o a dict with the name, id, xpath, class_name, tag_name, text, href, type_name,
        src, and html_tag
        :param paths: the name, id, xpath, class_name, tag_name, text, href, type_name, src, and html_tag as parameters
        :return: the web_element generated
        """
        return self.wait_and_perform_action(self.wait_to_be_clickable, self.send_enter_key_to, element=element, **paths)

    def wait_to_be_present_move_mouse_over_it_and_left_clicks_it(self, element=None, **paths):
        """
        Wait for the element from the current screen to be present in the DOM, performs an action of moving the mouse
        over the center of the element, then performs another action of left click wherever the mouse is located. DO
        NOT MOVE THE MOUSE WHILE THIS.
        :param element: the web_element o a dict with the name, id, xpath, class_name, tag_name, text, href, type_name,
        src, and html_tag
        :param paths: the name, id, xpath, class_name, tag_name, text, href, type_name, src, and html_tag as parameters
        :return: the web_element generated
        """
        return self.wait_and_perform_action(self.wait_to_be_present, self.move_mouse_over_it_and_left_click_it,
                                            element=element, **paths)

    def wait_to_be_clickable_move_mouse_over_it_and_left_clicks_it(self, element=None, **paths):
        """
        Wait for the element from the current screen to be in a clickable state, performs an action of moving the mouse
        over the center of the element, then performs another action of left click wherever the mouse is located. DO
        NOT MOVE THE MOUSE WHILE THIS.
        :param element: the web_element o a dict with the name, id, xpath, class_name, tag_name, text, href, type_name,
        src, and html_tag
        :param paths: the name, id, xpath, class_name, tag_name, text, href, type_name, src, and html_tag as parameters
        :return: the web_element generated
        """
        return self.wait_and_perform_action(self.wait_to_be_clickable, self.move_mouse_over_it_and_left_click_it,
                                            element=element, **paths)

    def wait_to_be_present_and_move_mouse_over_it(self, element=None, **paths):
        """
        Wait for the element from the current screen to be present in the DOM and performs an action of moving the mouse
        over the center of the element
        :param element: the web_element o a dict with the name, id, xpath, class_name, tag_name, text, href, type_name,
        src, and html_tag
        :param paths: the name, id, xpath, class_name, tag_name, text, href, type_name, src, and html_tag as parameters
        :return: the web_element generated
        """
        return self.wait_and_perform_action(self.wait_to_be_present, self.move_mouse_over, element=element, **paths)

    def wait_to_be_present_and_scroll_screen_to_it(self, element=None, **paths):
        """
        Wait for the element from the current screen to be present in the DOM, performs a javascript action of scrolling
        to the location of that element
        :param element: the web_element o a dict with the name, id, xpath, class_name, tag_name, text, href, type_name,
        src, and html_tag
        :param paths: the name, id, xpath, class_name, tag_name, text, href, type_name, src, and html_tag as parameters
        :return: the web_element generated
        """
        return self.wait_and_perform_action(self.wait_to_be_present, self.scroll_to, element=element, **paths)

    def wait_to_be_visible_and_move_mouse_over_it(self, element=None, **paths):
        """
        Wait for the element from the current screen to be visible (present in the DOM and size grater than zero) and
        performs an action of moving the mouse over the center of the element
        :param element: the web_element o a dict with the name, id, xpath, class_name, tag_name, text, href, type_name,
        src, and html_tag
        :param paths: the name, id, xpath, class_name, tag_name, text, href, type_name, src, and html_tag as parameters
        :return: the web_element generated
        """
        return self.wait_and_perform_action(self.wait_to_be_present, self.move_mouse_over, element=element, **paths)

    def wait_to_be_present_and_obtain_text(self, element=None, **paths):
        """
        Wait for the element from the current screen to be present in the DOM and returns the text it has
        :param element: the web_element o a dict with the name, id, xpath, class_name, tag_name, text, href, type_name,
        src, and html_tag
        :param paths: the name, id, xpath, class_name, tag_name, text, href, type_name, src, and html_tag as parameters
        :return: the text of the element or None if it doesn't has one
        """
        return self.wait_and_perform_action(self.wait_to_be_present, self.get_text, element=element ** paths)

    def wait_to_be_present_and_compare_text(self, text, element=None, **paths):
        """
        Wait for the element from the current screen to be present in the DOM, than compare if the element's text
        contains the desired text
        :param text: the text you want to compare against the text from the element
        :param paths: the name, id, xpath, class_name, tag_name, text, href, type_name, src, and html_tag as parameters
                :param element: the web_element o a dict with the name, id, xpath, class_name, tag_name, text, href, type_name,
        src, and html_tag
        :return: true or false
        """
        return self.wait_and_perform_action(self.wait_to_be_present, self.contains_text, value=text,
                                            element=element ** paths)

    def wait_to_be_present_and_get_size(self, element=None, **paths):
        """
        Wait for the element from the current screen to be present in the DOM and get its size in px
        :param element: the web_element o a dict with the name, id, xpath, class_name, tag_name, text, href, type_name,
        src, and html_tag
        :param paths: the name, id, xpath, class_name, tag_name, text, href, type_name, src, and html_tag as parameters
        :return: the web_element generated
        """
        return self.wait_and_perform_action(self.wait_to_be_present, self.get_size, element=element, **paths)['size']

    def wait_to_be_clickable(self, log=False, wait=0, **args):
        """Espera a que este en estado clicable y lo devuelve
            :Args:
             - name, id, xpath o class_name  - apuntando al elemento sobre el que se desea realizar la accion
        """
        return self.wait_to(EC.element_to_be_clickable, log=log, wait=wait, **args)

    def wait_to_be_selected(self, log=False, **args):
        """Espera a que este en estado seleccionado.
            :Args:
             - name, id, xpath o class_name  - apuntando al elemento sobre el que se desea realizar la accion
        """
        return self.wait_to(EC.element_located_to_be_selected, log=log, **args)

    def wait_to_be_present(self, log=False, wait=0, **args):
        """Espera a que este en estado seleccionado y lo devuelve
            :Args:
             - name, id, xpath o class_name  - apuntando al elemento sobre el que se desea realizar la accion
        """
        return self.wait_to(EC.presence_of_element_located, log=log, wait=wait, **args)

    def wait_to_be_visible(self, log=False, **args):
        """Espera a que este en estado seleccionado y lo devuelve
            :Args:
             - name, id, xpath o class_name  - apuntando al elemento sobre el que se desea realizar la accion
        """
        return self.wait_to(EC.visibility_of_element_located, log=log, **args)

    def wait_to(self, esperar, wait=0, log=False, **args):
        if wait > 0:
            self.wait(seg=wait)
        by = self.get_by(**args)
        if log:
            print(by)
        element = dict()
        element['element'] = WebDriverWait(Runner.Driver, 10).until(esperar((by[0], by[1])))
        return element

    def perform_wait(self, single_wait, element=None, **args):
        if isinstance(element, dict):
            assert isinstance(element['element'], WebElement), 'element[\'element\'] has to be a web_element'
            return element
        if isinstance(element, tuple):
            return single_wait(element=element)
        elif element is None:
            element = single_wait(**args)
            return element
        return element

    def wait_and_perform_action(self, wait_to, action, element=None, wait=0, parent=None, child=None, **args):
        """
        Wait for the element to be in a desired state, then performs an action over that element.
        :param wait_to: pass a function to wait for the desired state: wait_to_be_present, wait_to_be_selected,
        wait_to_be_clickable or use the generic function wait_to(desired_state)
        :param action: pass a function to perform the desired action: move_mouse_over, move_mouse_over_it_and_left_click_it,
        clear_text_and_input_new_text, get_text, get_attribute, get_size, get_element, get_children, send_home_key_to,
        send_end_key_to, send_down_key_to, send_enter_key_to, scroll_to, get_location, click or select
        :param element: a web_element previously generated or a dict with the following keys to generate a web_element:
        the name, id, xpath, class_name, tag_name, text, href, type_name, src, and html_tag as keys
        :param wait: the seconds you want for the script to wait before continuing.
        :param args: the name, id, xpath, class_name, tag_name, text, href, type_name, src, and html_tag as parameters
        :return: the web_element generated in most cases. Location, size or text when asked for
        """
        if isinstance(wait_to, list):
            for single_wait in wait_to:
                element = self.perform_wait(single_wait, element=element, child=child, parent=parent, **args)
        else:
            element = self.perform_wait(wait_to, element=element, child=child, parent=parent, **args)

        assert isinstance(element, dict), 'Something went wrong during wait'
        assert isinstance(element['element'], WebElement), 'Something went wrong during wait'

        if wait > 0:
            self.wait(seg=wait)

        return self.perform_actions(action, element, child=child, parent=parent, **args)

    def perform_actions(self, actions, element, child=None, parent=None, wait=0, **args):
        web_element = element
        web_element['value'] = None
        web_element['header'] = None
        web_element['text'] = None

        for key, value in args.items():
            if 'value' in key:
                web_element['value'] = value
            if 'header' in key:
                web_element['header'] = value
            if 'text' in key:
                web_element['text'] = value
            if 'wait' in key:
                self.wait(seg=value)

        if isinstance(actions, list):
            for single_action in actions:
                web_element = self.perform_action(single_action, web_element, child=child, parent=parent,
                                                  wait=wait)
            return web_element
        else:
            return self.perform_action(actions, web_element, child=child, parent=parent, wait=wait)

    def perform_action(self, single_action, element, log=False, child=None, wait=0):
        web_element = dict()
        if isinstance(element, WebElement):
            web_element['element'] = element
        elif isinstance(element, dict):
            web_element = element

            if wait > 0:
                self.wait(seg=wait)
        if single_action.__name__ in 'get_children' or single_action.__name__ in 'get_random_child':
            web_element = single_action(web_element, log=log, child=child)
        else:
            web_element = single_action(web_element, log=log)
        return web_element

    def click(self, element):
        """
        Perform a click with selenium over the element
        :param element: the web_element you want to click over
        :return: the previous web_element
        """
        web_element = element
        assert isinstance(web_element['element'], WebElement), 'Failed to transform to web_element'

        web_element['element'].click()
        return web_element

    def select(self, element, value=None):
        """
         Selects a value from the element from the current screen
        :param element: an web_element (type select) you wish to select value from
        :param value: the value you wish to select, not the text of the value
        """
        web_element = element
        assert isinstance(web_element['element'], WebElement), 'Failed to transform to web_element'

        if value is not None:
            web_element['value'] = value
        web_element['select'] = Select(web_element['element']).select_by_value(web_element['value'])
        return web_element

    def move_mouse_over(self, element):
        """
        Move the mouse over the center of the web_element using action_chains
        :param element: the web_element previously generated you want to move the mouse over
        :return: the same web_element
        """
        web_element = element
        if isinstance(web_element['element'], list) or isinstance(web_element['element'], tuple):
            assert isinstance(web_element['element'][0], WebElement), 'Failed to transform to web_element'

            action_chains = ActionChains(Runner.Driver)
            action_chains.move_to_element(web_element['element'][0])
            action_chains.perform()
            web_element['action_chains'] = action_chains
        else:
            assert isinstance(web_element['element'], WebElement), 'Failed to transform to web_element'

            action_chains = ActionChains(Runner.Driver)
            action_chains.move_to_element(web_element['element'])
            action_chains.perform()
            web_element['action_chains'] = action_chains

        return web_element

    def move_mouse_over_it_and_left_click_it(self, element):
        """
        Performs an action_chains action to move the mouse over the center of the element, then waits 0.2 seconds and
        performs another action_chains action to left click where to mouse is located in that moment.
        :param element: the web_element previously generated you want to left click it
        :return: the same web_element
        """
        web_element = element
        assert isinstance(web_element['element'], WebElement), 'Failed to transform to web_element'

        self.move_mouse_over(web_element)
        action_chains = ActionChains(Runner.Driver)
        action_chains.click(web_element['element'])
        action_chains.perform()
        web_element['action_chains'] = action_chains
        return web_element

    def clear_text_and_input_new_text(self, element, value=''):
        """Elimina el texto del elemento de la pantalla actual y manda un texto nuevo
            :Args:
             - element - un WebElement sobre el que se desea realizar la accion
             - texto - El texto que se desea introducir
        """
        web_element = element
        assert isinstance(web_element['element'], WebElement), 'Failed to transform to web_element'

        if value != '':
            web_element['value'] = value
        web_element['element'].clear()
        web_element['element'].send_keys(web_element['value'])
        return web_element

    def is_visible(self, element=None, **args):
        """
        Checks if the element is visible to the user or not.
        :param log: if print log or not
        :param element: the web_element. By default None and will generate one. Its prefered this way as you can get
        a Stale exception
        :param args: - name, id, xpath o class_name  - attribute pointing to the element you want to check visibility
        :return: dict with visibility as value
        """
        web_element = element
        try:
            assert isinstance(web_element['element'], WebElement), 'Failed to transform to web_element'

            web_element['visibility'] = web_element['element'].is_displayed()
            return web_element
        except WebDriverException:
            web_element['visibility'] = False
            return web_element

    def contains_text(self, element, **args):
        """comprueba si el texto obtenido del elemento de la pantalla principal contiene parcial o 
        totalmente el texto deseado y devuelve true o false
            :Args:
             - element - el elemento de la pantalla principal sobre el que se le va a comparar el texto
             - texto - el texto que se desea comparar
        """
        web_element = element
        web_element['contains_text'] = web_element['text'] in self.get_text(web_element['element'])['text']
        return web_element

    def get_text(self, element, text=None, log=False):
        """Devuelve el texto del elemento de la pantalla principal
           :Args:
             - element - un WebElement sobre el que se recupera el texto
        """
        web_element = element
        assert isinstance(web_element['element'], WebElement), 'Failed to transform to web_element'

        if log:
            print(type(web_element['element']))
            print(web_element['element'])
        web_element['text'] = web_element['element'].text
        return web_element

    def get_attribute(self, element, **args):
        """Devuelve el atributo deseado del elemento de la pantalla principal. Si no se pasa el elemento
        como parametro, se contruye de nuevo
            :Args:
             - atributo - el atributo del que se desea sacar el valor
             - element - un WebElement sobre el que se recupera el valor del atributo
             - name, id, xpath o class_name  - apuntando al elemento sobre el que se desea realizar la accion
        """
        # web_element = self.get_element(element)
        web_element = element
        assert isinstance(web_element['element'], WebElement), 'Failed to transform to web_element'
        for key, value in args.items():
            web_element[value] = web_element['element'].get_attribute(value)
        attribute = ''
        current_value = ''
        for key, value in web_element.items():
            if 'value' in key:
                attribute = web_element['element'].get_attribute(value)
                current_value = value
        web_element[current_value] = attribute  # This change dict size. Can't make assignment inside loop
        return web_element

    def get_size(self, element):
        """Get the size of the element from the current home
        :param element: web_element you want to know it's size
        :return: a map with the width and height of the web_element
        """
        web_element = element
        assert isinstance(web_element['element'], WebElement), 'Failed to transform to web_element'
        web_element['size'] = size
        return web_element

    def get_current_page(self):
        """
        Get the current url from the browser
        :return: the text with the current url
        """
        return Runner.Driver.current_url

    def get_children(self, element, child=None, **args):
        """
        Get all web_elements inside the current element constructed with the -**args- or from within parent
        :param element: the dict to generate the parent element. It will search from root if parent is not defined
        :param args: - name, id, xpath, class_name, tag, text, href and type  - pointing tot he parent element
        :return: a list with all the children
        """
        web_element = dict()
        if isinstance(element, tuple) and child is None:
            by = self.get_by(element=element, **args)
            web_element['element'] = Runner.Driver.find_elements(by[0], by[1])
        elif isinstance(element, tuple) and child is not None:
            by = self.get_by(element=element, **args)
            web_element['parent'] = Runner.Driver.find_element(by[0], by[1])
            if not isinstance(child, dict):
                by = self.get_by(xpath=child)
            else:
                by = self.get_by(element=child, **args)
            web_element['element'] = web_element['parent'].find_elements(by[0], by[1])
        elif isinstance(element, WebElement):
            if not isinstance(child, dict):
                by = self.get_by(xpath=child)
            else:
                by = self.get_by(element=child, **args)
            web_element['element'] = element.find_elements(by[0], by[1])
        elif isinstance(element, str):
            web_element['parent'] = Runner.Driver.find_element('xpath', element)
            if not isinstance(child, dict):
                by = self.get_by(xpath=child)
            else:
                by = self.get_by(element=child, **args)
            web_element['element'] = web_element['parent'].find_elements(by[0], by[1])
        elif isinstance(element, dict):
            web_element['parent'] = element['element']
            if not isinstance(child, dict):
                by = self.get_by(xpath=child)
            else:
                by = self.get_by(element=child, **args)
            web_element['element'] = web_element['parent'].find_elements(by[0], by[1])
        assert isinstance(web_element, dict)
        if isinstance(web_element['element'], list):
            if len(web_element['element']) > 0:
                assert isinstance(web_element['element'][0], WebElement)
        else:
            assert isinstance(web_element['element'], WebElement)
        return web_element

    def get_first_child(self, element, child=None, parent=None, **args):
        return self.get_children(element, child=child, parent=parent, **args)['element'][0]

    def get_child(self, element, parent=None, child=None, **args):
        """
        Get all web_elements inside the parent element
        :param parent: The element from which you want all children
        :param element: the dict to generate the child element.
        :param args: - name, id, xpath, class_name, tag, text, href and type  - pointing tot he parent element
        :return: a list with all the children
        """
        web_element = dict()
        if isinstance(element, dict) and isinstance(parent, WebElement):
            # by = ('', '')
            if isinstance(element['element'], tuple):
                by = element['element']
            else:
                by = self.get_by(element=element, **args)
            web_element['element'] = parent.find_element(by[0], by[1])
            return web_element
        if isinstance(element, tuple) and isinstance(child, str):
            by = self.get_by(element=element, **args)
            web_element['parent'] = Runner.Driver.find_element(by[0], by[1])
            web_element['element'] = web_element['parent'].find_element('xpath', child)
            return web_element
        elif isinstance(element, tuple) and isinstance(parent, WebElement):
            by = self.get_by(element=element, **args)
            web_element['element'] = parent.find_element(by[0], by[1])
            return web_element

        web_element = self.get_element(element)
        assert isinstance(web_element['element'], WebElement), 'Failed to transform to web_element'

        if child is not None:
            if not isinstance(child, dict):
                by = self.get_by(xpath=child)
            else:
                by = self.get_by(element=child, **args)
            assert isinstance(web_element['element'], WebElement), 'failed to transform to web_element'
            web_element['element'] = web_element['element'].find_element(by[0], by[1])
        elif parent is not None and isinstance(parent, WebElement):
            by = self.get_by(element=element, **args)
            web_element['element'] = parent.find_element(by[0], by[1])
        return web_element

    def get_by(self, element=None, **args):
        """
        Build a dictionary which will be used to generate the web_element
        :param element: a dictionary with the -args- parameters used
        :param args: name, identificador, xpath, class_name, tag_name, text, href, type_name, src, html_tag, log.
         Log will be used to print the path to the current element
        :return: a tuple (by, path) used to generate the web_element
        """
        d = ('', '')
        name = None
        identificador = None
        xpath = None
        class_name = None
        tag_name = None
        text = None
        href = None
        type_name = None
        src = None
        html_tag = '*'
        log = False

        for key, value in args.items():
            if 'xpath' in key:
                xpath = value
                continue
            if 'class_name' in key:
                class_name = value
                continue
            if 'type_name' in key:
                type_name = value
                continue
            if 'tag_name' in key:
                tag_name = value
                continue
            if 'name' in key:
                name = value
                continue
            if 'identificador' in key:
                identificador = value
                continue
            if 'text' in key:
                text = value
                continue
            if 'href' in key:
                href = value
                continue
            if 'src' in key:
                src = value
                continue
            if 'html_tag' in key:
                html_tag = value
                continue
            if 'log' in key:
                log = value
                continue
            if 'element' in key:
                element = value
                continue
        if isinstance(element, tuple):
            if log:
                print('***************************************')
                print('path {} \tby {}'.format(element[1], element[0]))
            return element

        if element is not None and isinstance(element, dict):
            name = ''
            identificador = ''
            xpath = ''
            class_name = ''
            tag_name = ''
            text = ''
            href = ''
            type_name = ''
            src = ''
            html_tag = '*'
            if 'xpath' in element:
                xpath = element['xpath']
            if 'name' in element:
                name = element['name']
            if 'id' in element:
                identificador = element['id']
            if 'class_name' in element:
                class_name = element['class_name']
            if 'tag_name' in element:
                tag_name = element['tag_name']
            if 'text' in element:
                text = element['text']
            if 'href' in element:
                href = element['href']
            if 'type_name' in element:
                type_name = element['type_name']
            if 'src' in element:
                src = element['src']
            if 'html_tag' in element:
                html_tag = element['html_tag']
            if 'element' in element:
                return self.get_by(element=element['element'])

        if xpath is not None:
            if xpath != '':
                d = (By.XPATH, xpath)
                if log:
                    print('***************************************')
                    print('by {}\tpath {}'.format(d[0], d[1]))
                return d
        if identificador is not None:
            if identificador != '':
                d = (By.ID, identificador)
                if log:
                    print('***************************************')
                    print('path {} \tby {}'.format(d[1], d[0]))
                return d
        if name is not None:
            if name != '':
                d = (By.NAME, name)
                if log:
                    print('***************************************')
                    print('path {} \tby {}'.format(d[1], d[0]))
                return d
        if class_name is not None:
            if class_name != '':
                if html_tag is not '*':
                    path = '//{}[contains(@class,\'{}\')]'.format(html_tag, class_name)
                else:
                    path = '//*[contains(@class,\'{}\')]'.format(class_name)
                d = (By.XPATH, path)
                if log:
                    print('***************************************')
                    print('path {} \tby {}'.format(d[1], d[0]))
                return d
        if tag_name is not None:
            if tag_name != '':
                d = (By.TAG_NAME, tag_name)
                if log:
                    print('***************************************')
                    print('path {} \tby {}'.format(d[1], d[0]))
                return d
        if text is not None:
            if text != '':
                if html_tag is not '*':
                    path = '//{}[contains(text(),\'{}\')]'.format(html_tag, text)
                else:
                    path = '//*[contains(text(),\'{}\')]'.format(text)
                d = (By.XPATH, path)
                if log:
                    print('***************************************')
                    print('path {} \tby {}'.format(d[1], d[0]))
                return d
        if href is not None:
            if href != '':
                if html_tag is not '*':
                    path = '//{}[contains(@href,\'{}\')]'.format(html_tag, href)
                else:
                    path = '//*[contains(@href,\'{}\')]'.format(href)
                d = (By.XPATH, path)
                if log:
                    print('***************************************')
                    print('path {} \tby {}'.format(d[1], d[0]))
                return d
        if type_name is not None:
            if type_name != '':
                if html_tag is not '*':
                    path = '//{}[contains(@type,\'{}\')]'.format(html_tag, type_name)
                else:
                    path = '//*[contains(@type,\'{}\')]'.format(type_name)
                d = (By.XPATH, path)
                if log:
                    print('***************************************')
                    print('path {} \tby {}'.format(d[1], d[0]))
                return d
        if src is not None:
            if src != '':
                if html_tag is not '*':
                    path = '//{}[contains(@src,\'{}\')]'.format(html_tag, src)
                else:
                    path = '//*[contains(@src,\'{}\')]'.format(src)
                d = (By.XPATH, path)
                if log:
                    print('***************************************')
                    print('path {} \tby {}'.format(d[1], d[0]))
                return d
        return d

    def send_key(self, key, wait=0):
        """
        Legacy method. It's better to use scroll_to
        :param key: str. Key you want to send. It will be parsed
        :param wait: after sending keys, how many seconds to wait
        :return: action_chains
        """
        if 'home' in str(key).lower():
            return self.send_home_key()
        if 'end' in str(key).lower():
            return self.send_end_key()
        if 'up' in str(key).lower():
            return self.send_up_key()
        if 'down' in str(key).lower() or 'dn' in str(key).lower():
            return self.send_down_key()
        if wait > 0:
            return self.wait(seg=wait)

    def send_home_key_to(self, element):
        """
        Send the HOME key to the web_element
        :param element: web_element you want to send key to
        :return: dict with element as value
        """
        web_element = self.get_element(element)
        assert isinstance(web_element['element'], WebElement), 'Failed to transform to web_element'

        web_element['element'].send_keys(Keys.ENTER)
        return web_element

    def send_home_key(self):
        """
        Send the HOME key to the browser
        :return: action_chain generated
        """
        action_chains = ActionChains(Runner.Driver)
        action_chains.send_keys(Keys.HOME)
        action_chains.perform()
        return action_chains

    def send_end_key_to(self, element):
        """
        Send the END key to the web_element
        :param log: if print log or not
        :param element: web_element
        :return: a dict with element as value
        """
        web_element = self.get_element(element)
        assert isinstance(web_element['element'], WebElement), 'Failed to transform to web_element'

        web_element['element'].send_keys(Keys.END)
        return web_element

    def send_end_key(self):
        """
        Send the END key to the browser
        :return: the action_chain generated
        """
        action_chains = ActionChains(Runner.Driver)
        action_chains.send_keys(Keys.END)
        action_chains.perform()
        return action_chains

    def send_down_key_to(self, element):
        """
        Sends the PgDn key to the element
        :return: the web_element received
        """
        web_element = self.get_element(element)
        assert isinstance(web_element['element'], WebElement), 'Failed to transform to web_element'

        web_element.send_keys(Keys.PAGE_DOWN)
        return web_element

    def send_down_key(self):
        """
        Sends the PgDn key to the browser
        :return: the action_chains created
        """
        action_chains = ActionChains(Runner.Driver)
        action_chains.send_keys(Keys.PAGE_DOWN)
        action_chains.perform()
        return action_chains

    def send_enter_key(self):
        """
        Sends the PgDn key to the browser
        :return: the action_chains created
        """
        action_chains = ActionChains(Runner.Driver)
        action_chains.send_keys(Keys.ENTER)
        action_chains.perform()
        return action_chains

    def send_enter_key_to(self, element, **args):
        """
        Sends the PgDn key to the browser
        :return: the or web_element received
        """
        # web_element = self.get_element(element, **args)
        web_element = element
        assert isinstance(web_element['element'], WebElement), 'Failed to transform to web_element'

        web_element['element'].send_keys(Keys.ENTER)
        return web_element

    def send_up_key(self):
        """
        Sends the PgUp key to the browser
        :return: the action_chains created
        """
        action_chains = ActionChains(Runner.Driver)
        action_chains.send_keys(Keys.PAGE_UP)
        action_chains.perform()
        return action_chains

    def scroll_to(self, element, wait='0'):
        """
        Scroll the screen and matched the top with the start of the element minus 20px
        :param wait: the number of seconds it will wait after scroll.
        :param element: the web_element you want to scroll to. It can also generate a web_element from a dict or a tuple
        :return: a dict with element as value
        """
        web_element = element
        assert isinstance(web_element['element'], WebElement), 'Failed to transform to web_element'

        try:
            if web_element['header'] is not None:
                if isinstance(web_element['header'], int):
                    header = web_element['header']
                else:
                    header = web_element['header']['height']
                script = "window.scrollTo(0, {});".format(
                    web_element['element'].location['y'] - 20 - header)
            else:
                script = "window.scrollTo(0, {});".format(web_element['element'].location['y'] - 20)
        except KeyError:
            script = "window.scrollTo(0, {});".format(web_element['element'].location['y'] - 20)
        Runner.Driver.execute_script(script)
        self.wait(seg=int(wait))
        web_element['wait'] = wait
        return web_element

    def scroll_to_first(self, element, wait='0'):
        assert isinstance(element['element'], list), 'This method only works with list'
        self.scroll_to(element['element'][0])
        return element

    def scroll_to_location(self, x=0, y=0):
        """
        Legacy method. Better to use scroll_to
        :param x: in pixels
        :param y: in pixels
        :param log: if print log or not
        :return: None
        """
        script = "window.scrollTo({}, {});".format(x, y)
        Runner.Driver.execute_script(script)
        return None

    def move_mouse_over_location(self, element, x=0, y=0):
        try:
            action_chains = element['action_chains']
        except WebDriverException:
            action_chains = ActionChains(Runner.Driver)
        action_chains.move_by_offset(x, y)
        action_chains.perform()
        return element

    def get_location(self, element):
        web_element = self.get_element(element)
        assert isinstance(web_element['element'], WebElement), 'Failed to transform to web_element'

        web_element['location'] = web_element['element'].location
        return web_element

    def right_click(self, element):
        """
        Right click where the mouse is located over at that moment
        :param element: web_element
        :return: a dict with element as value
        """
        web_element = self.get_element(element)
        assert isinstance(web_element['element'], WebElement), 'Failed to transform to web_element'

        action_chains = ActionChains(Runner.Driver)
        action_chains.context_click(web_element['element'])
        action_chains.perform()
        web_element['action_chains'] = action_chains
        return web_element

    def left_click(self, element):
        """
        Right click where the mouse is located over at that moment
        :param element: web_element
        :param log: if print log or not
        :return: a dict with element as value
        """
        web_element = self.get_element(element)
        assert isinstance(web_element['element'], WebElement), 'Failed to transform to web_element'

        action_chains = ActionChains(Runner.Driver)
        action_chains.click(web_element['element'])
        action_chains.perform()
        web_element['action_chains'] = action_chains
        return web_element

    def select_first_value_from_select(self, element):
        web_element = self.get_element(element)
        assert isinstance(web_element['element'], WebElement), 'Failed to transform to web_element'

        select = Select(web_element['element']).select_by_index(0)
        web_element['select'] = select
        return web_element

    def get_random_child(self, element, child=None, **args):
        children = self.get_children(element, child=child, ** args)['element']
        element = self.get_random_element_from_list(children)
        return_val = dict()
        return_val['element'] = element
        return return_val

    def get_random_element_from_list(self, my_list):
        import random
        return random.choice(my_list)

    def get_href(self, element, **args):
        web_element = element
        assert isinstance(web_element['element'], WebElement), 'Failed to transform to web_element'

        web_element['value'] = 'href'
        assert isinstance(web_element['element'], WebElement), 'element is not a web_element'
        return self.get_attribute(web_element)

    def click_all(self, element, **args):
        if isinstance(element, dict):
            if isinstance(element['element'], list):
                for one_element in element['element']:
                    self.click(one_element)
        elif isinstance(element['element'], list):
            for one_element in element['element']:
                self.click(one_element)
        return element
