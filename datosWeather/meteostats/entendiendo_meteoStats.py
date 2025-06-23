import pandas as pd
import numpy as np
from meteostat import Stations, Daily, Hourly
from datetime import datetime, timedelta
import time
import folium  
import os

def check_station_data_availability(station_id, station_name, max_retries=2):
    """
    Verifica la disponibilidad de datos diarios y horarios para una estación específica
    """
    print(f"Verificando estación: {station_name} (ID: {station_id})")
    
    # Definir período de prueba (último mes para no sobrecargar)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    
    results = {
        'station_id': station_id,
        'station_name': station_name,
        'daily_available': False,
        'daily_records': 0,
        'daily_has_coco': False,
        'daily_coco_count': 0,
        'daily_error': None,
        'hourly_available': False,
        'hourly_records': 0,
        'hourly_has_coco': False,
        'hourly_coco_count': 0,
        'hourly_error': None,
        'last_daily_date': None,
        'last_hourly_date': None
    }
    
    # Verificar datos DIARIOS
    for attempt in range(max_retries):
        try:
            daily_data = Daily(station_id, start_date, end_date)
            daily_df = daily_data.fetch()
            
            if not daily_df.empty:
                results['daily_available'] = True
                results['daily_records'] = len(daily_df)
                results['last_daily_date'] = daily_df.index.max().strftime('%Y-%m-%d')
                
                # Verificar COCO en datos diarios
                if 'coco' in daily_df.columns:
                    results['daily_has_coco'] = True
                    results['daily_coco_count'] = daily_df['coco'].count()
                
                print(f"  ✓ Datos diarios: {results['daily_records']} registros (último: {results['last_daily_date']})")
                if results['daily_has_coco']:
                    print(f"    ✓ COCO diarios: {results['daily_coco_count']} registros")
            else:
                print(f"  ✗ Sin datos diarios")
            
            break 
            
        except Exception as e:
            if attempt == max_retries - 1:  # Último intento
                results['daily_error'] = str(e)
                print(f"  ✗ Error en datos diarios: {e}")
            else:
                time.sleep(1)  # Esperar antes del siguiente intento
    
    # Verificar datos HORARIOS 
    hourly_start = end_date - timedelta(days=30)  
    
    for attempt in range(max_retries):
        try:
            hourly_data = Hourly(station_id, hourly_start, end_date)
            hourly_df = hourly_data.fetch()
            
            if not hourly_df.empty:
                results['hourly_available'] = True
                results['hourly_records'] = len(hourly_df)
                results['last_hourly_date'] = hourly_df.index.max().strftime('%Y-%m-%d %H:%M')
                
                # Verificar COCO en datos horarios
                if 'coco' in hourly_df.columns:
                    results['hourly_has_coco'] = True
                    results['hourly_coco_count'] = hourly_df['coco'].count()
                
                print(f"  ✓ Datos horarios: {results['hourly_records']} registros (último: {results['last_hourly_date']})")
                if results['hourly_has_coco']:
                    print(f"    ✓ COCO horarios: {results['hourly_coco_count']} registros")
            else:
                print(f"  ✗ Sin datos horarios")
            
            break  
            
        except Exception as e:
            if attempt == max_retries - 1:  # Último intento
                results['hourly_error'] = str(e)
                print(f"  ✗ Error en datos horarios: {e}")
            else:
                time.sleep(1)  # Esperar antes del siguiente intento
    
    # Pequeña pausa entre estaciones para no sobrecargar la API
    time.sleep(0.3)
    
    return results

def get_argentina_stations():
    """
    Obtiene todas las estaciones meteorológicas de Argentina
    """
    print("Buscando estaciones meteorológicas en Argentina...")
    
    try:
        # Buscar estaciones en Argentina
        stations = Stations()
        stations_df = stations.fetch()
        stations_df = stations_df[stations_df['country'] == 'AR']
        print(f"Encontradas {len(stations_df)} estaciones en Argentina")
        
        return stations_df
    
    except Exception as e:
        print(f"Error buscando estaciones: {e}")
        return pd.DataFrame()

def create_argentina_stations_report():
    """
    Crea un reporte completo de todas las estaciones de Argentina
    """
    print("="*60)
    print("MAPEADOR DE ESTACIONES METEOROLÓGICAS DE ARGENTINA")
    print("="*60)
    
    # Obtener estaciones
    stations_df = get_argentina_stations()
    
    if stations_df.empty:
        print("No se pudieron obtener estaciones de Argentina")
        return
    
    print(f"\nIniciando verificación de {len(stations_df)} estaciones...")
    
    # Lista para almacenar resultados
    all_results = []
    
    # Procesar cada estación
    for i, (station_id, station_info) in enumerate(stations_df.iterrows(), 1):
        print(f"\n[{i}/{len(stations_df)}] ", end="")
        
        # Obtener información básica de la estación
        station_result = {
            'station_id': station_id,
            'station_name': station_info.get('name', 'Sin nombre'),
            'region': station_info.get('region', 'Sin región'),
            'latitude': station_info.get('latitude', None),
            'longitude': station_info.get('longitude', None),
            'elevation': station_info.get('elevation', None),
            'country': station_info.get('country', 'AR'),
        }
        
        # Verificar disponibilidad de datos
        data_availability = check_station_data_availability(station_id, station_result['station_name'])
        
        # Combinar información básica con disponibilidad de datos
        station_result.update(data_availability)
        
        all_results.append(station_result)
        
    # Crear DataFrame final
    final_df = pd.DataFrame(all_results)

    base_path = os.path.dirname(os.path.abspath(__file__))
    
    csv_path = os.path.join(base_path, "meteostats_estaciones_argentina.csv")
    final_df.to_csv(csv_path, index=False)

    # Crear resumen
    print(f"\n{'='*60}")
    print("RESUMEN DE RESULTADOS")
    print(f"{'='*60}")
    
    print(f"Total de estaciones analizadas: {len(final_df)}")
    
    # Estadísticas de disponibilidad
    daily_available = final_df['daily_available'].sum()
    hourly_available = final_df['hourly_available'].sum()
    daily_with_coco = final_df['daily_has_coco'].sum()
    hourly_with_coco = final_df['hourly_has_coco'].sum()
    
    print(f"\nDisponibilidad de datos:")
    print(f"  Datos diarios disponibles: {daily_available}/{len(final_df)} ({daily_available/len(final_df)*100:.1f}%)")
    print(f"  Datos horarios disponibles: {hourly_available}/{len(final_df)} ({hourly_available/len(final_df)*100:.1f}%)")
    
    print(f"\nDisponibilidad de códigos COCO:")
    print(f"  COCO en datos diarios: {daily_with_coco}/{len(final_df)} ({daily_with_coco/len(final_df)*100:.1f}%)")
    print(f"  COCO en datos horarios: {hourly_with_coco}/{len(final_df)} ({hourly_with_coco/len(final_df)*100:.1f}%)")
    
    print(f"\n{'='*60}")
    print("ARCHIVOS GENERADOS:")
    print("  📊 argentina_meteorological_stations_complete.csv - Reporte completo")
    
    # Crear un mapa centrado en Argentina
    m = folium.Map(location=[-38.41, -63.61], zoom_start=4)
    
    # Agregar cada estación como un marcador
    for _, row in final_df.iterrows():
        if pd.notna(row['latitude']) and pd.notna(row['longitude']):
            folium.Marker(
                location=[row['latitude'], row['longitude']],
                popup=row['station_name'],
                icon=folium.Icon(color='blue', icon='cloud')
            ).add_to(m)

    # Mostrar el mapa en Jupyter o exportarlo como HTML
    html_path = os.path.join(base_path, "mapa_meteostats.html")
    m.save(html_path)   
    
    return final_df

# Ejecutar el análisis completo
create_argentina_stations_report()