#!/usr/bin/env python3
import json
import os

def create_wonderland_js():
    """Crear archivo JS con los datos de Wonderland"""
    
    # Leer el JSON de datos
    with open('wonderland_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Convertir a formato JS
    js_numbers = []
    
    for number_key, number_data in data.items():
        number_id = int(number_key.replace('Number_', ''))
        
        # Determinar archivo de audio (preferir mp3, luego wav, luego mp4)
        audio_file = None
        if number_data['audio_nombre']:
            audio_file = number_data['audio_nombre']
        elif number_data['audio_saludo']:
            audio_file = number_data['audio_saludo']
        
        # Detectar extensión real del archivo de audio
        if audio_file:
            # Verificar que el archivo existe
            if os.path.exists(audio_file):
                js_numbers.append({
                    'id': number_id,
                    'image': number_data['imagen'],
                    'audio': audio_file
                })
            else:
                # Buscar archivo de audio alternativo
                number_dir = f"wonderland_assets/Number_{number_id}"
                audio_found = None
                
                for ext in ['.mp3', '.wav', '.mp4']:
                    test_file = f"{number_dir}/audio{ext}"
                    if os.path.exists(test_file):
                        audio_found = test_file
                        break
                
                js_numbers.append({
                    'id': number_id,
                    'image': number_data['imagen'],
                    'audio': audio_found
                })
        else:
            js_numbers.append({
                'id': number_id,
                'image': number_data['imagen'],
                'audio': None
            })
    
    # Generar código JavaScript
    js_content = f"""// Datos de Wonderland generados automáticamente
const wonderlandNumbers = {json.dumps(js_numbers, indent=2)};

// Verificar que tenemos todos los números
console.log(`Cargados ${json.dumps(len(js_numbers))} números de Wonderland`);
"""
    
    # Escribir archivo
    with open('wonderland_data.js', 'w', encoding='utf-8') as f:
        f.write(js_content)
    
    print(f"✅ Archivo wonderland_data.js creado con {len(js_numbers)} números")
    
    # Estadísticas
    with_images = sum(1 for n in js_numbers if n['image'])
    with_audio = sum(1 for n in js_numbers if n['audio'])
    
    print(f"📊 Estadísticas:")
    print(f"   Con imagen: {with_images}")
    print(f"   Con audio: {with_audio}")

if __name__ == "__main__":
    create_wonderland_js()