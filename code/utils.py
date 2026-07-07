import requests 
from bs4 import BeautifulSoup

def read_word_list(path:str) -> list[str]:
    '''
    reads in file with keywords

    returns a list 

    ARGS:
        path: path to file
    '''
    word_list = []
    with open(path, 'r') as words:
        for word in words: 
            word_list.append(word.strip())
    
    return word_list

def get_category_names(url:str) -> dict[str, str]:
    '''
    helper function that takes in an repository and 
    gets the plain language names of the sub-categories

    returns a map between arXiv convention and plain language name
    (e.g. 'CV':'Computer Vision')

    please note the web scraping matches the page structure 
    as of 2026-07-06 - this may need to be updated in the future

    ARGS:
        url: url to an arXiv repository 
    '''

    resp = requests.get(url)
    if resp.status_code == 200:
        arxiv = resp.text
    else:
        raise Exception('unable to retrieve page content')
    
    soup = BeautifulSoup(arxiv, 'html.parser')
    h2 = soup.find('h2')
    categories_list = h2.find_all_next('li')

    category_map = {}
    for category in categories_list:
        category_name = category.find('b')
        name_parts = category_name.text.split(' - ')

        category_map[name_parts[0]] = name_parts[1]

    return category_map