from fastapi import FastAPI, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from pydantic import BaseModel
from database import VideoDB
from code import CodedSet, gen_code

# Pydantic model for user login
class User(BaseModel):
    username: str
    password: str

# Pydantic model for token
class Token(BaseModel):
    access_token: str
    token_type: str | None = None

class VideoUpload(BaseModel):
    access_token: str
    video_ref: str | None = None

# In-memory "database" for demo purposes
users_db = {
    "testuser": {
        "username": "testuser",
        "hashed_pw": "$2b$12$U5lJlYI1aDxlJGTvgTLFzOw3DdUoh6hZZv/njOSVYZ2lDOLkzkRrO",  # "testpassword" hashed using bcrypt
    }
}

# Configuration
SECRET_KEY = "a_very_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Initialize FastAPI app and OAuth2PasswordBearer
db = VideoDB()
db.create_vid_table()
app = FastAPI()
admin_token = "QBP7-4OEE-PIP5-C37L"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
token_set = CodedSet()

# Function to verify password hash
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Function to hash password
def hash_password(password):
    return pwd_context.hash(password)

# Function to authenticate user
def authenticate_user(username: str, password: str):
    user = users_db.get(username)
    if user is None:
        return None
    if not verify_password(password, user["hashed_password"]):
        return None
    return user

@app.post("/create-user", status_code=200)
async def create_user(form_data: User, response: Response):
    if form_data.username in users_db.keys():
        response.status_code = 400
        return {"message": "Username exists"}
    hash = hash_password(form_data.password)
    users_db[form_data.username] = {"username": form_data.username, "hashed-pw": hash}
    access_token = token_set.add_new_entry(hash)
    return {"access_token": access_token, "token_type": "bearer", "username": form_data.username}

# Login endpoint
@app.post("/login", status_code = 200)
async def login_for_access_token(form_data: User, response: Response):
    user = authenticate_user(form_data.username, form_data.password)
    if user is None:
        response.status_code = 401
        return {'message': 'Invalid credentials'}
    access_token = token_set.get_code(users_db[form_data.username]['hashed_pw'])
    return {"access_token": access_token, "token_type": "bearer", "username": form_data.username}

# Endpoint to access a protected resource
@app.post("/protected-users")
async def read_protected_data(token: Token, response: Response):
    if token.access_token == admin_token:
        return users_db
    else:
        response.code = 404
        return {'message': 'Not authorized'}

@app.post("/all-videos")
async def get_all_videos(token: Token, response: Response):
    if token.access_token == admin_token:
        df = db.load_all_pd()
        return df.to_dict('records')
    else:
        response.code = 404
        return {'message': 'Not authorized'}

@app.post("/upload-vid", status_code=200)
async def read_protected_data(form_data: VideoUpload, response: Response):
    if token_set.is_valid(form_data.access_token):
        new_entry = {
            'token': form_data.access_token,
            'vid_ref': form_data.video_ref,
        }
        entry_id = db.insert_tuple(new_entry)['id']
        if entry_id == -1:
            response.status_code = 400
            return {'message': 'Problem uploading vid'}
        return {'message': 'Successfully added video to database', 'entry_id': entry_id}
    else:
        response.status_code = 400
        return {'message': 'Invalid access token'}

@app.post("/get-user-vids", status_code=200)
async def read_protected_data(form_data: VideoUpload):
    df = db.load_query_pd('token', form_data.access_token)
    return df.to_dict('records')