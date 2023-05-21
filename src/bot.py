import os

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@tree.command(name = "create_alert", description = "Create an alert profile")
@discord.app_commands.describe(location='location name (example: AlbanyNY)')
async def first_command(interaction, location: str):
    # TODO - Create an alert profile
    await interaction.response.send_message("Creating an alert profile is not yet supported!")

@tree.command(name = "delete_alert", description = "Delete an alert profile")
@discord.app_commands.describe(alert_profile_name='alert profile name')
async def first_command(interaction, alert_profile_name: str):
    # TODO - Delete an alert profile
    await interaction.response.send_message("Deleting an alert profile is not yet supported!")

@tree.command(name = "list_alerts", description = "List all of your alert profiles")
async def first_command(interaction):
    # TODO - List all alert profiles
    await interaction.response.send_message("Listing all alert profiles is not yet supported!")

@tree.command(name = "check_alerts", description = "Check all alert profiles")
async def first_command(interaction):
    # TODO - Check all alert profiles
    await interaction.response.send_message("Check all alert profiles!")

def main():
    client.run(TOKEN)

if __name__ == '__main__':
    main()