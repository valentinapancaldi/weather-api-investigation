Comparación de APIs de datos climáticos para proyectos de análisis

Objetivo del proyecto
Este proyecto tiene como finalidad evaluar y comparar distintas APIs de datos climáticos para determinar cuál es más conveniente utilizar en un análisis futuro.
Se consideran los siguientes criterios:

- Atributos climáticos disponibles
- Disponibilidad de datos históricos
- Capacidades de pronóstico (forecasting)
- Facilidad de uso e integración 
- Precio y planes gratuitos (cantidad de llamadas mensuales permitidas)


APIs evaluadas
Hasta el momento, el análisis incluye:

- Meteostat
- WeatherAPI
- Visual Crossing Weather


Archivos generados
Para cada API, se generan los siguientes archivos dentro de una subcarpeta específica del directorio datos_weather:

*_estaciones_argentina.csv: listado de estaciones meteorológicas en Argentina con nombre, latitud, longitud y si tienen datos diarios disponibles.

*_atributos_clima.csv: listado de atributos climáticos ofrecidos por la API en los datos diarios.

mapa_*.html: mapa interactivo con la ubicación de las estaciones en Argentina usando Folium.

    
API Keys necesarias y configuración de variables de entorno

Para acceder a los datos de WeatherAPI y Visual Crossing Weather, necesitás una clave de API (API key). Para proteger estas claves y evitar subirlas a GitHub, se deben definir en un archivo .env en la raíz del proyecto. Este archivo no se sube al repositorio y contiene tus claves reales.

Se incluye un archivo .env.example con la estructura y nombres de las variables necesarias para que puedas crear tu propio .env con tus claves.

WeatherAPI

1. Crear una cuenta gratuita en https://www.weatherapi.com/
2. Ir a la sección "API Keys" en el panel de usuario.
3. Copiar la clave generada y reemplazar en el código Python donde dice API_KEY = '--'.

Visual Crossing Weather

1. Registrarse en https://www.visualcrossing.com/weather-api
2. Desde el panel de usuario, copiar tu API key gratuita.
3. Reemplazar en el código donde se indica API_KEY = '--'.
   
Meteostat no requiere clave de API si se utiliza la librería oficial de Python (pip install meteostat).
Si se accede vía la API REST (en formato JSON), sí existen límites mensuales y se requiere registro.

Pasos para configurar el archivo .env
1. Copiá el archivo .env.example y renombralo a .env
2. Reemplazá los valores de ejemplo por tus propias API keys

Dependencias necesarias
Para poder ejecutar los scripts y generar los resultados, es necesario tener instaladas las siguientes librerías de Python:

- requests
- pandas
- folium
- meteostat
- numpy
- python-dotenv
- temacity
- tqdm
