import os

import chromedriver_autoinstaller
import django
from celery import Celery
from celery.schedules import crontab
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from news.models import News, Tag


def create_instance(news_list: list):
    """
    creates News instance using scraped data

    Args:
        news_list (list): list of dictionaries included news fields
    """
    
    for news in news_list:
        # Try to create new news
        try:
            new_instance = News.objects.create(
                title = news['title'],
                content = news['content'],
                source = news['source']
            )
            
            tags = []
            for news_tag in news['tags']:
                
                # Try to create new tag if it doesn't exist
                try:
                    tag = Tag.objects.create(title=news_tag)
                except:
                    tag = Tag.objects.filter(title=news_tag).first()
                
                tags.append(tag)
                    
            new_instance.tags.set(tags)
    
        except:
            continue
        

def scrape_news_via_link(driver: webdriver, links: list):
    """
    this function gets fresh news links and scrape to return news data

    Args:
        driver (webdriver): chrome webdriver
        links (list): fresh news links

    Returns:
        list: fresh news data like title, tags, ....
    """
    
    news_list = []
    for link in links:
        # To try get news page using link and get news data
        try:
            driver.get(link)
            news = {}
            news['title'] = driver.find_element(By.CSS_SELECTOR, ".hwtfkB").text
            
            # To check if News already exist in database
            if News.objects.filter(title=news['title']):
                continue
            
            news['tags'] = [tag.text for tag in driver.find_elements(By.CSS_SELECTOR, ".eMeOeL")]
            news['source'] = link
            
            sentences = [str(sentence.text) for sentence in \
                driver.find_elements(By.CSS_SELECTOR, ".hXzioD > \
                .typography__StyledDynamicTypographyComponent-t787b7-0")]
            news['content'] =  ' '.join(sentences)    
                
            news_list.append(news)
            
        except:
            continue
    
    return news_list


def get_news_links(driver, url):
    """
    this function gets website url and returns fresh news links

    Args:
        driver (webdriver): chrome webdriver
        url (str): website url

    Returns:
        list: fresh news links
    """
    
    driver.get(url)
    
    # To get all fresh_news elements
    try:   
        elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, \
                ".link__CustomNextLink-sc-1r7l32j-0.eoKbWT.BrowseArticleListItemDesktop__WrapperLink-zb6c6m-6.bzMtyO")))
    
    except Exception as e:
        print('failed to get elements...')
        print(e)
    
    # To get all fresh_news links
    links = []
    for element in elements:
        link = element.get_attribute('href')
        if str(link).startswith('https://www.zoomit.ir/'):
            links.append(link)
    
    return links


app = Celery('tasks', broker="redis://redis:6379")

@app.task
def run():
    # define chrome options
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument('--disable-dev-shm-usage')
    
    # Install ChromeDriver using autoinstaller
    chromedriver_autoinstaller.install()
    
    # Step_1: get all fresh_news links  
    driver = webdriver.Chrome(options=chrome_options)
    url = "https://www.zoomit.ir/archive/?sort=Newest"
    links = get_news_links(driver, url)
    driver.close()
    
    # Step_2: scrape fresh_news
    driver = webdriver.Chrome(options=chrome_options)
    news_list = scrape_news_via_link(driver, links)
    driver.close()
    
    # Step_3: creating instance frome scraped data
    create_instance(news_list)
    print('Done!')
    

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
app.conf.beat_schedule = {
    "run-me-every-day": {
        "task": "tasks.run",
        # To run every day at 7 am
        "schedule": crontab(hour=7, minute=0)
    }
}
    
