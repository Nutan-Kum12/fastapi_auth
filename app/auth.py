from fastapi import APIRouter, HTTPException, Depends
from app.schemas import UserCreate, UserLogin, ShowUser
from app.database import user_collection
from app.utils import hash_password, verify_password, create_access_token, decode_token
from fastapi.security import OAuth2PasswordBearer
from bson import ObjectId

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Signup
@router.post("/signup", response_model=ShowUser)
async def signup(user: UserCreate):
    if await user_collection.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Email already registered")
    user_dict = user.dict()
    user_dict["hashed_password"] = hash_password(user.password)
    del user_dict["password"]
    await user_collection.insert_one(user_dict)
    return ShowUser(**user_dict)

# Login
@router.post("/login")
async def login(user: UserLogin):
    db_user = await user_collection.find_one({"email": user.email})
    if not db_user or not verify_password(user.password, db_user["hashed_password"]):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    token = create_access_token(data={"email": user.email})
    return {"access_token": token, "token_type": "bearer"}

# Get user details
@router.get("/me", response_model=ShowUser)
async def get_user(token: str = Depends(oauth2_scheme)):
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = await user_collection.find_one({"email": payload["email"]})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return ShowUser(**user)
