import os
import discord
from discord.ext import commands

TOKEN = os.getenv("DISCORD_TOKEN")
AD_CHANNEL_NAME = "advertisement"  # your real ad channel name

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True

bot = commands.Bot(command_prefix="!", intents=intents)

AD_KEYWORDS = ["discord.gg", "twitch.tv", "youtube.com", "invite.gg", "join my server"]

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if message.channel.name == AD_CHANNEL_NAME:
        return

    if any(keyword in message.content.lower() for keyword in AD_KEYWORDS):
        try:
            await message.delete()
            await message.channel.send(
                f"{message.author.mention}, advertising is only allowed in #{AD_CHANNEL_NAME}.",
                delete_after=5
            )
            print(f"🗑 Deleted ad from {message.author} in #{message.channel}")
        except Exception as e:
            print(f"⚠️ Error deleting message: {e}")

    await bot.process_commands(message)

bot.run(TOKEN)
