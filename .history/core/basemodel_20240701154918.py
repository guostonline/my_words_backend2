from pydantic import BaseModel


class SignupRequest(BaseModel):
    email: str
    password: str
    user_name: str

class Login(BaseModel):
       email: str
    password: str
    
class Client(BaseModel):
    user_id: str
    user_name:str
    email: str
    number_phone: str
    gender:str
    bird_year: int
    type:str
    
class SentenceRequest(BaseModel):
	sentence: str
 
class AddWord(BaseModel):
    word:str
    traduction:str
    example:str
    vote:int
    source_id:str
    definition: str
    know: bool
    type: str
    user_id:str 
    
    
class Token(BaseModel):
    token:str    