# MongoDB
import sys
import pymongo
from bson.objectid import ObjectId

# Date
import datetime

# Global variables
uri = ""
db = None

# Functions

# Function that allow us to connect to the Database
def connect_mongo():
    global db
    client = pymongo.MongoClient(uri)
    db = client.get_default_database()

# DUDA: Para el POC debemos generar una función que cree un torneo cada tres días?
# Agregar nombre torneo
# Function to create a tournament
def createTournament():
    global db
    collection = db["torneos"]
    document = {
        "start_date": datetime.datetime.utcnow(),
        "end_date": datetime.datetime.utcnow() + datetime.timedelta(days=15),
        "isAvailable": True,
    }
    return collection.insert_one(document)
   
# Function to enroll a player in X tournament
def enroll( email, tournament_id, score ):
    global db

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
            return collection.update_one({"email":email}, {'$push':{'torneos':ObjectId(tournament_id)}})
        # If not, enrolls for the first time
        else:
            print("First enrollment")
            document = {
                "email": email,
                "torneos": [ObjectId(tournament_id)],
                "puntaje": score,
            }
            return collection.insert_one(document)
        
    # Tournament doesn't exist  
    else:
        print("one doesn't exist")
        return

# Function to retrieve a random question
def retrieveQuestion():
    global db
    collection = db["preguntas"]
    # TO-DO: QUE LAS PREGUNTAS NO SE REPITAN
    for question in collection.aggregate([{ '$sample': { 'size': 1 } }]):
        return question

# DUDA: Ranking global para PoC
# TO-DO: Merge answers and send right position
# Function to retrieve global top N players
def retrieveGlobalRanking( N ):
    global db
    collection = db["jugador-torneo"]

# Function to retrieve player's position in global ranking
def retrieveIndividualRanking( email ):
    return

# Function to increase score
def updateScore( email, result, bet ):
    global db
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

#connect to mongo
try:
    connect_mongo()
    print("Connection successful")
    createTournament()
    createTournament()
    createTournament()
    
    print(enroll("samb@quizit.com","5f960d8c27eddbbf601ca785",20))
    #print(updateScore("sa@quizit.com",True,1))
except:
    print("Couldn't connect to MongoDB")