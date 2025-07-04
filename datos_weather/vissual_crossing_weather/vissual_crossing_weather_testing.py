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

# Parámetros para reintentos
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

def obtener_datos_visualcrossing(api_key, base_path):
    """
    Consulta la API de Visual Crossing para las ciudades definidas y guarda la info de estaciones y atributos.
    """
    lista_estaciones = []
    atributos_clima_set = set()

    for city_raw in tqdm(ciudades, desc="Consultando ciudades"):
        city = f"{city_raw},AR"
        print(f"Procesando {city_raw}...")

        url = (
            f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/"
            f"{city}?unitGroup=metric&key={api_key}&include=days"
        )

        try:
            data = hacer_request_con_reintentos(url)
        except Exception as e:
            print(f"❌ Error al procesar {city_raw} tras varios intentos: {e}")
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

    return lista_estaciones, atributos_clima_set

def main():
    load_dotenv()
    API_KEY = os.getenv('api_key_vissual_crossing')
    base_path = os.path.dirname(os.path.abspath(__file__))

    lista_estaciones, atributos_clima_set = obtener_datos_visualcrossing(API_KEY, base_path)

    guardar_estaciones_y_atributos(
        lista_estaciones=lista_estaciones,
        atributos_clima_set=atributos_clima_set,
        base_path=base_path,
        nombre_api="visualcrossing"
    )

    df_est = pd.DataFrame(lista_estaciones)
    generar_mapa_estaciones(
        df=df_est,
        nombre_archivo_html="mapa_visualcrossing.html",
        base_path=base_path,
        lat_col='latitude',
        lon_col='longitude',
        nombre_col='name'
    )

if __name__ == "__main__":
    main()
