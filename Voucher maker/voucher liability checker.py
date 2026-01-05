import time
import random
import os  # For checking if the text file exists

def generate_voucher_code():
    chars = "ABCDEFGHIJKLMNOPQRSTUYVXYZ0123456789"  # Possible characters
    coderaw = [random.choice(chars) for _ in range(16)]  # Make voucher
    coderaw.insert(4, "-")  # Insert dashes
    coderaw.insert(9, "-")
    coderaw.insert(14, "-")
    return ''.join(coderaw)  # Join the list into a string

def read_existing_codes(file_name):
    # If the file exists, read and return the list of existing codes
    if os.path.exists(file_name):
        with open(file_name, "r") as file:
            return {line.strip() for line in file}  # Use a set for fast lookup
    return set()

def save_code(file_name, code):
    # Append the new code to the file
    with open(file_name, "a") as file:
        file.write(code + "\n")

# Main program
spent = float(input("How much did you spend? (£)>>> "))
if spent >= 150:
    print("You received a £10 voucher!\nYour code is now being generated.")
    
    file_name = "voucherhistory.txt"  # sets file name
    existing_codes = read_existing_codes(file_name)  # Load past codes
    
    codecooked = generate_voucher_code()
    
    if codecooked in existing_codes:  # Check if code is a dupe
        print("Error: Duplicate voucher code detected! Generation failed. reopen to try again")
    else:
        save_code(file_name, codecooked)  # Save the unused code
        print(f"Your voucher code is: {codecooked}")
else:
    print("Sorry, you have not recieved a voucher, ")
