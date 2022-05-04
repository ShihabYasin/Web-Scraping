# Web Scraping:   


### Used Selenium, beautifulsoup4 etc.  

Customized Web scraping from website pages given a root domain url.

1. Check this function in ```main.py``` to set max depth to search for.

```python
def get_deep_link(links, depth=0, max_depth=2):
```
2. Check ```scraping_utility.py``` to set different params for web-scraping.
```python
def get_all_links_from_page_url(url, scrolling_button_text, include_pattern, exclude_pattern, SCROLL_COUNT, SCROLL_PAUSE_TIME,
                                implicit_delay_seconds, options,
                                base_url, selenium_chrome_driver_path):
    '''

    :param url:
    :param include_pattern: Pattern to follow
    :param exclude_pattern: Pattern not to follow
    :param SCROLL_COUNT: Number of scrolling to load more news
    :param SCROLL_PAUSE_TIME: After scrolling time delay to load elements
    :param implicit_delay_seconds: DOM element loading delay
    :param options: Driver options
    :param base_url: Target domain site url
    :param selenium_chrome_driver_path:
    :return:
    '''
```