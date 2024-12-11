from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from time import sleep
import json

def extraer_info_pagina(url):
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")  
        chrome_options.add_argument("--disable-gpu")
        
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        
        driver.get(url)
        
        sleep(3)
        
        html = driver.page_source
        
        soup = BeautifulSoup(html, 'html.parser')
        
        texto_sin_etiquetas = soup.get_text(separator="\n", strip=True)
        
        driver.quit()
        
        return {'url': url, 'texto_sin_etiquetas': texto_sin_etiquetas}
    
    except Exception as e:
        return {'url': url, 'error': str(e)}

def guardar_en_txt(informacion, nombre_archivo):
    with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
        archivo.write(f"Información extraída de la URL: {informacion['url']}\n\n")
        archivo.write(f"Texto extraído sin etiquetas HTML:\n")
        archivo.write(f"{informacion['texto_sin_etiquetas']}\n\n")
        print(f"Información guardada en {nombre_archivo}")

def main():
    try:
        with open('enlaces_reforma_judicial.json', 'r', encoding='utf-8') as f:
            links = json.load(f)
    except FileNotFoundError:
        print("No se encontraron enlaces guardados.")
        return

    if not links:
        print("No se encontraron enlaces.")
        return
    
    for idx, link in enumerate(links, 1):
        info_pagina = extraer_info_pagina(link)
        if 'error' in info_pagina:
            print(f"Error al extraer la información de {link}: {info_pagina['error']}")
        else:
            archivo_txt = f'informacion_extraida_{idx}.txt' 
            guardar_en_txt(info_pagina, archivo_txt)

if __name__ == '__main__':
    main()
