from pprint import pprint
from pymongo import MongoClient
from flask_restful import Resource
from flask import request
from repositories.requests import handleRequest
import bcrypt

# instanciando mongoClient na porta default
client = MongoClient("localhost", 27017)
# novo database de nome SentencesDatabase
db = client.SimiliarityDatabase
# nova colecttion de nome Users
Users = db.Users

#criar resource
class Register(Resource):
  def post(self):
    body = request.get_json()
    if body:
      res = handleRequest(Users,body, 'register')
    return res

class Detect(Resource):
  def patch(self):
    body = request.get_json()
    if body:
      res = handleRequest(Users,body, 'detect')
    return res

class GetUsers(Resource):
  def get(self):
    body = request.get_json()
    if body:
      res = handleRequest(Users,body, 'get-users')
    return res

class Refill(Resource):
  def patch(self):
    body = request.get_json()
    if body:
      res = handleRequest(Users,body, 'refill')
    return res