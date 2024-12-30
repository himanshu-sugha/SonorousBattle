from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes , CallbackContext
import requests ,logging
import json , random 
import googleapiclient.discovery

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)
# Backend API URL
BASE_URL = "http://localhost:5000"
# Command: /votetrack


api_service_name = "youtube"
api_version = "v3"
api_key = 'AIzaSyCvFmxeLHGXeZ285886WEuHev9W8QJ81eA';
youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=api_key)

from data import addresses_list , sanitize_string , GENRES , is_valid_json


from wallet_mappins1 import user_wallet_mapping


async def vote_track(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Votes for a track in a battle."""
    if len(context.args) != 4:
        await update.message.reply_text("Usage: /votetrack <battleId> <trackNumber> <userAddress> <paymentAmount>")
        return

    try:
        # Extracting arguments
        battleId, trackNumber, userAddress, paymentAmount = context.args
        payload = {
            "battleId": int(battleId),
            "trackNumber": int(trackNumber),
            "userAddress": userAddress,
            "paymentAmount": paymentAmount,
        }

        # Making API request
        response = requests.post(f"{BASE_URL}/votetrack", json=payload)
        data = response.json()

        if response.status_code == 200:
            message = (
                f"✅ {data['message']} \n"
                f"Transaction Hash: {data.get('transactionHash', 'N/A')}"
            )
        else:
            message = f"❌ Error: {data.get('error', 'Unknown error')}"
    except ValueError:
        message = "❌ Invalid input. Ensure that <battleId> and <trackNumber> are numbers."
    except Exception as e:
        logger.error(f"Exception occurred: {e}")
        message = "❌ Failed to connect to the backend."

    await update.message.reply_text(message)

# Command: /battlevotes
async def get_votes(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Fetches current votes for a battle."""
    if len(context.args) != 1:
        await update.message.reply_text("Usage: /battlevotes <battleId>")
        return

    battleId = context.args[0]

    try:
        response = requests.get(f"{BASE_URL}/battle/{battleId}/votes")
        
        try:
            data = response.json()
        except ValueError:
            logger.error("Invalid JSON response")
            await update.message.reply_text("❌ Backend returned an invalid response.")
            return

        if response.status_code == 200:
            message = (
                f"🎶 Battle ID: {data['battleId']}\n"
                f"Track 1 Votes: {data['track1Votes']}\n"
                f"Track 2 Votes: {data['track2Votes']}"
            )
        else:
            message = f"❌ Error: {data['error']}"
    except Exception as e:
        logger.error(e)
        message = "❌ Failed to connect to the backend."

    await update.message.reply_text(message)

# Command: /battledetails
async def get_battle_details(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Fetches details of a battle."""
    if len(context.args) != 1:
        await update.message.reply_text("Usage: /battledetails <battleId>")
        return

    battleId = context.args[0]

    try:
        response = requests.get(f"{BASE_URL}/battle/{battleId}/details")
        data = response.json()

        if response.status_code == 200:
            message = (
                f"🎶 Battle ID: {data['battleId']}\n"
                f"Track 1: {data['track1']} (Votes: {data['votesTrack1']})\n"
                f"Track 2: {data['track2']} (Votes: {data['votesTrack2']})\n"
                f"Timestamp: {data['timestamp']}"
                f"Active: {'Yes' if data['isActive'] else 'No'}\n"
            )
        else:
            message = f"❌ Error: {data['error']}"
    except Exception as e:
        logger.error(e)
        message = "❌ Failed to connect to the backend."

    await update.message.reply_text(message)

# Command: /battlevoters
async def get_total_voters(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Fetches total voters for a battle."""
    if len(context.args) != 1:
        await update.message.reply_text("Usage: /battlevoters <battleId>")
        return

    battleId = context.args[0]

    try:
        response = requests.get(f"{BASE_URL}/battle/{battleId}/voters")
        data = response.json()

        if response.status_code == 200:
            message = f"🎶 Total Voters for Battle {data['battleId']}: {data['totalVoters']}"
        else:
            message = f"❌ Error: {data['error']}"
    except Exception as e:
        logger.error(e)
        message = "❌ Failed to connect to the backend."

    await update.message.reply_text(message)

# Command: /leaderboard
async def leaderboard(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Fetches the leaderboard for top tracks."""
    try:
        if len(context.args) != 1:
            await update.message.reply_text("Usage: /leaderboard <battleId>")
            return
        battle_id = context.args[0]  
        response = requests.get(f"{BASE_URL}/leaderboard/{battle_id}")  # Pass battleId here
        data = response.json()

        if response.status_code == 200:
            leaderboard_text = "🎶 Leaderboard\n"
            for idx, entry in enumerate(data['leaderboard']):
                leaderboard_text += f"{idx+1}. {entry['track']} - {entry['votes']} votes\n"
        else:
            leaderboard_text = f"❌ Error: {data['error']}"
    except Exception as e:
        logger.error(e)
        leaderboard_text = "❌ Failed to connect to the backend."

    await update.message.reply_text(leaderboard_text)

# Command: /closebattle
async def close_battle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Closes a battle and retrieves the winner."""
    try:
        # Making API request to get the winner after battle is closed
        battleId = context.args[0] 
        response = requests.get(f"http://localhost:5000/battle/{battleId}/winner")
        data = response.json()

        if response.status_code == 200:
            winnerVotersList = data.get("winnerVotersList", [])
            winner = data.get("part1","N/A")
            resultMessage=data.get("resultMessage","Not able to get Balance Sheet")
            
            voters = "\n".join(winnerVotersList)
            message = f"👥 {winner} \n\n👥 Winner Voters are : {voters}\n\n Balance Sheet\n\n {resultMessage}"
        else:
            message = f"❌ Error: {data.get('error', 'Unknown error')}"

    except Exception as e:
        logger.error(f"Exception occurred: {e}")
        message = "❌ Failed to connect to the backend."

    await update.message.reply_text(message)

# Command: /balance
async def get_balance(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Fetches and displays the current balance."""
    try:
        # Making API request
        response = requests.get("http://localhost:5000/balance")
        data = response.json()

        if response.status_code == 200:
            balance = data.get("balance", "Unknown")
            message = f"💰 Current Balance: {balance}"
        else:
            message = f"❌ Error: {data.get('error', 'Unable to fetch balance')}"
    except Exception as e:
        logger.error(f"Exception occurred: {e}")
        message = "❌ Failed to connect to the backend."

    await update.message.reply_text(message)

# Command: /voterslist
async def get_voters_list(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Fetches and displays the voters list for a specific battle in a visually appealing format.
    """
    if len(context.args) != 1:
        await update.message.reply_text(
            "Usage: /voterslist <battleId>\nExample: /voterslist 12345"
        )
        return

    battle_id = context.args[0]

    try:
        # Making API request
        response = requests.get(f"http://localhost:5000/battle/{battle_id}/votersList")
        data = response.json()

        if response.status_code == 200:
            battle_id = data.get("battleId", "Unknown")
            voters_list = data.get("votersList", [])

            if voters_list:
                voters = "\n".join([f"🔸 {voter}" for voter in voters_list])
                message = (
                    f"👥 **Voters for Battle ID {battle_id}:**\n\n"
                    f"{voters}"
                )
            else:
                message = f"👥 **No voters yet for Battle ID {battle_id}.**"
        else:
            message = f"❌ **Error:** {data.get('error', 'Unable to fetch voters list')}"

    except Exception as e:
        logger.error(f"Exception occurred: {e}")
        message = "❌ **Failed to connect to the backend. Please try again later.**"

    await update.message.reply_text(message, parse_mode="Markdown")

# Command: /transfertouser
async def transfer_to_owner(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Transfers money from the contract to the specified user address."""
    if len(context.args) != 3:
        await update.message.reply_text("Usage: /transfertouser <amount> <userAddress> <senderAddress>")
        return

    amount, userAddress, senderAddress = context.args
    payload = {"userAddress": userAddress, "amount": amount, "senderAddress": senderAddress}

    try:
        # Making POST request
        response = requests.post("http://localhost:5000/transferToOwner", json=payload)
        data = response.json()

        if response.status_code == 200 and data.get("success"):
            message = f"✅ Transfer successful to address: {userAddress}"
        else:
            message = f"❌ Transfer failed: {data.get('error', 'Unknown error occurred')}"
    except Exception as e:
        logger.error(f"Exception occurred: {e}")
        message = "❌ Failed to connect to the backend."

    await update.message.reply_text(message)

async def fetch_battle_data(payload):
    """Function to fetch battle data from the backend."""
    try:
        logger.info(f"Payload type: {type(payload)}")
        logger.info(f"Raw payload: {payload}")
        
        # Make sure payload is a proper dictionary
        if isinstance(payload, str):
            payload = json.loads(payload)  # Convert string to dict if needed
        
        response = requests.post(
            f"{BASE_URL}/startbattle", 
            json=payload,
            headers={'Content-Type': 'application/json'}
        )
        
        logger.info(f"Response status: {response.status_code}")
        
        if response.status_code == 200:
            return response.json()
        else:
            logger.error(f"Error response: {response.text}")
            return {"error": f"HTTP {response.status_code}: {response.text}"}
    except json.JSONDecodeError as e:
        logger.error(f"JSON Decode Error: {e}")
        raise
    except Exception as e:
        logger.error("Error during request:", exc_info=True)
        raise Exception("Failed to connect to the backend") from e

# Callback handler for genre selection
async def handle_genre_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles genre selection, starts the battle, and sets up voting UI."""
    query = update.callback_query
    await query.answer()

    # Extract selected genre
    print(f"Callback data received: {query.data}")
    _, genre = query.data.split("|")
    print(f"Selected genre: {genre}")

    # Step 1: Fetch two random tracks from Spotify for the selected genre
    try:
        print("Fetching tracks from YouTube...")
    # Search for tracks in the specified genre
        search_response = youtube.search().list(
        q=f"{genre} song",  # Adding 'song' to the query to filter results
        type="video",
        part="id,snippet",
        maxResults=10
        ).execute()

        tracks = search_response["items"]
        print(f"Tracks fetched: {len(tracks)} found.")

        # Filter out non-song results by checking titles or descriptions
        filtered_tracks = [
        track for track in tracks
        if "song" in track["snippet"]["title"].lower()
        or "official audio" in track["snippet"]["title"].lower()
        or "official music video" in track["snippet"]["title"].lower()
        ]

        print(f"Filtered tracks: {len(filtered_tracks)} found.")

        if len(filtered_tracks) < 2:
            print("Not enough tracks found.")
            return {"error": "❌ Not enough tracks found in the selected genre."}

        # Randomly select two tracks
        selected_tracks = random.sample(filtered_tracks, 2)
        track1 = selected_tracks[0]
        track2 = selected_tracks[1]
        selected_addresses = random.sample(addresses_list, 2)
        creator1 = selected_addresses[0]
        creator2 = selected_addresses[1]

        # Extract track details
        track1_id = track1["id"]["videoId"]
        track1_name = sanitize_string(track1["snippet"]["title"])
        track1_artist = sanitize_string(track1["snippet"]["channelTitle"])
        track1_preview = f"https://www.youtube.com/watch?v={track1_id}"
        track1_thumbnail = track1["snippet"]["thumbnails"]["high"]["url"]  # Higher quality thumbnail

        track2_id = track2["id"]["videoId"]
        track2_name = sanitize_string(track2["snippet"]["title"])
        track2_artist = sanitize_string(track2["snippet"]["channelTitle"])
        track2_preview = f"https://www.youtube.com/watch?v={track2_id}"
        track2_thumbnail = track2["snippet"]["thumbnails"]["high"]["url"]

        # Debug track details
        print(f"Track 1: {track1_name} by {track1_artist}")
        print(f"Track 2: {track2_name} by {track2_artist}")
        print(f"Track 1 Preview: {track1_preview}")
        print(f"Track 2 Preview: {track2_preview}")

    # Create dictionary for track details
        tracks_data = {
        track1_id: {"name": track1_name, "artist": track1_artist, "preview": track1_preview},
        track2_id: {"name": track2_name, "artist": track2_artist, "preview": track2_preview},
        }

        dictionaryStoringArtistsWithWalletAddresses = {
        creator1: track1_artist,
        creator2: track2_artist,
        }
    except Exception as e:
        logger.error(f"Error fetching tracks: {e}")
        print(f"Error fetching tracks: {e}")
        await query.edit_message_text("❌ Failed to fetch tracks from Youtube.")

    # Step 3: Get payment amount for the selected genre
    payment_amount = GENRES.get(genre, 0)
    print(f"Payment amount for {genre}: {payment_amount}")

    # Retrieve the wallet address
    user_address = ""
    try:
        user_id = query.from_user.id  # Get the unique user ID
        user_id=str(user_id)

    # Check if the user's wallet is stored in the global mapping
        print("trying to get the wallet address:")
        print("wallet mapping:",user_wallet_mapping)
        if user_id not in user_wallet_mapping:
            await query.edit_message_text("❌ You haven't set your wallet address yet. Use /setwallet to set it.")
            return

    # Retrieve the wallet address for the user
        user_address = user_wallet_mapping[user_id]["wallet"]
        await query.edit_message_text(f"✅ Your wallet address is {user_address}.")
    except Exception as e:
        logger.error(f"Exception occurred: {e}")
        await query.edit_message_text("❌ Failed to retrieve wallet address.")


    except Exception as e:
        logger.error(f"Exception occurred: {e}")
        print(f"Exception occurred while fetching wallet: {e}")
        await query.edit_message_text("❌ Failed to retrieve wallet address.")
        return

    # Step 4: Prepare payload
    payload = {
        "track1": track1_name,
        "track2": track2_name,
        "creatorTrack1": creator1,
        "creatorTrack2": creator2,
        "userAddress": user_address,
        "paymentAmount": payment_amount,
    }
    
    print(f"Payload prepared: {payload}")
    payload = json.dumps(payload)
    if is_valid_json(payload):
        print(f"\n\n\nValid json payload\n")
    else:
        print(f"\n\n\n Invalid json payload\n\n")
    print(f"Dumped Payload prepared: {payload}")

    try:
        data = await fetch_battle_data(payload)  # Call the separate function for fetching data
        
        if "error" in data:
            # If an error is found in the data, return the error message
            await query.edit_message_text(f"❌ Error: {data['error']}")
            return

        battleId = data.get("battleId", "N/A")
        if battleId == "N/A":
            await query.edit_message_text("❌ Battle creation failed.")
            return

        message = (
            f"🎵 {data['message']}\n"
            f"Battle ID: {battleId}\n"
            f"Balance Before: {data['balanceBefore']}\n"
            f"Balance After: {data['balanceAfter']}\n"
            f"Transaction Hash: {data['transactionHash']}"
        )
        await query.edit_message_text(message)
        print("after the sending transaction of battle start")

    except Exception as e:
        # General error handling
        logger.error("General error occurred", exc_info=True)
        await query.edit_message_text("❌ Failed to connect to the backend.")
        return

    # Run the asyncio event loop
    # asyncio.run(start_battle())

    # Step 6: Set up the voting UI
    messageToSendToCallBack=f"Vote for your favorite track below:\n\n"f"Track 1: {track1_name} by {creator1}\n"f"Track 2: {track2_name} by {creator2}\n"
    buttons = [
        [
            InlineKeyboardButton(
                f"🎵 Vote Track 1 (0 votes)",
                callback_data=f"vote|track1|{battleId}|{payment_amount}",
            ),
            InlineKeyboardButton(
                f"🎵 Vote Track 2 (0 votes)",
                callback_data=f"vote|track2|{battleId}|{payment_amount}",
            ),
        ]
    ]

    # Send tracks with thumbnails
    await query.message.reply_photo(
        photo=track1_thumbnail,
        caption=(
            f"🎵 Track 1: {track1_name}\n"
            f"By: {track1_artist}\n"
            f"[Preview]({track1_preview})"
        ),
        parse_mode="Markdown"
    )

    await query.message.reply_photo(
        photo=track2_thumbnail,
        caption=(
            f"🎵 Track 2: {track2_name}\n"
            f"By: {track2_artist}\n"
            f"[Preview]({track2_preview})"
        ),
        parse_mode="Markdown"
    )

    voting_keyboard = InlineKeyboardMarkup(buttons)

    await query.message.reply_text(
        f"Vote for your favorite track below:\n\n"
        f"Track 1: {track1_name} by {dictionaryStoringArtistsWithWalletAddresses[creator1]}\n"
        f"Track 2: {track2_name} by {dictionaryStoringArtistsWithWalletAddresses[creator2]}\n"
    )
    await query.message.reply_text("Give your votes here",reply_markup=voting_keyboard, )

# Callback handler for voting (handles both UI updates and functionality)
async def handle_voting(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles voting for tracks and updates the user with a separate message."""
    query = update.callback_query
    await query.answer()

    # Extract the data from the callback_data
    try:
        # Unpack the data based on the updated structure
        _, voted_track, battle_id, payment_amount= query.data.split("|")
    except ValueError:
        print("vote_track: ",vote_track,"battle_id: ",battle_id,"payment_amount: ",payment_amount)
        await query.message.reply_text("❌ Invalid voting data received. Please try again.")
        return

    # Convert battle_id and payment_amount to appropriate types
    try:
        battle_id = int(battle_id)  # Convert to integer if necessary
        payment_amount = float(payment_amount)  # Convert to float for numeric operations
    except ValueError:
        await query.message.reply_text("❌ Invalid data format in voting information.")
        return

    # Determine the track number (1 or 2) based on the vote
    track_number = 1 if voted_track == "track1" else 2

    user_address = ""
    try:
        user_id = query.from_user.id  # Get the unique user ID
        user_id=str(user_id)

    # Check if the user's wallet is stored in the global mapping
        if user_id not in user_wallet_mapping:
            await query.edit_message_text("❌ You haven't set your wallet address yet. Use /setwallet to set it.")
            return

    # Retrieve the wallet address for the user
        user_address = user_wallet_mapping[user_id]["wallet"]
        # await query.edit_message_text(f"✅ Your wallet address is {user_address}.")
    except Exception as e:
        logger.error(f"Exception occurred: {e}")
        await query.edit_message_text("❌ Failed to retrieve wallet address.")


    # Prepare the payload to send to the backend
    if not battle_id or not user_address or not payment_amount:
        await query.message.reply_text("❌ Missing required information to process your vote.")
        return

    payload = {
        "battleId": battle_id,
        "trackNumber": track_number,
        "userAddress": user_address,
        "paymentAmount": payment_amount,
    }

    transaction_hash = ""
    try:
        # Step 1: Make API request to process the vote
        print("YOUR PAYLOAD IS THIS:")
        print(payload)
        response = requests.post(f"{BASE_URL}/votetrack", json=payload)

        # Try to parse the JSON response
        data = response.json() if response.status_code == 200 else {}

        # Step 2: Handle response status codes
        message_from_backend=""
        if response.status_code == 200:
            transaction_hash = data.get("transactionHash", "N/A")
            message_from_backend = data.get("message", "N/A")

            if message_from_backend=="You have already voted in this battle." :
                message = message = "❌ You have already voted in this battle."
            elif transaction_hash!="N/A":
                message = (
                f"✅ Your vote for Track {track_number} has been recorded!\n"
                f"Transaction Hash: {transaction_hash}")
            else:
                message="ELse Case ----"
        elif response.status_code == 500 and message_from_backend=="Battle voting period has ended":
                message = "❌ Battle voting period has ended"
        else:
            # Handle non-200 status codes
            message = f"❌ Error: {data.get('error', 'Unknown error occurred.')}"
    except requests.exceptions.RequestException as e:
    # Catch network-related exceptions
        message = f"❌ Failed to connect to the backend. {str(e)}"

    # Send the user a separate response message
    await query.message.reply_text(message)

    # Step 2: Update the voting UI with backend vote counts

    try:
            # Fetch updated vote counts from the backend
            response = requests.get(f"{BASE_URL}/battle/{battle_id}/votes")
            data = response.json()

            if response.status_code == 200:
                buttons = [
                    [
                        InlineKeyboardButton(
                            f"🎵 Vote Track 1 ({data['track1Votes']} votes)",
                            callback_data=f"vote|track1|{battle_id}|{payment_amount}",
                        ),
                        InlineKeyboardButton(
                            f"🎵 Vote Track 2 ({data['track2Votes']} votes)",
                            callback_data=f"vote|track2|{battle_id}|{payment_amount}",
                        ),
                    ]
                ]
                voting_keyboard = InlineKeyboardMarkup(buttons)

                # Update the voting UI with current vote counts
                await query.edit_message_text(
                    "Give your votes here",
                    reply_markup=voting_keyboard,
                )
            else:
                await query.message.reply_text(
                    f"❌ Failed to fetch updated votes. Error: {data.get('error', 'Unknown error.')}"
                )
    except Exception as e:
            logger.error(f"Exception occurred while updating UI: {e}")
            # await query.message.reply_text("❌ Failed to update the voting UI.")


async def fetch_battle_data(payload):
    """Function to fetch battle data from the backend."""
    try:
        logger.info(f"Payload type: {type(payload)}")
        logger.info(f"Raw payload: {payload}")
        
        # Make sure payload is a proper dictionary
        if isinstance(payload, str):
            payload = json.loads(payload)  # Convert string to dict if needed
        
        response = requests.post(
            f"{BASE_URL}/startbattle", 
            json=payload,
            headers={'Content-Type': 'application/json'}
        )
        
        logger.info(f"Response status: {response.status_code}")
        
        if response.status_code == 200:
            return response.json()
        else:
            logger.error(f"Error response: {response.text}")
            return {"error": f"HTTP {response.status_code}: {response.text}"}
    except json.JSONDecodeError as e:
        logger.error(f"JSON Decode Error: {e}")
        raise
    except Exception as e:
        logger.error("Error during request:", exc_info=True)
        raise Exception("Failed to connect to the backend") from e

async def start_battle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Starts a new music battle with genre selection."""
    if len(context.args) != 0:
        await update.message.reply_text(
            "Usage: /startbattle"
        )
        return

    # Step 1: Create Inline Keyboard for Genre Selection
    buttons = []
    for genre in GENRES.keys():
        buttons.append([InlineKeyboardButton(genre, callback_data=f"genre|{genre}")])

    keyboard = InlineKeyboardMarkup(buttons)

    await update.message.reply_text(
        "🎶 Select a music genre for the battle:",
        reply_markup=keyboard,
    )

# Command: /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Lists all available commands."""
    help_text = (
        "🎉 *Available Commands*:\n\n"
        "🚀 *General Commands:*\n"
        "/start - Start the bot\n"
        "/help - List commands\n"
        "/startbattle - Start a music battle\n"
        "/battlevotes <battleId> - Get current votes in the battle\n"
        "/battledetails <battleId> - Get details of a battle\n"
        "/battlevoters <battleId> - Get total voters for a battle\n"
        "/leaderboard <battleId> - Get the top voters\n"
        "/getVotersList <battleId> - Get voters of the Battle\n"
        "/getContractBalance - Get the balance held by the contract\n"
        "/closeBattle <battleId> - Close the battle with specific battleId\n"
        "/transferToOwner <amount> <userAddress> <senderAddress> - Send the money from contract to the senderAddress: Only Owner\n"
        
        # Wallet-related commands
        "💼 *Wallet Management:*\n"
        "/setwallet <wallet_address> - Set your wallet address for the first time. If you've already set one, it will return your current wallet.\n"
        "/changewallet <new_wallet_address> - Change your existing wallet address.\n"
        "/getwallet - Get your current wallet address. If you haven't set one, it will inform you.\n"
        "/listwallets - List all wallet addresses set by users in this group.\n"
    )
    await update.message.reply_text(help_text)
