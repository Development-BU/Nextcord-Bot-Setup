import nextcord
from nextcord.ext import commands
import aiohttp

# --- Configuration ---

BOT_TOKEN = "YOUR TOKEN HERE"
WEBHOOK_URL = "YOUR WEBHOOK HERE"
developer = "DEVELOPER_NAME"
version = "1.0.0"
forthisperson = "EXAMPLE"

# --- Bot Setup ---
# Define the bot's intents.
# You might need more intents depending on what your bot will do in the future.
intents = nextcord.Intents.default()
intents.message_content = True # Required to read message content for commands if not using slash commands exclusively
intents.members = True # Useful for getting member info in embeds

# Initialize the bot with a command prefix (though slash commands don't use it)
# and the defined intents.
bot = commands.Bot(command_prefix="!", intents=intents)

# --- Event: Bot Ready ---
@bot.event
async def on_ready():
    """
    This event fires when the bot successfully connects to Discord.
    It's a good place to confirm the bot is online.
    """
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")
    print("dsc.gg/botuniverse")
    # You can also set the bot's activity here if you wish
    await bot.change_presence(activity=nextcord.Game(name="dsc.gg/botuniverse"))


# --- Slash Command: /help ---
@bot.slash_command(name="help", description="Shows a list of available commands.")
async def help_command(interaction: nextcord.Interaction):
    """
    Responds with an embed listing the bot's commands.
    """
    help_embed = nextcord.Embed(
        title="Bot Commands",
        description="Here are the commands you can use:",
        color=nextcord.Color.blue()
    )
    help_embed.add_field(
        name="/help",
        value="Shows this help message.",
        inline=False
    )
    help_embed.add_field(
        name="/about",
        value="Gives information about this bot.",
        inline=False
    )
    help_embed.add_field(
        name="/report <message>",
        value="Sends an bug report to the developers",
        inline=False
    )
    help_embed.set_footer(text=f"dsc.gg/botuniverse | Coded By {developer}")
    await interaction.response.send_message(embed=help_embed, ephemeral=True) # ephemeral=True makes the message only visible to the user who used the command


# --- Slash Command: /about ---
@bot.slash_command(name="about", description="Provides information about the bot.")
async def about_command(interaction: nextcord.Interaction):
    """
    Responds with an embed containing information about the bot.
    """
    about_embed = nextcord.Embed(
        title="About This Bot",
        description="A Custom Discord Bot Made by BotUniverse With Tons of Commands!",
        color=nextcord.Color.green()
    )
    about_embed.add_field(
        name="Developer",
        value=f"BotUniverse/{developer}", # You can customize this
        inline=True
    )
    about_embed.add_field(
        name="Version",
        value=f"{version}",
        inline=True
    )
    about_embed.add_field(
        name="Completed For",
        value=f"{forthisperson}",
        inline=True
    )
    
    about_embed.set_footer(text="Built with Care and Support.")
    await interaction.response.send_message(embed=about_embed, ephemeral=True)


# --- Slash Command: /report ---
@bot.slash_command(name="report", description="Sends a Bug Report to Developers")
async def report_command(
    interaction: nextcord.Interaction,
    msg: str = nextcord.SlashOption(name="message", description="The content of your report", required=True)
):
    """
    Sends a report message to a predefined webhook URL as an embed.
    The report includes the user who sent it (but remains anonymous on the webhook side)
    and the channel it was sent from.
    """
    if not WEBHOOK_URL or WEBHOOK_URL == "YOUR_WEBHOOK_URL_HERE":
        await interaction.response.send_message(
            "Error: Webhook URL is not configured. Please contact the bot developer.",
            ephemeral=True
        )
        return

    report_embed = nextcord.Embed(
        title=f"Report: {bot.user}",
        description=f"**Report from:** {interaction.user.mention} (ID: `{interaction.user.id}`)\n"
                    f"**Guild:** {interaction.guild.name} (ID: `{interaction.guild.id}`)",
        color=nextcord.Color.red(),
        timestamp=nextcord.utils.utcnow() # Adds a timestamp to the embed
    )
    report_embed.add_field(
        name="Included Report Info.",
        value=msg,
        inline=False
    )
    report_embed.set_footer(text=f"Reported by {interaction.user.display_name}", icon_url=interaction.user.avatar.url if interaction.user.avatar else nextcord.Embed.Empty)

    try:
        # Use aiohttp for the HTTP client session to send the webhook
        async with aiohttp.ClientSession() as session:
            webhook = nextcord.Webhook.from_url(WEBHOOK_URL, session=session)
            # Corrected: Use None if bot's avatar is not available
            await webhook.send(embed=report_embed, username=f"Report : {bot.user}", avatar_url=bot.user.avatar.url if bot.user.avatar else None)
        
        await interaction.response.send_message(
            "Your report has been sent successfully! Thank you for your feedback.",
            ephemeral=True
        )
    except Exception as e:
        print(f"Failed to send webhook: {e}")
        await interaction.response.send_message(
            "There was an error sending your report. Please try again later or contact an administrator.",
            ephemeral=True
        )

# --- Run the Bot ---
if __name__ == "__main__":
    # Ensure you replace "YOUR_BOT_TOKEN_HERE" with your actual bot token
    bot.run(BOT_TOKEN)
