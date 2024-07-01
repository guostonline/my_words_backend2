
#from firebase_admin import credentials, auth
import requests
import pyrebase
class FirebaseUserManager:  
    def __init__(self):
        # Initialize the Firebase Admin SDK
        self.api_key='AIzaSyBdZ_V7ZNxnMqajCsn3o-Tpq2s7ljeB-RY'
        config = {
        "apiKey": "AIzaSyBkdguSzjeIFWbyJHHAH5Tp11LE-kTmuvU",
        "authDomain": "my-words-f9d53.firebaseapp.com",
        "projectId": "my-words-f9d53",
        "databaseURL": "https://my-words-f9d53.firebaseio.com",
        "storageBucket": "my-words-f9d53.appspot.com",
        "messagingSenderId": "729320734965",
        "appId": "1:729320734965:web:2086227dea1b94b1f305bc",
        "measurementId": "G-CSGGDDDCZH"
    }
        firebase = pyrebase.initialize_app(config)
        self.auth = firebase.auth()
   
    
    def login_user(self, email, password):
       
        url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={self.api_key}"
        payload = {
            "email": email,
            "password": password,
            "returnSecureToken": True
        }
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            data = response.json()
            print('Successfully logged in user:', data['localId'])
            return data['idToken']
        else:
            print('Error logging in user:', response.json())
            return None
    
    
    def create_user(self, email, password):
        try:
            user = self.auth.create_user_with_email_and_password(email, password)
            print('Successfully created user:', user)
            return user
        except Exception as e:
            print('Failed to create user:', e)
            return e
    
    # Function to sign in a user
    def sign_in(self,email, password):
        
        try:
            user = self.auth.sign_in_with_email_and_password(email, password)
            print('Successfully signed in:', user)
            return user
        except Exception as e:
            print('Failed to sign in:', e)
            return e

    # Example usage
    
    

        
        
