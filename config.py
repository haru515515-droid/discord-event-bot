import os
from dotenv import load_dotenv

load_dotenv()

# Bot configuration
BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')

# Data files
EVENTS_FILE = 'events.json'
QUIZ_FILE = 'quizzes.json'
LOTTERY_FILE = 'lotteries.json'

# Bot settings
COMMAND_PREFIX = '!'
