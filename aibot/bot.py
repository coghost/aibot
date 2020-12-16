import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import WebDriverException, TimeoutException
from selenium.webdriver.common.keys import Keys


class Bot(object):
    def __init__(self, driver, **kwargs):
        self.driver = driver

    def wdw_get_elements(self, handler, to=30, method='until',
                         ignored_exceptions=(TimeoutException,),
                         show_log=False, freq=0.5):
        """
        wdw_get_elements is a wrapper just to ensure the handler can run until timeout,
        and we do not want to throw the exceptions

        Usage:
            1.
            self.bot.wdw_get_elements(lambda x: x.get_elems(locator))
            2.
            def a_time_cost_method():
                return True/False
            self.bot.wdw_get_elements(a_time_cost_method, to=20)

        Args:
            handler (): the handler to ensure
            to (): timeout
            method (): until/until_not
            ignored_exceptions (): exceptions, we only want to show warning
            show_log (): if show the warning or not
            freq (): poll frequency

        Returns:
            return what the handler returns
        """
        if method != 'until':
            method = 'until_not'
        try:
            return getattr(WebDriverWait(self, to, min(freq, to), ignored_exceptions), method)(handler)
        except ignored_exceptions as ie:
            if show_log:
                print(ie)
        except Exception as e:
            print(e)

    def get_elems(self, locator, index=0, root=None):
        """ WARN: this is an immediately action

        first of all get_elems will always find multiple elems,
        if index is None, will return all found elems
        else just return the element with supplied index.

        there 3 types of return value:
            1. nothing found, just return elems which is []
            2. index is None = multiple elems, just return elems
            3. index is int = not multiple, just return elems[index]

        Args:
            locator (WebElement/tuple/str): elem locator
            index (int/None): select which elem, None to get all elements
            root (WebElement/None): if from the whole driver

        Returns:
            WebElement
        """
        if not isinstance(locator, tuple) and not isinstance(locator, str):
            return locator

        if isinstance(locator, str):
            locator = (By.CSS_SELECTOR, locator)

        root = root or self.driver
        try:
            elements = root.find_elements(*locator)

            if index is None:
                return elements

            if elements and isinstance(index, int):
                return elements[index]
        except WebDriverException as e:
            raise Exception(f'[Err]: get {locator} failed with {e}')

    def get_elements(self, locator, timeout=30, index=0, root=None, method='until'):
        """ simple wrapper of wdw_get_elements(driver.get_elems)

        Args:
            locator (str/tuple/WebElement):
            timeout (float/int):
            index (int/None):
            root (None/WebElement):
            method (str):

        Returns:
            WebElement
        """
        elem = self.wdw_get_elements(
            lambda x: x.get_elems(locator, index=index, root=root), to=timeout, method=method)
        return elem

    @staticmethod
    def clear_by_backspace(element, length=0, attr='value'):
        length = length or len(element.get_attribute(attr)) + 8
        element.send_keys(Keys.BACKSPACE * length)

    def update_text(self, locator, value, attr='value', index=0, root=None):
        if isinstance(locator, str):
            locator = (By.CSS_SELECTOR, locator)
        elem = self.get_elements(locator, index=index, root=root)
        try:
            self.clear_by_backspace(elem, attr=attr)
        except:
            elem.clear()
        elem.send_keys(value)

    def switch_to_window(self, window, timeout=30):
        start_ms = time.time() * 1000.0
        stop_ms = start_ms + (timeout * 1000.0)
        for i in range(int(timeout) * 10):
            try:
                window_handle = self.driver.window_handles[window]
                self.driver.switch_to.window(window_handle)
                return True
            except IndexError:
                now_ms = time.time() * 1000.0
                if now_ms >= stop_ms:
                    break
                time.sleep(0.1)
            raise Exception(f"Window was not present after {timeout} seconds!")
