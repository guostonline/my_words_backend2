import os
from supabase import create_client, Client
from core.basemodel import Client

class MySupabase:
    def __init__(self) -> None:
        self.api_url = "https://psrlxxbkagngdfqksvky.supabase.co"
        self.api_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBzcmx4eGJrYWduZ2RmcWtzdmt5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTc0OTkyNDMsImV4cCI6MjAzMzA3NTI0M30.Hjc_L8xPZaqrvfBZ9_96vqtor0TZtLiqAxCEFkAttkU"
        self.supabase: Client = create_client(self.api_url, self.api_key)

    def sign_up(self, email, password,user_name):

        credentials={
        "email": email,
        "password":password,
        "options": {"data": {"user_name": user_name, "bird_year": 27}},
    
  }
        user = self.supabase.auth.sign_up(credentials)
        return user

    def login(self, email, password):
        try:
           
            data = self.supabase.auth.sign_in_with_password({"email": email, "password": password})
            return {"email": email, "authenticated": True, "user": data}
        except Exception as e:
            return {"email": email, "authenticated": False, "error": str(e)}

    def add_word(self,
            word:str,
                traduction:str,
                example:str,
                vote:int,
                source_id:str,
                definition: str,
                know: bool,
                plan: str,
                user_id:str):
        result = self.supabase.table('word').insert({
            'word':word,
                'traduction':traduction,
                'example':example,
                'vote':vote,
                'source_id':source_id,
                'definition': definition,
                'know': know,
                'plan': plan,
                'user_id':user_id
        }).execute()
       
        return result.data
    
    def get_user_id(self, token: str):
        try:
            user = self.supabase.auth.api.get_user(token)
            return user.id
        except Exception as e:
            return {"error": str(e)}
    
    def set_user_info(self,client:Client):
        result=self.supabase.table("users").insert({
             'user_id': client.user_id,
            'user_name': client.user_name,
            'email': client.email,
            'number_phone': client.number_phone,
            'gender':client.gender,
            'bird_year': client.bird_year,
            'type':client.type,
        }).execute()
        return result.data
