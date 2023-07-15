from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pandas as pd
import time
from datetime import datetime

opciones = Options()
opciones.add_experimental_option("detach", True)

servicio = Service(ChromeDriverManager().install())

driver = webdriver.Chrome(service=servicio,
                          options=opciones)

#url base
base_url = "https://collections.louvre.fr/en/recherche?page=1&limit=100&lt=list"
driver.get(base_url)
driver.maximize_window()
time.sleep(2)

article_count = int((driver.find_element(By.XPATH, '//*[@id="count_text"]').text).split(" ")[0])
page_count = int(driver.find_element(By.XPATH, '//*[@id="search__sorting"]/div[1]/form/span[2]').text)

catalogue_df = pd.DataFrame(columns=["article_url", "img_url","page"])

for page in range(1,140):
    page_url = f'https://collections.louvre.fr/en/recherche?page={page}&limit=100&lt=list"'
    driver.get(page_url)
    print(f'Scraping page {page}.')
    cards = driver.find_elements(By.XPATH, '//*[@id="search__grid"]/div')
    for card in cards:
        card_html = card.get_attribute("innerHTML")     
        article_url_part = card_html.split('href="')[1].split('" ')[0]
        article_img_url = card_html.split('src="')[1].split('" ')[0]
        catalogue_df.loc[len(catalogue_df)] = [article_url_part , article_img_url, page]
driver.quit()
catalogue_df['ark_id'] = catalogue_df["article_url"].str.split("/").str[3]
catalogue_df['article_id'] = catalogue_df["article_url"].str.split("/").str[4]

catalogue_df.to_excel(r"C:\Users\buong\SQLita\Louvre\main_catalogue.xlsx", index=False)

metadata_df = pd.read_excel(r"C:\Users\buong\SQLita\Louvre\metadata.xlsx")
metadata_df.loc[len(metadata_df)] = [datetime.now().strftime("%Y-%m-%d %H:%M:%S"),article_count,page_count,len(catalogue_df)]
metadata_df.to_excel('metadata.xlsx',index=False)