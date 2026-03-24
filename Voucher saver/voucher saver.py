import json as js

def main():
    try:
        with open("voucher_data.json", "r") as file:
            data = js.load(file)
    except FileNotFoundError:
        with open("./Voucher saver/voucher_data.json", "w") as file:
            data = js.load(file)
    
    print("Welcome to the Voucher Saver!")

if __name__ == "__main__":
    main()