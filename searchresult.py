import csv
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common import exceptions
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common import exceptions

def create_webdriver_instance():
    options = Options()
    options.headless = False
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    return driver

def search_query(driver, search):
    driver.get('https://www.google.com')
    sleep(5)
    try:
        driver.find_element(By.XPATH, ".//input[@title='Search']").send_keys(search)
        driver.find_element(By.XPATH, ".//input[@title='Search']").send_keys(Keys.RETURN)
    except exceptions.NoSuchElementException:
        print("Webpage failed to load properly")
        return 1
    except exceptions.StaleElementReferenceException:
        return 1
    else:
        return 0

def scrape_results(driver):
    sleep(30)
    try:
        search_result = driver.find_elements(By.XPATH, ".//div[@class='MjjYud']")
    except exceptions.NoSuchElementException:
        print("No Element Found")
        return 
    except exceptions.StaleElementReferenceException:
        return
    else:
        return search_result 

def header_links(search_result):
    try:
        search = search_result.find_element(By.XPATH, ".//div[@class='yuRUbf']")
        link = search.find_element(By.TAG_NAME, 'a').get_attribute('href')
        heading = search.find_element(By.TAG_NAME, 'h3').text
    except exceptions.NoSuchElementException:
        print("Links No Element Found")
        link = "None"
        heading = "None"
        return link , heading
    except exceptions.StaleElementReferenceException:
        print("Links No Element Found")
        link = "None"
        heading = "None"
        return link , heading
    else:
        return link , heading

    
def description(search_result):
    description = ""
    try:
        desc = search_result.find_element(By.XPATH, ".//div[@data-content-feature='1']")
        description_span =  desc.find_elements(By.TAG_NAME, 'span')
        print(len(description_span))
        for i in range(len(description_span)):
            description += description_span[i].text 
    except exceptions.NoSuchElementException:
        print("Description No Element Found")
        description = "None"
        return description
    except exceptions.StaleElementReferenceException:
        print("Description No Element Found")
        description = "None"
        return description
    else:
        return description

def save_data_to_csv(head_link, heading, desc, filepath):
    data = []
    data.append(head_link)
    data.append(heading)
    data.append(desc)
    with open(filepath, 'a+', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(data)

def next_page(driver):
    try:
        table = driver.find_element(By.TAG_NAME, 'table')
        next_page = table.find_element(By.ID, 'pnnext').send_keys(Keys.RETURN)
    except exceptions.NoSuchElementException:
        next_page = "None"
        return next_page
    except exceptions.StaleElementReferenceException:
        next_page = "None"
        return next_page 

def main(filepath):
    driver = create_webdriver_instance()
    search = "site:twitter.com #kashmir"
    next = "1"
    search_flag = search_query(driver, search)

    while next != "None":
        if search_flag != 1:
            search_results = scrape_results(driver)
            print(len(search_results))
            for search_result in search_results:
                head_link , heading = header_links(search_result)
                desc = description(search_result)
                print(head_link)
                print(heading)
                print(desc)
                if (head_link != "None" and heading != "None" and desc != "None" ):
                    save_data_to_csv(head_link, heading, desc, filepath)
            next = next_page(driver)
        sleep(30)
    
    driver.close()
         

if __name__ == '__main__':
    path = 'GoogleResult.csv'
    
    main(path)