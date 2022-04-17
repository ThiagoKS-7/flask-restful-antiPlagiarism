'''
Registrar user 0 tokens
Cada user recebe 10 tokens
post de similarity - 1 token
'''
from flask import Flask,render_template
from flask_restful import Api 
# from models.resources.manage_sentence import Register, Store, GetUsers

app = Flask(__name__)
api =  Api(app)
 
title = "Flask tutorial"
subtitle = "Running on port 5000"


# '''
#  ***********************
#  *       API ROUTES    *
#  ***********************
# '''
# api.add_resource(Register, '/register')
# api.add_resource(Store, '/store')
# api.add_resource(GetUsers, '/get-users')

'''
***********************
*       APP ROUTES    *
***********************
'''
@app.route('/')
def hello_world():
  return render_template('index.html', title=title, subtitle=subtitle)


if __name__ == '__main__':
  app.run(debug=True)

