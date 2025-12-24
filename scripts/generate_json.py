#!/usr/bin/env python3
import os
import json
from pathlib import Path

def get_file_size(file_path):
    """Obtiene el tamaño de un archivo en bytes"""
    try:
        return os.path.getsize(file_path)
    except:
        return 0

def analyze_wonderland_assets():
    """Analiza todos los directorios Number_X y genera el JSON"""
    base_dir = Path("wonderland_assets")
    result = {}
    
    for number in range(0, 101):  # 0 a 100
        number_dir = base_dir / f"Number_{number}"
        
        if not number_dir.exists():
            print(f"Advertencia: Directorio {number_dir} no encontrado")
            continue
            
        # Inicializar entrada para este número
        entry = {
            "imagen": None,
            "audio_nombre": None,
            "audio_saludo": None
        }
        
        # Buscar archivos en el directorio
        image_file = None
        audio_files = []
        
        for file_path in number_dir.iterdir():
            if file_path.is_file():
                if file_path.name == "image.png":
                    image_file = file_path
                elif file_path.name.startswith("audio."):
                    audio_files.append(file_path)
        
        # Establecer path de imagen
        if image_file:
            entry["imagen"] = str(image_file)
        
        # Analizar audios por tamaño
        if len(audio_files) >= 2:
            # Obtener tamaños de archivos
            audio_sizes = [(f, get_file_size(f)) for f in audio_files]
            audio_sizes.sort(key=lambda x: x[1])  # Ordenar por tamaño
            
            # El más pequeño es el nombre, el más grande es el saludo
            entry["audio_nombre"] = str(audio_sizes[0][0])  # Más pequeño
            entry["audio_saludo"] = str(audio_sizes[-1][0])  # Más grande
            
        elif len(audio_files) == 1:
            # Solo hay un audio, asumimos que es el nombre
            entry["audio_nombre"] = str(audio_files[0])
            entry["audio_saludo"] = None
            
        # Añadir al resultado
        result[f"Number_{number}"] = entry
        
        print(f"✓ Procesado Number_{number}: "
              f"imagen={'✓' if entry['imagen'] else '✗'}, "
              f"audios={len(audio_files)}")
    
    return result

def main():
    print("Analizando archivos descargados...")
    data = analyze_wonderland_assets()
    
    # Guardar JSON
    output_file = "wonderland_data.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Archivo JSON generado: {output_file}")
    
    # Mostrar estadísticas
    total_numbers = len(data)
    with_images = sum(1 for entry in data.values() if entry['imagen'])
    with_nombre = sum(1 for entry in data.values() if entry['audio_nombre'])
    with_saludo = sum(1 for entry in data.values() if entry['audio_saludo'])
    
    print(f"\n📊 Estadísticas:")
    print(f"   Total números: {total_numbers}")
    print(f"   Con imagen: {with_images}")
    print(f"   Con audio nombre: {with_nombre}")
    print(f"   Con audio saludo: {with_saludo}")

if __name__ == "__main__":
    main()