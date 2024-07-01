# from firebase_admin import credentials, auth
from fastapi import FastAPI, HTTPException, status, Depends
import requests
import pyrebase


class FirebaseUserManager:
    def __init__(self):
        # Initialize the Firebase Admin SDK
        self.api_key = "AIzaSyBdZ_V7ZNxnMqajCsn3o-Tpq2s7ljeB-RY"
        config = {
            "apiKey": "AIzaSyBkdguSzjeIFWbyJHHAH5Tp11LE-kTmuvU",
            "authDomain": "my-words-f9d53.firebaseapp.com",
            "projectId": "my-words-f9d53",
            "databaseURL": "https://my-words-f9d53.firebaseio.com",
            "storageBucket": "my-words-f9d53.appspot.com",
            "messagingSenderId": "729320734965",
            "appId": "1:729320734965:web:2086227dea1b94b1f305bc",
            "measurementId": "G-CSGGDDDCZH",
            "serviceAccount": "firebase.json",
        }
        firebase = pyrebase.initialize_app(config)
        self.auth = firebase.auth()
        self.database = firebase.database()

    def login_user(self, email, password):
        try:
            user = auth.create_user(
        email='user@example.com',
        email_verified=False,
        password='secretPassword',
        display_name='John Doe',
        disabled=False
)
            return user        
        except Exception as e:
            print(e)
        

    def create_user(self, email, password):
        try:
            user = self.auth.create_user_with_email_and_password(email, password)
            print("Successfully created user:", user)
            return user
        except Exception as e:
            print("Failed to create user:", e)
            return e

    # Function to sign in a user
    def sign_in(self, email, password):

        try:
            user = self.auth.sign_in_with_email_and_password(email, password)
            print("Successfully signed in:", user)
            return user
        except Exception as e:
            print("Failed to sign in:", e)
            return e

    def get_current_user(self, token: str) -> str:
        try:
            user = self.auth.get_account_info(token)
            user_id = user["users"][0]["localId"]
            return user_id
        except:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
            )

    def add_word(
        self,
        word: str,
        traduction: str,
        example: str,
        vote: int,
        source_id: str,
        definition: str,
        know: bool,
        type: str,
        user_id: str,
    ):
        try:
            data = (
                self.database.child("users")
                .child(user_id)
                .set(
                    {
                        "word": word,
                        "traduction": traduction,
                        "example": example,
                        "vote": vote,
                        "source_id": source_id,
                        "definition": definition,
                        "know": know,
                        "type": type,
                        "user_id": user_id,
                    }
                )
            )
            return {"message": "Fake data added successfully", "data": data}
        except Exception as e:
            print(e)

    def test_word(self):
        try:
            test = self.database.child("users").child("chakib").set({
                "name": "chakib"
            })
            return {"message": "Test word added successfully", "data": test}
        except Exception as e:
            print("Failed to add test word:", e)
            return {"error": str(e)}
        
