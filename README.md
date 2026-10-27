# Brecha digital en Argentina — frontend

Especial interactivo de datos sobre acceso a **internet fijo** en Argentina
(penetración, fibra óptica y velocidad), a partir de datos abiertos de ENACOM
y el Censo 2022 (INDEC). Autora: **Micaela López** (Jujuy).

Es un sitio estático de **un solo archivo** (`site.html`): HTML + CSS + JS vanilla,
sin dependencias de build salvo las fuentes de Google. Pensado para hostear en
GitHub Pages.

---

## Cómo correrlo

```bash
# ver el sitio ya construido
python3 -m http.server 8000      # y abrir http://localhost:8000/site.html

# reconstruir site.html tras editar template o datos
python3 build.py
```

`build.py` inyecta los datos y los mapas (JSON) dentro de `template.html` y
escribe `site.html`. **No editar `site.html` a mano**: se regenera. El diseño y
la lógica viven en `template.html`; los datos, en los `.json`.

---

## Estructura

```
web/
├─ template.html     Diseño + lógica. Tiene 2 placeholders: __DATA__ y __GEO__
├─ data_nac.json     Datos nacionales (24 jurisdicciones) → reemplaza __DATA__
├─ geo_nac.json      Mapa de provincias (simplificado) → reemplaza __GEO__
├─ jujuy_deptos.json Datos de Jujuy por departamento (16)  [AÚN NO USADO EN EL HTML]
├─ jujuy_geo.json    Mapa de departamentos de Jujuy (16)    [AÚN NO USADO EN EL HTML]
├─ conclusiones.md   Texto ampliado de conclusiones (copy para la web) [NUEVO]
├─ build.py          Inyecta los JSON en el template → site.html
├─ site.html         Build actual (versión nacional)
├─ datos/            CSV descargables + diccionario [NUEVO]
│  ├─ penetracion_provincias_2026.csv
│  ├─ serie_penetracion_2014_2026.csv
│  ├─ jujuy_departamentos_2026.csv
│  ├─ jujuy_regiones_2026.csv
│  └─ diccionario_datos.md
└─ README.md
```

---

## Esquema de los datos

### `data_nac.json` (nacional, nivel provincia)
```jsonc
{
  "provincias": { "Jujuy": { "pen": 66.4, "fibra": 47.8, "vel": 101.7 }, ... },  // 24
  "serie":      { "Jujuy": [18.7, ... , 66.4], ... },   // penetración anual, 13 pts
  "nacional":   [49.9, ... , 85.4],                     // serie país, 13 pts
  "years":      [2014, ... , 2026]                      // 13 años
}
```
- `pen` = accesos cada 100 hogares · `fibra` = **% del total de accesos** · `vel` = Mbps medios.

### `geo_nac.json` (mapa de provincias)
FeatureCollection. Cada feature: `properties.prov` en MAYÚSCULAS sin acentos
(`"BUENOS AIRES"`, `"TIERRA DEL FUEGO"`). El JS las cruza con los nombres de
`provincias` por normalización (función `norm()` en `template.html`).

### `jujuy_deptos.json` (Jujuy, nivel departamento) — listo, falta cablearlo
```jsonc
{
  "departamentos": {
    "Dr. Manuel Belgrano": {
      "pen": 104.9, "fibra": 46.0, "vel": 111.3,
      "accesos": 104908, "hogares": 100036,
      "region": "Valles", "codigo": "38021", "satelital": 0.0
    }, ...  // 16 departamentos
  },
  "provincial":  { "pen": 66.4, "fibra": 47.8, "vel": 101.7, "ranking_nac": "16/24" },
  "serie_jujuy": [18.7, ... , 66.4],   // misma serie anual que data_nac
  "serie_pais":  [49.9, ... , 85.4],
  "serie_years": [2014, ... , 2026]
}
```
Mismas 3 métricas que el nacional, para reutilizar la lógica del explorador tal cual.

### `jujuy_geo.json` (mapa de departamentos de Jujuy)
FeatureCollection, 16 features. `properties.dep` coincide **exacto** con las claves
de `departamentos` (ya normalizado), y `properties.codigo` trae el código INDEC.
No hace falta normalizar: cruce directo por `dep`.

---

## El plan: JUJUY PRIMERO

El rediseño actual abre con el país y trata a Jujuy como "punto de partida".
**Hay que darlo vuelta: Jujuy es el protagonista, el país es el segundo nivel.**

Estructura objetivo (de arriba hacia abajo):

1. **Hero** centrado en Jujuy (el trabajo nació como TFI sobre Jujuy).
2. **Contexto** — por qué importa la brecha (ya está, ajustar el foco a Jujuy).
3. **Explorador de Jujuy por departamento** — NUEVO. Reusar el mismo componente
   del explorador nacional pero con `jujuy_geo.json` + `jujuy_deptos.json`:
   mapa coroplético de los 16 departamentos, ranking, detalle y las 3 métricas.
   Dato diferencial: Jujuy es la única provincia con desagregación departamental
   (requirió cruzar ENACOM por localidad con hogares del Censo 2022).
4. **Hallazgos de Jujuy** — contrastes internos fuertes y reales en los datos:
   - Susques 114,6 y Cochinoca 100,3 accesos/100 hog. (incluyen conexiones no
     residenciales) vs. Humahuaca 20,6 o Yavi 20,2.
   - Cochinoca con 90,9% de fibra (efecto del Plan Federal de Internet / ARSAT
     llegando a Abra Pampa) vs. varios departamentos de Puna/Quebrada en ~0%.
   - Velocidad media provincial 101,7 Mbps, pero Ledesma 36,5 y Palpalá 57,1.
5. **"Ampliar la mirada al país"** — acá entra el explorador NACIONAL actual
   (provincias) + sus hallazgos + la tabla de 24 jurisdicciones. Es el segundo
   nivel, se puede ir completando los próximos días.
6. **Metodología** y footer (ya están).

### Notas / caveats a respetar
- `pen` puede superar 100: incluye conexiones no residenciales. Ya hay nota al pie.
- La serie temporal 2014–2026 existe sólo a nivel **Jujuy y país** (anual). Los
  **departamentos son una foto única** (2.º trim. 2026): no graficar serie por depto.
- `fibra` siempre como **% del total de accesos** (no confundir con la columna
  "Fibra c/100 hog." del xlsx original; acá ya está convertida a %).

## Descargas de datasets (NUEVO)
Agregar una sección donde la gente pueda **descargar los datasets**. Los archivos
ya están en `datos/` (ver `datos/diccionario_datos.md` para el esquema). Basta con
enlaces de descarga (`<a href="datos/archivo.csv" download>`), idealmente con una
línea por archivo que diga qué contiene y cuántas filas. No hace falta generar nada:
los CSV son estáticos y se sirven tal cual.

## Conclusiones ampliadas (NUEVO — marcado como clave)
El texto completo está en `conclusiones.md`, con 6 bloques encabezados y ya apoyado
en cifras reales. Reemplaza/expande la sección "Hallazgos" actual (hoy son 4 tarjetas
sueltas). Mantener el tono editorial y los números tal cual; es contenido revisado,
no reescribir las cifras.

### TODO
- [ ] Cablear el explorador departamental de Jujuy (markup + JS sobre los JSON ya listos).
- [ ] Reordenar la narrativa a Jujuy-primero / país-segundo.
- [ ] Sumar sección de **descargas** enlazando los CSV de `datos/`.
- [ ] Expandir la sección de **conclusiones** con el texto de `conclusiones.md`.
- [ ] `git init`, primer commit, deploy a GitHub Pages.
- [ ] (Opcional) sumar más provincias con desagregación si se consiguen los datos.

---

## Fuentes
- **ENACOM** — Portal de Datos Abiertos (acceso a internet fijo: penetración,
  tecnologías y velocidad, por provincia y por localidad).
- **INDEC** — Censo 2022 (hogares por departamento de Jujuy).
- **Límites geográficos**: provincias (Polymaps-Argentina) y departamentos
  (repo `mgaitan/departamentos_argentina`), simplificados con shapely.
