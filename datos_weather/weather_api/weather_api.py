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

API_KEY = os.getenv('api_key_weather_api')

base_path = os.path.dirname(os.path.abspath(__file__))


lista_estaciones = []
atributos_clima_set = set()

for city in ciudades:
    print(f"Procesando {city}...")
    # Consultar historial de un día cualquiera 
    url = (
        f"http://api.weatherapi.com/v1/history.json?"
        f"key={API_KEY}&q={city},Argentina&dt=2025-06-15"
    )
    r = requests.get(url)
    data = r.json()
    
    loc = data.get('location', {})
    forecast = data.get('forecast', {})
    forecast_day = forecast.get('forecastday', [])
    
    # Registrar estaciones por ciudad
    lista_estaciones.append({
        'name': city,
        'latitude': loc.get('lat'),
        'longitude': loc.get('lon'),
        'has_daily_history': bool(forecast_day)
    })
    
    # Extraer atributos climáticos
    if forecast_day:
        # Tomamos el primer día
        ky = forecast_day[0].get('day', {})
        atributos_clima_set.update(ky.keys())
    
    time.sleep(1)

# Guardar estaciones
df_est = pd.DataFrame(lista_estaciones)
ruta_est = os.path.join(base_path, "weatherapi_estaciones_argentina.csv")
df_est.to_csv(ruta_est, index=False, encoding='utf-8')

# Guardar atributos
df_attr = pd.DataFrame(sorted(atributos_clima_set), columns=['atributo'])
ruta_attr = os.path.join(base_path, "weatherapi_atributos_clima.csv")
df_attr.to_csv(ruta_attr, index=False, encoding='utf-8')

print(f"CSV estaciones guardado en: {ruta_est}")
print(f"CSV atributos guardado en: {ruta_attr}")

# Crear mapa
generar_mapa_estaciones(
    df=df_est,
    nombre_archivo_html="mapa_weatherapi.html",
    base_path=base_path,
    lat_col='latitude',
    lon_col='longitude',
    nombre_col='name'
)