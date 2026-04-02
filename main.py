import discord
from discord.ext import commands
from discord import app_commands
import google.genai as genai
from flask import Flask
from dotenv import load_dotenv
import os
import threading
import time
import logging
from collections import defaultdict, deque

# ── Logging ───────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
log = logging.getLogger(__name__)

# ── .env bootstrap ────────────────────────────────────────────────────────────
if not os.path.exists('.env'):
    with open('.env', 'w') as f:
        f.write('DISCORD_TOKEN=your_discord_bot_token_here\n')
        f.write('GEMINI_API_KEY=your_gemini_api_key_here\n')
    log.info("Created .env template. Fill in your tokens and restart.")

load_dotenv()
DISCORD_TOKEN  = os.getenv('DISCORD_TOKEN')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

run_bot = True
if not DISCORD_TOKEN or not GEMINI_API_KEY:
    log.error("Missing DISCORD_TOKEN and/or GEMINI_API_KEY. Set them in .env or Render dashboard.")
    run_bot = False

# ── Gemini ────────────────────────────────────────────────────────────────────
if run_bot:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-2.5-flash')

# ── Bot setup ─────────────────────────────────────────────────────────────────
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=commands.when_mentioned_or('!'), intents=intents)

# Per-channel rolling context (last 20 messages)
chat_history: dict[int, deque] = defaultdict(lambda: deque(maxlen=20))

# Per-user conversation history for /ask (last 20 lines = 10 turns)
user_conversations: dict[int, list] = defaultdict(list)

# ── Helpers ───────────────────────────────────────────────────────────────────
def _safe_desc(text: str, limit: int = 100) -> str:
    return text if len(text) <= limit else text[: limit - 1] + "…"


async def _gemini(prompt: str) -> str:
    try:
        resp = model.generate_content(prompt)
        return resp.text[:1900]
    except Exception as exc:
        log.exception("Gemini error")
        return f"⚠️ Gemini error: {exc}"


# ── Slash command table ───────────────────────────────────────────────────────
SLASH_COMMANDS: dict[str, tuple[str, str]] = {
    # Server management
    "suggest-server-name":       ("Suggest a creative Discord server name",
                                   "Suggest a creative and unique name for a Discord server focused on gaming and community."),
    "suggest-channel-names":     ("Suggest 5 creative channel names",
                                   "Suggest 5 creative channel names for a gaming Discord server."),
    "suggest-role-names":        ("Suggest role names and hierarchies",
                                   "Suggest role names and hierarchies for a Discord server including admin, moderator and member roles."),
    "suggest-emoji-ideas":       ("Suggest custom emoji ideas",
                                   "Suggest custom emoji ideas for a Discord server themed around gaming and fun."),
    "suggest-bot-permissions":   ("Suggest appropriate bot permissions",
                                   "Suggest appropriate permissions for a bot in a Discord server."),
    "suggest-moderation-rules":  ("Suggest moderation rules for a server",
                                   "Suggest a set of moderation rules for a Discord server to maintain a positive community."),
    "suggest-welcome-message":   ("Suggest a welcome message for new members",
                                   "Suggest a welcoming message for new members joining a Discord server."),
    "suggest-goodbye-message":   ("Suggest a goodbye message for members",
                                   "Suggest a goodbye message for members leaving a Discord server."),
    "suggest-event-ideas":       ("Suggest event ideas like game nights",
                                   "Suggest event ideas for a Discord server such as game nights, tournaments, or community activities."),
    "suggest-server-themes":     ("Suggest theme ideas for a Discord server",
                                   "Suggest theme ideas for customizing a Discord server, including color schemes and layouts."),

    # Bot tips
    "suggest-bot-commands":      ("Suggest useful bot commands",
                                   "Suggest useful commands that a Discord bot should have for server management."),
    "suggest-bot-features":      ("Suggest advanced bot features",
                                   "Suggest advanced features for a Discord bot such as integrations or automation."),
    "suggest-integration-ideas": ("Suggest ways to integrate a bot",
                                   "Suggest ways to integrate a Discord bot with other services like Twitch or YouTube."),
    "suggest-custom-commands":   ("Suggest ideas for custom bot commands",
                                   "Suggest ideas for custom commands in a Discord bot tailored to a server's needs."),
    "suggest-bot-responses":     ("Suggest witty bot response ideas",
                                   "Suggest witty or helpful response ideas for a Discord bot to common user queries."),
    "suggest-error-handling":    ("Suggest error handling strategies",
                                   "Suggest error handling strategies for a Discord bot to improve reliability."),
    "suggest-logging-ideas":     ("Suggest logging features for a bot",
                                   "Suggest logging features for a Discord bot to track server activities."),
    "suggest-backup-strategies": ("Suggest backup strategies",
                                   "Suggest backup strategies for Discord server data and bot configurations."),
    "suggest-update-ideas":      ("Suggest ideas for updating a bot",
                                   "Suggest ideas for updating and maintaining a Discord bot over time."),
    "suggest-security-tips":     ("Suggest security tips for running a bot",
                                   "Suggest security tips for running a Discord bot safely."),

    # Game recommendations
    "suggest-games-friends":     ("Suggest multiplayer games for friends",
                                   "Suggest multiplayer games that are great for playing with friends."),
    "suggest-single-player":     ("Suggest single-player games",
                                   "Suggest engaging single-player games with compelling stories."),
    "suggest-multiplayer":       ("Suggest popular multiplayer games",
                                   "Suggest popular multiplayer games for online play."),
    "suggest-indie-games":       ("Suggest underrated indie games",
                                   "Suggest unique indie games that are underrated."),
    "suggest-classic-games":     ("Suggest classic games everyone should play",
                                   "Suggest classic games that everyone should play at least once."),
    "suggest-new-releases":      ("Suggest newly released games",
                                   "Suggest newly released games that are worth checking out."),
    "suggest-free-games":        ("Suggest high-quality free games",
                                   "Suggest high-quality free games available on various platforms."),
    "suggest-paid-games":        ("Suggest paid games with great value",
                                   "Suggest paid games that offer great value for money."),
    "suggest-mobile-games":      ("Suggest addictive mobile games",
                                   "Suggest addictive mobile games for on-the-go entertainment."),
    "suggest-pc-games":          ("Suggest top PC games by genre",
                                   "Suggest top PC games for different genres."),
    "suggest-console-games":     ("Suggest must-play console games",
                                   "Suggest must-play games for console platforms like PlayStation and Xbox."),
    "suggest-board-games":       ("Suggest fun board games for group play",
                                   "Suggest fun board games for group play."),
    "suggest-card-games":        ("Suggest engaging card games",
                                   "Suggest engaging card games for various player counts."),
    "suggest-puzzle-games":      ("Suggest puzzle games that challenge",
                                   "Suggest puzzle games that challenge the mind."),
    "suggest-action-games":      ("Suggest action-packed games",
                                   "Suggest action-packed games with intense gameplay."),

    # Strategies
    "strategy-chess":            ("Strategy tips for Chess",
                                   "Provide detailed strategic tips for playing Chess effectively."),
    "strategy-poker":            ("Strategy tips for Poker",
                                   "Provide strategy advice for playing Poker."),
    "strategy-dota2":            ("Strategy tips for Dota 2",
                                   "Provide strategies for playing Dota 2."),
    "strategy-lol":              ("Strategy tips for League of Legends",
                                   "Provide strategies for playing League of Legends."),
    "strategy-csgo":             ("Strategy tips for CS:GO / CS2",
                                   "Provide strategies for playing Counter-Strike 2."),
    "strategy-overwatch":        ("Strategy tips for Overwatch 2",
                                   "Provide strategies for playing Overwatch 2."),
    "strategy-fortnite":         ("Strategy tips for Fortnite",
                                   "Provide strategies for playing Fortnite."),
    "strategy-apex":             ("Strategy tips for Apex Legends",
                                   "Provide strategies for playing Apex Legends."),
    "strategy-pubg":             ("Strategy tips for PUBG",
                                   "Provide strategies for playing PUBG."),
    "strategy-rocket-league":    ("Strategy tips for Rocket League",
                                   "Provide strategies for playing Rocket League."),
    "strategy-minecraft":        ("Strategy tips for Minecraft",
                                   "Provide comprehensive strategies for playing Minecraft."),
    "strategy-terraria":         ("Strategy tips for Terraria",
                                   "Provide strategies for playing Terraria."),
    "strategy-stardew":          ("Strategy tips for Stardew Valley",
                                   "Provide strategies for playing Stardew Valley."),
    "strategy-civilization":     ("Strategy tips for Civilization series",
                                   "Provide strategies for the Civilization series."),
    "strategy-total-war":        ("Strategy tips for Total War series",
                                   "Provide strategies for the Total War series."),

    # Misc
    "suggest-music-playlists":   ("Suggest music playlists for moods",
                                   "Suggest music playlists for different moods and activities."),
    "suggest-movies":            ("Suggest movies by genre",
                                   "Suggest movies based on different genres and themes."),
    "suggest-books":             ("Suggest books for various interests",
                                   "Suggest books for various interests and reading levels."),
    "suggest-coding-projects":   ("Suggest beginner coding projects",
                                   "Suggest beginner-friendly coding projects to build skills."),
    "suggest-learning-resources":("Suggest online learning resources",
                                   "Suggest online resources for learning new skills."),
}


def _register_slash_commands() -> None:
    for cmd_name, (desc, prompt) in SLASH_COMMANDS.items():
        async def _handler(interaction: discord.Interaction, p: str = prompt) -> None:
            await interaction.response.defer(thinking=True)
            text = await _gemini(p)
            await interaction.followup.send(text)

        _handler.__name__ = cmd_name.replace("-", "_")
        bot.tree.command(name=cmd_name, description=_safe_desc(desc))(_handler)

    log.info(f"Registered {len(SLASH_COMMANDS)} dynamic slash commands.")


_register_slash_commands()


# ── /ask ──────────────────────────────────────────────────────────────────────
@bot.tree.command(name="ask", description="Ask the AI anything (keeps a 10-turn memory per user)")
@app_commands.describe(question="Your question or message")
async def ask_command(interaction: discord.Interaction, question: str):
    await interaction.response.defer(thinking=True)
    uid = interaction.user.id
    history = user_conversations[uid]
    history.append(f"User: {question}")
    if len(history) > 20:
        user_conversations[uid] = history[-20:]
    context = "\n".join(user_conversations[uid])
    prompt = (
        "You are a helpful, friendly Discord AI assistant. "
        "Use the conversation history below to answer the user's latest message.\n\n"
        f"Conversation history:\n{context}\nAssistant:"
    )
    answer = await _gemini(prompt)
    user_conversations[uid].append(f"Assistant: {answer}")
    await interaction.followup.send(answer)


# ── /roast ────────────────────────────────────────────────────────────────────
@bot.tree.command(name="roast", description="Playfully roast a server member 🔥")
@app_commands.describe(member="The member to roast")
async def roast_command(interaction: discord.Interaction, member: discord.Member):
    await interaction.response.defer(thinking=True)
    prompt = (
        f"Write a fun, light-hearted, PG-13 roast for a Discord user named {member.display_name}. "
        "Keep it playful and not mean-spirited. 3–5 sentences max."
    )
    text = await _gemini(prompt)
    await interaction.followup.send(f"🔥 **Roasting {member.mention}:**\n{text}")


# ── /trivia ───────────────────────────────────────────────────────────────────
@bot.tree.command(name="trivia", description="Get a random trivia question with answer")
@app_commands.describe(topic="Optional topic (e.g. science, history, gaming)")
async def trivia_command(interaction: discord.Interaction, topic: str = "random"):
    await interaction.response.defer(thinking=True)
    prompt = (
        f"Give me one interesting {topic} trivia question. "
        "Format exactly like this:\n**Question:** ...\n**Answer:** ..."
    )
    text = await _gemini(prompt)
    await interaction.followup.send(text)


# ── /explain ──────────────────────────────────────────────────────────────────
@bot.tree.command(name="explain", description="Explain any concept in simple terms")
@app_commands.describe(concept="The concept or topic to explain")
async def explain_command(interaction: discord.Interaction, concept: str):
    await interaction.response.defer(thinking=True)
    prompt = (
        f"Explain '{concept}' in simple, clear terms that anyone can understand. "
        "Use an analogy if helpful. Keep it under 200 words."
    )
    text = await _gemini(prompt)
    await interaction.followup.send(f"📖 **{concept}**\n{text}")


# ── /poll-ideas ───────────────────────────────────────────────────────────────
@bot.tree.command(name="poll-ideas", description="Generate poll ideas for your server")
@app_commands.describe(theme="Topic or theme for the poll (e.g. gaming, movies)")
async def poll_ideas_command(interaction: discord.Interaction, theme: str = "general"):
    await interaction.response.defer(thinking=True)
    prompt = (
        f"Generate 5 fun and engaging Discord poll ideas around the theme: '{theme}'. "
        "Format each as '📊 **Poll:** ...' with 3–4 answer options listed below it."
    )
    text = await _gemini(prompt)
    await interaction.followup.send(text)


# ── /joke ─────────────────────────────────────────────────────────────────────
@bot.tree.command(name="joke", description="Get a random joke 😂")
@app_commands.describe(category="Optional: dark, dad, programming, general")
async def joke_command(interaction: discord.Interaction, category: str = "general"):
    await interaction.response.defer(thinking=True)
    prompt = f"Tell me a funny {category} joke. Keep it short and punchy."
    text = await _gemini(prompt)
    await interaction.followup.send(f"😂 {text}")


# ── /quote ────────────────────────────────────────────────────────────────────
@bot.tree.command(name="quote", description="Get an inspirational or funny quote")
@app_commands.describe(mood="Optional: motivational, funny, wisdom, gaming")
async def quote_command(interaction: discord.Interaction, mood: str = "motivational"):
    await interaction.response.defer(thinking=True)
    prompt = f"Give me one {mood} quote. Format: '\"quote\" — Author'"
    text = await _gemini(prompt)
    await interaction.followup.send(f"✨ {text}")


# ── /story ────────────────────────────────────────────────────────────────────
@bot.tree.command(name="story", description="Generate a short creative story")
@app_commands.describe(prompt="Story idea or theme (e.g. 'a dragon who loves coding')")
async def story_command(interaction: discord.Interaction, prompt: str):
    await interaction.response.defer(thinking=True)
    full_prompt = (
        f"Write a short, entertaining story (150–200 words) based on this idea: '{prompt}'. "
        "Make it creative and fun."
    )
    text = await _gemini(full_prompt)
    await interaction.followup.send(f"📖 **Story time!**\n{text}")


# ── /translate ────────────────────────────────────────────────────────────────
@bot.tree.command(name="translate", description="Translate text to another language")
@app_commands.describe(text="Text to translate", language="Target language (e.g. French, Japanese)")
async def translate_command(interaction: discord.Interaction, text: str, language: str):
    await interaction.response.defer(thinking=True)
    prompt = f"Translate the following text to {language}. Reply with only the translation:\n\n{text}"
    result = await _gemini(prompt)
    await interaction.followup.send(f"🌐 **{language}:** {result}")


# ── /server-info ──────────────────────────────────────────────────────────────
@bot.tree.command(name="server-info", description="Show information about this server")
async def server_info_slash(interaction: discord.Interaction):
    g = interaction.guild
    if not g:
        await interaction.response.send_message("This command only works in a server.", ephemeral=True)
        return
    embed = discord.Embed(title=f"📊 {g.name}", color=0x5865F2)
    embed.set_thumbnail(url=g.icon.url if g.icon else None)
    embed.add_field(name="Owner",      value=str(g.owner),                       inline=True)
    embed.add_field(name="Members",    value=str(g.member_count),                inline=True)
    embed.add_field(name="Channels",   value=str(len(g.channels)),               inline=True)
    embed.add_field(name="Roles",      value=str(len(g.roles)),                  inline=True)
    embed.add_field(name="Created",    value=g.created_at.strftime("%b %d, %Y"), inline=True)
    embed.add_field(name="Boost Tier", value=str(g.premium_tier),                inline=True)
    await interaction.response.send_message(embed=embed)


# ── /user-info ────────────────────────────────────────────────────────────────
@bot.tree.command(name="user-info", description="Show info about a server member")
@app_commands.describe(member="The member to look up (defaults to you)")
async def user_info_slash(interaction: discord.Interaction, member: discord.Member = None):
    m = member or interaction.user
    embed = discord.Embed(title=f"👤 {m.display_name}", color=m.color)
    embed.set_thumbnail(url=m.display_avatar.url)
    embed.add_field(name="Username",        value=str(m),                                              inline=True)
    embed.add_field(name="ID",              value=str(m.id),                                           inline=True)
    embed.add_field(name="Joined Server",   value=m.joined_at.strftime("%b %d, %Y") if m.joined_at else "N/A", inline=True)
    embed.add_field(name="Account Created", value=m.created_at.strftime("%b %d, %Y"),                  inline=True)
    embed.add_field(name="Top Role",        value=m.top_role.mention,                                  inline=True)
    embed.add_field(name="Bot?",            value="Yes" if m.bot else "No",                            inline=True)
    await interaction.response.send_message(embed=embed)


# ── /remind ───────────────────────────────────────────────────────────────────
@bot.tree.command(name="remind", description="Set a reminder (up to 1440 minutes / 24 hrs)")
@app_commands.describe(minutes="Minutes from now", message="What to remind you about")
async def remind_slash(interaction: discord.Interaction, minutes: int, message: str):
    if minutes < 1 or minutes > 1440:
        await interaction.response.send_message("Please choose between 1 and 1440 minutes.", ephemeral=True)
        return
    await interaction.response.send_message(
        f"⏰ Got it! I'll remind you about **'{message}'** in **{minutes} minute(s)**.", ephemeral=True
    )
    await discord.utils.sleep_until(
        discord.utils.utcnow().__class__.utcnow()
        .__class__.fromtimestamp(time.time() + minutes * 60)
    )
    try:
        await interaction.user.send(f"⏰ **Reminder:** {message}")
    except discord.Forbidden:
        chan = interaction.channel
        if chan:
            await chan.send(f"{interaction.user.mention} ⏰ **Reminder:** {message}")


# ── /chat-history ─────────────────────────────────────────────────────────────
@bot.tree.command(name="chat-history", description="Show the last 20 messages seen by bot in this channel")
async def chat_history_slash(interaction: discord.Interaction):
    history = chat_history.get(interaction.channel_id, deque())
    if not history:
        await interaction.response.send_message("No history recorded yet in this channel.", ephemeral=True)
        return
    text = "\n".join(history)
    await interaction.response.send_message(f"```\n{text[:1800]}\n```", ephemeral=True)


# ── /clear-my-memory ──────────────────────────────────────────────────────────
@bot.tree.command(name="clear-my-memory", description="Clear your personal conversation history with the bot")
async def clear_memory_slash(interaction: discord.Interaction):
    user_conversations.pop(interaction.user.id, None)
    await interaction.response.send_message("✅ Your conversation memory has been cleared.", ephemeral=True)


# ── Flask keep-alive ──────────────────────────────────────────────────────────
flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return "Bot is alive! ✅"

@flask_app.route('/health')
def health():
    total = len(SLASH_COMMANDS) + 14
    return {"status": "ok", "total_commands": total}

def _run_flask():
    flask_app.run(host='0.0.0.0', port=int(os.getenv('PORT', 8080)), use_reloader=False)


# ── Bot events ────────────────────────────────────────────────────────────────
@bot.event
async def on_ready():
    log.info(f"Logged in as {bot.user} (ID: {bot.user.id})")

    try:
        synced = await bot.tree.sync()
        log.info(f"Synced {len(synced)} global commands. May take up to 1 hour to appear everywhere.")
    except Exception as exc:
        log.exception(f"Command sync failed: {exc}")

    await bot.change_presence(
        activity=discord.Activity(type=discord.ActivityType.watching, name="your server | /ask")
    )


@bot.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return

    chat_history[message.channel.id].append(
        f"{message.author.display_name}: {message.content}"
    )

    await bot.process_commands(message)

    if message.content.startswith('/') or message.content.startswith('!'):
        return

    # Helper function for AI chat response
    async def respond_as_chat():
        async with message.channel.typing():
            context = '\n'.join(chat_history[message.channel.id])
            prompt = (
                "You are a helpful Discord assistant. "
                "Use the conversation history below to answer the user's message.\n\n"
                f"History:\n{context}\nUser: {message.content}\nAssistant:"
            )
            text = await _gemini(prompt)
        await message.reply(text)

    # Reply when directly @mentioned
    if bot.user in message.mentions:
        await respond_as_chat()
        return

    # Reply when message is a reply to the bot
    if message.reference:
        try:
            ref_msg = await message.channel.fetch_message(message.reference.message_id)
            if ref_msg.author == bot.user:
                await respond_as_chat()
                return
        except:
            pass

    # Reply when message contains the bot's name
    if bot.user.name.lower() in message.content.lower():
        await respond_as_chat()
        return


@bot.event
async def on_member_join(member: discord.Member):
    channel = member.guild.system_channel
    if channel:
        embed = discord.Embed(
            title="👋 Welcome!",
            description=f"Hey {member.mention}, welcome to **{member.guild.name}**! Glad to have you here. 🎉",
            color=0x57F287
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_footer(text=f"Member #{member.guild.member_count}")
        await channel.send(embed=embed)


@bot.event
async def on_member_remove(member: discord.Member):
    channel = member.guild.system_channel
    if channel:
        embed = discord.Embed(
            title="👋 Goodbye!",
            description=f"**{member.display_name}** has left the server. We'll miss you!",
            color=0xED4245
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        await channel.send(embed=embed)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    raise error


# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == '__main__':
    threading.Thread(target=_run_flask, daemon=True).start()
    if run_bot:
        bot.run(DISCORD_TOKEN)
    else:
        log.warning("Bot not started — missing tokens. Keep-alive server is running.")
        try:
            while True:
                time.sleep(60)
        except KeyboardInterrupt:
            pass
