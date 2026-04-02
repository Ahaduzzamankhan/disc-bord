import discord
from discord.ext import commands
import google.generativeai as genai
from flask import Flask
from dotenv import load_dotenv
import os
import threading

# Create .env if not exists
if not os.path.exists('.env'):
    with open('.env', 'w') as f:
        f.write('DISCORD_TOKEN=your_discord_bot_token_here\n')
        f.write('GEMINI_API_KEY=your_gemini_api_key_here\n')
    print("Created .env file. Please fill in your tokens and run again.")
    exit()

# Load environment variables
load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

# Bot setup
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

# Flask app for keep-alive
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is alive!"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

# Event handlers
@bot.event
async def on_ready():
    print(f'Bot is ready as {bot.user}')

# Command definitions

# Discord Server Management Commands
@bot.command()
async def suggest_server_name(ctx):
    prompt = "Suggest a creative and unique name for a Discord server focused on gaming and community."
    response = model.generate_content(prompt)
    await ctx.send(response.text)

@bot.command()
async def suggest_channel_names(ctx):
    prompt = "Suggest 5 creative channel names for a gaming Discord server, including categories like general, gaming, and voice channels."
    response = model.generate_content(prompt)
    await ctx.send(response.text)

@bot.command()
async def suggest_role_names(ctx):
    prompt = "Suggest role names and hierarchies for a Discord server, including admin, moderator, and member roles."
    response = model.generate_content(prompt)
    await ctx.send(response.text)

@bot.command()
async def suggest_emoji_ideas(ctx):
    prompt = "Suggest custom emoji ideas for a Discord server themed around gaming and fun."
    response = model.generate_content(prompt)
    await ctx.send(response.text)

@bot.command()
async def suggest_bot_permissions(ctx):
    prompt = "Suggest appropriate permissions for a bot in a Discord server to function effectively without being overpowered."
    response = model.generate_content(prompt)
    await ctx.send(response.text)

@bot.command()
async def suggest_moderation_rules(ctx):
    prompt = "Suggest a set of moderation rules for a Discord server to maintain a positive community."
    response = model.generate_content(prompt)
    await ctx.send(response.text)

@bot.command()
async def suggest_welcome_message(ctx):
    prompt = "Suggest a welcoming message for new members joining a Discord server."
    response = model.generate_content(prompt)
    await ctx.send(response.text)

@bot.command()
async def suggest_goodbye_message(ctx):
    prompt = "Suggest a goodbye message for members leaving a Discord server."
    response = model.generate_content(prompt)
    await ctx.send(response.text)

@bot.command()
async def suggest_event_ideas(ctx):
    prompt = "Suggest event ideas for a Discord server, such as game nights, tournaments, or community activities."
    response = model.generate_content(prompt)
    await ctx.send(response.text)

@bot.command()
async def suggest_server_themes(ctx):
    prompt = "Suggest theme ideas for customizing a Discord server, including color schemes and layouts."
    response = model.generate_content(prompt)
    await ctx.send(response.text)

# Bot Tips Commands
@bot.command()
async def suggest_bot_commands(ctx):
    prompt = "Suggest useful commands that a Discord bot should have for server management."
    response = model.generate_content(prompt)
    await ctx.send(response.text)

@bot.command()
async def suggest_bot_features(ctx):
    prompt = "Suggest advanced features for a Discord bot, such as integrations or automation."
    response = model.generate_content(prompt)
    await ctx.send(response.text)

@bot.command()
async def suggest_integration_ideas(ctx):
    prompt = "Suggest ways to integrate a Discord bot with other services like Twitch or YouTube."
    response = model.generate_content(prompt)
    await ctx.send(response.text)

@bot.command()
async def suggest_custom_commands(ctx):
    prompt = "Suggest ideas for custom commands in a Discord bot tailored to a server's needs."
    response = model.generate_content(prompt)
    await ctx.send(response.text)

@bot.command()
async def suggest_bot_responses(ctx):
    prompt = "Suggest witty or helpful response ideas for a Discord bot to common user queries."
    response = model.generate_content(prompt)
    await ctx.send(response.text)

@bot.command()
async def suggest_error_handling(ctx):
    prompt = "Suggest error handling strategies for a Discord bot to improve reliability."
    response = model.generate_content(prompt)
    await ctx.send(response.text)

@bot.command()
async def suggest_logging_ideas(ctx):
    prompt = "Suggest logging features for a Discord bot to track server activities."
    response = model.generate_content(prompt)
    await ctx.send(response.text)

@bot.command()
async def suggest_backup_strategies(ctx):
    prompt = "Suggest backup strategies for Discord server data and bot configurations."
    response = model.generate_content(prompt)
    await ctx.send(response.text)

@bot.command()
async def suggest_update_ideas(ctx):
    prompt = "Suggest ideas for updating and maintaining a Discord bot over time."
    response = model.generate_content(prompt)
    await ctx.send(response.text)

@bot.command()
async def suggest_security_tips(ctx):
    prompt = "Suggest security tips for running a Discord bot safely."
    response = model.generate_content(prompt)
    await ctx.send(response.text)

# Game Recommendations Commands
@bot.command()
async def suggest_games_for_friends(ctx):
    prompt = "Suggest multiplayer games that are great for playing with friends."
    response = model.generate_content(prompt)
    await ctx.send(response.text)

@bot.command()
async def suggest_single_player_games(ctx):
    prompt = "Suggest engaging single-player games with compelling stories."
    response = model.generate_content(prompt)
    await ctx.send(response.text)

@bot.command()
async def suggest_multiplayer_games(ctx):
    prompt = "Suggest popular multiplayer games for online play."
    response = model.generate_content(prompt)
    await ctx.send(response.text)

@bot.command()
async def suggest_indie_games(ctx):
    prompt = "Suggest unique indie games that are underrated."
    response = model.generate_content(prompt)
    await ctx.send(response.text)

@bot.command()
async def suggest_classic_games(ctx):
    prompt = "Suggest classic games that everyone should play at least once."
    response = model.generate_content(prompt)
    await ctx.send(response.text)

@bot.command()
async def suggest_new_releases(ctx):
    prompt = "Suggest newly released games that are worth checking out."
    response = model.generate_content(prompt)
    await ctx.send(response.text)

@bot.command()
async def suggest_free_games(ctx):
    prompt = "Suggest high-quality free games available on various platforms."
    response = model.generate_content(prompt)
    await ctx.send(response.text)

@bot.command()
async def suggest_paid_games(ctx):
    prompt = "Suggest paid games that offer great value for money."
    response = model.generate_content(prompt)
    await ctx.send(response.text)

@bot.command()
async def suggest_mobile_games(ctx):
    prompt = "Suggest addictive mobile games for on-the-go entertainment."
    response = model.generate_content(prompt)
    await ctx.send(response.text)

@bot.command()
async def suggest_pc_games(ctx):
    prompt = "Suggest top PC games for different genres."
    response = model.generate_content(prompt)
    await ctx.send(response.text)

@bot.command()
async def suggest_console_games(ctx):
    prompt = "Suggest must-play games for console platforms like PlayStation and Xbox."
    response = model.generate_content(prompt)
    await ctx.send(response.text)

@bot.command()
async def suggest_board_games(ctx):
    prompt = "Suggest fun board games for group play."
    response = model.generate_content(prompt)
    await ctx.send(response.text)

@bot.command()
async def suggest_card_games(ctx):
    prompt = "Suggest engaging card games for various player counts."
    response = model.generate_content(prompt)
    await ctx.send(response.text)

@bot.command()
async def suggest_puzzle_games(ctx):
    prompt = "Suggest puzzle games that challenge the mind."
    response = model.generate_content(prompt)
    await ctx.send(response.text)

@bot.command()
async def suggest_action_games(ctx):
    prompt = "Suggest action-packed games with intense gameplay."
    response = model.generate_content(prompt)
    await ctx.send(response.text)

# Game Strategies Commands
@bot.command()
async def strategy_for_chess(ctx):
    prompt = "Provide strategic tips for playing chess effectively."
    response = model.generate_content(prompt)
    await ctx.send(response.text)

@bot.command()
async def strategy_for_poker(ctx):
    prompt = "Provide strategy advice for playing poker."
    response = model.generate_content(prompt)
    await ctx.send(response.text)

@bot.command()
async def strategy_for_dota(ctx):
    prompt = "Provide strategies for playing Dota 2."
    response = model.generate_content(prompt)
    await ctx.send(response.text)

@bot.command()
async def strategy_for_lol(ctx):
    prompt = "Provide strategies for playing League of Legends."
    response = model.generate_content(prompt)
    await ctx.send(response.text)

@bot.command()
async def strategy_for_csgo(ctx):
    prompt = "Provide strategies for playing Counter-Strike: Global Offensive."
    response = model.generate_content(prompt)
    await ctx.send(response.text)

@bot.command()
async def strategy_for_overwatch(ctx):
    prompt = "Provide strategies for playing Overwatch."
    response = model.generate_content(prompt)
    await ctx.send(response.text)

@bot.command()
async def strategy_for_fortnite(ctx):
    prompt = "Provide strategies for playing Fortnite."
    response = model.generate_content(prompt)
    await ctx.send(response.text)

@bot.command()
async def strategy_for_apex(ctx):
    prompt = "Provide strategies for playing Apex Legends."
    response = model.generate_content(prompt)
    await ctx.send(response.text)

@bot.command()
async def strategy_for_pubg(ctx):
    prompt = "Provide strategies for playing PUBG."
    response = model.generate_content(prompt)
    await ctx.send(response.text)

@bot.command()
async def strategy_for_rocket_league(ctx):
    prompt = "Provide strategies for playing Rocket League."
    response = model.generate_content(prompt)
    await ctx.send(response.text)

@bot.command()
async def strategy_for_minecraft(ctx):
    prompt = "Provide strategies for playing Minecraft."
    response = model.generate_content(prompt)
    await ctx.send(response.text)

@bot.command()
async def strategy_for_terraria(ctx):
    prompt = "Provide strategies for playing Terraria."
    response = model.generate_content(prompt)
    await ctx.send(response.text)

@bot.command()
async def strategy_for_stardew_valley(ctx):
    prompt = "Provide strategies for playing Stardew Valley."
    response = model.generate_content(prompt)
    await ctx.send(response.text)

@bot.command()
async def strategy_for_civilization(ctx):
    prompt = "Provide strategies for playing Civilization series."
    response = model.generate_content(prompt)
    await ctx.send(response.text)

@bot.command()
async def strategy_for_total_war(ctx):
    prompt = "Provide strategies for playing Total War series."
    response = model.generate_content(prompt)
    await ctx.send(response.text)

# Other Suggestions Commands
@bot.command()
async def suggest_music_playlists(ctx):
    prompt = "Suggest music playlists for different moods and activities."
    response = model.generate_content(prompt)
    await ctx.send(response.text)

@bot.command()
async def suggest_movies(ctx):
    prompt = "Suggest movies based on different genres and themes."
    response = model.generate_content(prompt)
    await ctx.send(response.text)

@bot.command()
async def suggest_books(ctx):
    prompt = "Suggest books for various interests and reading levels."
    response = model.generate_content(prompt)
    await ctx.send(response.text)

@bot.command()
async def suggest_coding_projects(ctx):
    prompt = "Suggest beginner-friendly coding projects to build skills."
    response = model.generate_content(prompt)
    await ctx.send(response.text)

@bot.command()
async def suggest_learning_resources(ctx):
    prompt = "Suggest online resources for learning new skills."
    response = model.generate_content(prompt)
    await ctx.send(response.text)

# Run the bot and Flask server
if __name__ == '__main__':
    threading.Thread(target=run_flask).start()
    bot.run(DISCORD_TOKEN)