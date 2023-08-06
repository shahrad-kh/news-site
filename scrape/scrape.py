import json
import time

import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


def write_to_file(News: list):
    """
    this function gets all news data and writes them in a json file

    Args:
        News (list): all news data
    """
    
    data = {'News': News}
    
    with open('./news.json', 'a+', encoding='utf-8') as f:
        json.dump(data, f)


def scrape_news_via_link(driver: webdriver, links: list):
    """this function gets all news links and scrape to return news data

    Args:
        driver (webdriver): chrome webdriver
        links (list): all news links

    Returns:
        list: all news data like title, tags, ....
    """
    
    News = []
    for link in links:
        # To try get news page using link and get news data
        try:
            driver.get(link)
            news = {}
            news['title'] = driver.find_element(By.CSS_SELECTOR, ".eNoCZh").text
            news['tags'] = [tag.text for tag in driver.find_elements(By.CSS_SELECTOR, ".eMeOeL")]
            news['source'] = link
            
            sentences = [str(sentence.text) for sentence in \
                driver.find_elements(By.CSS_SELECTOR, ".dfnkIg > \
                .typography__StyledDynamicTypographyComponent-t787b7-0")]
            news['content'] =  '\n'.join(sentences)    
                
            News.append(news)
            
        except:
            continue
    
    return News


def get_news_links(driver: webdriver, url: str):
    """this function gets website url and returns all news links

    Args:
        driver (webdriver): chrome webdriver
        url (str): website url

    Returns:
        list: all news links
    """
    
    driver.get(url)
    
    # To click on see_more button
    for t in range(5):
        try:
            more_button = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".eByvXQ")))
            more_button.click()

        except Exception as e:
            print(e)
            continue
    
    # To get all news elements
    try:   
        elements = WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".iCQspp")))
    
    except Exception as e:
        print('failed to get elements...')
        print(e)
    
    # To get all news links
    links = []
    for element in elements:
        link = element.get_attribute('href')
        if not link.startswith('https://www.zoomg.ir/'):
            links.append(link)
    
    return links


if __name__ == '__main__':
    
    # define chrome options
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument('--disable-dev-shm-usage')
    
    # Install ChromeDriver using autoinstaller
    chromedriver_autoinstaller.install()
    
    # Step_1: get all news links
    driver = webdriver.Chrome(options=chrome_options)
    url = "https://www.zoomit.ir/archive/?sort=Newest"
    links = get_news_links(driver, url)
    driver.close()
    
    # Step_2: scrape news
    driver = webdriver.Chrome(options=chrome_options)
    News = scrape_news_via_link(driver, links)
    driver.close()
    
    # Step3: writing data in a json file
    write_to_file(News)
    print('Done!')