import os


def database():

    # Read the database connection url from the enivronment variable
    DATABASE_URL = os.environ.get('DATABASE_URL')

    return DATABASE_URL
