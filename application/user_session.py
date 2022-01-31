import psycopg2
from application.database import database
from flask import session


def user_session():

# When the user opens the 'getting started' page, a session is initiated for the encryption
# Information about this session data needs to be stored in the database
# If the user wants to start again with their encryption methods and reset the data,
# they will be routed to this page and a new session will be initiated

# 1. Set or reset initial variables
    # Read the database connection url from the enivronment variable
    DATABASE_URL = database()
    # Reset database connection
    manucrypt_db = None
    # If the 'user_base' session variable has been allocated from a previous session
    if 'user_base' in session:
        # Then release the session variable
        session.pop('user_base', None)
    # Cursor guidance from: https://www.postgresqltutorial.com/postgresql-python/transaction/
    try:

# 2. Create a table to store user's session information
        # Set user ID to 0
        user_id = 0
        # Create a new database connection
        manucrypt_db = psycopg2.connect(DATABASE_URL)
        # Create a new cursor
        cursor = manucrypt_db.cursor()
        # Create a users table - if one does not already exist in the database
        # The user will be allocated a new user ID every time they start a new encryption session
        # - User ID: to keep track of user sessions
        # - Session: name for the table where the session encryption data will be stored
        # - Timestamp: to reuse the oldest session slots for future sessions
        create_users_table = """CREATE TABLE IF NOT EXISTS users (
                                    id INT NOT NULL,
                                    session varchar(255),
                                    time TIMESTAMPTZ
                                    )
                                    """
        cursor.execute(create_users_table)

# 3. Allocate a user ID for the session
        # Check database for existing encryption tables
        search_tables = """SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"""
        cursor.execute(search_tables)
        tables = cursor.fetchall()
        # Iterate through tables
        for table in tables:
            # Find users table in database
            if 'users' in table:
                # Find number of users in table
                entries = """SELECT * FROM users"""
                cursor.execute(entries)
                total = cursor.rowcount
                # The user's ID is a number allocated between 1 and 20
                # If maximum has not been previously allocated
                # Then allocate the next available user ID number to the current user
                if total < 20:
                    user_id = total + 1
                # If all 20 user IDs have been taken
                else:
                    # Then sort the user ID's in order of how recently they were allocated
                    # Find the oldest user ID
                    find_oldest_entry = """SELECT * FROM users ORDER BY time ASC LIMIT 1"""
                    cursor.execute(find_oldest_entry)
                    oldest = cursor.fetchall()
                    # Allocate the oldest user ID number to the current user
                    # Delete the previous data from the oldest user ID
                    for user in oldest:
                        user_id = user[0]
                        delete_old_user = """DELETE FROM users WHERE id = %s"""
                        cursor.execute(delete_old_user, (user_id,))

# 4. Allocate a session name and store it as a session variable
        # If the 'user_session' session variable has been allocated from a previous session
        if 'user_session' in session:
            # Then release the session variable
            session.pop('user_session', None)
        # Allocate the session variable 'user_session'
        # The variable will be used as the name of the table
        # where all the user's encryption data from the current session will be stored
        session['user_session'] = "user_session_%s" % user_id
        user_session = session.get('user_session')

# 5. Allocate a user sequence, store it as a session variable and commit it to the database
        # When encryption methods are removed from the user's session table
        # the row ids will no longer be in sequence
        # The user sequence will be used as to reset the ids when this happens
        # If the 'user_seq' session variable has been allocated from a previous session   
        if 'user_seq' in session:
            # Then release the session variable
            session.pop('user_seq', None)
        # Allocate a user sequence name and store it as a session variable
        session['user_seq'] = "user_seq_%s" % user_id
        user_seq = session.get('user_seq')
        # Delete any previously allocated sequences in the database with the same name
        # drop sequence: https://www.postgresql.org/docs/9.1/sql-dropsequence.html
        delete_seq = """DROP SEQUENCE %s CASCADE"""
        cursor.execute(delete_seq % user_seq)
        # Create a new user sequence in the database
        # create sequence: https://www.postgresqltutorial.com/postgresql-serial/
        create_seq = """CREATE SEQUENCE %s"""
        cursor.execute(create_seq % user_seq)

# 6. Allocate a timestamp for the launch of the user's session
        # Get the current time and date to allocate to the user's session
        get_timestamp = """SELECT NOW()"""
        cursor.execute(get_timestamp)
        current_time = cursor.fetchall()

# 7. Enter the user's session data into the user table
        # Enter data into the users table
        add_user = ("INSERT INTO users"
                    "(id, session, time)"
                    "VALUES (%s, %s, %s)")
        user_data = (user_id, user_session, current_time[0])
        cursor.execute(add_user, user_data)

# 8. Allocate a table to the user to store password encryption data from the session
        # Check database for existing user session tables
        search_tables = """SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"""
        cursor.execute(search_tables)
        for table in cursor.fetchall():
            # If a table already exists under the user's current session name
            if user_session in table:
                # Then delete the data
                delete_table = """DROP TABLE %s"""
                cursor.execute(delete_table % user_session)
        # Create a new table for the user's encryption data from this session
        create_table = """CREATE TABLE %s (
                            id INT NOT NULL DEFAULT nextval('%s'),
                            method varchar(255),
                            characters varchar(255),
                            location varchar(255),
                            custom_location INT
                            )
                            """
        cursor.execute(create_table % (user_session, user_seq))
        
# 9. Commit all the transactions
        manucrypt_db.commit()
        # Close the cursor
        cursor.close()
    # Complete transaction according to: https://www.postgresqltutorial.com/postgresql-python/transaction/
    except psycopg2.DatabaseError as error:
        print(error)
    finally:
        if manucrypt_db is not None:
            manucrypt_db.close()

# 10. Return to manucrypt.py
    return
