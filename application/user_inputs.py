import psycopg2
from application.database import database
from application.encryption_log import encryption_log
from application.password_encryption import encryption_add, encryption_replace, encryption_capitalise
from flask import request, session


def user_input_data():

    # The encryption method just submitted by the user is stored in the database
    # Along with all previous encryption methods submitted by the user in the current session
    # The password is created by using a base word and then applying the user's encryption to the word
    # The word 'example' is used by default, but the intention is for the website name to be used as the base word
    # The user can select website names from a dropdown list, or specify their own to test out the encryption

# 1. Set or reset initial variables
    # Read the database connection url from the enivronment variable
    DATABASE_URL = database()
    # Reset connection
    manucrypt_db = None
    # Set the custom location to '0' - for when a custom location is not selected
    custom_location = 0
    # When a change is made to the  encryption key - 'mod' will be set to 1 to signify a modification
    mod = 0
    # When the results page is returned - 'root' will record what page it has been returned from
    root = None

# 2. Get the encryption method selected by the user
    # Get the encryption method from the user input
    method = request.form.get("select_method")

# 3. Set the base word for the password
    # If the user has selected from the dropdown of website names on the encryption page
    # Then set the base as the selected website
    base = request.form.get("site_dropdown")
    # If the user has not selected from the dropdown of website names
    if not base:
        # Then look for a base word session variable that has been allocated in the current session
        base = session.get('user_base')
        # If a base word has not been previously allocated by the user
        if not base:
            # Then set the base as 'example' by default
            base = "example"

# 4. Check for a 'remove encryption' request from user
        # Find out which page the form was submitted from and set it as 'root'
        root = request.form['submit_button']
        # If the user submitted a form (by clicking the submit button)
        if root:
            # But an encryption method was not selected
            if not method:
                # The user may have sent a request to remove an encryption
                # If the user has selected an encryption method to remove
                if root == "remove":
                    # Then get the selected encryption
                    remove = request.form.get("remove_select")
                    # If an encryption selection is found
                    if remove:
                        # The encryption log is used to keep track of the user's encryptions within the current session
                        # Remove the specified encryption from the encryption log using the encryption_log function
                        encryption_key = encryption_log("remove", remove, 9, 9)
                        # Set 'mod' to 1 - to signify that a modification has been made to the encryption key
                        mod = 1
                    else:
                        # Then the user has not made a selection - return error message
                        apology = "You didn't specify an encryption to remove"
                        return ("error", apology, root, 0)
                # If the user has been directed from an apology
                elif root == "apology":
                    # Set 'mod' to 1 - to reset the results page
                    mod = 1
                else:
                    # The user has not filled out the form correctly - return error message
                    apology = "You didn't specify anything"
                    return ("error", apology, root, 0)

# 5. Check for a website selection from the user
    # If the user has selected from the dropdown of website names
    else:
        # Then check for a custom website (base word) input
        if base == "custom":
            # Find out which page the form was submitted from and set it as 'root'
            root = request.form['submit_button']
            # Set the base word as the user's custom input (website name)
            base = request.form.get("custom_site_input")
            # If the user has not filled in the custom input text field
            if not base:
                # Then return an error message
                apology = "You didn't type in a website name to test"
                return ("error", apology, root, 0)
        # Allocate 'base' to the session variable 'user_base'
        # This will maintain the base word throughout the user's session until changed by the user
        session['user_base'] = base
    # Set a 'website' variable as the same as the base word
    # This will be used to display the website name along with the encrypted password
    website = base

# 6. Look for previously defined encryptions from the current session
    try:
        # Create a new database connection
        manucrypt_db = psycopg2.connect(DATABASE_URL)
        # Create a new cursor
        cursor = manucrypt_db.cursor()
        # Get the user session name - to allocate the data to the corresponding encryption table
        user_session = session.get('user_session')
        # Ititiate query to select all data from the current 'user_session' encryption table
        # The table includes all previously specified encryptions
        fetch_data = """SELECT * FROM %s"""
        cursor.execute(fetch_data % user_session)
        table = cursor.fetchall()
        # Commit the transaction
        manucrypt_db.commit()
        # Close the cursor
        cursor.close()

# 7. Apply all pre-existing encryption methods to the password
        # For each existing encryption method in the table
        for row in table:
            # Define the specification for the encryption
            row_method = row[1]
            row_characters = row[2]
            row_location = row[3]
            row_custom_location = row[4]
            # Add the encryption specification to the base word using encryption.py
            # Then update the base word to include the new encryption
            if row_method == "Add":
                row_add = encryption_add(
                    base, row_characters, row_location, row_custom_location)
                base = row_add
            elif row_method == "Replace":
                row_replace = encryption_replace(
                    base, row_characters, row_location, row_custom_location)
                base = row_replace
            elif row_method == "Capitalise":
                row_capitalise = encryption_capitalise(
                    base, row_location, row_custom_location)
                base = row_capitalise
    # Complete transaction according to: https://www.postgresqltutorial.com/postgresql-python/transaction/
    except psycopg2.DatabaseError as error:
        print(error)
    finally:
        if manucrypt_db is not None:
            manucrypt_db.close()

# 8. Add the most recent encryption method submitted by the user

# 8a. If ecryption method 'Add' was selected by the user:
    # Get user inputs from the 'add' section of form
    if method == "Add":
        # Characters
        characters = request.form.get("characters_add")
        if not characters:
            # Return error message
            apology = "You didn't type in any characters"
            return ("error", apology, root, 0)
        # Location
        location = request.form.get("location_add")
        if not location:
            # Return error message
            apology = "You didn't choose a location"
            return ("error", apology, root, 0)
        else:
            # Custom Location
            if location == "specific location":
                custom_location = request.form.get("add_custom_input")
                if custom_location == '0':
                    # Return error message
                    apology = "If you want to add your characters at the beginning, use location number 1."
                    return ("error", apology, root, 0)
                if not custom_location:
                    # Return error message
                    apology = "You didn't type in a specific location"
                    return ("error", apology, root, 0)
                else:
                    custom_location = int(custom_location)
            # The encryption log is used to keep track of the user's encryption methods within the current session
            # Add the current encyption specification to the encryption log using encryption_log function
            log = encryption_log(
                method, characters, location, custom_location)
            # Extrapolate the encrypion key from the log
            encryption_key = log[0]
            # Check for a false entry from the log
            false_entry = log[1]
        # If a false entry is found
        if false_entry == 9:
            # Maintain the password from before refresh
            password = base
        else:
            # Else apply the current encryption specification to the base word - to create the password using encryption.py
            password = encryption_add(
                base, characters, location, custom_location)
        # Set 'mod' to 1 - to signify that a modification has been made to the encryption key
        mod = 1
        # Return the data to manucrypt.py
        return (password, website, encryption_key, mod)

# 8b. If ecryption method 'Replace' was selected by the user:
    # Get user inputs from the 'replace' section of form
    elif method == "Replace":
        # Characters
        characters = request.form.get("characters_replace")
        if not characters:
            # Return error message
            apology = "You didn't type in any characters"
            return ("error", apology, root, 0)
        # Location
        location = request.form.get("location_replace")
        if not location:
            # Return error message
            apology = "You didn't choose a location"
            return ("error", apology, root, 0)
        else:
            # Custom Location
            if location == "specific character":
                custom_location = request.form.get("replace_custom_input")
                if custom_location == '0':
                    # Return error message
                    apology = "If you want to replace the first character, use location number 1."
                    return ("error", apology, root, 0)
                if not custom_location:
                    # Return error message
                    apology = "You didn't type in a specific location"
                    return ("error", apology, root, 0)
                else:
                    custom_location = int(custom_location)
            # The encryption log is used to keep track of the user's encryption methods within the current session
            # Add the current encyption specification to the encryption log using encryption_log function
            log = encryption_log(
                method, characters, location, custom_location)
            # Define encryption key as a list
            encryption_key = list()
            # Extrapolate the data for the key from the log
            encryption_key = log[0]
           # Check for a false entry from the log
            false_entry = log[1]
        # If a false entry is found
        if false_entry == 9:
            # Maintain the password from before refresh
            password = base
        else:
            # Else apply the current encryption specification to the base word - to create the password using encryption.py
            password = encryption_replace(
                base, characters, location, custom_location)
        # Set 'mod' to 1 - to signify that a modification has been made to the encryption key
        mod = 1
        # Return the data to manucrypt.py
        return (password, website, encryption_key, mod)

# 8c. If ecryption method 'Capitalise' was selected by the user:
    # Get inputs from 'capitalise' section of the form
    elif method == "Capitalise":
        # Location
        location = request.form.get("location_capitalise")
        if not location:
            # Return error message
            apology = "You didn't choose a location"
            return ("error", apology, root, 0)
        else:
            # Custom Location
            if location == "specific character":
                custom_location = request.form.get(
                    "capitalise_custom_input")
                if custom_location == '0':
                    # Return error message
                    apology = "If you want to capitalise the first character, use location number 1."
                    return ("error", apology, root, 0)
                if not custom_location:
                    # Return error message
                    apology = "You didn't type in a specific location"
                    return ("error", apology, root, 0)
                else:
                    custom_location = int(custom_location)
            # The encryption log is used to keep track of the user's encryption methods within the current session
            # Add the current encyption specification to the encryption log using encryption_log function
            log = encryption_log(
                method, 0, location, custom_location)
            # Extrapolate the encrypion key from the log
            encryption_key = log[0]
            # Check for a false entry from the log
            false_entry = log[1]
        # If a false entry is found
        if false_entry == 9:
            # Maintain the password from before refresh
            password = base
        else:
            # Else apply the current encryption specification to the base word - to create the password using encryption.py
            password = encryption_capitalise(base, location, custom_location)
        # Set 'mod' to 1 - to signify that a modification has been made to the encryption key
        mod = 1
        # Return the data to manucrypt.py
        return (password, website, encryption_key, mod)

# 9. Refresh - if no selections have been made on the page, a browser refresh has occurred
    else:
        # Send a false entry to encryption log
        encryption_key = encryption_log(9, 9, 9, 9)
        # Extrapolate only the encryption key from the return data
        key = encryption_key[0]
        # Reset the password to the previous base word
        password = base
        # If the results page was loaded from the error page
        if root == 'error':
            # Then set mod to 1 - to reset the 'next' options
            mod = 1
        # Return the data to manucrypt.py
        return (password, website, key, mod)
