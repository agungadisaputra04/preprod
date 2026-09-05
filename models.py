from pydantic import BaseModel


class User(BaseModel):
    nama: str
    umur: int


class UserUpdate(BaseModel):
    nama: str
    umur: int


class UserPatch(BaseModel):
    nama: str | None = None
    umur: int | None = None


class UserResponse(BaseModel):
    id: int
    nama: str
    umur: int


class UserCreateResponse(BaseModel):
    message: str
    data: UserResponse


class UserListResponse(BaseModel):
    total: int
    data: list[UserResponse]


class UserUpdateResponse(BaseModel):
    message: str
    data: UserResponse


class UserPatchResponse(BaseModel):
    message: str
    data: UserResponse


class UserDeleteResponse(BaseModel):
    message: str
    data: UserResponse
