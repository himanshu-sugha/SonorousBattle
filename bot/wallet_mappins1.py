import json

# Global dictionary to store user wallet mappings
user_wallet_mapping = {}

def load_user_wallet_data():
    """
    Loads user wallet data from a JSON file and updates the global variable.
    """
    global user_wallet_mapping
    print("load_user_wallet_data--------------------------------------------starts")
    try:
        # Open the JSON file and load data into the global dictionary
        with open("../user_wallet_mapping.json", "r") as file:
            user_wallet_mapping = json.load(file)
            print("user_wallet_mapping loaded successfully:", user_wallet_mapping)
    except FileNotFoundError as e:
        print("Error:", e)
        print("File not found. Initializing with an empty dictionary.")
        user_wallet_mapping = {}

# Load data into the global variable
load_user_wallet_data()

# Print the final global variable
print("user_wallet_mapping after loading:", user_wallet_mapping)
