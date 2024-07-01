from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, EmailStr
import firebase_admin
from firebase_admin import credentials, auth, firestore
import requests

# Initialize Firebase Admin SDK
cred = credentials.Certificate("firebase.json")
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

    def sign_up(self, email: str, password: str):
        try:
            user = auth.create_user(
        email=email,
        email_verified=False,
        password=password,
        display_name='John Doe',
        disabled=False
)
            return user        
        except Exception as e:
            print(e)

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
            doc_ref = db.collection("users").document(user_id).document(word_id)
            doc_ref.update(update_data)
            return {"message": "Word updated successfully"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def delete_word(self, user_id: str, word_id: str):
        try:
            doc_ref = db.collection("users").document(user_id).document(word_id)
            doc_ref.delete()
            return {"message": "Word deleted successfully"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

# Pydantic models for request validation
