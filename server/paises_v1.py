from datetime import datetime
from typing import Optional, List
from fastapi import APIRouter, HTTPException, Query, Request, Path
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from bson.objectid import ObjectId
from models.pais_model import Pais, PaisCreate, PaisUpdate, PaisDeleteResponse
from db_connection import DatabaseConnection
from api_utils import APIUtils

router = APIRouter()

endpoint_name = "paises"
version = "v1"

@router.get("/" + endpoint_name + "/email/{email}", tags=["Paises CRUD endpoints"], response_model=List[Pais])
async def get_paises_by_email(request: Request, email: str = Path(description="Email del usuario")):
    """Obtener todos los países asociados a un email."""

    APIUtils.check_accept_json(request)

    try:
        query = {"email": email}
        paises = DatabaseConnection.query_document("paises", query)

        total_count = DatabaseConnection.count_documents("paises", query)

        return JSONResponse(
            status_code=200,
            content=paises,
            headers={"Accept-Encoding": "gzip", "X-Total-Count": str(total_count)}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al buscar los países: {str(e)}")

@router.get("/" + endpoint_name, tags=["Paises CRUD endpoints"], response_model=List[Pais])
async def get_paises(
    request: Request,
    fields: str | None = Query(None, description="Campos específicos a devolver"),
    sort: str | None = Query(None, description="Campos por los que ordenar, separados por comas"),
    offset: int = Query(default=0, description="Índice de inicio para los resultados de la paginación"),
    limit: int = Query(default=10, description="Cantidad de países a devolver, por defecto 10")
):
    """Obtener todos los países."""

    APIUtils.check_accept_json(request)

    try:
        projection = APIUtils.build_projection(fields)
        sort_criteria = APIUtils.build_sort_criteria(sort)

        paises = DatabaseConnection.query_document(
            "paises", {}, projection, sort_criteria, offset, limit
        )

        total_count = DatabaseConnection.count_documents("paises", {})

        return JSONResponse(
            status_code=200,
            content=paises,
            headers={"Accept-Encoding": "gzip", "X-Total-Count": str(total_count)}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al buscar los países: {str(e)}")

@router.get("/" + endpoint_name + "/{id}", tags=["Paises CRUD endpoints"], response_model=Pais)
async def get_pais_by_id(request: Request, id: str = Path(description="ID del país")):
    """Obtener un país por su ID."""

    APIUtils.check_accept_json(request)

    try:
        pais = DatabaseConnection.read_document_id("paises", id)
        if pais is None:
            return JSONResponse(status_code=404, content={"detail": f"País con ID {id} no encontrado"})

        return JSONResponse(status_code=200, content=pais,
                            headers={"Content-Type": "application/json", "X-Total-Count": "1"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener el país: {str(e)}")

@router.post("/" + endpoint_name, tags=["Paises CRUD endpoints"], response_model=Pais)
async def create_pais(request: Request, pais: PaisCreate):
    """Crear un nuevo país."""

    APIUtils.check_content_type_json(request)

    try:
        pais_dict = pais.model_dump()
        pais_dict['_id'] = DatabaseConnection.create_document("paises", pais_dict)

        return JSONResponse(status_code=201, content=pais_dict,
                            headers={"Content-Type": "application/json"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear el país: {str(e)}")

@router.put("/" + endpoint_name + "/{id}", tags=["Paises CRUD endpoints"], response_model=Pais)
async def update_pais(request: Request, pais: PaisUpdate, id: str = Path(description="ID del país")):
    """Actualizar un país por su ID."""

    APIUtils.check_content_type_json(request)

    try:
        pais_dict = pais.model_dump()
        non_none_fields = {k: v for k, v in pais_dict.items() if v is not None}
        if not non_none_fields:
            return JSONResponse(status_code=422, content={"detail": "No has especificado ningún campo del país"})

        updated_document = DatabaseConnection.update_document_id("paises", id, non_none_fields)
        if updated_document is None:
            return JSONResponse(status_code=404, content={"detail": "No se ha encontrado un país con ese ID. No se ha editado nada"})

        json_serializable_document = jsonable_encoder(updated_document)

        return JSONResponse(
            status_code=200,
            content={
                "detail": "El país se ha editado correctamente",
                "result": json_serializable_document
            }
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar el país: {str(e)}")

@router.delete("/" + endpoint_name + "/{id}", tags=["Paises CRUD endpoints"], response_model=PaisDeleteResponse)
async def delete_pais(id: str = Path(description="ID del país")):
    """Eliminar un país por su ID."""

    try:
        count = DatabaseConnection.delete_document_id("paises", id)
        if count == 0:
            return JSONResponse(status_code=404, content={"detail": "No se ha encontrado un país con ese ID. No se ha borrado nada."})

        return JSONResponse(status_code=200, content={"details": "El país se ha eliminado correctamente"},
                            headers={"Content-Type": "application/json"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar el país: {str(e)}")
