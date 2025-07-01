import requests
import pandas as pd
import folium
import os
import time
from dotenv import load_dotenv
import sys

# Añadir el path del directorio padre de 'datos_weather' al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utiles import ciudades
from utiles import generar_mapa_estaciones

load_dotenv()  # Carga variables desde el archivo .env

API_KEY = os.getenv('api_key_vissual_crossing')

base_path = os.path.dirname(os.path.abspath(__file__))


# Variables para datos de estaciones y atributos
lista_estaciones = []
atributos_clima_set = set()

# Recorrer cada ciudad
for city_raw in ciudades:
    city = f"{city_raw},AR"
    print(f"Procesando {city_raw}...")
    
    url = (
        f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/"
        f"{city}?unitGroup=metric&key={API_KEY}&include=days"
    )
    
    try:
        r = requests.get(url)
        r.raise_for_status()
        data = r.json()
    except Exception as e:
        print(f"❌ Error al procesar {city_raw}: {e}")
        continue

    lat = data.get('latitude') 
    lon = data.get('longitude')
    days = data.get('days', [])
    has_daily = bool(days)

    if has_daily:
        primer_dia = days[0]
        atributos_clima_set.update(primer_dia.keys())

    lista_estaciones.append({
        'name': city_raw,
        'latitude': lat,
        'longitude': lon,
        'has_daily_data': has_daily
    })

    time.sleep(0.8)

# Guardar estaciones en CSV
df_est = pd.DataFrame(lista_estaciones)
ruta_est = os.path.join(base_path, "visualcrossing_estaciones_argentina.csv")
df_est.to_csv(ruta_est, index=False, encoding='utf-8')
print(f"CSV de estaciones guardado en: {ruta_est}")

# Guardar atributos climáticos en CSV (un atributo por fila)
df_attr = pd.DataFrame(sorted(atributos_clima_set), columns=['atributo'])
ruta_attr = os.path.join(base_path, "visualcrossing_atributos_clima.csv")
df_attr.to_csv(ruta_attr, index=False, encoding='utf-8')
print(f"CSV de atributos climáticos guardado en: {ruta_attr}")

# Crear mapa folium con todas las ciudades
generar_mapa_estaciones(
    df=df_est,
    nombre_archivo_html="mapa_visualcrossing.html",
    base_path=base_path,  
    lat_col='latitude',
    lon_col='longitude',
    nombre_col='name'
)