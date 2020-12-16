from .bot import Bot


class AiBot(object):
    def __init__(self, driver, **kwargs):
        self.driver = driver
        self.bot = Bot(driver, **kwargs)

    def get(self, url):
        self.driver.get(url)

    def update_text(self, locator, text, attr='value'):
        """ alias of bot.update_text """
        self.bot.update_text(locator, text, attr=attr)
