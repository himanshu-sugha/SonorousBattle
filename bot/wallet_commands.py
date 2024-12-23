import logging
from telegram import Update
from telegram.ext import CallbackContext
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

user_wallet_mapping={}

from wallet_mappins1 import user_wallet_mapping

# Save data to a file for persistence
def save_user_wallet_data():
    with open("user_wallet_mapping.json", "w") as file:
        json.dump(user_wallet_mapping, file)

# Load data from a file during bot initialization

async def change_wallet(update: Update, context: CallbackContext):
    """Allow the user to change their existing wallet address."""
    user_id = update.message.from_user.id
    user_id=str(user_id)

    # Check if the user has a wallet address set
    if user_id not in user_wallet_mapping:
        await update.message.reply_text("You haven't set your wallet address yet. Use /setwallet to set it.")
        return

    # Check if the user has provided a new wallet address
    if not context.args:
        await update.message.reply_text("Please provide a new wallet address, e.g., /changewallet 0xDEF456...")
        return

    # Join the arguments to form the new wallet address
    new_wallet = " ".join(context.args)

    # Update the wallet address in the mapping
    user_wallet_mapping[user_id]["wallet"] = new_wallet

    try:
        save_user_wallet_data()  # Save the updated data
    except Exception as e:
        logger.error(f"Problem in storing data: {e}")

    # Confirm the wallet address has been updated
    await update.message.reply_text(f"Your wallet address has been updated to {new_wallet}.")


async def get_wallet(update: Update, context: CallbackContext):
    print("user_wallet_mapping in get wallet function",user_wallet_mapping)
    """Retrieve the wallet address for the user."""
    user_id = update.message.from_user.id
    

    # print("user Id",user_id)
    user_id=str(user_id)
    print("user Id",user_id)

    # Check if the user's wallet is stored
    if user_id not in user_wallet_mapping:
        await update.message.reply_text("You haven't set your wallet address yet.")
        print("Not Availble useraddress")
        return ""

    wallet = user_wallet_mapping[user_id]["wallet"]
    user_info = user_wallet_mapping[user_id]["user_info"]

    await update.message.reply_text(f"Your wallet address is {wallet} (Linked to {user_info}).")
    return wallet

async def list_wallets(update: Update, context: CallbackContext):
    print("user_wallet_mapping",user_wallet_mapping)
    """List all wallet addresses stored globally."""
    if not user_wallet_mapping:
        await update.message.reply_text("No wallet addresses have been set yet.")
        return

    response = "Global Wallet Mappings:\n"
    for user_id, info in user_wallet_mapping.items():
        user_info = info["user_info"]
        wallet = info["wallet"]
        response += f"User ID {user_id} ({user_info}): {wallet}\n"

    await update.message.reply_text(response)

async def set_wallet(update: Update, context: CallbackContext):
    """Set the wallet address for the user, if it's their first time."""
    user_id = update.message.from_user.id
    user_id=str(user_id)

    # Check if the user already has a wallet address set
    if user_id in user_wallet_mapping:
        # If the wallet is already set, notify the user with their current wallet
        wallet = user_wallet_mapping[user_id]["wallet"]
        await update.message.reply_text(
            f"Your wallet address is already set to {wallet}. If you want to change it, use /changewallet."
        )
        return

    # Check if the user has provided a wallet address
    if not context.args:
        await update.message.reply_text("Please provide a wallet address, e.g., /setwallet 0xABC123...")
        return

    # Join the arguments to form the wallet address
    wallet = " ".join(context.args)
    
    # Store the wallet address for the user
    user_wallet_mapping[user_id] = {
        "wallet": wallet,
        "user_info": update.message.from_user.username or "Unknown",
    }

    try:
        save_user_wallet_data()  # Save the updated data
    except Exception as e:
        logger.error(f"Problem in storing data: {e}")

    # Confirm the wallet address has been set
    await update.message.reply_text(f"Wallet address for @{update.message.from_user.username} set to {wallet}.")
