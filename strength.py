from zxcvbn import zxcvbn
# Uses the Dropbox 'zxcvbn' algorithm: https://github.com/dropbox/zxcvbn


def password_strength(password):
    # Checks strength of password

    # Get password score from 'zxcvbn'
    check = zxcvbn(password)

    # Define result as a score out of 4 from 'zxcvbn'
    result = (str(check["score"]) + "/4")

    # Define comments for score 0
    if check["score"] == 0:
        comments = ("Risky business - that's way too guessable!")

    # Define comments for score 1
    elif check["score"] == 1:
        comments = ("Room for improvement - that's very guessable!")

    # Define comments for score 2
    elif check["score"] == 2:
        comments = ("Not too bad - that's somewhat guessable!")

    # Define comments for score 3
    elif check["score"] == 3:
        comments = ("Good job bud - that's safely unguessable!")

    # Define comments for score 4
    elif check["score"] == 4:
        comments = ("You nailed it - that's very unguessable!")

    # Define approximate hacking time for various hacker speeds from 'zxcvbn'
    speed_1 = ((check["crack_times_display"]
               ["online_throttling_100_per_hour"]))
    speed_2 = ((check["crack_times_display"]
               ["online_no_throttling_10_per_second"]))
    speed_3 = ((check["crack_times_display"]
               ["offline_slow_hashing_1e4_per_second"]))
    speed_4 = ((check["crack_times_display"]
               ["offline_fast_hashing_1e10_per_second"]))

    # Define password warnings from 'zxcvbn'
    if check["feedback"]["warning"]:
        warnings = ("Warning: " + (check["feedback"]["warning"]))
    else:
        warnings = 0

    # Define password suggestions from 'zxcvbn'
    n = len(check["feedback"]["suggestions"])
    if n == 0:
        suggestions = 0
    else:
        for x in range(n):
            suggestions = ("Suggestion: " +
                           (check["feedback"]["suggestions"][x]))

    # Return results of password strength test
    return(result, comments, speed_1, speed_2, speed_3, speed_4, warnings, suggestions)
