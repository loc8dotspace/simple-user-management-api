from flask import abort, url_for
from passlib.apps import custom_app_context as pwd

# Mongo Helper functions

def append_url( user ):
    user.update( { 'url' : url_for( 'get_user' ,
        username = user['username'],
        _external = True ) } )
    return user

def get_all_existing_users( users ):
    users_cursor = users.find( {}, { '_id' : 0, 'password_hash' : 0 } )
    return { 'users' : map( append_url, users_cursor ) }

def add_one_new_user( users, form ):
    # Validate presense of all inputs
    if ( 'username' in form.keys() and
            'password' in form.keys() and
            'role' in form.keys() ):
        username = form['username']
        password = form['password']
        role = form['role']
        # Validate individual input
        if ( username != None and password != None and role != None ):
            if users.find( { 'username' : form['username'] } ).count() == 0:
                # Insert
                obj_id = users.insert_one( { 'username' : username,
                    'password_hash' : pwd.encrypt( password ),
                    'role' : role } )
                return username
                pass
            else:
                # Error: username exists
                abort( 405 )
            pass
            pass
        else:
            # Error: username, password and role, at least one None
            abort( 400 )
            pass
    else:
        # Error: username, password and role, all three not provided
        abort( 400 )
        pass
    pass

def get_users_matching_username( users, username ):
    users_cursor = users.find( { 'username' : username }, 
            { '_id' : 0, 'password_hash' : 0 } )
    return { 'users' : map( append_url, users_cursor ) }

def update_existing_user( users, username, form ):
    if users.find( { 'username' : username } ).count() == 0:
        # Error: username not registered
        abort( 404 )
        pass
    else:
        updates_performed = dict()
        if 'password' in form.keys():
            password = form['password']
            if password != None:
                result = users.update_one( { 'username' : username },
                        { '$set' : { 
                            'password_hash' : pwd.encrypt( password ) } } )
                updates_performed.update( { 'password' : 'hashed' } )
            else:
                # Error: password field is None
                abort( 400 )
                pass
            pass
        if 'role' in form.keys():
            role = form['role']
            if role != None:
                result = users.update_one( { 'username' : username },
                        { '$set' : { 'role' : role } } )
                updates_performed.update( { 'role' : role } )
            else:
                # Error: role field is None
                abort(400 )
                pass
            pass
        return { 'Parameters Updated' : updates_performed }
        pass
    pass

def delete_users_matching_username( users, username ):
    result = users.delete_many( { 'username' : username } )
    if result.deleted_count == 0:
        abort( 404 )
    else:
        return { 'message' : 'Deleted users',
                 'Deleted Count' : str( result.deleted_count ) }
    pass

def authenticate_existing_user( users, form ):
    if ( 'username' in form.keys() and
            'password' in form.keys() ):
        username = form['username']
        password = form['password']
        if ( username != None and password != None ):
            user_cursor = users.find( { 'username' : username },
                    { '_id' : 0, 'password_hash' : 1 } )
            if user_cursor.count() != 0:
                return pwd.verify( password, user_cursor.next().pop( 'password_hash' ) )
                pass
            else:
                # Error : username doesn't exist
                abort( 405 )
                pass
            pass
        else:
            # Error : either username or password is None
            abort( 400 )
            pass
        pass
    else:
        # Error: Both username and password not supplied
        abort( 400 )
        pass
    pass

