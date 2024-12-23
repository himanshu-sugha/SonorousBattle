import asyncio,json,websockets,logging,socket
BOT_TOKEN = "7606681330:AAHNUpi_k1tfUIKyBeFGn1HusWDahrnUxMw"
from telegram import Bot
from telegram.ext import Application

bot = Bot(token=BOT_TOKEN)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Simple in-memory storage
active_chats = set()
server = socket.socket()
server.bind(( 'localhost' ,9999))

def format_battle_result(result):
    """
    Formats the battle result received from the backend into a readable structure.

    :param result: dict, the raw result from the backend containing keys 'part1', 'winnerVotersList', and 'resultMessage'.
    :return: str, formatted battle result as a readable string.
    """
    try:
        # Extract the components of the result
        part1 = result.get('part1', 'No summary available')
        winner_voters_list = result.get('winnerVotersList', [])
        result_message = result.get('resultMessage', 'No details available')

        # Format each part
        formatted_result = []
        
        # Add the summary
        formatted_result.append(f"\nBattle Summary:\n{'-' * 20}\n{part1}\n")

        # Add the winner voters list
        formatted_result.append("\nWinner Voters List:\n" + "-" * 20)
        if winner_voters_list:
            for i, voter in enumerate(winner_voters_list, start=1):
                formatted_result.append(f"{i}. {voter}")
        else:
            formatted_result.append("No voters available.")

        # Add the detailed result message
        # formatted_result.append(f"\nBattle Details:\n{'-' * 20}\n{result_message}\n")

        # Combine all parts into a single formatted string
        return "\n".join(formatted_result)

    except Exception as e:
        return f"An error occurred while formatting the battle result: {e}"

def add_active_chat(chat_id: int):
    active_chats.add(chat_id)

def remove_active_chat(chat_id: int):
    active_chats.discard(chat_id)

def get_active_chats():
    return active_chats


telegram_app = None


async def send_telegram_message(battle_result: dict):
    """Send battle result to Telegram"""
    if telegram_app is None:
        logging.error("Telegram application not initialized")
        return

    try:
        # Format the message
        message = format_battle_result(battle_result)
        
        # Get active chats from your storage (you'll need to implement this)
        active_chats = get_active_chats()  # You need to implement this
        
        # Send to all active chats
        for chat_id in active_chats:
            await telegram_app.bot.send_message(
                chat_id=chat_id,
                text=message,
                parse_mode='HTML'
            )
            
    except Exception as e:
        logging.error(f"Error sending Telegram message: {e}")

# def format_battle_message(battle_result: dict) -> str:
    """Format battle result for Telegram message"""
    try:
        winner = battle_result.get('winner', 'Unknown')
        votes_track1 = battle_result.get('votesTrack1', 0)
        votes_track2 = battle_result.get('votesTrack2', 0)
        reward = battle_result.get('reward', '0')
        
        message = (
            "🎵 Battle Results\n\n"
            f"🏆 Winner: {winner}\n"
            f"📊 Votes:\n"
            f"Track 1: {votes_track1}\n"
            f"Track 2: {votes_track2}\n"
            f"💰 Reward: {reward} ETH"
        )
        return message
    except Exception as e:
        logging.error(f"Error formatting battle message: {e}")
        return "Error formatting battle result"

async def listen_for_battle_result():
    """WebSocket listener function"""
    uri = "ws://localhost:8080"
    
    while True:
        try:
            async with websockets.connect(uri) as websocket:
                logging.info("Connected to WebSocket server")
                
                while True:
                    try:
                        message = await websocket.recv()
                        data = json.loads(message)
                        
                        if data.get("type") == "battleResult":
                            logging.info("Battle Result Received")
                            # Send to Telegram
                            await send_telegram_message(data.get("payload"))
                            
                    except websockets.exceptions.ConnectionClosed:
                        logging.error("WebSocket connection closed")
                        break
                        
        except Exception as e:
            logging.error(f"WebSocket error: {e}")
            await asyncio.sleep(5)  # Wait before reconnecting

def run_websocket_listener():
    while True:
        try:
            asyncio.run(listen_for_battle_result())
        except Exception as e:
            logger.error(f"WebSocket listener crashed: {e}")
            asyncio.sleep(5)  # Wait before restarting

def init_telegram_handler(application: Application):
    """Initialize the telegram application global variable"""
    global telegram_app
    telegram_app = application
