from zxcvbn import zxcvbn
# Uses the Dropbox 'zxcvbn' algorithm: https://github.com/dropbox/zxcvbn


def password_strength(password):
    # Checks strength of password

# 1. Define a password score
    # Get password score from 'zxcvbn'
    check = zxcvbn(password)
    # Define score as a score out of 4 from 'zxcvbn'
    score = (str(check["score"]) + "/4")

# 2. Define comments for the score
    # Score: 0
    if check["score"] == 0:
        comments = ("Risky business - that's way too guessable!")
    # Score: 1
    elif check["score"] == 1:
        comments = ("Room for improvement - that's very guessable!")
    # Score: 2
    elif check["score"] == 2:
        comments = ("Not too bad - that's somewhat guessable!")
    # Score: 3
    elif check["score"] == 3:
        comments = ("Good job bud - that's safely unguessable!")
    # Score: 4
    elif check["score"] == 4:
        comments = ("You nailed it - that's very unguessable!")

# 3. Define approximate hacking time for offline slow hashing from 'zxcvbn'
    speed = ((check["crack_times_display"]
              ["offline_slow_hashing_1e4_per_second"]))

# 4. Return results of password strength test
    return(score, comments, speed)
