# Function for adding characters:
def add(base, characters, location, custom_location):

    # Define list to append characters to - one at a a time
    character_list = []

    if location == "at the beginning of":
        # Append the user input characters first
        character_list.append(characters)
        # Then append the rest of the base
        character_list.append(base)

    elif location == "at the end of":
        # Append the base first...
        character_list.append(base)
        # Then append the user input characters
        character_list.append(characters)

    elif location == "between all characters in":
        # Iterating through the base
        for x in range(len(base)):
            # Append each character in the base
            character_list.append(base[x])
            if x < (len(base) - 1):
                # Then append the user input characters
                character_list.append(characters)

    elif location == "specific location":
        # Iterating through the base
        for x in range(len(base)):
            # If x is equal to the custom location...
            if (x+1) == custom_location:
                # Append the user input characters
                character_list.append(characters)
                # Then append the original base character for this location
                character_list.append(base[x])
            else:
                # Otherwise just continue to append the characters of the base
                character_list.append(base[x])

    # Join the character list into a single string
    password = "".join(character_list)

    # Return the new password with the encryption included
    return password


# Function for replacing characters
def replace(base, characters, location, custom_location):

    # Define list to append characters to - one at a a time
    character_list = []

    # Define the location as a number

    if location == "with the first character of":
        # Define location as 1
        location = [1]

    elif location == "with the last character of":
        # Define location as the last character in the base
        location = [len(base)]

    elif location == "with every other character in":
        # Define location as a list
        location = []
        # Iterate through the length of the base
        for x in range(len(base)+1):
            # Append even numbers to the location list
            if (x % 2) == 0:
                location.append(x)

    elif location == "specific character":
        # Define the location as specified by the user
        location = [custom_location]

    # Then iterate through the characters in the base
    for x in range(len(base)):
        # If x is found in the location list
        if (x+1) in location:
            # Append the user input characters
            character_list.append(characters)
        else:
            # Otherwise append the characters of the base
            character_list.append(base[x])

    # Join the character list into a single string
    password = "".join(character_list)

    # Return the base with the encryption included
    return password


# Function for capitalising characters:
def capitalise(base, location, custom_location):

    # Define list to append characters to - one at a a time
    character_list = []

    # Define the location as a number

    if location == "the first character of":
        # Define location as 1
        location = [1]

    elif location == "the last character of":
        # Define location as the last character in the base
        location = [len(base)]

    elif location == "the first & last characters of":
        # Define the locations as 1 and the last character in the base
        location = [1, len(base)]

    elif location == "every other character of":
        # Define location as a list
        location = []
        # Iterate through the length of the base
        for x in range(len(base)):
            # Append even numbers to the location list
            if (x % 2) == 0:
                location.append(x + 1)

    elif location == "specific character":
        # Define the location as specified by the user
        location = [custom_location]

    # Then iterate through the characters in the base
    for x in range(len(base)):
        # If the current character is alphabetic
        if base[x].isalpha():
            # And if x is found in the location list...
            if (x+1) in location:
                # Capitalise the character
                character_list.append(base[x].upper())
            else:
                # Otherwise just append the original character from the base
                character_list.append(base[x])
        # If the current character in the base is a symbol or number...
        else:
            # Just append as is
            character_list.append(base[x])

    # Join the character list into a single string
    password = "".join(character_list)

    # Return the base with the encryption included
    return password
