import requests
import pandas as pd
import folium
import os
import time

API_KEY = '--'

base_path = os.path.dirname(os.path.abspath(__file__))

ciudades = [
    # ========================
    # Capitales de provincias
    # ========================
    'La Plata', 'San Fernando del Valle de Catamarca', 'Resistencia', 'Rawson', 'Córdoba', 'Corrientes', 'Paraná', 'Formosa', 'San Salvador de Jujuy',
    'Santa Rosa', 'La Rioja', 'Mendoza', 'Posadas', 'Neuquén', 'Viedma', 'Salta', 'San Juan', 'San Luis', 'Río Gallegos', 'Santa Fe',
    'Santiago del Estero', 'Ushuaia', 'San Miguel de Tucumán', 'Buenos Aires',

    # ==================================
    # Subzonas en grandes ciudades (mayor granularidad)
    # ==================================
    'Buenos Aires - Norte', 'Buenos Aires - Centro', 'Buenos Aires - Sur', 'Buenos Aires - Oeste',
    'Córdoba - Norte', 'Córdoba - Centro', 'Córdoba - Sur',
    'Mendoza - Norte', 'Mendoza - Sur',
    'Rosario - Norte', 'Rosario - Sur',

    # ================================
    # Ciudades grandes y medianas
    # ================================
    'Rosario', 'Mar del Plata', 'Bahía Blanca', 'San Carlos de Bariloche', 'Comodoro Rivadavia', 'San Rafael',
    'San Nicolás de los Arroyos', 'Río Cuarto', 'Concordia', 'Santa Rosa', 'San Justo', 'Godoy Cruz',
    'Villa María', 'Villa Mercedes', 'Tandil', 'Venado Tuerto', 'Rafaela', 'Trelew', 'San Martín (Mza)', 'Oberá',
    'General Roca', 'Goya', 'Paso de los Libres', 'Concepción del Uruguay', 'Yerba Buena', 'Alta Gracia',
    'Carlos Paz', 'El Calafate', 'Esquel', 'El Bolsón', 'Villa La Angostura', 'Chos Malal', 'Pico Truncado',
    'Río Grande', 'Perito Moreno', 'Los Antiguos', 'San Luis del Palmar', 'Monte Quemado', 'Santa Victoria Este',
    'Las Lajitas', 'Tinogasta', 'Abra Pampa', 'La Quiaca', 'Piedra del Águila', 'Villa Pehuenia',

    # ================================
    # Ciudades de la Provincia de Buenos Aires (fuera de CABA)
    # ================================
    'Avellaneda', 'Quilmes', 'Morón', 'Lomas de Zamora', 'Lanús', 'Berazategui', 'San Miguel', 'Tigre', 'San Isidro',
    'Vicente López', 'José C. Paz', 'Ituzaingó', 'Merlo', 'Florencio Varela', 'Campana', 'Zárate', 'San Pedro',
    'Pergamino', 'Junín', 'San Nicolás de los Arroyos', 'Chivilcoy', 'Bragado', '9 de Julio', 'Pehuajó',
    'Trenque Lauquen', 'Carlos Casares', 'General Madariaga', 'Monte Hermoso', 'Tandil', 'Balcarce', 'Olavarría',
    'Azul', 'Benito Juárez', 'Necochea', 'Tres Arroyos', 'Miramar', 'Villa Gesell', 'Pinamar', 'Dolores',
    'Carmen de Patagones', 'Carhué', 'Lincoln', 'Punta Alta', 'Pigüé', 'Coronel Suárez', 'Coronel Pringles',
    'Ramallo', 'Salto', 'Rojas', 'Colón (Buenos Aires)', 'Arrecifes', '25 de Mayo (La Pampa)'
]

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
m = folium.Map(location=[-38.41, -63.61], zoom_start=4)
for _, r in df_est.iterrows():
    folium.Marker(
        location=[r.latitude, r.longitude],
        popup=r.name,
        icon=folium.Icon(color='blue', icon='cloud')
    ).add_to(m)
map_path = os.path.join(base_path, "mapa_visualcrossing.html")
m.save(map_path)
print(f"Mapa guardado en: {map_path}")
