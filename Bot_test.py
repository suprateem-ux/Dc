import os
import discord
from discord.ext import commands
from datetime import timedelta

TOKEN = os.getenv("DISCORD_TOKEN")
AD_CHANNEL_NAME = "advertisement"  # allowed ad channel name (partial match allowed)

# --- the specific channel to ignore completely ---
IGNORE_CHANNEL_ID = 1435937331709214760  # from your provided link

# --- Intents ---
intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# --- Keywords that count as advertising ---
AD_KEYWORDS = [
    "discord.gg",
    "invite.gg",
    "youtube.com",
    "twitch.tv",
    "kick.com",
    "chess.com",
    "telegram.me",
    "instagram.com",
    "join my server",
    "join my",
    "follow",
    "lichess.org/team",
    "lichess.org/swiss",
    "lichess.org/tournament",
    "lichess.org/blog",
    "subscribe",
    "facebook"
]

EXEMPT_ROLES = ["Admin", "Moderators"]
ad_offenders = {}  # track repeat offenders


@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")


@bot.event
async def on_message(message: discord.Message):
    # ignore bot messages
    if message.author.bot:
        return

    # ✅ ignore the specific channel completely
    if message.channel.id == IGNORE_CHANNEL_ID:
        return

    # ✅ allow if message is in advertisement channel (partial name match)
    if AD_CHANNEL_NAME.lower() in message.channel.name.lower():
        return

    # ✅ allow exempt roles
    if any(role.name in EXEMPT_ROLES for role in message.author.roles):
        return

    msg_lower = message.content.lower()

    # detect ad
    contains_ad = any(keyword in msg_lower for keyword in AD_KEYWORDS)
    contains_lichess_blog = "lichess.org/@/" in msg_lower and "/blog/" in msg_lower

    if contains_ad or contains_lichess_blog:
        try:
            await message.delete()
            user_id = message.author.id
            ad_offenders[user_id] = ad_offenders.get(user_id, 0) + 1

            # first offense → warn
            if ad_offenders[user_id] == 1:
                warning = (
                    f"{message.author.mention}, Advertising is only allowed in "
                    f"channels like **#{AD_CHANNEL_NAME}**!\n"
                    "Next time, you’ll be **timed out for 5 minutes.**"
                )
                await message.channel.send(warning)
                print(f"🗑 Deleted ad from {message.author} (1st offense)")

            # second offense → timeout
            else:
                timeout_duration = timedelta(minutes=5)
                await message.author.timeout(timeout_duration, reason="Repeated advertisement")
                await message.channel.send(f"{message.author.mention}, As your wish 🙂 — timed out for 5 minutes.")
                print(f"⏳ Timed out {message.author} for 5 minutes (2nd offense)")

        except Exception as e:
            print(f"⚠️ Error handling ad from {message.author}: {e}")

    await bot.process_commands(message)


bot.run(TOKEN)
