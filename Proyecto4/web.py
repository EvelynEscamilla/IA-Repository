from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from time import sleep

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

def guardar_en_txt(informacion, nombre_archivo='informacion_extraida.txt'):
    with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
        archivo.write(f"Información extraída de la URL: {informacion['url']}\n\n")
        archivo.write(f"Texto extraído sin etiquetas HTML:\n")
        archivo.write(f"{informacion['texto_sin_etiquetas']}\n\n")
        print(f"Información guardada en {nombre_archivo}")

def main():
    url = input("Introduce la URL de la página a extraer: ").strip()
    info_pagina = extraer_info_pagina(url)
    if 'error' in info_pagina:
        print(f"Error al extraer la información: {info_pagina['error']}")
    else:
        guardar_en_txt(info_pagina)

if __name__ == '__main__':
    main()
