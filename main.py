from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse
import psycopg
import logging

from database import get_connection

from models import (
    User,
    UserUpdate,
    UserPatch,
    UserResponse,
    UserCreateResponse,
    UserListResponse,
    UserUpdateResponse,
    UserPatchResponse,
    UserDeleteResponse,
)

from repository import (
    create_user,
    get_users,
    get_user_by_id,
    update_user,
    patch_user,
    delete_user,
)


app = FastAPI()


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s"
)

logger = logging.getLogger(__name__)


def get_connection_factory():
    return get_connection


@app.exception_handler(psycopg.Error)
async def database_exception_handler(request, exc):
    logger.exception(
        "Database error on %s %s",
        request.method,
        request.url.path
    )

    return JSONResponse(
        status_code=500,
        content={
            "detail": "Terjadi kesalahan pada server"
        }
    )

@app.get("/")
def root():
    return {
        "message": "API is running",
        "version": "1.0"
    }

@app.get("/version")
def get_version():
    return {
        "version": "1.0"
    }

@app.post(
    "/user",
    status_code=201,
    response_model=UserCreateResponse
)
def create_user_endpoint(
    user: User,
    connection_factory=Depends(get_connection_factory)
):
    new_user = create_user(
        user.nama,
        user.umur,
        connection_factory
    )

    return {
        "message": "User berhasil disimpan",
        "data": {
            "id": new_user[0],
            "nama": new_user[1],
            "umur": new_user[2]
        }
    }


@app.get(
    "/users",
    response_model=UserListResponse
)
def get_users_endpoint(
    connection_factory=Depends(get_connection_factory)
):
    users = get_users(connection_factory)

    data = []

    for user in users:
        data.append({
            "id": user[0],
            "nama": user[1],
            "umur": user[2]
        })

    return {
        "total": len(data),
        "data": data
    }


@app.get(
    "/users/{user_id}",
    response_model=UserResponse
)
def get_user_endpoint(
    user_id: int,
    connection_factory=Depends(get_connection_factory)
):
    user = get_user_by_id(
        user_id,
        connection_factory
    )

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User tidak ditemukan"
        )

    return {
        "id": user[0],
        "nama": user[1],
        "umur": user[2]
    }


@app.put(
    "/users/{user_id}",
    response_model=UserUpdateResponse
)
def update_user_endpoint(
    user_id: int,
    user: UserUpdate,
    connection_factory=Depends(get_connection_factory)
):
    updated_user = update_user(
        user_id,
        user.nama,
        user.umur,
        connection_factory
    )

    if updated_user is None:
        raise HTTPException(
            status_code=404,
            detail="User tidak ditemukan"
        )

    return {
        "message": "User berhasil diupdate",
        "data": {
            "id": updated_user[0],
            "nama": updated_user[1],
            "umur": updated_user[2]
        }
    }


@app.patch(
    "/users/{user_id}",
    response_model=UserPatchResponse
)
def patch_user_endpoint(
    user_id: int,
    user: UserPatch,
    connection_factory=Depends(get_connection_factory)
):
    updated_user = patch_user(
        user_id,
        user.nama,
        user.umur,
        connection_factory
    )

    if updated_user is None:
        raise HTTPException(
            status_code=404,
            detail="User tidak ditemukan"
        )

    return {
        "message": "User berhasil diupdate sebagian",
        "data": {
            "id": updated_user[0],
            "nama": updated_user[1],
            "umur": updated_user[2]
        }
    }


@app.delete(
    "/users/{user_id}",
    response_model=UserDeleteResponse
)
def delete_user_endpoint(
    user_id: int,
    connection_factory=Depends(get_connection_factory)
):
    deleted_user = delete_user(
        user_id,
        connection_factory
    )

    if deleted_user is None:
        raise HTTPException(
            status_code=404,
            detail="User tidak ditemukan"
        )

    return {
        "message": "User berhasil dihapus",
        "data": {
            "id": deleted_user[0],
            "nama": deleted_user[1],
            "umur": deleted_user[2]
        }
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }
