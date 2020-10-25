# MongoDB
import sys
import pymongo

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
    collection = db["jugador-torneo"]
    # TO-DO: CORROBORAR QUE EL MAIL Y EL TORNEO EXISTEN
    # TO-DO: Error codes
    # DUDA: Puntaje global, aplica para ranking de todos los torneos y ranking global
    document = {
        "email": email,
        "torneos": [tournament_id],
        "puntaje": score,
    }
    return collection.insert_one(document)

# Function to retrieve a random question
def retrieveQuestion():
    global db
    collection = db["preguntas"]
    # TO-DO: QUE LAS PREGUNTAS NO SE REPITAN
    for question in collection.aggregate([{ '$sample': { 'size': 1 } }]):
        return question

# Function to retrieve global top N players
def retrieveRanking( N ):
    global db
    collection = db["jugador-torneo"]

# Function to retrieve X tournament top N players

# Function to retrieve player's position in global ranking

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

#connect to mongo
try:
    connect_mongo()
    print("Connection successful")
    #print(enroll("sam@quizit.com","1",20))
    #print(updateScore("sa@quizit.com",True,1))
except:
    print("Couldn't connect to MongoDB")