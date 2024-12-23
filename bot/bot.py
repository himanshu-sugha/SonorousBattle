from telegram import Update
from telegram.ext import ContextTypes
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    CallbackQueryHandler
)

# Telegram bot token
BOT_TOKEN = "8125453843:AAFpfmYh97iFq-_wmaah_a3_98KfmJaEMPY"

# bot commands  
from BotCommands import vote_track , get_battle_details , get_votes , leaderboard , get_total_voters , get_voters_list , transfer_to_owner , close_battle ,get_balance , handle_voting , handle_genre_selection ,start_battle,help_command

# wallet functions 
from wallet_commands import set_wallet,change_wallet,get_wallet,list_wallets

# websocket Connection
from threading import Thread
from websocket import  run_websocket_listener , init_telegram_handler, add_active_chat

# Start command
async def start(update: Update,context: ContextTypes.DEFAULT_TYPE):
    """Sends a welcome message."""
    add_active_chat(update.effective_chat.id)
    await update.message.reply_text("Welcome to the Music Battle Bot! 🎶\nType /help to see available commands.")
    await update.message.reply_text("Use /setwallet <wallet> to link your wallet address.")

# main function 
def main():
    
    application = Application.builder().token(BOT_TOKEN).build()    

    # Register bot commands
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("startbattle", start_battle))
    application.add_handler(CommandHandler("votetrack", vote_track))
    application.add_handler(CommandHandler("battlevotes", get_votes))
    application.add_handler(CommandHandler("battledetails", get_battle_details))
    application.add_handler(CommandHandler("battlevoters", get_total_voters))
    application.add_handler(CommandHandler("leaderboard", leaderboard))
    application.add_handler(CommandHandler("transferToOwner", transfer_to_owner))
    application.add_handler(CommandHandler("getVotersList", get_voters_list))
    application.add_handler(CommandHandler("getContractBalance", get_balance))
    application.add_handler(CommandHandler("closeBattle", close_battle))

    application.add_handler(CallbackQueryHandler(handle_voting, pattern=r"^vote\|"))
    application.add_handler(CallbackQueryHandler(handle_genre_selection, pattern=r"^genre\|"))

    application.add_handler(CommandHandler("setwallet", set_wallet))
    application.add_handler(CommandHandler("changewallet", change_wallet))
    application.add_handler(CommandHandler("getwallet", get_wallet))
    application.add_handler(CommandHandler("listwallets", list_wallets))

    init_telegram_handler(application)

    # Start WebSocket listener in a background thread
    ws_thread = Thread(target=run_websocket_listener, daemon=True)
    ws_thread.start()

    # Start the bot
    print("Bot started...")
    application.run_polling()

if __name__ == "__main__":
    main()
