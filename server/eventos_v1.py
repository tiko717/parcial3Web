from datetime import datetime

from typing import Optional, Dict, List
from fastapi import APIRouter, HTTPException, Query, Request, Path
from fastapi.responses import JSONResponse
import dateutil.parser as parser
from fastapi.encoders import jsonable_encoder

from bson.objectid import ObjectId
from models.evento_model import Evento, EventoCreate, EventoUpdate, EventoDeleteResponse
from db_connection import DatabaseConnection
from api_utils import APIUtils

router = APIRouter()

endpoint_name = "eventos"
version = "v1"


@router.get("/" + endpoint_name + "/nearby", tags=["Eventos CRUD endpoints"], response_model=List[Evento])
async def get_eventos_nearby(
    request: Request,
    lat: float = Query(None, description="Latitud central para la búsqueda"),
    lon: float = Query(None, description="Longitud central para la búsqueda"),
    fields: str | None = Query(None, description="Campos específicos a devolver"),
    sort: str | None = Query(None, description="Campos por los que ordenar, separados por comas"),
    offset: int = Query(default=0, description="Índice de inicio para los resultados de la paginación"),
    limit: int = Query(default=10, description="Cantidad de eventos a devolver, por defecto 10")
):
    """Obtener eventos cercanos a una latitud y longitud específicas."""

    APIUtils.check_accept_json(request)

    try:
        # Construir proyección, criterio de orden y paginación
        projection = APIUtils.build_projection(fields)
        sort_criteria = APIUtils.build_sort_criteria(sort)

        # Construir la consulta para latitud y longitud
        query = {
            "lat": {"$gte": lat - 0.2, "$lte": lat + 0.2},
            "lon": {"$gte": lon - 0.2, "$lte": lon + 0.2}
        }

        eventos = DatabaseConnection.query_document(
            "eventos", query, projection, sort_criteria, offset, limit, hasDate=True
        )

        total_count = DatabaseConnection.count_documents("eventos", query)

        return JSONResponse(
            status_code=200,
            content=eventos,
            headers={"Accept-Encoding": "gzip", "X-Total-Count": str(total_count)}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al buscar los eventos: {str(e)}")

@router.get("/" + endpoint_name, tags=["Eventos CRUD endpoints"], response_model=List[Evento])
async def get_eventos(
    request: Request,
    fields: str | None = Query(None, description="Campos específicos a devolver"),
    sort: str | None = Query(None, description="Campos por los que ordenar, separados por comas"),
    offset: int = Query(default=0, description="\u00cdndice de inicio para los resultados de la paginaci\u00f3n"),
    limit: int = Query(default=10, description="Cantidad de eventos a devolver, por defecto 10")
):
    """Obtener todos los eventos."""

    APIUtils.check_accept_json(request)

    try:
        # Construir proyección, criterio de orden y paginación
        projection = APIUtils.build_projection(fields)
        sort_criteria = APIUtils.build_sort_criteria(sort)

        eventos = DatabaseConnection.query_document(
            "eventos", {}, projection, sort_criteria, offset, limit, hasDate=True
        )

        total_count = DatabaseConnection.count_documents("eventos", {})

        return JSONResponse(
            status_code=200,
            content=eventos,
            headers={"Accept-Encoding": "gzip", "X-Total-Count": str(total_count)}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al buscar los eventos: {str(e)}")




@router.get("/" + endpoint_name + "/{id}", tags=["Eventos CRUD endpoints"], response_model=Evento)
async def get_evento_by_id(request: Request, id: str = Path(description="ID del evento")):
    """Obtener un evento por su ID."""

    APIUtils.check_accept_json(request)

    try:
        evento = DatabaseConnection.read_document_id("eventos", id, hasDate=True)
        if evento is None:
            return JSONResponse(status_code=404, content={"detail": f"Evento con ID {id} no encontrado"})
        
        return JSONResponse(status_code=200, content=evento,
                            headers={"Content-Type": "application/json", "X-Total-Count": "1"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener el evento: {str(e)}")



@router.post("/" + endpoint_name, tags=["Eventos CRUD endpoints"], response_model=Evento)
async def create_evento(request: Request, evento: EventoCreate):
    """Crear un nuevo evento."""

    APIUtils.check_content_type_json(request)

    try:
        evento_dict = evento.model_dump()
        evento_dict['timestamp'] = datetime.strptime(evento.timestamp, "%d/%m/%Y %H:%M")
        evento_dict['_id'] = DatabaseConnection.create_document("eventos", evento_dict, hasDate=True)
        
        return JSONResponse(status_code=201, content=evento_dict,
                            headers={"Content-Type": "application/json"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear el evento: {str(e)}")

@router.put("/" + endpoint_name + "/{id}", tags=["Eventos CRUD endpoints"], response_model=Evento)
async def update_evento(request: Request, evento: EventoUpdate, id: str = Path(description="ID del evento")):
    """Actualizar un evento por su ID."""
    
    APIUtils.check_content_type_json(request)

    try:
        evento_dict = evento.model_dump()
                
        if evento.timestamp is not None:
            evento_dict['timestamp'] = datetime.strptime(evento.timestamp, "%d/%m/%Y %H:%M")
                
        non_none_fields = {k: v for k, v in evento_dict.items() if v is not None}
        if not non_none_fields:
            return JSONResponse(status_code=422, content={"detail": "No has especificado ningún campo del evento"})
                
        updated_document = DatabaseConnection.update_document_id("eventos", id, non_none_fields, hasDate=True if evento.timestamp is not None else False)
        if updated_document is None:
            return JSONResponse(status_code=404, content={"detail": "No se ha encontrado un evento con ese ID. No se ha editado nada"})
                
        json_serializable_document = jsonable_encoder(updated_document)

        return JSONResponse(
            status_code=200,
            content={
                "detail": "El evento se ha editado correctamente",
                "result": json_serializable_document
            }
        )
    
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=f"Error de formato: {str(ve)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar el evento: {str(e)}")


@router.delete("/" + endpoint_name + "/{id}", tags=["Eventos CRUD endpoints"], response_model=EventoDeleteResponse)
async def delete_evento(id: str = Path(description="ID del evento")):
    """Eliminar un evento por su ID."""

    try:
        count = DatabaseConnection.delete_document_id("eventos", id)
        if count == 0:
            return JSONResponse(status_code=404, content={"detail": "No se ha encontrado un evento con ese ID. No se ha borrado nada."})
        
        return JSONResponse(status_code=200, content={"details": "El evento se ha eliminado correctamente"},
                            headers={"Content-Type": "application/json"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar el evento: {str(e)}")
    
