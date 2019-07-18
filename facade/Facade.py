from screen.Screen import Screen


def accept_cookies():
    from selenium.common.exceptions import TimeoutException
    try:
        screen.click_accept_cookies()
    except TimeoutException:
        print('cookies already accepted')


def check_size(element, size):
    """
    Bunch of asserts with default message
    :param element: the element you want to check
    :param size: a map. height and width are the only two options
    :return: nothing
    """
    assert element['height'] >= size[
        0], 'Main page did not loaded properly. Size element is {} and expected one is {}'.format(element['height'],
                                                                                                  size[0])
    assert element['width'] >= size[
        1], 'Main page did not loaded properly. Size element is {} and expected one is {}'.format(element['width'],
                                                                                                  size[1])


def check_no_size(element):
    """
    Bunch of asserts with default message
    :param element: the element you want to check
    :param size: a map. height and width are the only two options
    :return: nothing
    """
    assert element[
               'height'] == 0, 'Main page did not loaded properly. Size element is {} and expected one is {}'.format(
        element['height'],
        '0')
    assert element['width'] == 0, 'Main page did not loaded properly. Size element is {} and expected one is {}'.format(
        element['width'],
        '0')


def check_href(element, href='/', known_href='/'):
    assert element is not None, 'There is no href attribute'
    assert element != '', 'There is no href attribute'
    assert href not in known_href, 'href is not the same'


def check_css_visibility_image(element):
    """
    Checks if -element- contains ng-hide.
    :param element: the text you want to check
    :return: nothing
    """
    assert 'ng-hide' not in element, 'Image is not visible on screen'


def check_text(text_desired, text_given):
    if not isinstance(text_desired, str) and not isinstance(text_given, str):
        text_desired = str(text_desired)
        text_given = str(text_given)
    assert text_desired.lower() in text_given.lower(), 'Text {} doesn\'t match {}'.format(text_desired, text_given)


screen = Screen()


def scroll_down():
    """
    Sends to the body html element, the key END
    :return: nothing
    """
    screen.send_end_key()


def scroll_up():
    """
    Sends to the body html element, the key HOME
    :return: nothing
    """
    screen.send_home_key()


class Facade:
    def wait(self, url=None, seg=1, timeout=20, log=False):
        """
        If the url is defined, it will check every -seg- if the current browser url contains the -url-' It will check -timeout-
        times
        :param log: print log to console
        :param url: partial url that the browser should be on
        :param seg: how many seconds before trying again
        :param timeout: how many times will it try
        :return: nothing
        """
        if url is not None:
            if log:
                print('***Waiting for ' + url + ' to load')
            screen.wait(seg=seg, url=url, timeout=timeout)
            if log:
                print('***' + url + ' loaded successfully')
        else:
            screen.wait(seg=seg)
