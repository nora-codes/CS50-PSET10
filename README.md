# CS50-PSET10 Final Project: Manucrypt

## Summary

### Video Demo

https://youtu.be/xbEME2TbwcQ

### Description

A website where users can create, modify and strength test a unique and universal
password encryption key - to use on all of their accounts.

Languages used: Python, PostgreSQL, Flask, Jinja, Javascript, HTML, CSS

### References

Deployed on Heroku:
https://www.heroku.com

Password speed calculated using Dropbox 'zxcvbn' alogrithm for Python:
https://github.com/dwolfhub/zxcvbn-python

## Project Details: Setup

### Procfile

Used to declare what command should be executed to start the app.

Ref: https://devcenter.heroku.com/articles/getting-started-with-python#define-a-procfile

### requirements.txt

Used to list the required packages for the app.

Ref: https://boscacci.medium.com/why-and-how-to-make-a-requirements-txt-f329c685181e

### run.py

Used to point Flask to the app and setting it to run.

Ref: Guidance from https://www.section.io/engineering-education/complete-guide-on-installing-flask-for-beginners/

### runtime.txt

Used to specify which runtime to use on the app.

Ref: https://devcenter.heroku.com/articles/python-runtimes

### __init__.py

Used to specify that the directories containing the file should be treated as packages.

Ref: https://newbedev.com/flask-importerror-no-module-named-app

### database.py

Reads the database connection url from the environment variable.

### session_config.py

Sets the Flask session configuration

### layout.html

Sets out the .html template to use with Jinja for all pages, including meta tags, fonts,
stylesheets, header and footer.

### error.html

Displays an error page when an error has been made by the user, showing an apology
specific to the error.

## Project Details: Run

### manucrypt.py

Assigns the three .html pages to their respective app functions. Each function gets the
required data for the page and renders the templates.

Introduction:
- Route "/"
- Function index()
- Renders introduction.html

Getting Started:
- Route "/getting_started"
- Function getting_started()
- Calls user_session.py
- Renders getting_started.html

Result:
- Route "/results"
- Function result()
- Calls user_inputs.py
- Calls password_strength.py
- Renders error.html
- Renders results.html

## Project Details: Introduction

### introduction.html

Displays a welcome page with information (in collapsabble text boxes) including:
- Why it's important to use different and complex passwords for each of your accounts
- An explantion of what encryption is
- What the website does and how to use it

Followed by a button that sends the user to the 'getting started page'

### user session.py

- Function user_session()
- No return values

Called from the 'getting started' page and initiates a session for the encryption.
The session will be used to store data for the user's current encryption key in the
database.

A 'users table' is created for the user to store the session information:
- id: A number between 1 and 20. The program will take the next available number.
- session: A session name that is created and stored as a session variable
- time: A timestamp from when the session was initiated. This is used to reallocate
the oldest row in the table to the current user if there are no empty rows to use.

An 'encryption table' is created to store the user's encryption data from the current
session:
- id: Uses a sequence that is created and stored as a session variable. The sequence
starts at 1 and moves up in increments of 1. If a row is deleted in the table by the
user, this sequence will be missing a number. In this case, the sequence and all the id
numbers can be reset.
- method: This is the method of encryption chosen by the user. The options are 'add
- characters', 'replace characters' and 'capitalise characters'.
- location: This is the location of the chosen encryption in the password. This will
be stored as characters because the user will choose the location from a dropdown list,
with options such as 'first character', 'last character' and 'between all characters'.
- custom location: This is an option column for when the user inputs a specific location
for the chosen encryption. The location is stored as a number where 1 reperesents the
first character, 2 represents the second, and so on.

If the user wants to start again with their encryption key and reset all the data,
they will be routed back to the 'getting started' page, which will call this 'user
session' function and a new session will be initiated

## Project Details: Getting Started

### getting_started.html

Displays a page for the user to enter the firest encryption method of their key.

The encryption will first be tested on the base word 'example', which creates a
password that would be used on www.example.com

A collapsable 'top tip' is included to give the user ideas on what types of
encryption would be useful on a real site

The the user input form is displayed using encryption.html. This is where the user specifies an encryption
method to include in their universal encryption key.

When the user clicks the 'test password' button, they are navigated to the results page.

### encryption.html

The user input form with the following options:

- Add characters: Type in characters to add and choose the location to add them either
from a dropdown list or manually entered by the user.

- Replace characters: Choose the location of the characters to replace, either from a
dropdown list or manually entered but the user and type in characters to replace them
with.

- Capitalise characters: Choose the location of the characters to capitalise, either from
a dropdown list or manually entered by the user.

### user_inputs.py

- Function getting_started()
- Calls encryption_log.py
- Calls password encryption.py
- Returns the encrypted password, the corresponding website and the encryption key
(optional: mod variable to check for modifications in the password)

Called from the user input form, which can be submitted by the user from the 'getting
started' or 'results' page.

The user's most recent encryption specification is extracted from the user input form:
- method: Encryption method (add, replace or capitalise)
- characters: Characters entered by the user for 'add' or 'replace' encryption methods.
- location: The location of the encryption method in the password, selected from a
dropdown list.
- custom location: When the user has entered a specific location for the encryption
method.
- remove: If the user has selected to remove an encryption method, this variable
specifies which encryption method to remove and it is removed using encryption_log.py
- base: The base word for the encryption. The user can choose the base word from a
dropdown list of website names or type in their own. If the user has not selected a base
word, then 'example' is used by default.
- website: Same as base, but without the encryption applied. This variable will be used
to display the website name, along with it's corresponding password.
- root: The .html page from which the form was submitted
- mod: A variable to record when a modification has been made to the password. If the
page has been refreshed for example, no modifications have been made.

When the program is extracting this data from the user input form, it looks for specific
errors caused by the user and returns a custom apology note based on the error.

The user's encryption table is accessed and all previously defined encryption methods
are applied to the base word using password_encryption.py

Then the user's most recent encryption method added to the user's encryption table using
encryption_log.py and an encyption key is created.

Then the user's most recent encryption method is applied to the base word using
password_encryption.py.

### encryption_log.py

- Function encryption_log()
- Returns the encryption key (optional: false entry)

Called from user_inputs.py, the encryption log is used to keep track of the user's
encryptions within the current session.

First, the data from the user's most recent request is updated in the user's encryption
table.

- If the user has added an encryption, the details of the encryption are inserted into the
table in the next available slot.

- If the user has requested to remove an encryption, the specificed encryption row is
removed from the encryption table. This however, causes the ids for the rows in the table
to be out of sequence, so the session variable sequence and ids in the table are reset.

Then, an encryption key is created to allow the user to remember all of their encryption
methods. The raw data from the encryption table is not readable, so a readable version
of the data is created as a list of sentences to be presented on the results page.

### password encryption.py

Called from user_inputs.py, the given encryption specification is applied to the base
word.

- Function encryption_add()
- Returns the encrypted password

Takes the base word and adds the user's specified characters to the word in the location
also specified by the user.

- Function encryption_replace()

Takes the base word and replaces the characters specified by the user with the characters
also specified by the user.

- Function encryption_capitalise()

Takes the base word and capitalises the characters specified by the user.

## Project Details: Results

### results.html

Displays the results of the user's encryptions so far. The page has been divided into
sections using jinja to reduce the length of the code. The sections include the following:

- Website: Displayed using password.html. Shows the website name that corresponds to the
password that has been created. If the user has not specified a website, then
www.example.com is used here.

- Password: Displayed using password.html. Shows the password that would be used with the
given website, including all of the user's encryptions so far.

- Hacker speed: Displayed using score.html. Shows the estimated hacker speed to guess the
given password, as calculated by 'zxcvbn'.

- Comments: Displayed using comments.html. Shows comments on the score of the password
to incentivise the user to achieve a 4/4 score.

- What next dropdown: Displayed using next.html. Gives the user options of what to do next with their password
encryption.

- Start over button: Displayed using restart.html. Creates a warning pop up to make sure
that the user wants to start over. If the user selects ok, they are navigated back to the
'getting started' page.

### password.html

Displays the website and password in simple text.

### score.html

Displays a box which changes colour in a traffic light system according to the password
score. The colour system used red for a low score, through to green for a good score.
When a 4/4 score is reached, the box flashes and turns to white and party popper emojis
are displayed. This gives the user incentive to achieve a high score with their
encryption. Due to the complexity of the code to acheive the changing colours, the actual
text is displayed using a seperate file - score_data.html.

### score_data.html

Displays the hacker speed and password score in simple text.

### comments.html

Displays the score comments in simple text.

### next.html

Displayed on the results.html page. Provides a dropdown of options to the user of what to
do next with the password encryption, including the following:

- Test the key on a different website: Diplayed using website.html. Give the user the
option to change the website from www.example.com. It can be changed to one of a list
of website options from the dropdown, or the user can manually input a website name.
- Add an encryption: Diplayed using encryption.html as used previously on
getting_started.html. This is the user same input form for the user to specify another
encryption method to include in their key.
- Remove an encryption: Provides a dropdown for users to select which of their existing
encryption methods to delete from the key.
- View password requirements: Diplayed using requirements.html. Show a list of password
requirements to help the user in creating encryption methods.
- View your encryption key: Diplayed using key.html. Shows the user's universal
encryption key to remember for all of their passwords. It is diplayed as a numbered list
of sentences describing each encryption method and the order in which to use them.

### website.html

Displays a dropdown of website options for the user to choose from. One of the options
is 'test your own...' where the user can type in a website name instead.

### encryption.html

See previous summary of encryption.html in the 'Project Details: Getting Started' section.

### requirements.html

Displays the same list in plain text as previously used in the 'top tip' sections of the
'getting started' page, showing password requirements that are typically required on
website accounts.

### key.html

Displays the user's encryption key in simple text.

### restart.html

Displays the 'start over' button and includes the script to trigger the warning pop-up
box to confirm the reset with the user.

### password_strength.py

- Function password_strength()
- Calls the Dropbox 'zxcvbn' algorithm: https://github.com/dropbox/zxcvbn
- Returns the password score, comments on the password and the hacker speed.

Called from the result() function in manucrypt.py, the given password is sent through the
'zxcvbn' program to get a strength analysis. Comments are then assigned to the password
score.





