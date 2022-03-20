from utils.base import *
from utils.scraper import ScrapInterface

class WebScraper:
  def __init__(self, scraper: ScrapInterface = None):
    self.service = ChromeService(executable_path=ChromeDriverManager().install())
    self.driver = webdriver.Chrome(service=self.service)
    self.scraper = scraper

  def get_browser(self):
    return self.driver
  
  def scraping(self, **kwargs):
    assert self.scraper is not None, "Scraper is empty, please set scraper first"
    return self.scraper.scraping(driver=self.driver, **kwargs)
  
  def set_scraper(self, scraper: ScrapInterface):
    assert isinstance(scraper, ScrapInterface), "TypeError"
    self.scraper = scraper