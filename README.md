# SonorousBattle

SonorousBattle is a Telegram bot integrated with blockchain functionality. This bot allows users to engage in music battles, vote on battles, and manage blockchain-based transactions related to the battles. It offers an interactive and secure way to handle music competitions and related financial transactions.

---

## Table of Contents
- [Commands](#commands)
- [Features](#features)
- [Diagram](#diagram)
- [Installation](#installation)
- [Contact Info](#contact-info)

---

## Commands

### Telegram Bot Commands:

- `/start` - Start the bot.
- `/help` - List all available commands.
- `/startbattle` - Start a new music battle.
- `/battlevotes <battleId>` - Retrieve the current votes for a specific battle.
- `/battledetails <battleId>` - Get detailed information about a specific battle.
- `/battlevoters <battleId>` - Get the total number of voters for a battle.
- `/leaderboard <battleId>` - Display the top voters in a battle.
- `/getVotersList <battleId>` - Fetch the list of all voters in a battle.
- `/getContractBalance` - Retrieve the balance held by the blockchain contract.
- `/closeBattle <battleId>` - Close a specific battle identified by battleId.
- `/transferToOwner <amount> <userAddress> <senderAddress>` - Transfer funds from the contract to the sender’s address (owner only).

---

## Features

- Interactive Telegram bot interface for music battles.
- Integration with Spotify API to fetch and display tracks for battles.
- Blockchain functionality to manage transactions and battle data securely.
- Voting system for users to choose their favorite tracks.
- Leaderboard to showcase top voters.
- Smart contract-based fund management.

---

## Diagram

(Insert a visual diagram here illustrating the interaction between Telegram bot, Spotify API, and blockchain backend.)

---

## Installation

### Prerequisites:
- Node.js
- Python
- Hardhat

# Complete Setup Script for Hardhat and Bot 

```bash
#!/bin/bash

# ============================================
# Setup Script for Hardhat and Telegram Bot
# ============================================

# Step 1: Start the Hardhat Node
echo "🚀 Starting Hardhat Node..."
npx hardhat node &

# Wait for Hardhat Node to initialize
echo "⏳ Waiting for Hardhat Node to initialize..."
sleep 5

# Step 2: Deploy Smart Contracts
echo "📜 Deploying Smart Contracts..."
npx hardhat run scripts/deploy.js --network localhost

# Step 3: Install Bot Dependencies
echo "📦 Installing Bot Dependencies..."
pip install requests python-telegram-bot python-dotenv

# Step 4: Create and Configure the .env File
echo "🛠️ Creating .env file for the bot configuration..."
cat <<EOL > .env
# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
API_BASE_URL=http://localhost:3000/api
EOL
echo "✅ .env file created! Remember to replace 'your_telegram_bot_token_here' with your actual Telegram bot token."

# Step 5: Run the Bot
echo "🤖 Starting the Telegram Bot..."
python bot.py

# ============================================
# Script Execution Completed
# ============================================
