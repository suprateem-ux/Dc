import os
import discord
from discord.ext import commands

TOKEN = os.getenv("DISCORD_TOKEN")
AD_CHANNEL_NAME = "advertisement"  # change to your real advertisement channel name

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Keywords considered as advertisements
AD_KEYWORDS = [
    "discord.gg",
    "invite.gg",
    "youtube.com",
    "twitch.tv",
    "kick.com",
    "lichess.org",
    "chess.com",
    "telegram.me",
    "instagram.com",
    "join my server",
    "join my",
    "follow me on"
]

# Roles exempted from deletion
EXEMPT_ROLES = ["Admin", "VIP"]  # change to your exact role names

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    # --- Skip advertisement channel ---
    if message.channel.name.lower() == AD_CHANNEL_NAME.lower():
        return

    # --- Skip exempt roles ---
    if any(role.name in EXEMPT_ROLES for role in message.author.roles):
        return

    # --- Detect ad keywords ---
    if any(keyword in message.content.lower() for keyword in AD_KEYWORDS):
        try:
            await message.delete()
            warning = (
                f"{message.author.mention}, 🚫 advertising is only allowed in "
                f"#{AD_CHANNEL_NAME}!\n"
                "⚠️ It will be **timeout next time** if I see you again advertising here."
            )
            await message.channel.send(warning, delete_after=8)
            print(f"🗑 Deleted ad from {message.author} in #{message.channel}")
        except Exception as e:
            print(f"⚠️ Error deleting message: {e}")

    await bot.process_commands(message)

bot.run(TOKEN)
