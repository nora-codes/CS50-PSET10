import psycopg2
import inflect
from psycopg2 import sql
from flask import session
from application.database import database


def encryption_log(method, characters, location, custom_location):

    # The encryption log is used to keep track of the user's encryptions within the current session

    # 1. Set or reset initial variables
    # Read the database connection url from the enivronment variable
    DATABASE_URL = database()
    # Reset database connection
    manucrypt_db = None
    # Define a list called encryption_key - this will be used later
    encryption_key = list()

    # 2. Get all of the encryption data from the user's current session
    try:
        # Create a new database connection
        manucrypt_db = psycopg2.connect(DATABASE_URL)
        # Create a new cursor
        cursor = manucrypt_db.cursor()
        # Get the user session name to get the data from the corresponding encryption table
        user_session = session.get('user_session')
        # Get the user sequence name for the user's session table
        user_seq = session.get('user_seq')
        # Ititiate query to select all data from the current 'user_session' table
        # The table includes all previously specified encryptions
        fetch_data = """SELECT * FROM %s"""
        cursor.execute(fetch_data % user_session)
        table = cursor.fetchall()
        # Get number of rows in the table
        last = cursor.rowcount

    # 3. Check for a browser refresh
        # Detect if the current encryption specification is the same as the last encryption in the table
        # Get the last row in the table and check for similarities
        for row in table:
            if last == row[0]:
                if method == row[1] and location == row[3] and custom_location == row[4]:
                    if characters == row[2] or characters == int(row[2]):
                        # If browser has been refreshed - log the entry as false using 'method'
                        method = 9

    # 4. Check for a 'remove encryption' request from user
        if not method == 9:
            # If 'remove encryption' was selected
            if method == "remove":
                # Delete the selected encryption method
                delete_encryption = sql.SQL("DELETE FROM {table} WHERE id = %s").format(
                    table=sql.Identifier(user_session))
                cursor.execute(delete_encryption, characters)
                # Reset the user's session sequence (for the table ids) to start again at 1
                # alter sequence: https://www.postgresql.org/docs/current/sql-altersequence.html
                reset_sequence = sql.SQL("ALTER SEQUENCE {seq} RESTART WITH 1").format(
                    seq=sql.Identifier(user_seq))
                cursor.execute(reset_sequence)
                # Update all the user's table id numbers using the user's reset sequence
                # default: https://www.postgresql.org/docs/9.3/ddl-default.html
                update_id = sql.SQL("UPDATE {table} SET id = DEFAULT").format(
                    table=sql.Identifier(user_session))
                cursor.execute(update_id)

    # 5. Log the user's most recent encryption specification (if one has been been submitted)
            else:
                # Ititiate a query to insert the data into the current 'user_session' table
                add_encryption = sql.SQL("INSERT INTO {table}"
                                         "(method, characters, location, custom_location)"
                                         "VALUES ({fields})").format(
                    fields=sql.SQL(',').join([
                        sql.Literal(method),
                        sql.Literal(characters),
                        sql.Literal(location),
                        sql.Literal(custom_location),
                    ]),
                    table=sql.Identifier(user_session))
                cursor.execute(add_encryption)

    # 6. Get the updated user session table data - including the most recent addition or removal
        # Ititiate query to select all data from 'user_session' table
        # The table now includes the user's most recent encryption data
        fetch_data = """SELECT * FROM %s"""
        cursor.execute(fetch_data % user_session)
        table = cursor.fetchall()
        # Commit the transactions
        manucrypt_db.commit()
        # Close the cursor
        cursor.close()

    # The user will need a way to remember all of their encryption methods
    # An encryption key must be created as a list of readable sentences that the user can remember
    # The data for each encryption method must be converted into a readable sentence
    # The list variable 'encryption_key' will be used to store this data

    # 7. Extract the data from the current user session table and enter it into the 'encryption_key' list
        # Set the encryption method number 'n' as 1 (we'll use this later)
        n = 1
        # For each encryption method specificed by the user
        # Extract the data from the current user session table
        for row in table:
        # Method:
            key_method = row[1]
        # Characters:
            key_characters = row[2]
        # Location:
        # Define 'key_location' as the section of the sentence to be read as the location
            # If a custom location is used
            if row[4] > 0:
                # Then use inflect to get ordinals of the location numbers
                x = inflect.engine()
                # Create the location section of the sentence
                if row[1] == "Add":
                    key_location = "at the " + \
                        x.ordinal(row[4]) + " place in"
                elif row[1] == "Replace":
                    key_location = "with the " + \
                        x.ordinal(row[4]) + " character in"
                elif row[1] == "Capitalise":
                    key_location = "the " + \
                        x.ordinal(row[4]) + " character in"
            # If the user has selected a location from the dropdown list
            else:
                # Then the location section of the sentence is pre-defined in encryption.html
                key_location = row[3]
            # Input all data from current table row into an 'encryption_method' dictionary
            encryption_method = {
                "id": n,
                "method": key_method,
                "characters": key_characters,
                "location": key_location
            }
            # We will use 'n' defined earlier as the encryption_method number
            # Iterate to next number
            n = (n + 1)
            # Add the 'encryption_ method' dictionary data to the 'encryption_key' list
            encryption_key.append(encryption_method)
    # Complete transaction according to: https://www.postgresqltutorial.com/postgresql-python/transaction/
    except psycopg2.DatabaseError as error:
        print(error)
    finally:
        if manucrypt_db is not None:
            manucrypt_db.close()

    # 9. Return 'method' to flag any false entries and the 'encryption_key' as a list of dictionaries
        # Where each 'encryption_method' dictionary in the list corresponds to an encryption method entered by the user
        # These 'encryption_method' dictionaries will be used to form the list of sentences which together form the user's encrytion key
    return (encryption_key, method)
