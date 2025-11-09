import os
import discord
from discord.ext import commands

TOKEN = os.getenv("DISCORD_TOKEN")
AD_CHANNEL_NAME = "advertisement"  # change to your actual advertisement channel name

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Keywords that count as advertisement
AD_KEYWORDS = ["discord.gg", "twitch.tv", "youtube.com", "invite.gg", "join my server"]

# Roles that are exempt from deletion
EXEMPT_ROLES = ["Admin", "VIP"]  # change to match your server role names

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return  # ignore other bots

    # --- Skip if it's in the advertisement channel ---
    if message.channel.name.lower() == AD_CHANNEL_NAME.lower():
        return

    # --- Skip if user has any exempt role ---
    if any(role.name in EXEMPT_ROLES for role in message.author.roles):
        return

    # --- Check for advertisement keywords ---
    if any(keyword in message.content.lower() for keyword in AD_KEYWORDS):
        try:
            await message.delete()
            await message.channel.send(
                f"{message.author.mention}, advertising is only allowed in #{AD_CHANNEL_NAME}!",
                delete_after=5
            )
            print(f"🗑 Deleted ad from {message.author} in #{message.channel}")
        except Exception as e:
            print(f"⚠️ Error deleting message: {e}")

    await bot.process_commands(message)

bot.run(TOKEN)
