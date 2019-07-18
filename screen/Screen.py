from utils.BasicAction import BasicAction

accept_cookies = ('xpath', '//*[contains(@class,"cookies") and contains(@class,"btn")]')


class Screen(BasicAction):
    def click_accept_cookies(self):
        return self.wait_and_perform_action(self.wait_to_be_visible, self.click, element=accept_cookies)
