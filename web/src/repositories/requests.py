import bcrypt
from flask import Response
from datetime import datetime
import spacy


def checkPostedData(collection,body, functionName):
  # checa se um dos dois parametros ñ tá no body
  if 'username' not in body or 'password' not in body:
    error = {
      "message": "Error: missing required parameter usr/pwd.",
      "status": 301
    }
    return error
  # Ifs encadeados pra checar qual função é
  if functionName == 'register':
    usr = body["username"]
    pwd = body["password"].encode('utf-8') #precisa passar com encode utf-8
    #encripta password
    hash_pwd = bcrypt.hashpw(pwd, bcrypt.gensalt())
    have_same_data = collection.find_one({'Username': usr})
    # se o user ainda não existir, deixa criar
    if not have_same_data:
      collection.insert_one({
        "Username":usr,
        "Password":hash_pwd,
        "Text1":"",
        "Text2":"",
        "Similiarity":"", 
        "Tokens": 10,
        "CreatedAt": datetime.now(),
        "UpdatedAt":""
      })
      retJson = {
      "message":"You successfully signed up!",
      "status": 200
      }
    else:
      retJson = {
       "message":"Error! User already exists.",
       "status": 400
      }

    return retJson

  elif functionName == 'detect':
    usr = body["username"]
    pwd = body["password"]
    text1 = body["text1"]
    text2 = body["text2"]
    pwd_exists = collection.find_one({'Username': usr})["Password"]
    #se existe um password pra aquele user, é pq ele existe
    if pwd_exists:
      #faz update
      tokens = collection.find_one({'Username': usr})["Tokens"]
      #se o user tiver tokens, deixa passar
      if tokens <= 0:
        retJson = {
          "message":"Error! Not enough tokens.",
          "status": 301
        }
      else:
        # usa natural language processing pra comparar os textos
        nlp = spacy.load("en_core_web_sm")
        text1 = nlp(text1)
        text2 = nlp(text2)
        ratio = text1.similarity(text2)
        tokens = tokens -1
        collection.update_one({'Username': usr}, {"$set": {
          "Similiarity": ratio,
          "Tokens": tokens,
          "UpdatedAt": datetime.now(),
        }})
        retJson = {
          "message":"Sentence successfully saved.",
          "Tokens": tokens,
          "status": 200,
        }
    else:
      retJson = {
      "message":"Error! User or password incorrect.",
      "status": 400
      }

    return retJson

  elif functionName == 'get-users':
    usr = body["username"]
    pwd_exists = collection.find_one({'Username': usr})["Password"]
    #se existe um password pra aquele user, é pq ele existe
    if pwd_exists:
      #faz update
      tokens = collection.find_one({'Username': usr})["Tokens"]
      #se o user tiver tokens, deixa passar
      if tokens <= 0:
        retJson = {
          "message":"Error! Not enough tokens.",
          "status": 301
        }
      else:
        tokens = tokens -1
        result = []
        for col in collection.find({},{"Username":1, "Text1":1, "Text2":1, "Tokens":1}):
          result.append({
            "username":col["Username"],
            "text1":col["Text1"],
            "text2":col["Text2"],
            "tokens":col["Tokens"],
          })
        
        retJson = {
          "message":"Data successfully retrieved.",
          "data": result,
          "Tokens": tokens,
          "status": 200,
        }
    else:
      retJson = {
      "message":"Error! User or password incorrect.",
      "status": 400
      }

    return retJson

  elif functionName == 'refill':
    usr = body["username"]
    target=body["target"]
    pwd = body["password"]
    tokens = body["tokens"]
    pwd_exists = collection.find_one({'Username': usr})["Password"]
    #se existe um password pra aquele user, é pq ele existe
    if pwd_exists and usr == 'admin':
      #faz update
      collection.update_one({'Username': target}, {"$set": {
        "Tokens": tokens,
        "UpdatedAt": datetime.now(),
      }})
      retJson = {
        "message":"Sentence successfully saved.",
        "Tokens": tokens,
        "status": 200,
      }
    else:
      retJson = {
      "message":"Error! Only admin can refill tokens.",
      "status": 400
      }

    return retJson


# tenta checar se a request tá certa
# se não der, retorna bad request
def handleRequest(collection,body, routeName):
    print(collection,body,routeName)
    try:  
      res = checkPostedData(collection,body, routeName)
      return res
    except Exception as e:
      error = Response("Error!  " + str(e) + "is not allowed or spected on the request.",status=400)
      return error