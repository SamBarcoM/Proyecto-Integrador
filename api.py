# MongoDB
import sys
import pymongo
import requests
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

# Global variables
load_dotenv()
app = Flask(__name__)
api = Api(app)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
uri = os.getenv("URI_MONGODB")

# Functions

# DUDA: Para el POC debemos generar una función que cree un torneo cada tres días?
# Agregar nombre torneo
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
            return "previously enrrolled and updated tournamnet"
        # If not, enrolls for the first time
        else:
            print("First enrollment")
            document = {
                "email": email,
                "torneos": [ObjectId(tournament_id)],
                "puntaje": score,
            }
            collection.insert_one(document)
            return document
        
    # Tournament doesn't exist  
    else:
        print("one doesn't exist")
        return

# Function to retrieve a random question
def retrieveQuestion():
    client = pymongo.MongoClient(uri)
    db = client.get_default_database()

    collection = db["preguntas"]
    # TO-DO: QUE LAS PREGUNTAS NO SE REPITAN
    for question in collection.aggregate([{ '$sample': { 'size': 1 } }]):
        return question

# DUDA: Ranking global para PoC
# TO-DO: Merge answers and send right position
# Function to retrieve global top N players
def retrieveGlobalRanking( N ):
    client = pymongo.MongoClient(uri)
    db = client.get_default_database()
    collection = db["jugador-torneo"]

# Function to retrieve player's position in global ranking
def retrieveIndividualRanking( email ):
    return

# Function to increase score
def updateScore( email, result, bet ):
    client = pymongo.MongoClient(uri)
    db = client.get_default_database()
    collection = db["jugador-torneo"]
    # Player got question right
    if result == True:
        print("Player ", email," got the question right")
        if bet == 0:
            score = 2
        elif bet == 1:
            score = 4
        elif bet == 2:
            score = 6
        else:
            print("ERROR: Bet value not valid")
            return
        # DUDA: Score global
        collection.update_one({"email":email},{'$inc':{"puntaje":score}})        
    # Player got question wrong
    else:
        print("Player ", email," got the question wrong")
        return
    return

# Function to retrieve user's tournaments

# Fuction to retrieve all active tournaments

# TO-DO: Delete True-False questions

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
                "correct_answer": question.get('correct_answer', ""),
                "incorrect_answers": question.get("incorrect_answers", "")
            }
            return response
        except ValueError as ex:
             _logger.error("Value error: %s", ex)
        return  jsonify({'error': "Value error"})

api.add_resource(GET_QUESTIONS, '/getQuestions')  # Route_3

if __name__ == '__main__':
    app.run(port='5000')