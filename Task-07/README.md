# 🏴‍☠️ Task 07: Dank Memer Discord Bot (The Berry Broker)

Welcome to the Grand Line! This project is a One Piece-themed custom Discord bot that creates a server-wide pirate economy. Users start as rookies with a small stash of Berries and can earn, trade, gamble, and raid their way to the top of the Worst Generation leaderboard.

## ✨ Features & Commands

### 💰 Economy & Progression
* `!bounty` - Check your current Berry balance.
* `!setsail` - Claim a daily reward of 500 Berries (24-hour cooldown).
* `!trade @user <amount>` - Transfer Berries to another crewmate.
* `!worstgeneration` - Displays the Top 5 richest pirates on the server.
* `!raid @user` - Attempt to steal Berries from another user. 50% chance of success, but if you fail, you lose Berries retreating! (1-hour cooldown).

### ⚔️ Games & Gambling
* `!duel <rock/paper/scissors>` - Challenge the bot to a sword fight. Win and earn 50 Berries, lose and the bot takes your wager.

### 🎭 Fun & API Integration
* `!roast @user` - Hurls a random One Piece-themed insult at a rival pirate.
* `!logpose` - Uses `aiohttp` to asynchronously fetch a random character's intel (name, bounty, devil fruit) from a public One Piece API.

## 🛠️ Tech Stack & Concepts Applied
* **Language:** Python 3
* **Library:** `discord.py` (with Message Content and Server Members intents enabled)
* **Database:** `sqlite3` (for tracking users, balances, and cooldown timestamps)
* **API Requests:** `aiohttp` (for asynchronous web requests)
* **Security:** `python-dotenv` (keeping the Bot Token secure and hidden out of source control)

## 📁 Project Structure (Bonus Objective Achieved)
The bot's architecture was modularized into **Cogs** for better code maintainability, fulfilling the bonus objective for this task:

```text
Task-07/
├── .env                  # Secret Discord Token (Ignored by Git)
├── .gitignore            # Ignores venv, caches, and DB files
├── bot.py                # Main entry point and bot initialization
├── database.py           # SQLite connection and query executions
├── README.md             # Project documentation
└── cogs/                 # Modular command categories
    ├── economy.py        # Handles balances, trading, and raiding
    ├── fun.py            # Handles API requests and roasts
    └── games.py          # Handles gambling and duels
