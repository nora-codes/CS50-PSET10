import mysql.connector
import inflect

from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from encryption import add, replace, capitalise
from strength import password_strength


# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded (Harvard CS50: Finance project documentation)
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Postgress / SQL Alchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/[LucyNora]'
db = SQLAlchemy(app)
engine = create_engine('postgresql://localhost/[YOUR_DATABASE_NAME]')

# Ensure responses aren't cached (Harvard CS50: Finance project documentation)


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Initialise database
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="7Znuawk59L",
    database="mydatabase"
)
cursor = mydb.cursor()


@app.route("/")
# Index page - introducing how the website works
def index():

    # Return 'introduction' page
    return render_template("introduction.html")


@app.route("/getting_started", methods=["GET", "POST"])
# User chooses first encyption method to get started with their custom encryption
def getting_started():

    # Check database for existing tables
    cursor.execute("Show tables;")
    tables = cursor.fetchall()

    # If 'user_encryptions' table already exists - delete the data
    if tables:
        for x in tables[0]:
            if x == 'user_encryptions':
                sql = "DROP TABLE user_encryptions"
                cursor.execute(sql)

    # Create a new table for user encryption inputs
    cursor.execute("CREATE TABLE user_encryptions(id INT AUTO_INCREMENT PRIMARY KEY, method varchar(255), characters varchar(255), location varchar(255), custom_location INT)")

    # Return 'getting started' page
    return render_template("getting_started.html")


@app.route("/encryption", methods=["GET", "POST"])
# Encryption page displaying details of the user's current encryption methods
def encryption():

    # If user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Get the encryption method from the user input
        method = request.form.get("select_method")

        # Set the base for the password (this will be the website name)
        # If the user has selected from a dropdown of site names on the encryption page...
        # Set the base as the selected site
        base = request.form.get("site_dropdown")

        # If the user has not selected from the dropdown of site names...
        if not base:

            # Then set the base as 'example' for now
            base = "example"

            # Find out which page the form was submitted from and set it as 'root'
            root = request.form['submit_button']

            # If a from was submitted by the user...
            if root:

                # And if an encryption method was not selected..
                if method == "Select":

                    # Then the user has not filled out the form correctly
                    # Return error message
                    apology = "You didn't specify anything"
                    return render_template("error.html", apology=apology, root=root)

        # If the user has selected from the dropdown of site names...
        else:

            # Check for custom site input
            if base == "custom":

                # Find out which page the form was submitted from and set it as 'root'
                root = request.form['submit_button']

                # Set the base as the user's custom input
                base = request.form.get("custom_site_input")

                # If the user has not filled in the custom input text field...
                if not base:

                    # Return error message
                    apology = "You didn't type in a website name to test"
                    return render_template("error.html", apology=apology, root=root)

        # Set 'site' as the same as the base
        # This will be used to display the site name along with the encrypted password
        site = base

        # Set the custom location to '0' - for when a custom location is not selected
        custom_location = 0

        # Ititiate mysql query to select all data from 'user_encryptions' table
        # The 'user_encryptions' table includes all previously specified encryptions
        cursor = mydb.cursor()
        sql_select_query = "SELECT * FROM user_encryptions"
        cursor.execute(sql_select_query)
        table = cursor.fetchall()

        # Apply all existing encryption methods from the table to the password

        # For each existing encryption method in the table...
        for row in table:

            # Define the specification for the encryption
            row_method = row[1]
            row_characters = row[2]
            row_location = row[3]
            row_custom_location = row[4]

            # Add the encryption to the base
            # Then update the base to the new encryption
            if row_method == "Add":
                row_add = add(
                    base, row_characters, row_location, row_custom_location)
                base = row_add
            elif row_method == "Replace":
                row_replace = replace(
                    base, row_characters, row_location, row_custom_location)
                base = row_replace
            elif row_method == "Capitalise":
                row__capitalise = capitalise(
                    base, row_location, row_custom_location)
                base = row__capitalise

        # Then add the most recent encryption from the user inut form - to the base

        # Get inputs from 'add' section of form
        # Render error messages where user errors are found
        if method == "Add":

            # Characters
            characters = request.form.get("characters_add")
            if not characters:
                apology = "You didn't type in any characters"
                return render_template("error.html", apology=apology, root=root)

            # Location
            location = request.form.get("location_add")
            if location == "specific location":

                # Custom Location
                custom_location = request.form.get("add_custom_input")
                if not custom_location:
                    apology = "You didn't type in a specific location"
                    return render_template("error.html", apology=apology, root=root)
                else:
                    custom_location = int(custom_location)

            # Add the encyption specification to the encryption log
            log = encryption_log(
                method, characters, location, custom_location)

            # Get the password encryption output from encryption.py
            password = add(base, characters, location, custom_location)

            # Test the password strength and return 'encryptions' page
            return test(password, site, log)

        # Get inputs from 'replace' section of form
        # Render error messages where user errors are found
        elif method == "Replace":

            # Characters
            characters = request.form.get("characters_replace")
            if not characters:
                apology = "You didn't type in any characters"
                return render_template("error.html", apology=apology, root=root)

            # Location
            location = request.form.get("location_replace")
            if location == "specific character":

                # Custom Location
                custom_location = request.form.get("replace_custom_input")
                if not custom_location:
                    apology = "You didn't type in a specific location"
                    return render_template("error.html", apology=apology, root=root)
                else:
                    custom_location = int(custom_location)

            # Add the encyption specification to the encryption log
            log = encryption_log(method, characters,
                                 location, custom_location)

            # Get the password encryption output from encryption.py
            password = replace(
                base, characters, location, custom_location)

            # Test the password strength and return 'encryptions' page
            return test(password, site, log)

        # Get inputs from 'capitalise' section of form
        # Render error messages where user errors are found
        elif method == "Capitalise":

            # Location
            location = request.form.get("location_capitalise")
            if location == "specific character":

                # Custom Location
                custom_location = request.form.get("capitalise_custom_input")
                if not custom_location:
                    apology = "You didn't type in a specific location"
                    return render_template("error.html", apology=apology, root=root)
                else:
                    custom_location = int(custom_location)

            # Add the encyption specification to the encryption log
            log = encryption_log(
                method, 0, location, custom_location)

            # Get the password encryption output from encryption.py
            password = capitalise(base, location, custom_location)

            # Test the password strength and return 'encryptions' page
            return test(password, site, log)

        # If the user did not input any additional encryption methods
        else:

            # Send a false entry to encryption log
            log = encryption_log(9, 9, 9, 9)

            # Reset the password base
            password = base

            # Test the password strength and return 'encryptions' page
            return test(password, site, log)

    # Else if user reached route via GET (as by clicking a link or via redirect)
    else:

        # Return the encryption page
        return render_template("encryption.html")


def encryption_log(method, characters, location, custom_location):
    # Log user encryption specification

    # Ititiate mysql query to select all data from 'user_encryptions' table
    # The 'user_encryptions' table includes all previously specified encryptions
    sql_select_Query = "select * from user_encryptions"
    cursor.execute(sql_select_Query)
    table = cursor.fetchall()
    last = cursor.rowcount

    # Check for browser refresh
    # Where the specification will be the same as the last row in the table
    for row in table:
        if last == row[0]:
            if method == row[1] and location == row[3] and custom_location == row[4]:
                if characters == int(row[2]) or characters == row[2]:
                    # If browser has been refreshed - log the entry as false
                    method = 9

    # Log the encryption entry (as long as the entry is not false - 9)
    if not method == 9:

        # Ititiate mysql query to insert the data into the 'user_encryptions' table
        add_encryption = ("INSERT INTO user_encryptions"
                          "(method, characters, location, custom_location)"
                          "VALUES (%s, %s, %s, %s)")
        encryption_data = (method, characters, location, custom_location)
        cursor.execute(add_encryption, encryption_data)
        mydb.commit()

    # Ititiate mysql query to select all data from 'user_encryptions' table
    sql_select_Query = "select * from user_encryptions"
    cursor.execute(sql_select_Query)
    table = cursor.fetchall()

    # Create a copy of the user_encryptions table data and enter it into a python list called 'keys'
    # This list can be used to display the data back to the user on the encryptions page as encryption keys
    keys = list()

    # Input data into the 'keys' list
    for row in table:

        # If a custom location is used...
        if row[4] > 0:
            # Use inflect to get ordinals of the location numbers
            x = inflect.engine()
            # Create an encryption keys for the user to remember
            if row[1] == "Add":
                log_location = "at the " + \
                    x.ordinal(row[4]) + " place in"
            elif row[1] == "Replace":
                log_location = "with the " + \
                    x.ordinal(row[4]) + " character in"
            elif row[1] == "Capitalise":
                log_location = "the " + \
                    x.ordinal(row[4]) + " character in"

        # If a location is used from a dropdown list...
        else:
            # Encryption keys for the user are defined in form.html
            # And used directly from the 'user_encryptions' table
            log_location = row[3]

        # Define data from the current table row
        table_id = row[0]
        method = row[1]
        characters = row[2]
        location = row[3]
        custom_location = row[4]

        # Input all data from current table row into a dictionary
        data = {
            "id": table_id,
            "method": method,
            "characters": characters,
            "location": log_location
        }

        # Add the dictionary data to the list of keys
        keys.append(data)

    # Return the keys as a list of dictionaries
    # Where each dictionary in the list corresponds to an encryption method entered by the user
    # And each dictionary contains the specification of the encryption method entered by the user
    return keys


def test(password, site, log):

    # Get the password strength results from strength.py
    # Uses the Dropbox 'zxcvbn' algorithm: https://github.com/dropbox/zxcvbn
    strength = password_strength(password)

    # Extrapolate results from return data
    result = strength[0]
    comments = strength[1]
    speed_1 = strength[2]
    speed_2 = strength[3]
    speed_3 = strength[4]
    speed_4 = strength[5]
    warnings = strength[6]
    suggestions = strength[7]

    # Return the 'encryption' page with password analysis
    return render_template("encryption.html",
                           site=site,
                           log=log,
                           password=password,
                           result=result,
                           comments=comments,
                           speed_1=speed_1,
                           speed_2=speed_2,
                           speed_3=speed_3,
                           speed_4=speed_4,
                           warnings=warnings,
                           suggestions=suggestions)


if __name__ == "__main__":
    app.run(debug=True)
