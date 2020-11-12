# MongoDB
import sys
import pymongo
import requests
import random
from bson.objectid import ObjectId
import os
import flask
import html
from flask import Flask, request
from flask_restful import Resource, Api
from flask_cors import CORS
from dotenv import load_dotenv
from flask_api import status
from jsonschema import validate, ValidationError
from flask import jsonify

# Date
import datetime

# JSON
import json
from bson import json_util

# Global variables
load_dotenv()
app = Flask(__name__)
api = Api(app)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
uri = os.getenv("URI_MONGODB")

# Dudas
## Persistencia de email entre pantallas

# Functions

# TO-DO Agregar nombre torneo
# Function to create a tournament
def createTournament():
    client = pymongo.MongoClient(uri)
    db = client.get_default_database()
    collection = db["torneos"]
    document = {
        "start_date": datetime.datetime.utcnow(),
        "end_date": datetime.datetime.utcnow() + datetime.timedelta(days=15),
        "isAvailable": True,
    }
    #Insert document in mongodb:
    collection.insert_one(document)
    return document
   
# Function to enroll a player in X tournament
def enroll( email, tournament_id, score ):
    client = pymongo.MongoClient(uri)
    db = client.get_default_database()

    # DUDA: Puntaje global, aplica para ranking de todos los torneos y ranking global
    # TO-DO: Verificar que no se inscribiera previamente

    # First, identify if tournament exists
    collection = db["torneos"]
    resultTournament = collection.find_one({"_id":ObjectId(tournament_id)})
    
    # Second, identify if player exists
    collection = db["jugadores"]
    resultPlayer = collection.find_one({"email":email})
    print(collection.find_one({"email":email}))

    # Both player and tournament exist
    if resultTournament != None and resultPlayer != None:
        print("Both exist")
        # Identify if the player has already registered to any other tournament
        collection = db["jugador-torneo"]
        resultEnrollment= collection.find_one({"email":email})
        
        # If player has previously enrolled, updates tournaments
        if resultEnrollment != None:
            print("Prev enrollment")
            collection.update_one({"email":email}, {'$push':{'torneos':ObjectId(tournament_id)}})
            return
        # If not, enrolls for the first time
        else:
            print("First enrollment")
            document = {
                "email": email,
                "torneos": [ObjectId(tournament_id)],
                "puntaje": score,
            }
            collection.insert_one(document)
            return parse_json(document)
        
    # Player doesn't exist
    else:
        print("one doesn't exist")
        return

# Function to retrieve a random question
def retrieveQuestion():
    client = pymongo.MongoClient(uri)
    db = client.get_default_database()
    actual_question: []
    collection = db["preguntas"]
    correct_answer = ""
    incorrect_answers = []
    r_number = 0
    response = {}

    actual_question = [question for question in collection.aggregate([{ '$sample': { 'size': 1 } }])]

    for i in actual_question:
        correct_answer = i.get("correct_answer", "")
        incorrect_answers = i.get("incorrect_answers", "")
        if correct_answer != "" or incorrect_answers != []:
            response = {
                "_id": i.get("_id", ""), 
                "category": i.get("category", ""), 
                "difficulty": i.get("difficulty", ""), 
                "question": i.get("question", ""),
                "correct_answer": "",
                "possible_answers": "",
            }
    
    incorrect_answers.append(correct_answer)
    random.shuffle(incorrect_answers)

    for i, j in enumerate(incorrect_answers):
        if j == correct_answer:
            correct_answer = i

    response.update(correct_answer = correct_answer, possible_answers = incorrect_answers)
    return response

# Function to retrieve global top N players
def retrieveRanking():
    client = pymongo.MongoClient(uri)
    db = client.get_default_database()
    collection = db["jugador-torneo"]
    pipeline = [ 
        {"$sort": {"puntaje": -1}}
    ]
    result = list(collection.aggregate(pipeline))

    global_ranking = {}
    for i in result:
        global_ranking[str(i.get("email", ""))] = i.get("puntaje", 0) 

    return global_ranking

# Function to retrieve individual score
def retrieveIndividualRanking(email: str = None):
    global_ranking = retrieveRanking()
    user_ranking = ""
    email_response = ""
    count = global_ranking.get(email, "")

    for idx, m in enumerate(global_ranking):
        if m == email:
            user_ranking = idx + 1
            email_response = m

    response = {
        "email": email_response,
        "user_ranking": user_ranking,
        "count": count
    }
    return response
    
# Function to increase score
def updateScore( email, result, bet ):
    client = pymongo.MongoClient(uri)
    db = client.get_default_database()
    collection = db["jugador-torneo"]
    # Player got question right
    score = 0
    if result == "True":
        print("Player ", email," got the question right")
        if bet == 0:
            score = 2
        elif bet == 1:
            score = 4
        elif bet == 2:
            score = 6
        else:
            return "ERROR: Bet value not valid"
        # DUDA: Score global
        collection.update_one({"email":email},{"$inc": {"puntaje": score}})        
    # Player got question wrong
    else:
        return "Player got the question wrong"
    return "Increased Points"

# Function to validate LogIn with email
def validateLogIn( email, password ):
    # Status codes
    # 200: Login Success
    # 401: Wrong password
    # 402: Email doesn't exist

    client = pymongo.MongoClient(uri)
    db = client.get_default_database()
    collection = db["jugadores"]

    if email.find("@") == -1:
        playerData = collection.find_one({ "username": email })
    else:
        playerData = collection.find_one({ "email": email })

    # Email not found
    if playerData is None:
        status = 402
        message = "Player's email is wrong"
    else:
        if playerData["password"] == password:
            status = 200
            message = "Login successful"
        elif playerData["password"] != password:
            status = 401
            message = "Password is wrong"
    
    result = {
        "status":status,
        "message": message
    }

    return result

# Function to retrieve user's tournaments
def retrievePlayerTournaments( email ):
    client = pymongo.MongoClient(uri)
    db = client.get_default_database()
    collection = db["jugador-torneo"]
    response = {}
    response["tournaments"] = []
    # Get list of tournament_id's 
    playerData = collection.find_one({ "email": email }, { "torneos": 1})
    # Build JSON with data from each tournament if isAvailable is true
    collection = db["torneos"]
    for tournament_id in playerData["torneos"]:
        tournament = collection.find_one({ "_id": tournament_id })
        if tournament["isAvailable"] == True:
            response["tournaments"].append(tournament)

    return parse_json(response)

# Fuction to retrieve all active tournaments
def retrieveAllTournaments():
    client = pymongo.MongoClient(uri)
    db = client.get_default_database()
    collection = db["torneos"]
    response = {}
    response["tournaments"] = []
    
    # Build JSON with data from each tournament if isAvailable is true
    tournaments = collection.find( )
    for tournament in tournaments:
        if tournament["isAvailable"] == True:
            response["tournaments"].append(tournament)

    return parse_json(response)

def parse_json(data):
    return json.loads(json_util.dumps(data))

#ENPOINT FOR FRONT DATA STATISTICS (GET)
class GET_STATISTICS(Resource):

    def get(self):
        try:
            #With this function I will create tournament
            create_tournament = createTournament()
            
            response = {
                "_id": str(create_tournament.get("_id", None)),
                "start_date": str(create_tournament.get("start_date", None)),
                "end_date": str(create_tournament.get("end_date", None)),
            }
            return response
        except ValueError as ex:
             _logger.error("Value error: %s", ex)
        return jsonify({'error': "Value error"})

api.add_resource(GET_STATISTICS, '/getStatistics')  # Route_1

#ENPOINT FOR FRONT ENROLL USERS (POST)
class ENROLL(Resource):

    def post(self):
        
        try:
            #For enrolling we need: email, tournament_id, score
            request_json = request.json
            
            #Get from request, we can change the name of the ids, depend in how its sent from front. 
            email = request_json.get("email", "")
            tournament_id = request_json.get("tournament_id", "")
            score = request_json.get("score", "")

            #Enrolling user 
            enroll_user = enroll(email, tournament_id, score)
            return enroll_user
        except ValueError as ex:
             _logger.error("Value error: %s", ex)
        return  jsonify({'error': "Value error"})

api.add_resource(ENROLL, '/enroll')  # Route_2

#ENPOINT FOR FRONT GET QUESTION (GET)
class GET_QUESTIONS(Resource):

    def get(self):
        try:
            question = retrieveQuestion()
            
            response = {
                'category': question.get("category", ""),
                'difficulty': question.get("difficulty", ""),
                'question': question.get("question", ""),
                "correct_answer": question.get('correct_answer', 0),
                "possible_answers": question.get("possible_answers", "")
            }

            return response 
        except ValueError as ex:
             _logger.error("Value error: %s", ex)
        return  jsonify({'error': "Value error"})

api.add_resource(GET_QUESTIONS, '/getQuestions')  # Route_3

#ENPOINT FOR FRONT GET RANKING(GET)
class GET_RANKING(Resource):

    def get(self):
        try:
            ranking = retrieveRanking()
            return ranking
        except ValueError as ex:
             _logger.error("Value error: %s", ex)
        return  jsonify({'error': "Value error"})
    
    def post(self):
        try:
            #For getting individual ranking we need email
            request_json = request.json
            email = request_json.get("email", "")
            ranking = retrieveIndividualRanking(email)
            return ranking
        except ValueError as ex:
             _logger.error("Value error: %s", ex)
        return  jsonify({'error': "Value error"})

api.add_resource(GET_RANKING, '/getGlobalRanking')  # Route_4

#ENDPOINT FOR FRONT TO UPDATE SCORE (POST)
class UPDATE_SCORE(Resource):
    def post(self):
        try:
            #For getting individual ranking we need email
            request_json = request.json
            email = request_json.get("email", "")
            result = request_json.get("result", "")
            bet = request_json.get("bet", "")
            ranking = updateScore(email, result, bet)
            return ranking
        except ValueError as ex:
             _logger.error("Value error: %s", ex)
        return  jsonify({'error': "Value error"})

api.add_resource(UPDATE_SCORE, '/updateScore')  # Route_4

#ENDPOINT FOR FRONT VALIDATE LOGIN (POST)
class LOGIN(Resource):
    def post(self):
        try:
            #For login we use email or username
            request_json = request.json
            email = request_json.get("email", "")
            password = request_json.get("password", "")
            response = validateLogIn(email,password)
            return response
        except ValueError as ex:
             _logger.error("Value error: %s", ex)
        return  jsonify({'error': "Value error"})

api.add_resource(LOGIN, '/login')  # Route_6

# ENDPOINT FOR FRONT GET TOURNAMENTS (POST)
class GET_TOURNAMENTS(Resource):
    def post(self):
        try:
            #For login we use email or username
            request_json = request.json
            # If request contains email, returns player tournaments
            try:
                email = request_json.get("email", "")
                response = retrievePlayerTournaments(email)
            # If request doesn't ccontain email returns all tournaments
            except:
                response = retrieveAllTournaments()
            return response
        except ValueError as ex:
             _logger.error("Value error: %s", ex)
        return  jsonify({'error': "Value error"})

api.add_resource(GET_TOURNAMENTS, '/getTournaments')  # Route_7


if __name__ == '__main__':
    app.run(port='5000')

