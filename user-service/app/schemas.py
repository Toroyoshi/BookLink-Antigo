from pydantic import BaseModel, EmailStr, Field, ConfigDict

class RegisterIn(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    email: EmailStr
    password: str = Field(min_length=4, max_length=200)
    role: str = Field(pattern=r"^(student|docente|staff)$")

class LoginIn(BaseModel):
    email: EmailStr
    password: str

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str
    is_active: bool
    model_config = ConfigDict(from_attributes=True) #router users.py converte automaticamente usando isto
    