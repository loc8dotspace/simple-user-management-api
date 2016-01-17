from pymongo import MongoClient
from passlib.app import custom_app_context as pwd

client = MongoClient( host = "db" )

ride_sharing = client.ride_sharing

users = ride_sharing.users

users.insert_one( {
    'username' : 'sid',
    'password_hash' : pwd.encrypt( 'test' ),
    'role' : 'driver' } )
