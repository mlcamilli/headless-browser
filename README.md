# Headless Browser

This docker file installs python 3+ and the necessary libraries and dependencies to use a PhantomJS, Chrome, or Firefox Headless Browser.

To use, inside the docker container bring up the python shell.


```python
>>> from headless_browser import ChromeScraper, FirefoxScraper, PhantomScraper
>>> scraper = ChromeScraper()
>>> scraper.get('http://www.google.com')
```
