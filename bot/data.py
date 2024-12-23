import json

# Predefined mappings
GENRES = {
    "Pop": 5,  # Payment amount for Pop genre
    "Rock": 10,
    "Hip-Hop": 15,
    "Classical": 3,
    "electronic":10,
    "jazz":20,
}

CREATOR_NAME_MAPPING = {
    "0x14dC79964da2C08b23698B3D3cc7Ca32193d9955": "Creator A",
    "0x23618e81E3f5cdF7f54C3d65f7FBc0aBf5B21E8f": "Creator B",
    "0xa0Ee7A142d267C1f36714E4a8F75612F20a79720": "Creator C",
    "0xBcd4042DE499D14e55001CcbB24a551F3b954096": "Creator D",
    "0x71bE63f3384f5fb98995898A86B02Fb2426c5788": "Creator E",
    "0x1CBd3b2770909D4e10f157cABC84C7264073C9Ec": "Creator F",
    "0xdF3e18d64BC6A983f673Ab319CCaE4f1a57C7097": "Creator G",
    "0xcd3B766CCDd6AE721141F452C550Ca635964ce71": "Creator H",
}

# Convert the dictionary keys (addresses) to a list
addresses_list = list(CREATOR_NAME_MAPPING.keys())

SONG_CREATOR_MAPPING = {
    "Pop": [
        {"song": "Pop Song 1", "creator": "0x14dC79964da2C08b23698B3D3cc7Ca32193d9955"},
        {"song": "Pop Song 2", "creator": "0x23618e81E3f5cdF7f54C3d65f7FBc0aBf5B21E8f"},
    ],
    "Rock": [
        {"song": "Rock Song 1", "creator": "0xa0Ee7A142d267C1f36714E4a8F75612F20a79720"},
        {"song": "Rock Song 2", "creator": "0xBcd4042DE499D14e55001CcbB24a551F3b954096"},
    ],
    "Hip-Hop": [
        {"song": "Hip-Hop Song 1", "creator": "0x71bE63f3384f5fb98995898A86B02Fb2426c5788"},
        {"song": "Hip-Hop Song 2", "creator": "0x1CBd3b2770909D4e10f157cABC84C7264073C9Ec"},
    ],
    "Classical": [
        {"song": "Classical Song 1", "creator": "0xdF3e18d64BC6A983f673Ab319CCaE4f1a57C7097"},
        {"song": "Classical Song 2", "creator": "0xcd3B766CCDd6AE721141F452C550Ca635964ce71"},
    ],
}

def is_valid_json(response_text):
    try:
        # Try to parse the response as JSON
        json.loads(response_text)
        return True
    except json.JSONDecodeError:
        # If an error occurs during parsing, it's not valid JSON
        return False

def sanitize_string(input_string):
    """
    Removes special characters like double quotes from the input string.
    """
    return input_string.replace('"', '').strip()
