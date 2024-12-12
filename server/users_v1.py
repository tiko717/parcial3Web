import httpx

from typing import List
from fastapi import APIRouter, HTTPException, Query, Request, Path
from fastapi.responses import JSONResponse
import json
from bson.objectid import ObjectId

from models.user_model import User, Review, UserCreate, UserUpdate, UserDeleteResponse
from db_connection import DatabaseConnection
from api_utils import APIUtils
from fastapi import Path, HTTPException
from fastapi.responses import JSONResponse

router = APIRouter()

client = httpx.AsyncClient()

endpoint_name = "users"
version = "v1"

@router.get("/" + endpoint_name, tags=["user CRUD endpoints"], response_model=List[User])
async def get_users(
    request: Request,
    email: str | None = Query(None, description="Email del usuario"),
    name: str | None = Query(None, description="Nombre del usuario"),
    surname: str | None = Query(None, description="Apellido del usuario"),
    description: str | None = Query(None, description="Descripción del usuario"),
    userName: str | None = Query(None, description="Nombre de usuario del usuario"),
    oauthId: str | None = Query(None, description="ID de autenticación del usuario"),
    oauthProvider: str | None = Query(None, description="Proveedor de autenticación del usuario"),
    oauthToken: str | None = Query(None, description="Token de autenticación del usuario"),
    profilePicture: str | None = Query(None, description="Foto de perfil del usuario"),
    fields: str | None = Query(None, description="Campos específicos a devolver"),
    sort: str | None = Query(None, description="Campos por los que ordenar, separados por comas"),
    offset: int = Query(default=0, description="Índice de inicio para los resultados de la paginación"),
    limit: int = Query(default=10, description="Cantidad de usuarios a devolver, por defecto 10"),
    hateoas: bool | None = Query(None, description="Incluir enlaces HATEOAS")
):
    APIUtils.check_accept_json(request)

    try:
        projection = APIUtils.build_projection(fields)
        sort_criteria = APIUtils.build_sort_criteria(sort)

        query = {}
        if email is not None:
            query["email"] = email
        if name is not None:
            query["name"] = name
        if surname is not None:
            query["surname"] = surname
        if oauthId is not None:
            query["oauthId"] = oauthId
        if oauthProvider is not None:
            query["oauthProvider"] = oauthProvider
        if profilePicture is not None:
            query["profilePicture"] = profilePicture       
        if description is not None:
            query["description"] = description
        if userName is not None:
            query["userName"] = userName


        users = DatabaseConnection.query_document("user", query, projection, sort_criteria, offset, limit)

        total_count = len(users)

        if hateoas:
            for user in users:
                user["href"] = f"/api/{version}/{endpoint_name}/{user['_id']}"

        return JSONResponse(status_code=200, content=users, 
                            headers={"Accept-Encoding": "gzip", "X-Total-Count": str(total_count)})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al buscar el usuario: {str(e)}")

@router.get("/" + endpoint_name + "/{id}", tags=["user CRUD endpoints"], response_model=User)
async def get_users_by_id(request: Request,
                        id: str = Path(description="ID del usuario", min_length=24, max_length=24),
                        oauth: bool = Query(False, description="Incluir información de autenticación"),
                        fields: str | None = Query(None, description="Campos específicos a devolver")):
    APIUtils.check_id(id)
    APIUtils.check_accept_json(request)
    projection = {}
    try:
        projection = APIUtils.build_projection(fields)
        if oauth:
            projection["oauthId"] = 1
            projection["oauthProvider"] = 1      
        
        user = DatabaseConnection.read_document("user", id, projection)
        if user is None:
            return JSONResponse(status_code=404, content={"detail": f"Usuario con ID {id} no encontrado"})

        return JSONResponse(status_code=200, content=user,
                            headers={"Content-Type": "application/json", "X-Total-Count": "1"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener el usuario: {str(e)}")

#añadir review a un usuario
@router.post("/" + endpoint_name + "/{id}/review", tags=["user CRUD endpoints"], response_model=User)
async def add_review_to_user(review: Review, id: str = Path(description="ID del usuario", min_length=24, max_length=24)):
    APIUtils.check_id(id)

    try:
        review_dict = review.model_dump()
        if review.user is None or review.rating is None:
            return JSONResponse(status_code=400, content={"detail": "El usuario y la valoración son obligatorios"}) 
        if review.rating < 1 or review.rating > 5:
            return JSONResponse(status_code=400, content={"detail": "La valoración debe estar entre 1 y 5"})
        
        user = DatabaseConnection.read_document("user", id)
        if user is None:
            return JSONResponse(status_code=404, content={"detail": f"Usuario con ID {id} no encontrado"})
        reviwer = DatabaseConnection.read_document("user", review_dict["user"])
        if reviwer is None:
            return JSONResponse(status_code=404, content={"detail": f"Usuario con ID {review_dict['user']} no encontrado"})

        if not user["reviews"]:  # Si user["reviews"] está vacío
            user["reviews"].append(review_dict)
        else:
            review_found = False
            for i in range(len(user["reviews"])):
                if user["reviews"][i]["user"] == review_dict["user"]:
                    user["reviews"][i] = review_dict  
                    review_found = True
                    break  
            if not review_found:
                user["reviews"].append(review_dict)  


        #convertir a obejct id todos los usuarios de las reviews
        for i in range(len(user["reviews"])):
            user["reviews"][i]["user"] = ObjectId(user["reviews"][i]["user"])

        changes = {"reviews": user["reviews"]}
        upadatedUser = DatabaseConnection.update_document("user", id, changes)
        reviews = upadatedUser["reviews"]
        if len(reviews) == 0:
            return JSONResponse(status_code=200, content={"detail": "El usuario no tiene reviews", "average": 0})
        
        total = 0
        for review in reviews:
            total += review["rating"]

        average = total / len(reviews)
        average = round(average, 2)
        newReview = {"totalRates": len(reviews), "ratingAverage": average}
        
    
        return JSONResponse(status_code=200, content=newReview,
                            headers={"Content-Type": "application/json", "X-Total-Count": "1"})

       
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear la review: {str(e)}")

#obtener media de las reviews de un usuario
@router.get("/" + endpoint_name + "/{id}/review-average", tags=["user CRUD endpoints"], response_model=User)
async def get_review_average(id: str = Path(description="ID del usuario", min_length=24, max_length=24)):
    APIUtils.check_id(id)

    try:
        user = DatabaseConnection.read_document("user", id)
        if user is None:
            return JSONResponse(status_code=404, content={"detail": f"Usuario con ID {id} no encontrado"})

        reviews = user["reviews"]
        if len(reviews) == 0:
            return JSONResponse(status_code=200, content={"detail": "El usuario no tiene reviews", "average": 0})
        
        total = 0
        for review in reviews:
            total += review["rating"]
        
        average = total / len(reviews)
        average = round(average, 2)
        return JSONResponse(status_code=200, content={"detail": f"La media de las reviews del usuario {id} es {average}", "average": average})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener la media de las reviews: {str(e)}")

@router.post("/" + endpoint_name, tags=["user CRUD endpoints"], response_model=User)
async def create_users(user: UserCreate, request: Request):
    APIUtils.check_content_type_json(request)

    try:
        body_dict = user.model_dump()
        if not check_unique_username(body_dict["userName"]):
            return JSONResponse(status_code=400, content={"detail": "El nombre de usuario ya existe"})
        body_dict["wantEmails"] = True
        body_dict["reviews"] = []

        DatabaseConnection.create_document("user", body_dict)
        return JSONResponse(status_code=201, content={"detail": "El usuario se ha creado correctamente", "result": body_dict},
                            headers={"Location": f"/api/{version}/{endpoint_name}/{body_dict['_id']}"} )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear el usuario: {str(e)}")

@router.put("/" + endpoint_name + "/{id}", tags=["user CRUD endpoints"], response_model=User)
async def update_users(user: UserUpdate, id: str = Path(description="ID del usuario", min_length=24, max_length=24)):
    APIUtils.check_id(id)

    try:
        updated_fields = user.model_dump()
        if "userName" in updated_fields and not check_unique_username(updated_fields["userName"]):
            return JSONResponse(status_code=400, content={"detail": "El nombre de usuario ya existe"})
        DatabaseConnection.update_document("user", id, updated_fields)
        return JSONResponse(status_code=200, content={"detail": f"El usuario ({id}) se ha actualizado correctamente."})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar el usuario: {str(e)}")

#fidn by oauthId
@router.get("/" + endpoint_name + "/oauth/{oauthId}", tags=["user CRUD endpoints"], response_model=User)
async def get_users_by_oauthId(request: Request,
                        oauthId: str = Path(description="ID de autenticación del usuario"),
                        oauthProvider: str = Query(None, description="Proveedor de autenticación del usuario"),
                        fields: str | None = Query(None, description="Campos específicos a devolver")):
    APIUtils.check_accept_json(request)
    projection = {}
    try:
        projection = APIUtils.build_projection(fields)
        query = {}
        if oauthId is not None:
            query["oauthId"] = oauthId
        if oauthProvider is not None:
            query["oauthProvider"] = oauthProvider
        
        user = DatabaseConnection.query_document("user", query, projection)
        if user is None or len(user) == 0:
            return JSONResponse(status_code=404, content={"detail": f"Usuario con oauthId {oauthId} no encontrado"})

        return JSONResponse(status_code=200, content=user,
                            headers={"Content-Type": "application/json", "X-Total-Count": "1"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener el usuario: {str(e)}")

@router.delete("/" + endpoint_name + "/{id}", tags=["user CRUD endpoints"], response_model=UserDeleteResponse)
async def delete_users(id: str = Path(description="ID del usuario", min_length=24, max_length=24)):
    APIUtils.check_id(id)

    try:
        count = DatabaseConnection.delete_document("user", id)
        if count == 0:
            return JSONResponse(status_code=404, content={"detail": "No se ha encontrado un usuario con ese ID. No se ha borrado nada."})

        return JSONResponse(status_code=200, content={"detail": f"El usuario ({id}) se ha eliminado correctamente."})
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar el usuario: {str(e)}")

#obtrenr perfil completo con reviews totales y media
@router.get("/" + endpoint_name + "/{id}/profile", tags=["user CRUD endpoints"], response_model=User)
async def get_user_profile(id: str = Path(description="ID del usuario", min_length=24, max_length=24)):
    APIUtils.check_id(id)
    projection = {}
    projection["oauthId"] = 0
    projection["oauthProvider"] = 0      
    
    
    try:
        user = DatabaseConnection.read_document("user", id, projection)
        if user is None:
            return JSONResponse(status_code=404, content={"detail": f"Usuario con ID {id} no encontrado"})

        reviews = user["reviews"]
        if len(reviews) == 0:
            user["ratingAverage"] = 0
            user["totalRates"] = 0
            return JSONResponse(status_code=200, content=user,
                            headers={"Content-Type": "application/json", "X-Total-Count": "1"})        
        total = 0
        for review in reviews:
            total += review["rating"]
        
        average = total / len(reviews)
        average = round(average, 2)
        user["ratingAverage"] = average
        user["totalRates"] = len(reviews)

        return JSONResponse(status_code=200, content=user,
                            headers={"Content-Type": "application/json", "X-Total-Count": "1"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener el perfil completo del usuario: {str(e)}")

@router.options("/" + endpoint_name, tags=["user OPTIONS endpoints"])
async def options_notifications():
    return JSONResponse(
        status_code=200,
        content={"methods": ["GET", "OPTIONS"]},
        headers={"Allow": "GET, POST, OPTIONS"}
    )

@router.options("/" + endpoint_name + "/{id}", tags=["user OPTIONS endpoints"])
async def options_notifications_by_id():
    return JSONResponse(
        status_code=200,
        content={"methods": ["GET", "PUT", "DELETE", "OPTIONS"]},
        headers={"Allow": "GET, PUT, DELETE, OPTIONS"}
    )

#fun to check if the userName is unique
def check_unique_username(userName):
    query = {"userName": userName}
    user = DatabaseConnection.query_document("user", query)
    if len(user) > 0:
        return False
    return True
