#!flask/bin/python
import os
from flask import Flask, abort, jsonify, request, url_for
from pymongo import MongoClient
from time import sleep
from db_actions import *

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"

client = MongoClient( os.environ['DB_PORT_27017_TCP_ADDR'], 27017)
#client = MongoClient( "192.168.99.100", 27017)

# Instantiate the database object
ride_sharing = client.ride_sharing
users = ride_sharing.users

# App routes
@app.route('/api/users', methods=['GET'])
def get_users():
    return jsonify( get_all_existing_users( users ) )

@app.route('/api/users', methods=['POST'])
def new_user():
    username = add_one_new_user( users, request.form )
    location = url_for( 'get_user', 
            username = username,
            _external = True )
    return ( jsonify( { 'message' : 'Welcome ' + request.form['username'] } ),
            201,
            { 'Location' : location } )

@app.route('/api/users/<username>', methods=['GET'])
def get_user( username ):
    return jsonify( get_users_matching_username( users, username ) ) 

@app.route('/api/users/<username>', methods=['DELETE'])
def delete_user( username ):
    return jsonify( delete_users_matching_username( users, username ) ) 

@app.route('/api/users/<username>', methods=['PUT'])
def put_user( username ):
    return jsonify( update_existing_user( users, username, request.form ) )

@app.route('/api/auth_user', methods=['POST'])
def auth_user():
    if authenticate_existing_user( users, request.form ):
        return ( jsonify( { 'message' : 'Welcome back' } ),
                200,
                { 'Location' : url_for( 'get_user', 
                    username = request.form['username'], 
                    _external = True ) } )
    else:
        # Error: Incorrect password
        abort( 403 )
        pass

if __name__ == '__main__':
    #app.run(host='127.0.0.1', debug=True)
    app.run(host='0.0.0.0', debug=True)
