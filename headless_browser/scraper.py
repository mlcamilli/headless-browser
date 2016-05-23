from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import os
import uuid
import shutil


class Scraper(object):

    def __init__(self, proxy=None, size=(1920, 1080), cleanup=True):
        self.cleanup = cleanup
        self.size = size
        self.service_args = []
        self.proxy = None
        if proxy:
            self.proxy = proxy
            self.service_args.append('--proxy={}'.format(proxy))
            # Can be http or socks5
            self.service_args.append('--proxy-type=http')
        self.desired = dict(DesiredCapabilities.PHANTOMJS)
        self.desired["phantomjs.page.settings.userAgent"] = (
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/53 "
            "(KHTML, like Gecko) Chrome/15.0.87"
        )
        self.initialize()

    def initialize(self):
        self.browser = webdriver.PhantomJS(desired_capabilities=self.desired,
                                           service_args=self.service_args)
        self.browser.set_window_size(*self.size)

    def quit(self):
        self.browser.quit()

    @property
    def html(self):
        return self.browser.page_source.encode('utf-8')

    def get(self, url):
        self.browser.get(url)

    def get_frame(self, selector):
        self.browser.switch_to.frame(selector)

    def by_id(self, selector):
        return self.browser.find_element_by_id(selector)

    def by_css(self, selector, multiple=False):
        if multiple:
            return self.browser.find_elements_by_css_selector(selector)
        else:
            return self.browser.find_element_by_css_selector(selector)

    def select_dropdown_option(self, element, value):
        select = Select(element)
        select.select_by_value(value)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.quit()


class ChromeScraper(Scraper):

    def initialize(self):
        self.display = Display(visible=0, size=self.size)
        self.display.start()
        self.browser = webdriver.Chrome(desired_capabilities=self.desired,
                                        service_args=self.service_args)

    def quit(self):
        self.browser.quit()
        self.display.stop()


class FirefoxScraper(Scraper):

    def initialize(self):
        """
        Initializes the scraper with a virtual display and a session specific
        download folder.
        """
        if os.environ.get('HEADLESS_DOWNLOAD_FOLDER'):
            download_folder = os.environ.get('HEADLESS_DOWNLOAD_FOLDER')
        else:
            download_folder = '{}/.downloads/'.format(os.getcwd())
        if not os.path.exists(download_folder):
            os.mkdir(download_folder)
        # Generate a random folder name
        self.download_folder = '{}{}/'.format(download_folder, uuid.uuid4())
        profile = webdriver.FirefoxProfile()
        profile.set_preference("browser.download.folderList", 2)
        profile.set_preference(
            "browser.download.manager.showWhenStarting", False)
        profile.set_preference("pdfjs.disabled", True)
        profile.set_preference(
            "browser.download.dir", self.download_folder)
        profile.set_preference(
            "browser.helperApps.neverAsk.saveToDisk",
            "application/pdf,text/csv,image/png,image/svg+xml")
        # Make sure we use their fonts
        profile.set_preference("browser.display.use_document_fonts" ,1)
        self.display = Display(visible=0, size=self.size)
        self.display.start()
        self.browser = webdriver.Firefox(
            firefox_profile=profile, capabilities=self.desired,
            proxy=self.proxy)

    def get_downloaded_files(self):
        if not os.path.exists(self.download_folder):
            return []
        files = os.listdir(self.download_folder)
        return ['{}{}'.format(self.download_folder, f) for f in files]

    def get_first_file(self):
        files = self.get_downloaded_files()
        return None if not files else files[0]

    def quit(self):
        self.browser.quit()
        self.display.stop()
        if self.cleanup:
            shutil.rmtree(self.download_folder, ignore_errors=True)
