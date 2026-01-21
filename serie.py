from datetime import date
from pydantic import BaseModel

class Serie(BaseModel):
    id: int | None = None
    nombre: str | None = None
    fecha_estreno: date | None = None

