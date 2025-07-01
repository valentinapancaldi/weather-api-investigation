import requests
import pandas as pd
import os
import time
from tqdm.auto import tqdm
from dotenv import load_dotenv
import sys

# Añadir el path del directorio padre de 'datos_weather' al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utiles import ciudades, generar_mapa_estaciones, guardar_estaciones_y_atributos

def obtener_datos_weatherapi(api_key, base_path):
    """
    Consulta la API de WeatherAPI para las ciudades definidas y guarda info de estaciones y atributos.
    """
    lista_estaciones = []
    atributos_clima_set = set()

    for city in tqdm(ciudades, desc="Consultando ciudades"):
        print(f"Procesando {city}...")
        
        url = (
            f"http://api.weatherapi.com/v1/history.json?"
            f"key={api_key}&q={city},Argentina&dt=2025-06-15"
        )

        try:
            r = requests.get(url)
            r.raise_for_status()
            data = r.json()
        except Exception as e:
            print(f"❌ Error al procesar {city}: {e}")
            continue

        loc = data.get('location', {})
        forecast = data.get('forecast', {})
        forecast_day = forecast.get('forecastday', [])

        lista_estaciones.append({
            'name': city,
            'latitude': loc.get('lat'),
            'longitude': loc.get('lon'),
            'has_daily_history': bool(forecast_day)
        })

        if forecast_day:
            primer_dia = forecast_day[0].get('day', {})
            atributos_clima_set.update(primer_dia.keys())

        time.sleep(1)

    return lista_estaciones, atributos_clima_set

def main():
    load_dotenv()
    API_KEY = os.getenv('api_key_weather_api')
    base_path = os.path.dirname(os.path.abspath(__file__))

    # Obtener datos
    lista_estaciones, atributos_clima_set = obtener_datos_weatherapi(API_KEY, base_path)

    # Guardar CSVs
    guardar_estaciones_y_atributos(
        lista_estaciones=lista_estaciones,
        atributos_clima_set=atributos_clima_set,
        base_path=base_path,
        nombre_api="weatherapi" 
    )

    # Crear mapa
    df_est = pd.DataFrame(lista_estaciones)
    generar_mapa_estaciones(
        df=df_est,
        nombre_archivo_html="mapa_weatherapi.html",
        base_path=base_path,
        lat_col='latitude',
        lon_col='longitude',
        nombre_col='name'
    )

if __name__ == "__main__":
    main()
