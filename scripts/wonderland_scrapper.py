import os
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from tqdm import tqdm

BASE = "https://wonderlandofficial.fandom.com/wiki/"
ASSET_BASE = "https://static.wikia.nocookie.net/wonderlandofficial/images/"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; Python download script)"
}

# Números que queremos bajar
numbers = [str(i) for i in range(0, 101)]  # 0 al 100

# Los archivos se guardarán en directorios por número

def fetch(url):
    r = requests.get(url, headers=HEADERS)
    return BeautifulSoup(r.text, "html.parser")

def extract_main_character_assets(soup, number):
    """Extrae solo los assets específicos: imagen 268px y audio latest"""
    assets = {'images': set(), 'audios': set()}
    
    # Buscar SOLO imágenes que contengan '268' en el nombre/URL
    for img in soup.find_all('img'):
        src = img.get('src') or img.get('data-src')
        if src and '268' in src and any(ext in src.lower() for ext in ['.png', '.jpg', '.jpeg', '.gif', '.webp']):
            if src.startswith('//'):
                src = 'https:' + src
            elif src.startswith('/'):
                src = 'https://static.wikia.nocookie.net' + src
            assets['images'].add(src)
            break  # Solo una imagen 268px
    
    # Buscar SOLO archivos de audio que contengan 'latest' en la URL
    for tag in soup.find_all(['a', 'audio']):
        href = tag.get('href') or tag.get('src')
        if href and 'latest' in href and any(ext in href.lower() for ext in ['.mp3', '.wav', '.ogg']):
            if href.startswith('//'):
                href = 'https:' + href
            elif href.startswith('/'):
                href = 'https://static.wikia.nocookie.net' + href
            assets['audios'].add(href)
    
    return assets

def get_direct_file_url_from_file_page(file_url):
    """
    Dada una URL de página File:, intenta extraer la URL directa del archivo
    """
    try:
        print(f"  Analizando: {file_url}")
        soup = fetch(file_url)
        
        # Buscar la imagen/audio/video real en la página File:
        # En Fandom, suele estar en un div con clase 'fullImageLink' o similar
        media_link = soup.find('div', class_='fullImageLink')
        if media_link:
            a_tag = media_link.find('a')
            if a_tag and a_tag.get('href'):
                direct_url = a_tag.get('href')
                if direct_url.startswith("//"):
                    direct_url = "https:" + direct_url
                print(f"  ✓ URL directa encontrada: {direct_url}")
                return direct_url
        
        # Buscar en elementos de audio/video
        audio_tag = soup.find('audio')
        if audio_tag and audio_tag.get('src'):
            direct_url = audio_tag.get('src')
            if direct_url.startswith("//"):
                direct_url = "https:" + direct_url
            print(f"  ✓ Audio encontrado: {direct_url}")
            return direct_url
            
        video_tag = soup.find('video')
        if video_tag and video_tag.get('src'):
            direct_url = video_tag.get('src')
            if direct_url.startswith("//"):
                direct_url = "https:" + direct_url
            print(f"  ✓ Video encontrado: {direct_url}")
            return direct_url
            
        # Buscar en cualquier enlace que contenga static.wikia
        for link in soup.find_all('a', href=True):
            href = link.get('href')
            if 'static.wikia' in href and any(ext in href.lower() for ext in ['.mp3', '.wav', '.ogg', '.png', '.jpg', '.jpeg', '.gif', '.webp']):
                if href.startswith("//"):
                    href = "https:" + href
                print(f"  ✓ Enlace static.wikia encontrado: {href}")
                return href
        
        # Buscar en atributos data-src o similar
        for img in soup.find_all('img'):
            for attr in ['data-src', 'data-image-key', 'src']:
                src = img.get(attr)
                if src and 'static.wikia' in src:
                    if src.startswith("//"):
                        src = "https:" + src
                    print(f"  ✓ Imagen encontrada en {attr}: {src}")
                    return src
                    
        print(f"  ✗ No se encontró URL directa en la página")
                
    except Exception as e:
        print(f"  ✗ Error extrayendo URL directa de {file_url}: {e}")
    
    return None

def download_file(url, number_folder, character_num=None):
    # intenta extraer un nombre de archivo
    name = url.split("/")[-1].split("?")[0]
    
    # Limpiar el nombre del archivo para evitar caracteres problemáticos
    name = re.sub(r'[^\w\-_\.]', '_', name)
    if not name or name == '_':
        name = "unknown_file"
    
    # Crear nombres más simples
    url_lower = url.lower()
    if any(ext in url_lower for ext in ['.png', '.jpg', '.jpeg', '.gif', '.webp']):
        name = f"image.png"  # Imagen principal
    elif any(ext in url_lower for ext in ['.mp3', '.wav', '.ogg']):
        # Determinar extensión de audio
        ext = '.mp3' if '.mp3' in url_lower else ('.wav' if '.wav' in url_lower else '.ogg')
        name = f"audio{ext}"  # Audio principal
    
    # Crear directorio para el número si no existe
    os.makedirs(number_folder, exist_ok=True)
    path = os.path.join(number_folder, name)

    if os.path.exists(path):
        print(f"⏭ Ya existe: {os.path.basename(number_folder)}/{name}")
        return

    try:
        print(f"Descargando: {os.path.basename(number_folder)}/{name}")
        r = requests.get(url, headers=HEADERS, stream=True)
        r.raise_for_status()  # Lanza excepción si hay error HTTP
        
        with open(path, "wb") as f:
            for chunk in r.iter_content(1024):
                f.write(chunk)
                
        print(f"✓ Descargado: {os.path.basename(number_folder)}/{name}")
    except Exception as e:
        print(f"✗ Error descargando {url} -> {e}")

# Crear directorio base
BASE_OUTPUT = "wonderland_assets"
os.makedirs(BASE_OUTPUT, exist_ok=True)

# Recorremos los números
for n in tqdm(numbers, desc="Procesando números"):
    page_url = BASE + "Number_" + n
    number_folder = os.path.join(BASE_OUTPUT, f"Number_{n}")
    print(f"\n--- Procesando Number {n} ---")
    soup = fetch(page_url)

    # Extraer assets específicos del personaje
    character_assets = extract_main_character_assets(soup, n)
    
    # También buscar páginas File: que contengan 'latest'
    file_links = set()
    for tag in soup.find_all(["a"], href=True):
        href = tag.get("href")
        if "File:" in href and 'latest' in href:
            file_links.add(href)
    
    print(f"Encontradas {len(character_assets['images'])} imágenes 268px, {len(character_assets['audios'])} audios latest, {len(file_links)} páginas File: con 'latest'")

    # Descargar imagen principal (solo si contiene '268')
    for img_url in character_assets['images']:
        download_file(img_url, number_folder, n)
    
    # Descargar audio principal (solo si contiene 'latest')
    for audio_url in character_assets['audios']:
        download_file(audio_url, number_folder, n)

    # Procesar páginas File: que contengan 'latest' para obtener URLs directas
    for file_link in file_links:
        if file_link.startswith("//"):
            file_url = "https:" + file_link
        elif file_link.startswith("/"):
            file_url = "https://wonderlandofficial.fandom.com" + file_link
        else:
            file_url = urljoin(page_url, file_link)
            
        print(f"Procesando página File: {os.path.basename(file_link)}")
        direct_url = get_direct_file_url_from_file_page(file_url)
        
        if direct_url and 'latest' in direct_url:
            if direct_url.startswith("//"):
                direct_url = "https:" + direct_url
            download_file(direct_url, number_folder, n)
        else:
            print(f"  → No se encontró URL 'latest' válida")

print("\n¡Descarga completada!")
