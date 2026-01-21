from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from data.db import series
from models.serie import Serie
import uvicorn

app = FastAPI()

app.mount("/static", StaticFiles(directory="src/static"), name="static")
templates = Jinja2Templates(directory="src/templates")

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    mensaje = "Hola mundo"
    return templates.TemplateResponse("index.html", {"request": request, "mensaje": mensaje})

@app.get("/series", response_class=HTMLResponse)
async def ver_series(request: Request):
    return templates.TemplateResponse("series.html", {"request": request, "series": series})

@app.get("/series/{serie_id}", response_class=HTMLResponse)
async def buscar_serie_por_id(serie_id: int, request: Request):
    serie_encontrada = buscar_serie(serie_id)
    if not serie_encontrada:
        raise HTTPException(status_code=404, detail="Serie no encontrada")
    return templates.TemplateResponse("serie_detalle.html", {"request": request, "serie": serie_encontrada})


@app.get("/api/series", response_model=list[Serie])
async def lista_series():
    return series

def siguiente_id() -> int:
    if len(series) == 0:
        return 1
    else:
        return max(serie.id for serie in series if serie.id is not None) + 1

@app.post("/api/series", response_model=Serie, status_code=201)
async def crear_serie(serie: Serie):
    serie.id = siguiente_id()
    series.append(serie)
    return serie

def buscar_serie(serie_id: int):
    for serie in series:
        if serie.id == serie_id:
            return serie
    return None

@app.put("/api/series/{serie_id}", response_model=Serie)
async def actualizar_serie(serie_id: int, serie_actualizada: Serie):
    serie = buscar_serie(serie_id)
    if serie is None:
        raise HTTPException(status_code=404, detail="Serie no encontrada")
    if serie_actualizada.nombre is not None:
        serie.nombre = serie_actualizada.nombre
    if serie_actualizada.fecha_estreno is not None:
        serie.fecha_estreno = serie_actualizada.fecha_estreno
    return serie

@app.delete("/api/series/{serie_id}", status_code=204)
async def eliminar_serie(serie_id: int):    
    serie = buscar_serie(serie_id)
    if serie is None:
        raise HTTPException(status_code=404, detail="Serie no encontrada")
    series.remove(serie)
    return None

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=3000, reload=True)

