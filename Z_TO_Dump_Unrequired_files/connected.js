const TelegramBot = require('node-telegram-bot-api');
const axios = require('axios');
const { v4: uuidv4 } = require('uuid');

// Configuration and API Keys
const TOKEN = process.env.TELEGRAM_BOT_TOKEN || "YOUR_TELEGRAM_BOT_TOKEN";
const YOUTUBE_API_KEY = process.env.YOUTUBE_API_KEY || "YOUR_YOUTUBE_API_KEY";
const BASE_URL = process.env.BACKEND_URL || "http://localhost:5000";

// Debugging Configuration
const DEBUG_MODE = true;

// Logging Function
function debugLog(message, type = 'info') {
    if (DEBUG_MODE) {
        const timestamp = new Date().toISOString();
        console[type](`[${timestamp}] ${message}`);
    }
}

class MusicBattleBot {
    constructor() {
        // From sugha.js: Predefined genre list
        this.genres = ['pop', 'rock', 'hip hop', 'classical', 'electronic', 'jazz'];
        
        // From bot.py: Battle management
        this.activeBattles = {};
        this.userSessions = {};

        // Initialize bot
        this.bot = new TelegramBot(TOKEN, { polling: true });
        this.initializeHandlers();
    }

    initializeHandlers() {
        // From sugha.js: Start command with rich welcome message
        this.bot.onText(/\/start/, this.handleStart.bind(this));

        // From bot.py: Comprehensive command handlers
        this.bot.onText(/\/help/, this.handleHelp.bind(this));
        this.bot.onText(/\/startbattle/, this.handleStartBattle.bind(this));
        this.bot.onText(/\/battledetails/, this.handleBattleDetails.bind(this));
        this.bot.onText(/\/leaderboard/, this.handleLeaderboard.bind(this));

        // From sugha.js: Inline voting mechanism
        this.bot.on('callback_query', this.handleVoting.bind(this));
    }

    async handleStart(msg) {
        const chatId = msg.chat.id;
        const userName = msg.from.first_name || 'User';

        const welcomeMessage = `
👋 Welcome to the Music Battle Bot, ${userName}! 🎶

Get ready for epic music showdowns where you can:
• Start random music battles
• Create custom track battles
• Earn rewards and climb the leaderboard

Type /help to see all available commands!
        `;

        this.bot.sendMessage(chatId, welcomeMessage);
        debugLog(`User ${userName} started the bot`);
    }

    handleHelp(msg) {
        const chatId = msg.chat.id;
        const helpMessage = `
🎵 **Music Battle Bot Commands** 🎵

• /start - Begin your music battle journey
• /startbattle - Begin a random or custom music battle
• /battledetails [battleId] - Get details of a specific battle
• /leaderboard - View top tracks and performers
        `;

        this.bot.sendMessage(chatId, helpMessage);
    }

    async handleStartBattle(msg) {
        const chatId = msg.chat.id;
        const genre = this.getRandomGenre();

        debugLog(`Starting battle in genre: ${genre}`);

        try {
            // From sugha.js: YouTube track fetching
            const tracks = await this.fetchTracksFromYouTube(genre);

            if (tracks.length < 2) {
                return this.bot.sendMessage(chatId, "Couldn't find enough tracks. Try again later.");
            }

            // Generate unique battle ID
            const battleId = uuidv4();

            // Create battle object
            this.activeBattles[battleId] = {
                tracks: tracks,
                votes: { track1: 0, track2: 0 },
                genre: genre,
                startTime: Date.now(),
                votedUsers: new Set()
            };

            // From sugha.js: Rich battle message with inline voting
            const battleMessage = this.createBattleMessage(battleId, tracks);
            
            this.bot.sendMessage(chatId, battleMessage, {
                parse_mode: "Markdown",
                reply_markup: {
                    inline_keyboard: [
                        [{ text: `🎶 Vote Track 1 (0 votes)`, callback_data: `vote_${battleId}_1` }],
                        [{ text: `🎶 Vote Track 2 (0 votes)`, callback_data: `vote_${battleId}_2` }]
                    ]
                }
            });

            // Start countdown
            this.startBattleCountdown(chatId, battleId);

        } catch (error) {
            debugLog(`Battle start error: ${error.message}`, 'error');
            this.bot.sendMessage(chatId, "An error occurred while starting the battle.");
        }
    }

    // Additional methods: fetchTracksFromYouTube, createBattleMessage, startBattleCountdown, etc.
    // (Implementations would follow similar patterns to sugha.js)
}

// Initialize and run the bot
const musicBattleBot = new MusicBattleBot();