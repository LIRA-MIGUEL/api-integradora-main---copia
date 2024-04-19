from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from bson import ObjectId
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

# Crea la aplicación FastAPI
app = FastAPI()

# Configura los orígenes permitidos (en tu caso, todos los orígenes)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Conexión a MongoDB
try:
    # Intenta establecer la conexión
    client = MongoClient('mongodb://localhost:27017/')

    db = client['integradora']
    DATOS = db['datos']

    # Imprime un mensaje si la conexión es exitosa
    print("Conexión exitosa a MongoDB Atlas")

except Exception as e:
    print("Error de conexión a MongoDB Atlas:", e)

# Define el modelo para el dato
class DatoCreate(BaseModel):
    numeroUnidad: str
    ruta: str
    horarioEntrada: str
    horarioSalida: str
    duracionViaje: str
    operador: str

# Define el endpoint POST para crear un nuevo dato
@app.post("/datos")
async def create_dato(dato_create: DatoCreate):
    try:
        # Convierte el dato_create en un diccionario
        nuevo_dato = dato_create.dict()

        # Inserta el nuevo dato en la colección
        resultado = DATOS.insert_one(nuevo_dato)

        # Si la inserción fue exitosa, devuelve el ID del nuevo dato
        if resultado.inserted_id:
            return {"mensaje": "Dato creado exitosamente", "id_dato": str(resultado.inserted_id)}
        else:
            raise HTTPException(status_code=500, detail="Error al crear el dato")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {e}")

# Define el endpoint GET para buscar un admin por ID
@app.get("/datos/{_id}")
async def get_dato_by_id(_id: str):
    respuesta = []
    try:
        # Busca el admin por su ID en la colección
        dato = DATOS.find({"_id": ObjectId(_id)})

        for resultado in dato:
            resultado['_id'] = str(resultado['_id'])
            respuesta.append(resultado)
        # Si el admin no se encuentra, levanta una excepción HTTP 404
        if respuesta is None:
            raise HTTPException(status_code=404, detail="dato no encontrado")

        return respuesta

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor, {e}")
    
@app.get("/datos")
async def get_all_datos():
    try:
        #busca los datos de la coleccion
        datos = DATOS.find({})

        respuesta = []
        for dato in datos: 
            dato['_id'] = str(dato['_id'])
            respuesta.append(dato)

        return respuesta
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor, {e}")
