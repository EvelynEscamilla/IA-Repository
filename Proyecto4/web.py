from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from time import sleep

# Función para extraer información de la página usando Selenium
def extraer_info_pagina(url):
    try:
        # Configuración de Selenium para usar Chrome sin interfaz gráfica (headless)
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Ejecutar sin abrir la ventana del navegador
        chrome_options.add_argument("--disable-gpu")  # Desactivar el uso de la GPU
        
        # Iniciar el WebDriver para Chrome
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        
        # Abrir la página web
        driver.get(url)
        
        # Esperar un poco para que JavaScript cargue la página (ajusta el tiempo según sea necesario)
        sleep(3)
        
        # Obtener el contenido completo de la página
        html = driver.page_source
        
        # Usar BeautifulSoup para parsear el HTML y extraer solo el texto
        soup = BeautifulSoup(html, 'html.parser')
        
        # Extraer todo el texto sin etiquetas HTML
        texto_sin_etiquetas = soup.get_text(separator="\n", strip=True)
        
        # Cerrar el navegador
        driver.quit()
        
        return {'url': url, 'texto_sin_etiquetas': texto_sin_etiquetas}
    
    except Exception as e:
        return {'url': url, 'error': str(e)}

# Función para guardar la información en un archivo de texto
def guardar_en_txt(informacion, nombre_archivo='informacion_extraida.txt'):
    with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
        archivo.write(f"Información extraída de la URL: {informacion['url']}\n\n")
        archivo.write(f"Texto extraído sin etiquetas HTML:\n")
        archivo.write(f"{informacion['texto_sin_etiquetas']}\n\n")
        print(f"Información guardada en {nombre_archivo}")

# Función principal
def main():
    # Solicitar al usuario la URL de la página que desea extraer
    url = input("Introduce la URL de la página a extraer: ").strip()
    
    # Extraer la información de la página
    info_pagina = extraer_info_pagina(url)
    
    # Si ocurrió algún error, mostrarlo
    if 'error' in info_pagina:
        print(f"Error al extraer la información: {info_pagina['error']}")
    else:
        # Guardar la información en un archivo .txt
        guardar_en_txt(info_pagina)

if __name__ == '__main__':
    main()
