import os
from typing import Optional, Dict
from fastapi import Request, HTTPException
from bson import ObjectId

class APIUtils:
    _is_docker = os.path.exists('/.dockerenv')
    _endpoints = {
        "wikis": {
            "host": "wiki-content-manager" if _is_docker else "localhost",
            "port": 8000 if _is_docker else 8000
        },
        "articles": {
            "host": "article-content-manager" if _is_docker else "localhost",
            "port": 8000 if _is_docker else 8001
        },
        "comments": {
            "host": "comments-content-manager" if _is_docker else "localhost",
            "port": 8000 if _is_docker else 8002
        }
    }

    @classmethod
    def get_endpoints(cls) -> str:
        """Obtiene la lista de endpoints existentes"""
        return cls._endpoints.keys()

    @classmethod
    def get_service_base_url(cls, service: str) -> str:
        """Obtener la URL base para un servicio específico."""
        if service not in cls.get_endpoints():
            raise ValueError(f"Service '{service}' not found in endpoints.")
        
        host = cls._endpoints[service]["host"]
        port = cls._endpoints[service]["port"]
        return f"http://{host}:{port}"

    @classmethod
    def get_service_url(cls, version: str, service: str) -> str:
        """Construir la URL para el servicio y versión especificados."""
        return f"{cls.get_service_base_url(service)}/api/{version}/{service}"

    @classmethod
    def construct_url(cls, version: str, service: str, path: str) -> str:
        """Construir la URL completa con una ruta específica."""
        return f"{cls.get_service_url(version, service)}/{path}".rstrip("/")

    @classmethod
    def check_accept_json(cls, request: Request):
        """Verificar si la cabecera Accept contiene 'application/json'."""
        accepted = request.headers.get("Accept", "")
        if "application/json" not in accepted and "*/*" not in accepted:
            raise HTTPException(status_code=406, detail="La cabecera Accept debe incluir 'application/json'")

    @classmethod
    def check_content_type_json(cls, request: Request):
        """Verificar si la cabecera Content-Type contiene 'application/json'."""
        if "application/json" not in request.headers.get("Content-Type", ""):
            raise HTTPException(status_code=415, detail="La cabecera Content-Type debe incluir 'application/json'")

    @classmethod
    def check_id(cls, id: str):
        """Verificar si el ID es válido usando la función de validación del DatabaseConnection."""
        if not cls.is_valid_objectid(id):
            raise HTTPException(status_code=400, detail="El ID proporcionado no es válido.")

    @classmethod
    def add_regex(cls, query: Dict[str, Dict], field: str, value: Optional[str]):
        """Agregar un filtro regex a la consulta si el valor no es None."""
        if value:
            query[field] = {"$regex": value, "$options": 'i'}

    @classmethod
    def build_projection(cls, fields: Optional[str]) -> Optional[dict]:
        """Construir el diccionario de proyección para los campos especificados."""
        if fields:
            return {field: 1 for field in fields.split(',')}
        return None

    @classmethod
    def build_sort_criteria(cls, sort: Optional[str]) -> Optional[list]:
        """Construir los criterios de ordenación a partir de la cadena de campos."""
        if sort:
            return [(field, 1) for field in sort.split(',')]
        return None

    @classmethod
    async def get(cls, client, url):
        response = await client.get(url, headers={"Accept" : "application/json"})
        return response.json()

    @classmethod
    def is_valid_objectid(cls, id: str) -> bool:
        """Devuelve True si es un id válido o False si no lo es"""
        try:
            ObjectId(id)
            return True
        except Exception:
            return False
