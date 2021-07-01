from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt
import requests
import subprocess
import json

app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://db:27017")
db = client.ImageRecognition
users = db["Users"]


def UserExists(username):
    if users.find({"Username": username}).count() == 0:
        return False
    else: 
        return True
    
    
def verifyPW(username, password):
    if not UserExists(username):
        return False
    
    hashedPW = users.find({
        "Username": username
    })[0]["Password"]
    
    if bcrypt.hashpw(password.encode("utf8"), hashedPW) == hashedPW:
        return True
    else:
        return False
    
    
def getUserTokenCount(username):
    tokens = users.find({
        "Username": username
    })[0]["Tokens"]
    return tokens


def tokenUpdate(username, tokens):
    users.update({
        "Username": username
    }, {
        "$set": {
            "Tokens": tokens
        }
    })
    
    
def generateReturnDictionary(status, msg):
    retJson = {
        "status": status , 
        "msg": msg 
    }
    return retJson


def generateReturnDictionaryTok(status, msg, tokens):
    retJson = {
        "status": status , 
        "msg": msg ,
        "Tokens remaining": tokens
    }
    return retJson


def verifyCredentials(username, password):
    if not UserExists(username):
        return generateReturnDictionary(301, "Invalid Username"), True
    correctPW = verifyPW(username, password)
    if not correctPW:
        return generateReturnDictionary(302, "Invalid Password"), True
    
    return None, False


class Register(Resource):
    def post(self):
        postedData = request.get_json()
        
        username = postedData["username"]
        password = postedData["password"]
        
        if UserExists(username):
            return jsonify( generateReturnDictionary(301, "Invalid Username: User already exists") )
        
        hashedPW = bcrypt.hashpw(password.encode("utf8"), bcrypt.gensalt())
        
        starterTokens = 5
        
        users.insert({
            "Username": username , 
            "Password": hashedPW ,
            "Tokens": starterTokens
        })
                
        return jsonify( (generateReturnDictionaryTok(200, "Successfully Registered", starterTokens)) )
 
    
class Classify(Resource):
    def post(self):
        postedData = request.get_json()
        
        username = postedData["username"]
        password = postedData["password"]
        url = postedData["url"]
        
        retJson, error = verifyCredentials(username, password)      
        if error:
            return jsonify(retJson)
        
        tokens = getUserTokenCount(username)
        
        if tokens <= 0 :
            return jsonify( generateReturnDictionaryTok(303, "Not Enough Tokens!", tokens ) )  
        
            # though requests we get the content of the url, r has the image we want
        r = requests.get(url)
        retJson = {}    
            # temp.jpg is the temporary image   
                  
        with open("temp.jpg", "wb") as f:       
                # into f we write the content of r, and by this we have downloaded an image with python
            f.write(r.content)    
                          
                # we open a new subprocess with classify py file,
                # and we pass the arguments the file wants by --model_dir which is in the current folder
                # the image file is in the current folder
            proc = subprocess.Popen('python classify_image.py --model_dir=. --image_file=./temp.jpg', 
                                     stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True
                                    )  

                # we wait until the subprocess is done
                # the subprocess writes the response json into a file
            proc.communicate()[0]
            proc.wait()

            #     # we now open that file
            # with open("text.json") as w:
            #         # we load the dictionary we stored into the file text
            #     retJson = json.load(w)
            
            with open("text.json","r") as f:
                data = f.read()
            retJson = json.loads(data)
        
        tokenUpdate(username, tokens-1)

        return retJson


class Refill(Resource):
    def post(self):
        postedData = request.get_json()
        
        username = postedData["username"]
        refillPW = postedData["refill_password"]
        refillAmount = postedData["refill_amount"]
        
        if not UserExists(username):
            return jsonify( generateReturnDictionary(301, "Invalid Username") )
        
        theRefillPW = "abc321"
        
        if not refillPW == theRefillPW:
            return jsonify( generateReturnDictionary(303, "Invalid Refill Password") )
        
        tokens = getUserTokenCount(username)
        
        newTokenTotal = tokens + refillAmount
        
        tokenUpdate(username, newTokenTotal)
        
        return jsonify( (generateReturnDictionaryTok(200, "Succefully Refilled Tokens", newTokenTotal)) )

api.add_resource(Register, '/register')
api.add_resource(Classify, '/classify')
api.add_resource(Refill, '/refill')

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
    
    