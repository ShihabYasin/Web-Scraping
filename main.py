import ast
import csv
import os
from scraping_utility import get_all_links_from_page_url, get_text_from_page_url, opts, selenium_chrome_driver_path


def write_csv(csvfile, rows):
    '''

    :param csvfile:
    :param rows: e.g. rows = [['URL', ['Physics', 'Physics']], ['URL1', ['Physics1', 'Physics1']], ['URL2', ['Physics2', 'Physics2']]]
    :return:
    '''

    with open (csvfile, 'a') as f:
        write = csv.writer (f)
        write.writerows (rows)


def read_csv(csvfile):
    '''

    :param csvfile:
    :return: List[url:str, list:str]
    '''
    with open (csvfile) as csv_file:
        csv_reader = csv.reader (csv_file, delimiter=',')
        retlists = []
        for idx, row in enumerate (csv_reader):
            ls = [n.strip () for n in ast.literal_eval (row[1])]
            retlists.append ([row[0], ls])  # returns url, texts_string_list

        return retlists


def get_deep_link(links, depth=0, max_depth=2):
    '''

    :param links:
    :param depth:
    :param max_depth: Website max page depth to search for.
    :return:
    '''
    if depth > max_depth:
        return links
    ret_links, ret_links_deeper = [], []
    for ln in links:
        collected_texts = list ()
        for line in get_text_from_page_url (start_url=ln):
            collected_texts.append (line)

        write_csv (csvfile='texts.csv', rows=[[ln, collected_texts]])
        # print (f"{ln}, {collected_texts}", file=open ('texts.csv', 'a'))

        ret_links += get_all_links_from_page_url (url=ln)

    ret_links_deeper = get_deep_link (links=ret_links, depth=depth + 1, max_depth=max_depth)

    return list (set (links + ret_links + ret_links_deeper))


if __name__ == '__main__':
    os.system ('sudo mount -o remount,size=8G /dev/shm')  # Increasing Browser Cache

    base_url = "https://www.domaintoscrap.com/"
    include_patterns = ["domaintoscrap.com"]
    exclude_patterns = ["en."]  # exclude subdomain if need
    scrolling_button_text = 'Next'

    get_deep_link (links=get_all_links_from_page_url (url=base_url, scrolling_button_text=scrolling_button_text, include_pattern=include_patterns, exclude_pattern=exclude_patterns, SCROLL_COUNT=5, SCROLL_PAUSE_TIME=1,
                                                      implicit_delay_seconds=3, options=opts,
                                                      base_url=base_url,
                                                      selenium_chrome_driver_path=selenium_chrome_driver_path), depth=0, max_depth=15)
