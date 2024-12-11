import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urlparse, parse_qs

def obtener_links_reforma_judicial():
    url = 'https://www.google.com/search?q=reforma+judicial+México+2024'
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("Error al hacer la solicitud, estado:", response.status_code)
        return []
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    links = []
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        
        if '/url?' in href:
            parsed_url = urlparse(href)
            params = parse_qs(parsed_url.query)
            actual_url = params.get('url', [None])[0]
            
            if actual_url:
                links.append(actual_url)
    
    if links:
        with open('enlaces_reforma_judicial.json', 'w', encoding='utf-8') as f:
            json.dump(links, f, ensure_ascii=False, indent=4)
        print(f"Se han guardado {len(links)} enlaces en 'enlaces_reforma_judicial.json'")
    else:
        print("No se encontraron enlaces.")
    
    return links

obtener_links_reforma_judicial()
