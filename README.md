# Headless Browser

This docker file installs python 2.7 and the necessary libraries and dependencies to use a PhantomJS, Chrome, or Firefox Headless Browser. 

To use, inside the docker container bring up the python shell.


```python
>>> from chrome_headless import ChromeScraper, FirefoxScraper, PhantomScraper
>>> scraper = ChromeScraper()
>>> scraper.get('http://www.google.com')
```
