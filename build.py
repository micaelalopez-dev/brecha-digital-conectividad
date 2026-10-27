#!/usr/bin/env python3
# Construye site.html inyectando datos y mapa en template.html
import json, pathlib
base = pathlib.Path(__file__).parent
tpl = (base/"template.html").read_text()
data = (base/"data_nac.json").read_text().strip()
geo  = (base/"geo_nac.json").read_text().strip()
# validar JSON antes de inyectar
json.loads(data); json.loads(geo)
out = tpl.replace("__DATA__", data).replace("__GEO__", geo)
(base/"site.html").write_text(out)
print("site.html:", len(out), "bytes")
