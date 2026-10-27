# Diccionario de datos

Datasets descargables del proyecto. Formato CSV, UTF-8 (con BOM, abren bien en
Excel), separador coma, decimal con punto. Fuente: ENACOM (Datos Abiertos) e INDEC
(Censo 2022). Corte: 2.º trimestre de 2026, salvo la serie histórica (anual).

Definiciones comunes:
- **Penetración**: accesos a internet fijo cada 100 hogares. Puede superar 100
  porque incluye conexiones no residenciales.
- **Fibra (% accesos)**: participación de la fibra óptica sobre el total de accesos.
- **Satelital (% accesos)**: participación de las conexiones satelitales sobre el total.
- **Velocidad media**: Mbps promedio de bajada contratados.

---

### `penetracion_provincias_2026.csv` — 24 filas
Foto comparativa de las 24 jurisdicciones.
`Provincia, Penetracion_accesos_c100hog, Fibra_pct_accesos, Velocidad_media_Mbps`

### `serie_penetracion_2014_2026.csv` — 25 filas
Penetración anual por provincia (una columna por año, 2014 a 2026) más la fila
`Total país`. Formato ancho.
`Provincia, 2014, 2015, ... , 2026`

### `jujuy_departamentos_2026.csv` — 16 filas
Desagregación departamental de Jujuy (lo que diferencia a este proyecto). Cruza
ENACOM por localidad con hogares del Censo 2022.
`Departamento, Region, Codigo_INDEC, Hogares_Censo2022, Accesos,
Penetracion_accesos_c100hog, Fibra_pct_accesos, Satelital_pct_accesos, Velocidad_media_Mbps`

### `jujuy_regiones_2026.csv` — 4 filas
Agregado por región de Jujuy (Valles, Ramal, Quebrada, Puna).
`Region, Departamentos, Accesos, Hogares_Censo2022, Penetracion_accesos_c100hog,
Fibra_pct_accesos, Satelital_pct_accesos, Velocidad_media_Mbps`
