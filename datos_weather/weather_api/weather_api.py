import requests
import pandas as pd
import os
import time
import logging
from tqdm.auto import tqdm
from dotenv import load_dotenv
from tenacity import retry, after_log, before_log, wait_fixed, stop_after_attempt
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utiles import ciudades, generar_mapa_estaciones, guardar_estaciones_y_atributos

# Logger para tenacity
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Parámetros de reintentos
max_tries = 3
wait_seconds = 1

@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.WARNING),
)
def hacer_request_con_reintentos(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

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
            data = hacer_request_con_reintentos(url)
        except Exception as e:
            print(f"❌ Error al procesar {city} tras varios intentos: {e}")
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

    lista_estaciones, atributos_clima_set = obtener_datos_weatherapi(API_KEY, base_path)

    guardar_estaciones_y_atributos(
        lista_estaciones=lista_estaciones,
        atributos_clima_set=atributos_clima_set,
        base_path=base_path,
        nombre_api="weatherapi" 
    )

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
