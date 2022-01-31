# CS50-PSET10 Final Project: Manucrypt

### Description

A website where users can create, modify and strength test a unique and universal
password encryption key that they can use on all of their online accounts.

Languages used: Python, PostgreSQL, Flask, Jinja, Javascript, HTML, CSS

### Video Demo

https://youtu.be/xbEME2TbwcQ

### Personal Comments

I have been encrypting my passwords using this method for years and during this time,
I have been explaining the idea to anyone that would listen. I thought it would be a
useful tool to create for my final project and help others in using my password method.

I started very small and wrote a program that worked on the command line. I then scaled
it to work as a web page, spent some time on the UX/UI and added a database to allow
for multiple encryption methods.

I then used [Heroku](https://www.heroku.com) to get it online for others to access. I
chose this platform after some research as it promised to get the app up and running
very quicky. In hindsight though, I regret this decision because in the time it
***actually*** took me to learn how to get the app working on Heroku, I could have
invested that time learning how to deploy the app online myself.

Since it has been running online, I have expanded the database to allow multiple users
to access the website simultaneously. This meant that I could send it to
friends for feedback. They were able to point out improvements in the UI/UX and find
bugs that I was unaware of.

After implementing all of the feedback and refining the app further, I decided to
finish working on the project. I have come so far since the beginning of this
project and learned so much more than I thought I woul - in order to get it to
work the way that it does.

All this growth however, means that if I were to start the project again, I would
definitely write the code in a completely different, much more efficient way. But
that's ok. For now, the app is working and available for people to access and
maybe I can come back to it in the future and make it much, much better!

### References

- Deployed on [Heroku](https://www.heroku.com).
- Password speed calculated using Dropbox [zxcvbn](https://github.com/dwolfhub/zxcvbn-python)
alogrithm for Python.
- Other references used in the writing of this app are included in the notes of the files.

## Project Details: TLDR Summary

Details of all the individual files in the app are included in the sections below, but
if that's too much to read, here is a summary of what the app does:

The tools on the website allow the user to design an encryption key to use on
passwords for all of their online accounts. This means that instead of having to
remember different passwords for each account, or even use a password manager, all
the user needs to do is remember one encryption key.

In order to use encrytion, the user needs text to encrypt. A 'base word' is used
as the inital text to be encrypted and once encryption has been used to modify
the base word, it can be used as a password. The more the base word is encrypted,
the more difficult it is to hack into. The base word used on this app is the name
of the website for which the user is creating a password.

   *For example, if the website is facebook, the base word for the password will be facebook.*

The user first creates a single encryption method to apply to the base word.

   *For example, if the encryption is:*

     *"add a '#' to the end of the text"*

    *The output of the password for facebook would be 'facebook#' or the password*
    *for instagram would be 'instagram#' and so on...*

The default website is "ww<span>w.</span>example.com" and the corresponding base word for this
website is "example". The user's encryption is initially applied to this default word
"example". The app then analyses this "example" password output and provides the user with a
strength score and an approximate hacking speed.

The user can then add or remove single encryption methods to the overall encryption
until they are happy with their password score and hacker speed. The user can also test their
encryption with other websites, as this changes the password and concequently, the strength
of the password.

Once the user is happy with their encryption, they can view an encryption key which
lists all of their current encryption methods, so they can memorise the key and start
using it on their actual passwords.

## Project Details: Setup

### [Procfile](/Procfile)

Used to declare what command should be executed to start the app on [Heroku](https://www.heroku.com).

### [requirements.txt](/requirements.txt)

Used to list the required packages for the app.

### [run.py](/run.py)

Used to point Flask to the app and set it to run.

### [runtime.txt](/runtime.txt)

Used to specify which runtime to use on the app.

### [init.py](/application/__init__.py)

Used to specify that the manucrypt directory is a Python package.

### [database.py](/application/database.py)

Reads the database connection url from the environment variable.

### [session_config.py](/application/session_config.py)

Sets the Flask session configuration.

### [layout.html](/application/templates/layout.html)

Sets out the .html template to use with Jinja for all pages, including meta tags, fonts,
stylesheets, header and footer.

### [error.html](/application/templates/error.html)

A template to display an apology when an error has been made by the user, showing an
apology message that is specific to the error.

## Project Details: Run

### [manucrypt.py](/application/manucrypt.py)

The main / root Python file that assigns the three .html pages to their respective app
functions. Each function gets the required data for the page and renders the html
templates.

**Introduction Page**:

Introduce the user to the website and the password encryption concept:

- Route: "/"
- Function: [index()](/application/manucrypt.py)
- Renders: [introduction.html](/application/templates/introduction.html)

**Getting Started Page**:

Guides the user through their first encryption method:

- Route: "/getting_started"
- Function: [getting_started()](/application/manucrypt.py)
- Calls: [user_session.py](/application/user_session.py)
- Renders: [getting_started.html](/application/templates/getting_started.html)

**Results Page**:

Applies the user's first encryption method to an example website and password and
presents a password strength analysis. The user can also add or remove other
encrytion methods to their universal encryption key, test the encryption out on other
websites and view their encryption key for memorisation.

- Route: "/results"
- Function: [result()](/application/manucrypt.py)
- Calls: [user_inputs.py](/application/user_inputs.py)
- Calls: [password_strength.py](/application/password_strength.py)
- Renders: [results.html](/application/templates/results.html)

## Project Details: Introduction Page

### [introduction.html](/application/templates/introduction.html)

Displays a welcome page with information including:
- Why it's important to use different and complex passwords for each of your accounts.
- An explantion of what encryption is.
- What the website does and how to use it.

Followed by a button that sends the user to the
[***getting_started.html***](/application/templates/getting_started.html) page.

## Project Details: Getting Started Page

### [user_session.py](/application/user_session.py)

- ***Function:*** [***user_session()***](/application/user_session.py)
- ***Return: None***

Before the [***getting_started.html***](/application/templates/getting_started.html) is rendered,
the user_session() function is called from [manucrypt.py](/application/manucrypt.py)
and initiates a session for the encryption.The session will be used to store data for
the user's current encryption key in the database.

**Users Table**

A table is created for the user to store their session information:

- *ID*: A number between 1 and 20. The program will take the next available number.

- *Session*: A session name is created in the format *"user_session_ID"* and stored as
a session variable.

- *Time*: A timestamp from when the session was initiated. This is used to reallocate
the oldest row in the table to the current user, if there are no empty rows to use.

**Encryption Table**

A table is created to store the user's encryption data from the current session:

- *ID*: A sequence is created, stored as a session variable and used to allocate the
next available ID number. The sequence starts at 1 and moves up in increments of 1. If
a row is deleted in the table by the user (because they request to remove an
encryption), an ID number in the table will be missing and the IDs will be out of
sequence. In this case, the session sequence is reset back to 1 and all of the IDs in
the table are reallocated in sequence.

- *Method*: The method of encryption chosen by the user. The options are 'add
characters', 'replace characters' and 'capitalise characters'.

- *Location*: The location of the chosen encryption within the password. The user can
choose the location from a dropdown list, with options such as 'first character',
'last character' and 'between all characters'.

- *Custom Location*: This is an optional column in the table for when the user wants
to add their encryption in a location not provided in the dropdown list. The location
is stored as a number where 1 reperesents the first character in the password, 2
represents the second, and so on.

If the user wants to start again with their encryption key and reset all of the data,
they will be routed back to the [***getting_started.html***](/application/templates/getting_started.html)
page, which will call [***user_session.py***](/application/user_session.py) again and
a new session will be initiated.

### [getting_started.html](/application/templates/getting_started.html)

Once a session has been initiated in [***user_session.py***](/application/user_session.py)
this page is displayed for the user to enter the first encryption method of their key.

It is explained to the user that the encryption will first be tested on the base word
'example', which creates a password that would be used for a website called
'ww<span>w.</span>example.com'

A collapsable 'top tip' is included to give the user ideas on what types of encryption would
be useful on a real website.

[***Encryption.html***](/application/templates/encryption.html) (see Project Details: Password Encryption
section) is used to display the user input form. This form is where the user specifies an encryption method to include
in their universal encryption key.

When the user clicks the 'test password' button, [***user_inputs.py***](/application/user_inputs.py)
(see Project Details: Password Encryption section) is called and they are navigated
to the [***results.html***](/application/templates/results.html) page.

## Project Details: Results Page

### [user_inputs.py](/application/user_inputs.py)

- ***Function:*** [***user_input_data()***](/application/user_inputs.py)
- ***Calls:*** [***encryption_log.py***](/application/encryption_log.py)
- ***Calls:*** [***password_encryption.py***](/application/password_encryption.py)
- ***Returns: The encrypted password, the corresponding website and the encryption key***
(optional: mod variable to check for modifications in the password)

Called from result() function in [***manucrypt.py***](/application/manucrypt.py) to extract
all just data submitted by the user.

See previous summary of [***user_inputs.py***](/application/user_inputs.py) in the
'Project Details: Getting Started' section, which calls [***password_encryption.py***](/application/password_encryption.py)
and [***encryption_log.py***](/application/encryption_log.py).

### [password_strength.py](/application/password_strength.py)

- ***Function:*** [password_strength()](/application/password_strength.py)
- ***Calls: Dropbox*** [***zxcvbn***](https://github.com/dwolfhub/zxcvbn-python)
- ***Returns: The password score, comments on the password and the hacker speed***

In the results() function of [***manucrypt.py***](/application/manucrypt.py), the
encrypted password, the corresponding website and the encryption key are returned from
[***user_inputs.py***](/application/user_inputs.py) (see Project Details: Password
Encryption section). The password_strength() function is then called to get a strength
analysis of the password using ['zxcvbn'](https://github.com/dwolfhub/zxcvbn-python). A
password score, comments and hacking speed are assigned to the password.

### [results.html](/application/templates/results.html)

Once all the data has been collected, the [***results.html***](/application/templates/results.html)
page displays the results of the user's encryptions so far. The page has been divided
into sections using jinja to reduce the length of the code. The sections include the
following:

- *Website*: Displayed using [***password.html***](/application/templates/password.html). Shows the
website name that corresponds to the password that has been created. If the user has not
specified a website, then 'ww<span>w.</span>example.com' is used here.

- *Password*: Displayed using [***password.html***](/application/templates/password.html). Shows
the encrypted password that would be used with the given website, including all of the
user's encryptions in the session.

- *Hacker speed*: Displayed using [***score.html***](/application/templates/score.html). Shows the
estimated hacker speed to guess the given password, as calculated by ['zxcvbn'](https://github.com/dwolfhub/zxcvbn-python).

- *Comments*: Displayed using [***comments.html***](/application/templates/comments.html). Shows
comments on the score of the password to incentivise the user to achieve a 4/4 score.

- *'What Next' Dropdown*: Displayed using [***next.html***](/application/templates/next.html).
Gives the user options of what to do next with their password encryption.

- *'Start Over' Button*: Displayed using [***restart.html***](/application/templates/restart.html).
- Produces a warning pop-up to make sure that the user wants to start over. If the user
selects ok, they are navigated back to the [***getting_started.html***](/application/templates/getting_started.html)
page.

### [password.html](/application/templates/password.html)

Displays the website and password in simple text.

### [score.html](/application/templates/score.html)

Displays a box which changes colour in a traffic light system according to the password
score. The colour system uses red for a low score, through to green for a good score.
When a 4/4 score is reached, the box flashes and turns to white and party popper emojis
are displayed. This gives the user incentive to achieve a high score with their
encryption. Due to the repetetive nature of the code required to acheive the changing
colours, the actual text of the score is displayed using a seperate file -
[***score_data.html***](/application/templates/score_data.html).

### [score_data.html](/application/templates/score_data.html)

Displays the hacker speed and password score in simple text.

### [comments.html](/application/templates/comments.html)

Displays the score comments in simple text.

### [next.html](/application/templates/next.html)

Provides a dropdown list, giving the user options of what to do next with the
encryption, including the following:

- *Test the key on a different website*: Displayed using [***website.html***](/application/templates/website.html).
Gives the user the option to change the website from 'ww<span>w.</span>example.com'. It
can be changed to one of a list of website options from the dropdown, or the user can
manually input a website name.

- *Add an encryption*: Diplayed using [***encryption.html***](/application/templates/encryption.html)
(see Project Details: Password Encryption section) as used previously on [***getting_started.html***](/application/templates/getting_started.html).
This is the same user input form to specify an additional encryption method to
include in their universal key.

- *Remove an encryption*: Provides a dropdown for users to select which of their existing
encryption methods to delete from the key. The deletion is executed by [***encryption_log.py***](/application/encryption_log.py)
(see Project Details: Password Encryption section).

- *View password requirements*: Displayed using [***requirements.html***](/application/templates/requirements.html).
Shows a list of standard password requirements to help the user in creating new
encryption methods.

- *View your encryption key*: Displayed using [***key.html***](/application/templates/key.html).
Shows the user's universal encryption key to memorise for all of their passwords.

### [website.html](/application/templates/website.html)

Displays a dropdown of website options for the user to choose from. One of the options
is 'test your own...', where the user can type in a website custom name instead.

### [requirements.html](/application/templates/requirements.html)

Displays the same list in plain text as previously used in the 'top tip' sections of the
[**getting_started.html**](/application/templates/getting_started.html) page, shows
password requirements that are typically required on website accounts.

### [key.html](/application/templates/key.html)

Displays the user's encryption key as a numbered list of sentences describing each
encryption method and the order in which to use them.

### [restart.html](/application/templates/ )

Provides a 'start over' button and includes the script to trigger a warning pop-up
box to confirm the reset with the user.

## Project Details: Password Encryption

### [encryption.html](/application/templates/encryption.html)

Contains the user input form with the following options:

- *Add Characters*: The user types in characters to add to the password and chooses the
location for them within the password, either from a dropdown list or entered manually.

- *Replace Characters*: The user chooses the location of the characters in the password
to replace, either from a dropdown list or entered manually. Then they type in
new characters to replace the old ones with.

- *Capitalise Characters*: The user chooses the location of the characters to
capitalise, either from a dropdown list or entered manually.

### [user_inputs.py](/application/user_inputs.py)

- ***Function:*** [***user_input_data()***](/application/user_inputs.py)
- ***Calls:*** [***encryption_log.py***](/application/encryption_log.py)
- ***Calls:*** [***password_encryption.py***](/application/password_encryption.py)
- ***Returns: The encrypted password, the corresponding website and the encryption key***
(optional: mod variable to check for modifications in the password)

Once the user has submitted the user input form on the [***getting_started.html***](/application/templates/getting_started.html)
or [***results.html***](/application/templates/results.html) page. The user_input_data()
function is called.

The user's most recent encryption specification is extracted from the user input form
and entered (along with other information) into the following variables:
- *Method*: Encryption method (add, replace or capitalise)

- *Characters*: Characters entered by the user for the 'add' or 'replace' encryption
methods.

- *Location*: The location of the encryption method within the password, selected from a
dropdown list.

- *Custom Location*: When the user wants to input a speicific location that is not
listed in the dropdown options.

- *Remove*: If the user has selected to remove an encryption method, this variable
specifies which encryption method to remove and it is removed using [***encryption_log.py***](/application/encryption_log.py).

- *Base*: The base word for the encryption. The base word is the name of the website
for which the password is being created. The user can choose the base word from a
dropdown list of website names or type in their own. If the user has not selected a
base word, then 'example' is used by default.

- *Website*: Same as the baseword , but without the encryption applied. This variable
will be used to display the website name to the user, along with it's corresponding
password.

- *Root*: The .html page from which the form was submitted.

- *Mod*: A variable to record when a modification has been made to the password. If the
page has been refreshed for example, no modifications have been made.

When the program is extracting this data from the user input form, it looks for
errors caused by the user and returns a custom apology note on the [***error.html***](/application/templates/error.html)
page, based on the specific error.

The user's most recent encryption method added to the user's encryption table on the
database using [***encryption_log.py***](/application/encryption_log.py), and an
encyption key is created.

The user's updated encryption table is then used to apply all previously defined
encryption methods to the base word, along with the most recently specified one, using
[***password_encryption.py***](/application/password_encryption.py).

### [error.html](/application/templates/error.html)

See previous summary of [***error.html***](/application/templates/error.html) in the
'Project Details: Setup' section.

### [encryption_log.py](/application/encryption_log.py)

- ***Function:*** [***encryption_log()***](/application/encryption_log.py)
- ***Returns: The encryption key*** (optional: false entry)

Called from [***user_inputs.py***](/application/user_inputs.py), the encryption log is
used to keep track of the user's encryptions within the current session, using the
database.

First, the data from the user's most recent request is updated the user's encryption
table.

- If the user has added an encryption, the specification of the encryption are inserted
into the table in the next available slot.

- If the user has requested to remove an encryption, the specificed encryption row is
removed from the table. When a row is removed from the table, an ID number
in the table will be missing and the IDs will be out of sequence. In this case, the
session sequence is reset back to 1 and all of the IDs in the table are reallocated
in sequence.

Once the table has been updated, an encryption key is created to allow the user to
remember all of their encryption methods. The raw data from the encryption table is not
readable, so a readable version of the data is created as a list of clear sentences to
be presented on the [***results.html***](/application/templates/results.html) page.

### [password_encryption.py](/application/password_encryption.py)

- ***Function:*** [***encryption_add()***](/application/password_encryption.py)
- ***Function:*** [***encryption_replace()***](/application/password_encryption.py)
- ***Function:*** [***encryption_capitalise()***](/application/password_encryption.py)
- ***Returns: The encrypted password***

Called from [***user_inputs.py***](/application/user_inputs.py), once the user's
encryption table has been updated in the database with the most recent entry, it
can be applied to the base word. There are three functions in this file:

- *Add Function*: Takes the base word and adds the user's specified characters to the
word in the location specified.

- *Replace Function*: Takes the base word and replaces the characters specified by the
user with the characters specified.

- *Capitalise Function*: Takes the base word and capitalises the characters specified by
the user.
