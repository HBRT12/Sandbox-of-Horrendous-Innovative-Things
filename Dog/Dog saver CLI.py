import json  # Needed for saving data
import os  # Needed to check system info for clear
import time  # needed for time delays
import uuid  # Needed to uniquely store entries

try:
    with open("./Dog/Stored_dogs.json") as dogs:  # Imports data from JSON
        stored_dog_dict = json.load(dogs)
        print("Successfully loaded stored data from JSON file.")
except:
    with open("Stored_dogs.json") as dogs:  # Imports data from JSON
        stored_dog_dict = json.load(dogs)
        print("Successfully loaded stored data from JSON file.")
time.sleep(1)

def store_dog(dog_dict, dog_data):
    dog_dict[dog_data[6]] = {"Name": dog_data[0],
                             "Age": dog_data[1],  # Adds user's dog information to imported dictionary
                             "Age in dog years": dog_data[2],
                             "Breed": dog_data[3],
                             "Fur type": dog_data[4],
                             "Privacy": dog_data[5]}

def get_user_info():
    dog_name = input("What is your dog called>>> ")
    try:
        age = int(input("How old is your dog?>>> "))
        age_in_dog_years = age * 7  # Calculates age in dog years
    except:  # Prevents crash from inputting non-int characters
        age = "No age provided"
        age_in_dog_years = "N/A"
    breed = input("What breed is your dog?>>> ")
    fur_type = input("What fur type does your dog have?>>> ")
    privacy = input("Do you want your data hidden when loaded?>>> ")
    if privacy.lower() in ["no", "nope", "n", "nah"]:  # Check if user doesn't want input hidden when loaded in Dog loader.py
        return [dog_name.capitalize(), age, age_in_dog_years, breed.capitalize(), fur_type.capitalize(), False, str(uuid.uuid4())[:8]]
    else:  # Returns True or False as last entry, depending on privacy input
        return [dog_name.capitalize(), age, age_in_dog_years, breed.capitalize(), fur_type.capitalize(), True, str(uuid.uuid4())[:8]]

def upload_dog_data(dog_dict):
    try:
        with open("./Dog/Stored_dogs.json","w") as dogs_file:  # Dumps dictionary with new entry to save file
            json.dump(dog_dict, dogs_file, indent=4)
    except:
        with open("Stored_dogs.json", "w") as dogs_file:
            json.dump(dog_dict, dogs_file, indent=4)
def display_info(user_info):
    os.system('cls' if os.name == 'nt' else 'clear')  # Clears terminal for better readability
    print(f"""Name: {user_info[0]}
    Age:{user_info[1]} (or {user_info[2]} in human years)
    Breed: {user_info[3]}
    Fur type: {user_info[4]}
    Keep data private: {user_info[5]}
    Entry ID: {user_info[6]}""")  # For context to indexes, see lines 28/30

user_inputs = get_user_info()  # Gets information from user
store_dog(stored_dog_dict, user_inputs)  # Stores information onto the dictionary
upload_dog_data(stored_dog_dict)  # Stores the dictionary to the JSON file-
display_info(user_inputs)  # Displays the user's input back to them in a formatted way
