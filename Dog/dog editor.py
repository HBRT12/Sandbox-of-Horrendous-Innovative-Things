import json  # Access save data
import tkinter as tk  # GUI

def get_data():
    try:
        with open("./Dog/Stored_dogs.json") as dogs:  # Imports data from JSON
            stored_dog_dict = json.load(dogs)
            print("Successfully loaded stored data from JSON file")
    except FileNotFoundError:
        try:
            with open("Stored_dogs.json") as dogs:
                stored_dog_dict = json.load(dogs)
                print("Successfully loaded stored data from JSON file")
        except Exception as e:
            print(f"Failed to load stored dogs: {e}")
            return {}
    except Exception as e:
        print(f"Error reading stored dogs: {e}")
        return {}
    return stored_dog_dict

data = get_data()  # Load data from JSON file
print(data["0179571f"])