from datetime import datetime
from pymongo import MongoClient, errors
from pymongo.server_api import ServerApi
from bson.objectid import ObjectId
import logging
import os
from dotenv import load_dotenv

# Configuración del registro de errores
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
load_dotenv()

class DatabaseConnection:
    """
    DatabaseConnection es una clase que maneja la conexión a una base de datos MongoDB y proporciona métodos para realizar operaciones CRUD (Crear, Leer, Actualizar, Eliminar) en las colecciones de la base de datos.
    Métodos de Clase:
    - connect(cls): Establece la conexión a la base de datos.
    - get_collection(cls, collection_name): Obtiene una colección específica de la base de datos.
    - create_document(cls, collection_name, document): Crea un nuevo documento en la colección especificada.
    - read_document(cls, collection_name, document_id): Lee un documento por su ID.
    - update_document(cls, collection_name, document_id, updated_fields): Actualiza un documento existente con los campos proporcionados.
    - delete_document(cls, collection_name, document_id): Elimina un documento por su ID.
    - close_connection(cls): Cierra la conexión a la base de datos.
    Atributos de Clase:
    - _client: Instancia del cliente MongoDB.
    - _db: Instancia de la base de datos MongoDB.
    Excepciones:
    - errors.ConnectionError: Se lanza si hay un error al establecer la conexión a la base de datos.
    - errors.PyMongoError: Se lanza si hay un error al realizar operaciones CRUD.
    - errors.InvalidId: Se lanza si el ID del documento no es válido.
    """

    _client = None
    _db = None

    @classmethod
    def connect(cls):
        """
        Establish a connection to the database.

        This method initializes a MongoDB client using the provided URI and
        certificate key file. If the connection is successful, it sets the
        client and database attributes for the class. If the connection fails,
        it logs an error message and raises a ConnectionError.

        Raises:
            errors.ConnectionError: If there is an error connecting to the database.
        """
        """Establecer la conexión a la base de datos."""
        if cls._client is None:
            try:
                uri = os.getenv('URI')
                cls._client = MongoClient(uri,server_api=ServerApi('1'))
                cls._db = cls._client['mimapa']
                logger.info("Conexión establecida a la base de datos.")
            except errors.ConnectionFailure as e:
                logger.error(f"Error de conexión a la base de datos: {e}")
                raise

    @classmethod
    def get_collection(cls, collection_name):
        """Obtener una colección específica de la base de datos."""
        cls.connect()
        return cls._db[collection_name]
    
    @classmethod
    def count_documents(cls, collection_name, query):
        collection = cls.get_collection(collection_name)
        return float(collection.count_documents(query))
    
    @classmethod
    def get_collection_fields(cls, collection_name, projection = None, hasDate = False):
        """Obtener una colección específica de la base de datos y mostrar los campos elegidos."""
        collection = cls.get_collection(collection_name)
        try:
            documents = collection.find(projection=projection)
            if documents is None:
                logger.warning(f"Colección no encontrada.")
                return []
            
            if hasDate:
                return [{**d, '_id': d['_id'].binary.hex(),'timestamp': d['timestamp'].strftime('%Y-%m-%d %H:%M:%S') if 'timestamp' in d else None} for d in documents]
            
            return [{**d, '_id': d['_id'].binary.hex()} for d in documents]

        except Exception as e:
            logger.error(f"ID de documento no válido: {e}")
            raise
    
    @classmethod
    def create_document(cls, collection_name, document, hasDate = False):
        """Crear un nuevo documento en la colección."""
        collection = cls.get_collection(collection_name)
        try:
            result = collection.insert_one(document)
            document['_id'] = document['_id'].binary.hex()
            if hasDate:
                document['timestamp'] = document['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
            logger.info(f"Documento creado con ID: {result.inserted_id}")
            return document['_id']
        except errors.PyMongoError as e:
            logger.error(f"Error al crear el documento: {e}")
            raise

    @classmethod
    def create_array_element_id(cls, collection_name, document_id, array_field, element):
        """Crear un nuevo elemento en un arreglo de un documento existente, a partir de un ID."""
        collection = cls.get_collection(collection_name)
        try:
            result = collection.update_one(
                {"_id": ObjectId(document_id)},
                {"$push": {array_field: element}}
            )
            if result.modified_count == 0:
                logger.warning(f"No se encontró el documento con ID {document_id} para agregar un elemento.")
                raise ValueError("Documento no encontrado para el ID proporcionado.")
            
            logger.info(f"Elemento agregado al documento con ID {document_id}.")
            return True
        except ValueError as e:
            raise e
        except errors.PyMongoError as e:
            logger.error(f"Error al agregar un elemento al documento: {e}")
            raise RuntimeError("Error de base de datos al agregar el elemento.")

    @classmethod
    def update_array_element_id(cls, collection_name, document_id, array_field, element_query, updated_fields):
        """Actualizar un elemento de un arreglo en un documento existente, a partir de un ID."""
        collection = cls.get_collection(collection_name)
        try:
            result = collection.update_one(
                {"_id": ObjectId(document_id), array_field: element_query},
                {"$set": {f"{array_field}.$": updated_fields}}
            )
            if result.modified_count == 0:
                logger.warning(f"No se encontró el documento con ID {document_id} para actualizar un elemento.")
                raise ValueError("Documento no encontrado para el ID proporcionado.")
            
            logger.info(f"Elemento actualizado en el documento con ID {document_id}.")
            return True
        except ValueError as e:
            raise e
        except errors.PyMongoError as e:
            logger.error(f"Error al actualizar un elemento en el documento: {e}")
            raise RuntimeError("Error de base de datos al actualizar el elemento.")
        

    @classmethod
    def delete_array_element_id(cls, collection_name, document_id, array_field, element_query):
        """Eliminar un elemento de un arreglo en un documento existente, a partir de un ID."""
        collection = cls.get_collection(collection_name)
        try:
            result = collection.update_one(
                {"_id": ObjectId(document_id)},
                {"$pull": {array_field: element_query}}
            )
            if result.modified_count == 0:
                logger.warning(f"No se encontró el documento con ID {document_id} para eliminar un elemento.")
                raise ValueError("Documento no encontrado para el ID proporcionado.")
            
            logger.info(f"Elemento eliminado del documento con ID {document_id}.")
            return True
        except ValueError as e:
            raise e
        except errors.PyMongoError as e:
            logger.error(f"Error al eliminar un elemento del documento: {e}")
            raise RuntimeError("Error de base de datos al eliminar el elemento.")

    @classmethod
    def read_document_id(cls, collection_name, document_id : str, projection = None, hasDate = False): # CAMBIO
        """Leer un documento por su ID."""
        collection = cls.get_collection(collection_name)
        try:
            document = collection.find_one({"_id": ObjectId(document_id)}, projection)
            if document is None:
                logger.warning(f"Documento con ID {document_id} no encontrado.")
            else:
                document['_id'] = document_id
                if hasDate:
                    document['timestamp'] = document['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
            return document
        except Exception as e:
            logger.error(f"ID de documento no válido: {e}")
            raise

    @classmethod
    def find_documents(cls, collection_name, query=None, projection=None, sort=None, offset=0, limit=10):
        """
        Busca múltiples documentos en una colección con soporte para proyección, orden y paginación.

        :param collection_name: Nombre de la colección donde buscar
        :param query: Diccionario de búsqueda (filtro)
        :param projection: Diccionario de proyección para campos específicos
        :param sort: Lista de criterios de ordenamiento [(campo, orden), ...]
        :param offset: Número de documentos a saltar (paginación)
        :param limit: Número máximo de documentos a devolver
        :return: Lista de documentos encontrados
        """
        try:
            collection = cls.get_collection(collection_name)
            cursor = collection.find(query or {}, projection)

            if sort:
                cursor = cursor.sort(sort)

            if offset:
                cursor = cursor.skip(offset)

            if limit:
                cursor = cursor.limit(limit)

            documents = list(cursor)
            
            # Convertir ObjectId a string
            for document in documents:
                document['_id'] = str(document['_id'])

            return documents

        except Exception as e:
            logger.error(f"Error al buscar documentos: {e}")
            raise

    
    @classmethod
    def query_document(cls, collection_name, document_query, projection=None, sort_criteria=None, skip=0, limit=0, id_list=None, hasDate=False): # CAMBIO
        """Realizar query según los parámetros."""
        collection = cls.get_collection(collection_name)
        try:
            if id_list:
                document_query['_id'] = {"$in": id_list}

            logger.warning(f"Query para la colección '{collection_name}': {document_query}")

            documents = collection.find(document_query, projection)

            if sort_criteria:
                documents = documents.sort(sort_criteria)
            if limit > 0:
                documents.limit(limit)
            if skip > 0:
                documents.skip(skip)

            if documents is None:
                logger.warning(f"Documento con {document_query} no encontrado.")
                return []

            if hasDate:

            # Convertir documentos a lista y manejar correctamente el campo 'timestamp'
                return [
                    {
                        **d,
                        '_id': d['_id'].binary.hex(),
                        'timestamp': d['timestamp'].isoformat() if isinstance(d.get('timestamp'), datetime) else d.get('timestamp')
                    }
                    for d in documents
                ]
    
            else:
                return [{**d, '_id': d['_id'].binary.hex()} for d in documents]
        except Exception as e:
            logger.error(f"Error al realizar la consulta: {e}")
            raise


    @classmethod
    def update_document_id(cls, collection_name, document_id, updated_fields, hasDate = False):
        """Actualizar un documento existente a partir de su ID y devolver el documento actualizado."""
        collection = cls.get_collection(collection_name)
        try:
            updated_document = collection.find_one_and_update(
                {"_id": ObjectId(document_id)},
                {"$set": updated_fields},
                return_document=True 
            )
            
            if updated_document is None:
                logger.warning(f"No se encontró el documento con ID {document_id} para actualizar.")
            else:
                updated_document["_id"] = updated_document['_id'].binary.hex()
                if hasDate:
                    updated_document['timestamp'] = updated_document['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
                logger.info(f"Documento con ID {document_id} actualizado.")

            return updated_document

        except errors.PyMongoError as e:
            logger.error(f"Error al actualizar el documento: {e}")
            raise

    @classmethod
    def delete_document_id(cls, collection_name, document_id):
        """Eliminar un documento por su ID."""
        collection = cls.get_collection(collection_name)
        try:
            result = collection.delete_one({"_id": ObjectId(document_id)})
            if result.deleted_count == 0:
                logger.warning(f"No se encontró el documento con ID {document_id} para eliminar.")
            else:
                logger.info(f"Documento con ID {document_id} eliminado.")
            return result.deleted_count
        except Exception as e:
            logger.error(f"ID de documento no válido: {e}")
            raise

    @classmethod
    def close_connection(cls):
        """Cerrar la conexión a la base de datos."""
        if cls._client is not None:
            cls._client.close()
            cls._client = None
            cls._db = None
            logger.info("Conexión a la base de datos cerrada.")

    @classmethod
    def is_valid_objectid(cls, id: str) -> bool:
        try:
            ObjectId(id)
            return True
        except Exception:
            return False

# Main para conectarse

if __name__ == '__main__':
    DatabaseConnection.connect()
    DatabaseConnection.close_connection()