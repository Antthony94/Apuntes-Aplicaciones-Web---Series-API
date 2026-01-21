# 📘 Guía Explicada Paso a Paso: FastAPI + Jinja2 (ASIR 2º)

> Esta guía está pensada para que **en ningún momento nos perdamos**. En cada apartado sabremos:
>
> * 📍 **Dónde estás dentro del proyecto**
> * ❓ **Por qué haces ese paso**
> * ⚙️ **Qué efecto tiene en la aplicación**
> * ➡️ **Qué es lo siguiente que debes hacer**
>
> Léela como si el profesor estuviera a tu lado explicándote el ejercicio.

---

## 🧠 0. Visión Global: ¿Qué estamos construyendo?

Vamos a desarrollar una **aplicación web híbrida**, algo muy típico en el examen de *Implantación de Aplicaciones Web*:

* Una **API REST** que devuelve y gestiona datos en **JSON** (pensada para máquinas).
* Un **frontend web** que devuelve **HTML dinámico** usando **Jinja2** (pensado para personas).

Todo esto usando **FastAPI como servidor web**.

👉 **Idea clave de examen**: un mismo servidor puede servir **API + Web**.

---

## 🏗️ 1. Estructura del Proyecto (Dónde estamos antes de programar)

📍 **Estamos en la carpeta raíz del proyecto**. Antes de escribir código, **creamos la estructura**, porque FastAPI y Python dependen mucho de las rutas.

Memoriza esto. En el examen suele ser lo primero.

```text
series-api-web/
│
├── requirements.txt         # Dependencias del proyecto
│
└── src/                     # Carpeta raíz del código
    ├── main.py              # 🧠 CEREBRO: servidor y rutas
    │
    ├── data/                # 💾 Datos (simulan una BD)
    │   └── db.py
    │
    ├── models/              # 📐 Modelos de datos
    │   └── serie.py
    │
    ├── static/              # 🎨 Archivos estáticos (CSS, imágenes)
    │
    └── templates/           # 🖼️ HTML dinámico (Jinja2)
        ├── index.html
        ├── series.html
        └── serie_detalle.html
```

🧠 **Por qué es importante**:

* Python usa esta estructura para los imports.
* El profesor valora mucho que el proyecto esté ordenado.

➡️ **Siguiente paso**: definir qué tipo de datos maneja nuestra aplicación.

---

## 🚀 2. Paso 1: Definir el Modelo (src/models/serie.py)

📍 **Estamos creando el modelo**, es decir, la definición del dato principal.

Antes de guardar o mostrar datos, necesitamos responder a esta pregunta:

> ❓ ¿Qué es una “Serie” dentro de mi aplicación?

### 🧩 Código

```python
from datetime import date
from pydantic import BaseModel

class Serie(BaseModel):
    id: int | None = None
    nombre: str | None = None
    fecha_estreno: date | None = None
```

🧠 **Qué estamos haciendo**:

* Creamos una clase que **hereda de BaseModel**.
* Definimos los campos y su tipo.

🧠 **Por qué lo hacemos**:

* FastAPI usa este modelo para:

  * Validar datos automáticamente.
  * Convertir JSON ⇄ objetos Python.

🎓 **Examen**:

* Si te cambian el enunciado (Alumnos, Productos, Libros), **solo cambia la clase**.

➡️ **Siguiente paso**: almacenar datos usando este modelo.

---

## 💾 3. Paso 2: Base de Datos Simulada (src/data/db.py)

📍 **Estamos creando la capa de datos**.

Si el examen **no pide SQL**, lo normal es usar una **lista en memoria**.

### 🧩 Código

```python
from models.serie import Serie

series: list[Serie] = [
    Serie(id=1, nombre="La casa de papel", fecha_estreno="2023-10-30"),
]
```

🧠 **Qué estamos haciendo**:

* Importamos el modelo.
* Creamos una lista de objetos `Serie`.

🧠 **Concepto importante**:

* Esto **NO es persistente**.
* Si paras el servidor, los datos se reinician.

🎓 **Examen**:

* El profesor quiere ver que sabes separar **datos** de **lógica**.

➡️ **Siguiente paso**: crear el servidor que conecta datos y vistas.

---

## 🧠 4. Paso 3: Controlador Principal (src/main.py)

📍 **Estamos en el archivo más importante**.

Aquí se conectan:

* Los datos
* Las rutas
* Las vistas

---

### 4.1 Configuración Inicial (MEMORIZAR)

```python
from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount("/static", StaticFiles(directory="src/static"), name="static")

templates = Jinja2Templates(directory="src/templates")
```

🧠 **Qué estamos haciendo**:

* Creamos la app.
* Indicamos dónde están los estáticos.
* Indicamos dónde están los HTML.

⚠️ **Esto siempre va igual en el examen**.

➡️ **Siguiente paso**: crear rutas web.

---

### 4.2 Rutas Web (HTML para personas)

📍 Estas rutas devuelven **HTML**, no JSON.

```python
@app.get("/series")
async def ver_series(request: Request):
    return templates.TemplateResponse("series.html", {
        "request": request,
        "series": series
    })
```

🧠 **Qué estamos haciendo**:

* Respondemos a `/series`.
* Pasamos datos al HTML.

⚠️ **Clave de examen**:

* `request` es obligatorio en Jinja2.

➡️ **Siguiente paso**: rutas de API.

---

### 4.3 Rutas API (JSON para máquinas)

```python
@app.post("/api/series", response_model=Serie, status_code=201)
async def crear_serie(serie: Serie):
    series.append(serie)
    return serie
```

🧠 **Qué estamos haciendo**:

* Creamos datos vía JSON.
* FastAPI valida automáticamente.

🎓 **Idea clave**:

* Un mismo backend sirve **HTML + API**.

➡️ **Siguiente paso**: mostrar datos en HTML.

---

## 🖼️ 5. Paso 4: Vistas Jinja2 (src/templates)

📍 **Estamos en el frontend**, pero sin JavaScript complejo.

### Sintaxis que debes saber

* `{{ variable }}` → imprimir
* `{% if %}` → condicional
* `{% for %}` → bucle

### Ejemplo (series.html)

```html
<table>
<tr><th>ID</th><th>NOMBRE</th><th>ACCIÓN</th></tr>

{% for serie in series %}
<tr>
<td>{{ serie.id }}</td>
<td>{{ serie.nombre }}</td>
<td><a href="/series/{{ serie.id }}">Ver</a></td>
</tr>
{% endfor %}
</table>
```

🧠 **Qué ocurre aquí**:

* Jinja2 recorre la lista Python.
* Genera HTML dinámico.

➡️ **Siguiente paso**: ejecutar y comprobar.

---

## 🏃‍♂️ 6. Ejecución del Proyecto

📍 **Estamos en la raíz del proyecto**.

```bash
uvicorn src.main:app --reload
```

🌍 Abre navegador:

* [http://127.0.0.1:8000/series](http://127.0.0.1:8000/series)

---

## ❌ 7. Errores Típicos de Examen

* Olvidar `request` en el template.
* Rutas mal definidas.
* Imports incorrectos.
* Duplicar nombres de funciones.

---

## ✅ 8. Checklist Mental para el Examen

1. Crear estructura
2. Crear modelo
3. Crear datos
4. Configurar FastAPI
5. Rutas web
6. Rutas API
7. Plantillas
8. Probar

🎓 **Si entiendes cada paso, sabes hacer el examen.**
