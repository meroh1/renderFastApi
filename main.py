# API RESTFUL
# Interfaz de programacion de aplicaciones para compartir recursos usando reglas 
# es decir, una API es un conjunto de reglas que definen como se puede interactuar con un recurso
# y que se puede compartir con otros programas

from typing import List, Optional
# uuid es un modulo que nos permite generar IDs únicos e irrepetibles
import uuid
# HTTPException es un modulo que nos permite manejar errores HTTP
from fastapi import FastAPI, HTTPException
# BaseModel es un modulo que nos permite definir el modelo/estructura de datos de un curso
from pydantic import BaseModel

# Inicializamos una variable donde tendrá todas las características de una API REST
app = FastAPI(
    title="API de Cursos",
    description="API REST para gestionar cursos",
    version="1.0.0"
)

# Ruta raíz para verificar que la API está funcionando
@app.get("/")
def raiz():
    return {"message": "API de Cursos funcionando correctamente"}

# Acá definimos el modelo/estructura de datos de un curso
class Curso(BaseModel):
    id: Optional[str] = None
    nombre: str
    descripcion: Optional[str] = None
    nivel: str
    duracion: int

# Ahora vamos a definir las operaciones CRUD (Create, Read, Update, Delete)
# vanis a crear rutas (endpoints) para cada una de las operaciones CRUD
# GET: Leeremos todos los cursos que haya en la db
# POST: Agregaremos un nuevo recurso a nuestra base de datos
# PUT: Modificaremos un recurso que coincida con el ID que mandemos
# DELETE: Eliminaremos un recurso que coincida con el ID que mandemos

# Simularemos una base de datos (DB)
cursos_db = []

# GET ALL: Leeremos todos los cursos que haya en la db
@app.get("/cursos/", response_model=List[Curso])
def obtener_cursos():
    return cursos_db


# POST: Agregaremos un nuevo cursoa nuestra base de datos
@app.post("/cursos/", response_model=Curso)
def crear_curso(curso:Curso):
    curso.id = str(uuid.uuid4()) # Usamos UUID para generar un ID único e irrepetible
    cursos_db.append(curso)
    return curso


# GET: Leeremos el curso que coincida con el ID que pidamos
@app.get("/cursos/{curso_id}", response_model=Curso)
def obtener_curso(curso_id:str):
    curso = next((curso for curso in cursos_db if curso.id == curso_id), None) # Con next tomamos la primera coincidencia del array devuelto
    if curso is None:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    return curso


# PUT: Modificaremos un curso que coincida con el ID que mandemos a la db
@app.put("/cursos/{curso_id}", response_model=Curso)
def actualizar_curso(curso_id:str, curso_actualizado:Curso):

    # Con next tomamos la primera coincidencia del array devuelto por la consulta a la db
    curso = next((curso for curso in cursos_db if curso.id == curso_id), None) 
    if curso is None:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    curso_actualizado.id = curso_id
    index = cursos_db.index(curso) # Buscamos el índice exacto donde está el curso en nuestra lista (DB)
    cursos_db[index] = curso_actualizado
    return curso_actualizado


# DELETE: Eliminaremos un curso que coincida con el ID que mandemos a la db
@app.delete("/cursos/{curso_id}", response_model=Curso)
def eliminar_curso(curso_id:str):
    curso = next((curso for curso in cursos_db if curso.id == curso_id), None) 
    # Con next tomamos la primera coincidencia del array devuelto por la consulta a la db
    if curso is None:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    cursos_db.remove(curso)
    return curso
