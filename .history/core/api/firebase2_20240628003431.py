from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, EmailStr
import firebase_admin
from firebase_admin import credentials, auth, firestore
import requests

# Initialize Firebase Admin SDK
cred = credentials.Certificate("path/to/firebase.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

class FirebaseUserManager:
    def __init__(self):
        self.api_key = "AIzaSyBdZ_V7ZNxnMqajCsn3o-Tpq2s7ljeB-RY"

    def create_user(self, email: str, password: str):
        try:
            user = auth.create_user(email=email, password=password)
            return {"localId": user.uid}
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    def sign_in(self, email: str, password: str):
        try:
            url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={self.api_key}"
            payload = {"email": email, "password": password, "returnSecureToken": True}
            response = requests.post(url, data=payload)
            if response.status_code == 200:
                data = response.json()
                return {"idToken": data["idToken"]}
            else:
                raise HTTPException(status_code=400, detail=response.json()["error"]["message"])
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    def get_current_user(self, token: str) -> str:
        try:
            decoded_token = auth.verify_id_token(token)
            user_id = decoded_token['uid']
            return user_id
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
            )

    def add_word(self, word: str, traduction: str, example: str, vote: int, source_id: str, definition: str, know: bool, type: str, user_id: str):
        try:
            doc_ref = db.collection("users").document(user_id).document()
            doc_ref.set({
                'word': word,
                'traduction': traduction,
                'example': example,
                'vote': vote,
                'source_id': source_id,
                'definition': definition,
                'know': know,
                'type': type,
            })
            return {"message": "Word added successfully"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def get_words(self, user_id: str):
        try:
            words_ref = db.collection("users").document(user_id)
            words = words_ref.stream()
            return [word.to_dict() for word in words]
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def update_word(self, user_id: str, word_id: str, update_data: dict):
        try:
            doc_ref = db.collection("users").document(user_id).collection("words").document(word_id)
            doc_ref.update(update_data)
            return {"message": "Word updated successfully"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def delete_word(self, user_id: str, word_id: str):
        try:
            doc_ref = db.collection("users").document(user_id).collection("words").document(word_id)
            doc_ref.delete()
            return {"message": "Word deleted successfully"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

# Pydantic models for request validation
class SentenceRequest(BaseModel):
    sentence: str

class SignupRequest(BaseModel):
    email: EmailStr
    password: str

class AddWord(BaseModel):
    idToken: str
    word: str
    traduction: str
    example: str
    vote: int
    source_id: str
    definition: str
    know: bool
    type: str

class UpdateWord(BaseModel):
    idToken: str
    word_id: str
    update_data: dict

app = FastAPI()
firebase = FirebaseUserManager()

@app.get("/")
async def read_root():
    return {"message": "Welcome to FastAPI"}

@app.post("/signup/")
async def signup(request: SignupRequest):
    email = request.email
    password = request.password
    client = firebase.create_user(email=email, password=password)
    return {"message": client}

@app.post("/login/")
async def login(request: SignupRequest):
    email = request.email
    password = request.password
    client = firebase.sign_in(email=email, password=password)
    return {"message": client}

@app.get("/current/")
async def get_current(token: str):
    user_id = firebase.get_current_user(token)
    return {"message": user_id}

@app.post("/add-word/")
async def add_word(request: AddWord):
    user_id = firebase.get_current_user(request.idToken)
    if user_id is None:
        raise HTTPException(status_code=401, detail="User not registered")
    res = firebase.add_word(
        word=request.word,
        traduction=request.traduction,
        example=request.example,
        vote=request.vote,
        source_id=request.source_id,
        definition=request.definition,
        know=request.know,
        type=request.type,
        user_id=user_id
    )
    return {"message": res}

@app.get("/get-words/")
async def get_words(token: str):
    user_id = firebase.get_current_user(token)
    words = firebase.get_words(user_id)
    return {"words": words}

@app.put("/update-word/")
async def update_word(request: UpdateWord):
    user_id = firebase.get_current_user(request.idToken)
    res = firebase.update_word(user_id, request.word_id, request.update_data)
    return {"message": res}

@app.delete("/delete-word/")
async def delete_word(token: str, word_id: str):
    user_id = firebase.get_current_user(token)
    res = firebase.delete_word(user_id, word_id)
    return {"message": res}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
