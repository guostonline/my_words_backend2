from pydantic import BaseModel


class SignupRequest(BaseModel):
    email: str
    password: str
   
    
class client(BaseModel):
    first_name: str
    last_name: str
    email: str
    number_phone: str
    gender:str
    
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