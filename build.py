#!/usr/bin/env python3
# Construye site.html inyectando datos y mapas en template.html
import json, pathlib
base = pathlib.Path(__file__).parent
tpl = (base/"template.html").read_text(encoding="utf-8")
data   = (base/"data_nac.json").read_text(encoding="utf-8").strip()
geo    = (base/"geo_nac.json").read_text(encoding="utf-8").strip()
data_j = (base/"jujuy_deptos.json").read_text(encoding="utf-8").strip()
geo_j  = (base/"jujuy_geo.json").read_text(encoding="utf-8").strip()
# validar JSON antes de inyectar
json.loads(data); json.loads(geo); json.loads(data_j); json.loads(geo_j)
out = (tpl.replace("__DATA__", data)
          .replace("__GEO__", geo)
          .replace("__DATA_JUJUY__", data_j)
          .replace("__GEO_JUJUY__", geo_j))
(base/"site.html").write_text(out, encoding="utf-8")
print("site.html:", len(out), "bytes")
