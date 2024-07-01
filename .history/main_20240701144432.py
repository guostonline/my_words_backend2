from core.api.nltk import NLTK
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from core.api.supabase import MySupabase
from core.api.firebase import FirebaseUserManager
from core.basemodel import *
from core.constant import *

app = FastAPI()
word = NLTK()
firebase = MySupabase()
test = word.convert_text_infinitive(
    "In a quiet village, a curious cat named Whiskers discovered a hidden garden. There, he found a magical flower "
    "that granted him the ability to speak. Whiskers shared tales of adventure with the villagers, enchanting them "
    "with his stories. One day, he told a story so captivating that the village became a famous storytelling hub. "
    "Whiskers, now a legend, continued to inspire joy and wonder in the hearts of all who visited."
)



@app.get("/")
async def read_root():
    return {"message": "Welcome to FastAPI"}


@app.post("/items/")
async def create_item(item: dict):
    return {"item": item}


@app.get("/verbs/", response_model=None)
async def extract_verbs(request: SentenceRequest):
    text = request.sentence
    result = word.convert_text_infinitive(text)
    return {"sentence": text, "result": result}


@app.post("/signup/", response_model=None)
async def signup(request: SignupRequest):

    client = firebase.sign_up(
        email=request.email, password=request.password, name=request.name
    )
    return {"message": client}


@app.post("/login/", response_model=None)
async def login(request: SignupRequest):
    email = request.email
    password = request.password

    client = firebase.login(email=email, password=password)
    print(client)
    return {"message": client}


@app.get("/current/", response_model=None)
async def get_current(token: Token):

    my_token = firebase.get_user_id(# `token.token` is accessing the `token` attribute of the `Token`
    # object. In this context, it is likely that `Token` is a Pydantic
    # model representing a token object, and `token.token` is used to
    # access the actual token value stored within the `token`
    # attribute of the `Token` object when passed as a parameter in
    # the `get_current` endpoint.
    token.token)
    return {
        "message": my_token,
    }


@app.post("/add-word/", response_model=None)
async def add_word(request: AddWord):
    
    

        res = firebase.add_word(
            word=request.word,
            traduction=traduction,
            example=example,
            vote=vote,
            source_id=source_id,
            definition=definition,
            know=know,
            type=type,
            user_id=user_id,
        )
    else:
        return {"message": "user not register"}
    return {"message": res}


@app.post("/test/", response_model=None)
async def test_word():
    firebase.get_user_id("test4@gmail.com")
    return {"message": "test"}
