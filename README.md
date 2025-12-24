# 🎯 Wonderland - Juegos Educativos para Juani

Una aplicación web educativa con 101 personajes de Wonderland para aprender números de forma interactiva.

🌐 **Demo en vivo**: [https://jeanbenitezu.github.io/wonderland-juani](https://jeanbenitezu.github.io/wonderland-juani)

📱 **PWA**: Se puede instalar como app nativa desde cualquier navegador moderno.

## 📁 Estructura del Proyecto

```
wonderland/
├── index.html               # Página principal con navegación
├── memory_game.html         # Juego de memoria (4 dificultades)
├── gallery.html             # Galería con búsqueda
├── favorite.html            # Selección de números favoritos
├── about.html               # Información de la aplicación
├── manifest.json            # Configuración PWA
├── sw.js                    # Service Worker para offline
├── data/                    # Datos de los personajes
│   ├── wonderland_data.js   # Datos en formato JavaScript
│   └── wonderland_data.json # Datos en formato JSON
├── assets/                  # Recursos multimedia
│   └── wonderland_assets/   # Imágenes y audio de 101 números
├── scripts/                 # Scripts de Python
│   ├── wonderland_scrapper.py
│   ├── create_js_data.py
│   └── generate_json.py
├── .venv/                   # Entorno virtual Python
└── package.json             # Configuración del proyecto
```

## 🚀 Inicio Rápido

### 📱 **Jugar online (GitHub Pages)**
1. Ve a: `https://TU-USUARIO.github.io/wonderland`
2. **Instalar como PWA**: 
   - **Móvil/Tablet**: Menú → "Instalar aplicación" o "Añadir a inicio"
   - **Desktop**: Icono de instalación en la barra de direcciones

### 💻 **Desarrollo local**
```bash
# Clonar repositorio
git clone https://github.com/TU-USUARIO/wonderland.git
cd wonderland

# Iniciar servidor local
python -m http.server 8000

# Abrir en navegador
open http://localhost:8000
```

### 🐍 **Generar datos (opcional)**
```bash
# Activar entorno virtual
source .venv/bin/activate

# Ejecutar web scraper
cd scripts && python wonderland_scrapper.py

# Generar archivos de datos
python create_js_data.py
python generate_json.py
```

## 🎮 Características

- **🧠 Juego de Memoria**: 4 niveles de dificultad (4, 6, 8, 12 cartas)
- **🖼️ Galería Interactiva**: Búsqueda y navegación por 101 números
- **⭐ Números Favoritos**: Sistema de persistencia local
- **🔊 Audio Pronunciación**: Sonido para cada número
- **📱 PWA**: Funciona offline una vez instalado
- **📐 Responsive**: Optimizado para tablets y móviles

## 🛠️ Tecnologías

- **Frontend**: HTML5, CSS3, JavaScript vanilla
- **PWA**: Service Worker, Web App Manifest
- **Backend**: Python (web scraping)
- **Assets**: 101 imágenes PNG + archivos de audio MP3/WAV

## 📋 Comandos Disponibles

```bash
npm run start          # Iniciar servidor de desarrollo
npm run build          # Copiar archivos a dist/
npm run scrape         # Ejecutar web scraper
npm run generate-data  # Generar archivos de datos
```

## 🎯 Optimizado para Juan Ignacio

Esta aplicación está especialmente diseñada para el aprendizaje de números en tablets, con:
- Fuentes grandes y legibles
- Interfaz táctil amigable
- Colores atractivos y animaciones suaves
- Sin distracciones innecesarias

## 📄 Licencia

MIT - Libre para uso educativo y personal.# wonderland-juani
