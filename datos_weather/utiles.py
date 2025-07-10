import folium
import os
import pandas as pd

def generar_mapa_estaciones(df, nombre_archivo_html, base_path, lat_col='latitude', lon_col='longitude', nombre_col='name'):
    """
    Genera un mapa de estaciones meteorológicas usando Folium.

    Parámetros:
    - df: DataFrame con las estaciones
    - nombre_archivo_html: nombre del archivo a guardar
    - base_path: ruta absoluta donde guardar el archivo HTML
    - lat_col: nombre de la columna con latitud
    - lon_col: nombre de la columna con longitud
    - nombre_col: nombre de la columna con el nombre de la estación
    """

    # Crear mapa centrado en Argentina
    m = folium.Map(location=[-38.41, -63.61], zoom_start=4)

    # Agregar marcadores
    for _, row in df.iterrows():
        if pd.notna(row[lat_col]) and pd.notna(row[lon_col]):
            folium.Marker(
                location=[row[lat_col], row[lon_col]],
                popup=row[nombre_col],
                icon=folium.Icon(color='blue', icon='cloud')
            ).add_to(m)

    # Guardar mapa
    recursos_path = os.path.join(base_path, 'recursos')
    map_path = os.path.join(recursos_path, nombre_archivo_html)
    m.save(map_path)
    print(f"Mapa guardado en: {map_path}")


def guardar_estaciones_y_atributos(lista_estaciones, atributos_clima_set, base_path, nombre_api):
    """
    Guarda dos archivos CSV:
    - Uno con las estaciones (a partir de lista_estaciones)
    - Otro con los atributos climáticos (a partir de un set)

    Parámetros:
        lista_estaciones (list): lista de diccionarios con las estaciones
        atributos_clima_set (set): conjunto de atributos climáticos
        base_path (str): ruta donde guardar los archivos
        nombre_api (str): prefijo para los nombres de archivo (por ejemplo 'weatherapi')
    """
    # Guardar estaciones
    df_est = pd.DataFrame(lista_estaciones)
    ruta_est = os.path.join(base_path, f"{nombre_api}_estaciones_argentina.csv")
    df_est.to_csv(ruta_est, index=False, encoding='utf-8')
    print(f"CSV de estaciones guardado en: {ruta_est}")

    # Guardar atributos
    df_attr = pd.DataFrame(sorted(atributos_clima_set), columns=['atributo'])
    ruta_attr = os.path.join(base_path, f"{nombre_api}_atributos_clima.csv")
    df_attr.to_csv(ruta_attr, index=False, encoding='utf-8')
    print(f"CSV de atributos climáticos guardado en: {ruta_attr}")


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