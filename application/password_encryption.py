# Function for adding characters:

def encryption_add(base, characters, location, custom_location):

    # 1. Define a list to append the password characters to (one at a time)
    character_list = []

# 2. Add the characters into the base word
    # Location: beginning
    if location == "at the beginning of":
        # Add the user input characters first
        character_list.append(characters)
        # Then add the rest of the base word characters
        character_list.append(base)
    # Location: end
    elif location == "at the end of":
        # Add the base word characters first...
        character_list.append(base)
        # Then add the user input characters
        character_list.append(characters)
    # Location: between
    elif location == "between all characters in":
        # Iterating through the base word characters
        for x in range(len(base)):
            # Add each character in the base
            character_list.append(base[x])
            if x < (len(base) - 1):
                # Then add the user input characters
                character_list.append(characters)
    # Location: custom
    elif location == "specific location":
        # Iterating through the base word characters
        for x in range(len(base)):
            # If x is equal to the custom location...
            if (x+1) == custom_location:
                # Add the user input characters
                character_list.append(characters)
                # Then add the original base word character for this location
                character_list.append(base[x])
            else:
                # Otherwise just continue to add the characters of the base word
                character_list.append(base[x])

# 3. Join the character list into a single string
    password = "".join(character_list)

# 4. Return the new password with the encryption included
    return password


# Function for replacing characters
def encryption_replace(base, characters, location, custom_location):

    # 1. Define list to append characters to (one at a time)
    character_list = []

# 2. Define the location as a number / numbers
    # Location: first
    if location == "with the first character of":
        # Define location as 1
        location = [1]
    # Location: last
    elif location == "with the last character of":
        # Define location as the last character in the base word
        location = [len(base)]
    # Location: alternate
    elif location == "with every other character in":
        # Define location as a list
        location = []
        # Iterate through the length of the base word
        for x in range(len(base)+1):
            # Add even numbers to the location list
            if (x % 2) == 0:
                location.append(x)
    # Location: custom
    elif location == "specific character":
        # Define the location as specified by the user
        location = [custom_location]

# 3. Iterate through the characters in the base and replace the specified characters
    for x in range(len(base)):
        # If x is found in the location list
        if (x+1) in location:
            # Add the user input characters
            character_list.append(characters)
        else:
            # Otherwise add the characters of the base word
            character_list.append(base[x])

# 4. Join the character list into a single string
    password = "".join(character_list)

# 5. Return the base with the encryption included
    return password


# Function for capitalising characters:
def encryption_capitalise(base, location, custom_location):

    # 1. Define list to append characters to (one at a time)
    character_list = []

# 2. Define the location as a number / numbers
    # Location: first
    if location == "the first character of":
        # Define location as 1
        location = [1]
    # Location: last
    elif location == "the last character of":
        # Define location as the last character in the base word
        location = [len(base)]
    # Location: first and last
    elif location == "the first & last characters of":
        # Define the locations as 1 and the number of the last character in the base word
        location = [1, len(base)]
    # Location: alternate
    elif location == "every other character of":
        # Define location as a list
        location = []
        # Iterate through the length of the base word
        for x in range(len(base)):
            # Add even numbers to the location list
            if (x % 2) == 0:
                location.append(x + 1)
    # Location: custom
    elif location == "specific character":
        # Define the location as specified by the user
        location = [custom_location]

# 3. Iterate through the characters in the base and capitalise the specified characters
    for x in range(len(base)):
        # If the current character is alphabetic
        if base[x].isalpha():
            # And if x is found in the location list...
            if (x+1) in location:
                # Capitalise the character
                character_list.append(base[x].upper())
            else:
                # Otherwise just add the original character from the base
                character_list.append(base[x])
        # If the current character in the base is a symbol or number...
        else:
            # Just add as is
            character_list.append(base[x])

# 4. Join the character list into a single string
    password = "".join(character_list)

# 5. Return the base with the encryption included
    return password
