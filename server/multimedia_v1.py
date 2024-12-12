from datetime import datetime
from bson import ObjectId

import random
import os

from typing import Optional, Dict, List
from fastapi import APIRouter, HTTPException, Query, Request, Path, UploadFile, File
from fastapi.responses import JSONResponse
import cloudinary
import cloudinary.uploader

from models.image_model import Image
from db_connection import DatabaseConnection
from api_utils import APIUtils

from dotenv import load_dotenv

load_dotenv()

cloudinary.config(
    cloud_name = os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key = os.getenv("CLOUDINARY_API_KEY"),
    api_secret = os.getenv("CLOUDINARY_API_SECRET"),
    secure=True
)
router = APIRouter()

endpoint_name = "media"
version = "v1"

@router.get("/" + endpoint_name, tags=["Images CRUD endpoints"], response_model=List[Image])
async def get_images(
    request: Request,
    ownerId: int | None = Query(None, description="ID del autor de la imagen", gt=0),
    name: str | None = Query(None, description="Nombre del archivo"),
    fields: str | None = Query(None, description="Campos específicos a devolver"),
    sort: str | None = Query(None, description="Campos por los que ordenar, separados por comas"),
    offset: int = Query(default=0, description="Índice de inicio para los resultados de la paginación"),
    limit: int = Query(default=10, description="Cantidad de imagenes a devolver, por defecto 10"),
    hateoas: bool | None = Query(None, description="Incluir enlaces HATEOAS")
):
    APIUtils.check_accept_json(request)

    try:
        query = build_query(ownerId, name)
        projection = APIUtils.build_projection(fields)
        sort_criteria = APIUtils.build_sort_criteria(sort)

        images = DatabaseConnection.query_document("image", query, projection, sort_criteria, offset, limit)
        
        total_count = len(images)

        if hateoas:
            for image in images:
                image["href"] = f"/api/{version}/{endpoint_name}/{image['_id']}"

        return JSONResponse(status_code=200, content=images, 
                            headers={"Accept-Encoding": "gzip", "X-Total-Count": str(total_count)})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al buscar la imagen: {str(e)}")

@router.get("/" + endpoint_name + "/{id}", tags=["Images CRUD endpoints"], response_model=Image)
async def get_image_by_id(request: Request, 
    id: str = Path(description="ID de la imagen", min_length=24, max_length=24),
    fields: str | None = Query(None, description="Campos específicos a devolver")
):
    APIUtils.check_id(id)
    APIUtils.check_accept_json(request)
    
    try:
        projection = APIUtils.build_projection(fields)

        image = DatabaseConnection.read_document("image", id, projection)
        if image is None:
            return JSONResponse(status_code=404, content={"detail": f"Imagen con ID {id} no encontrado"})
        
        return JSONResponse(status_code=200, content=image,
                            headers={"Content-Type": "application/json", "X-Total-Count": "1"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener la imagen: {str(e)}")

@router.post("/" + endpoint_name, tags=["Images CRUD endpoints"])
async def test_upload(file: UploadFile = File(...)):
    try:
        upload_result = cloudinary.uploader.upload(file.file)
        thumbnail_url = upload_result['secure_url']
        public_id = upload_result['public_id']

        new_image = Image()
        new_image.name = file.filename
        new_image.ownerId = 1 + (int)(10 * random.random())
        new_image.url = thumbnail_url

        body_dict = new_image.model_dump()
        body_dict["timestamp"] = datetime.now()

        DatabaseConnection.create_document("image", body_dict, hasDate=True)

        return JSONResponse(status_code=201, content={"detail": "La imagen se ha subido correctamente", "result": body_dict},
                            headers={"Location": f"/api/{version}/{endpoint_name}/{body_dict['_id']}"} )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al subir la imagen {str(e)}")

@router.options("/" + endpoint_name, tags=["Images OPTIONS endpoints"])
async def options_images():
    return JSONResponse(
        status_code=200,
        content={"methods": ["GET", "POST", "OPTIONS"]},
        headers={"Allow": "GET, POST, OPTIONS"}
    )

@router.options("/" + endpoint_name + "/{id}", tags=["Images OPTIONS endpoints"])
async def options_image_by_id():
    return JSONResponse(
        status_code=200,
        content={"methods": ["GET", "OPTIONS"]},
        headers={"Allow": "GET, OPTIONS"}
    )

def build_query(ownerId: Optional[int], name: Optional[str]) -> Dict[str, Dict]:
    """Construir una consulta a partir de los parámetros proporcionados."""
    query = {}

    if ownerId is not None:
        query["ownerId"] = ownerId

    if name is not None:
        query["name"] = name

    return query