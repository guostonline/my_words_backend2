from flask import Flask, request, jsonify
from core.api.nltk import NLTK
from core.api.supabase import MySupabase
from core.api.firebase import FirebaseUserManager
from core.basemodel import *
from core.constant import *

app = Flask(__name__)
word = NLTK()
firebase = MySupabase()

@app.route("/")
def read_root():
    return jsonify({"message": "Welcome to Flask"})

@app.route("/items/", methods=["POST"])
def create_item():
    item = request.json.get("item")
    return jsonify({"item": item})

@app.route("/verbs/", methods=["GET"])
def extract_verbs():
    sentence = request.args.get("sentence")
    result = word.convert_text_infinitive(sentence)
    return jsonify({"sentence": sentence, "result": result})

@app.route("/signup/", methods=["POST"])
def signup():
    request_data = request.json
    email = request_data.get("email")
    password = request_data.get("password")
    name = request_data.get("name")
    client = firebase.sign_up(email=email, password=password, name=name)
    return jsonify({"message": client})

@app.route("/login/", methods=["POST"])
def login():
    request_data = request.json
    email = request_data.get("email")
    password = request_data.get("password")
    client = firebase.login(email=email, password=password)
    return jsonify({"message": client})

@app.route("/current/", methods=["GET"])
def get_current():
    token = request.args.get("token")
    my_token = firebase.get_current_user(token)
    return jsonify({"message": my_token["message"]["localId"]})

@app.route("/add-word/", methods=["POST"])
def add_word():
    request_data = request.json
    id_token = request_data.get("idToken")
    user_id = firebase.get_current_user(id_token)
    
    if user_id is not None:
        word = request_data.get("word")
        traduction = request_data.get("traduction")
        example = request_data.get("example")
        vote = request_data.get("vote")
        source_id = request_data.get("source_id")
        definition = request_data.get("definition")
        know = request_data.get("know")
        type = request_data.get("type")
        
        res = firebase.add_word(
            word=word,
            traduction=traduction,
            example=example,
            vote=vote,
            source_id=source_id,
            definition=definition,
            know=know,
            type=type,
            user_id=user_id
        )
        return jsonify({"message": res})
    else:
        return jsonify({"message": "User not registered"})

@app.route("/test/", methods=["POST"])
def test_word():
    # Example endpoint, adjust as needed
    firebase.get_user_id("test4@gmail.com")
    return jsonify({"message": "test"})

if __name__ == "__main__":
    app.run(debug=True)
