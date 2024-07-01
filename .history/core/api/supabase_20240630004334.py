import os
from supabase import create_client, Client


class MySupabase:
    def __init__(self) -> None:
        self.api_url = "https://psrlxxbkagngdfqksvky.supabase.co"
        self.api_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBzcmx4eGJrYWduZ2RmcWtzdmt5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTc0OTkyNDMsImV4cCI6MjAzMzA3NTI0M30.Hjc_L8xPZaqrvfBZ9_96vqtor0TZtLiqAxCEFkAttkU"
        self.supabase: Client = create_client(self.api_url, self.api_key)

    def sign_up(self, email, password,name):

        credentials = {
    "email":email,
    "password": password,
    "data":{
        "first_name":name
    }
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
                type: str,
                user_id:str):
        data, count = self.supabase.table('word').insert({
            'word':word,
                'traduction':traduction,
                'example':example,
                'vote':vote,
                'source_id':source_id,
                'definition': definition,
                'know': know,
                'type': type,
                'user_id':user_id
        }).execute()
        return data,count
    
    def get_user_id(self, token: str):
        try:
            user = self.supabase.auth.api.get_user(token)
            return {"user_id": user.id}
        except Exception as e:
            return {"error": str(e)}
