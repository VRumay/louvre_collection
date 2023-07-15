import bs4
import pandas as pd
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
from datetime import datetime

def reemplazar_palabra(texto, nueva_palabra, palabra_anterior, palabra_posterior):
    # Buscar la posición de la palabra anterior y posterior
    pos_anterior = texto.find(palabra_anterior)
    pos_posterior = texto.find(palabra_posterior, pos_anterior + len(palabra_anterior))
    
    # Reemplazar la palabra
    if pos_anterior != -1 and pos_posterior != -1:
        pos_inicial = pos_anterior + len(palabra_anterior)
        pos_final = pos_posterior
        texto_reemplazado = texto[:pos_inicial] + nueva_palabra + texto[pos_final:]
        return texto_reemplazado
    else:
        return texto
    
catalogue = int(input("Cual catalogo quieres usar?: "))
catalogue_df = pd.read_excel(fr"C:\Users\buong\SQLita\Louvre\catalogues\catalogue-{catalogue}.xlsx")
urls = catalogue_df["article_url"].to_list()

inventory_df = pd.DataFrame(columns=["article_url","inner_html"])
counter = 0
start = datetime.now()
for url in urls:
    counter += 1
    print(counter)
    full_url = f"https://collections.louvre.fr{url}"
    try:
        website = urlopen(full_url)
        html = website.read()
        page_soup = soup(html, "html.parser")

        try:        
            inner_html = page_soup.find("div", {"class": "m-10col is-centered notice__fullcartel__inner"})
        except: 
            inner_html = "Inner HTML error"
    except:
        inner_html = "URL Link error"
    
    inner_html=str(inner_html).replace(""," ")
    inner_html=str(inner_html).replace(""," ")
    inventory_df.loc[len(inventory_df)] = [url, inner_html]
end = datetime.now()
print(end-start, (end-start)/15)
inventory_df.to_excel(fr"C:\Users\buong\SQLita\Louvre\inventories\inventory-{catalogue}.xlsx",index=False)



    

