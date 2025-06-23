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
m = folium.Map(location=[-38.41, -63.61], zoom_start=4)
for _, r in df_est.iterrows():
    folium.Marker(
        location=[r.latitude, r.longitude],
        popup=r.name,
        icon=folium.Icon(color='green')
    ).add_to(m)
map_path = os.path.join(base_path, "mapa_weatherapi.html")
m.save(map_path)
print(f"Mapa guardado en: {map_path}")
