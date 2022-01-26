from application import manucrypt_app
from application.session_config import session_config
from application.user_session import user_session
from application.user_inputs import user_input_data
from application.password_strength import password_strength
from flask import render_template, request

# Flask session configuration setup
session_config()


@manucrypt_app.route("/")
# Index page - introducing how the website works
def index():
    # Return 'introduction' page
    return render_template("introduction.html")


@manucrypt_app.route("/getting_started", methods=["GET", "POST"])
# User chooses first encyption method to get started with their password encryption
def getting_started():
    # Run user_session function to set or reset the user session
    user_session()
    # Return the 'getting started' page
    return render_template("getting_started.html")


@manucrypt_app.route("/results", methods=["GET", "POST"])
# Results page displaying details of the user's current password and password analysis
def result():
    # If user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
    # 1. Get user inputs and create the user's encrypted password
        user_inputs = user_input_data()
        # Check for error message
        if user_inputs[0] == "error":
            return render_template("error.html", apology=user_inputs[1], root=user_inputs[2])
    # 2. Get the password strength results from strength.py
        # Uses the Dropbox 'zxcvbn' algorithm: https://github.com/dropbox/zxcvbn
        strength = password_strength(user_inputs[0])
    # 3. Return the 'results' page with password analysis
        return render_template("results.html",
                               website=user_inputs[1],
                               password=user_inputs[0],
                               speed=strength[2],
                               score=strength[0],
                               comments=strength[1],
                               encryption_key=user_inputs[2],
                               mod=user_inputs[3],
                               )
    # Else if user reached route via GET (as by clicking a link or via redirect)
    else:
        # Return the results page
        return render_template("results.html")


if __name__ == "__main__":
    manucrypt_app.run(debug=True)
