import os

import discord
from dotenv import load_dotenv

import clearDarkSky as cds
import clearDarkSkyWeb as cds_web
import clearDarkSkyOptions as cdo

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)


# Set up bot
@client.event
async def on_ready():
    await tree.sync()
    print(f'{client.user} has connected to Discord!')


# Create Alert Profile
@tree.command(name = "create_alert", description = "Create an alert profile")
@discord.app_commands.describe(location='location name (example: AlbanyNY)')
@discord.app_commands.describe(alert_profile_name='alert profile name')
@discord.app_commands.describe(duration='min duration in hours')
async def _createAlertProfile(interaction, location: str, alert_profile_name: str, duration: int):
    # Validate location
    if not cds_web.validateLocationKey(location):
        await interaction.response.send_message("Invalid location! (examples: AlbanyNY, BttlRvr0AB, NrthCpPE, etc)\n \
            Find you location key from the url of your location and try again.")
        return

    profile = cds.AlertProfile(interaction.user.id, alert_profile_name, location)
    profile.setDuration(duration)
    profile.save()

    response = f"Successfully created alert profile {alert_profile_name} for {location}!"
    response += f"\nUse the `update_alert` command to set alert profile attributes."
    await interaction.response.send_message(response)


# Update Alert Profile
@tree.command(name = "update_alert", description = "Update an alert profile")
@discord.app_commands.describe(alert_profile_name='alert profile name')
async def _updateAlertProfile(interaction, alert_profile_name: str):
    # TODO - Update alert profile
    await interaction.response.send_message("Update alert profile is not yet implemented")
    

# Delete Alert Profile
@tree.command(name = "delete_alert", description = "Delete an alert profile")
@discord.app_commands.describe(alert_profile_name='alert profile name')
async def _deleteAlertProfile(interaction, alert_profile_name: str):
    profile = cds.AlertProfile(interaction.user.id, alert_profile_name)
    if profile.delete():
        await interaction.response.send_message(f"Successfully deleted alert profile {alert_profile_name}!")
    else:
        await interaction.response.send_message(f"Failed to delete alert profile {alert_profile_name}!")


# List Alert Profiles
@tree.command(name = "list_alerts", description = "List all of your alert profiles")
async def _listAlertProfile(interaction):
    profiles = cds.AlertProfile.getAll(interaction.user.id)
    if len(profiles) == 0:
        await interaction.response.send_message("You have no alert profiles!")
        return
    response = "Here are your alert profiles:\n"
    for profile in profiles:
        response += f"{profile.name} for {profile.get(cds.AlertProfile.LOCATION)}\n"
    await interaction.response.send_message(response)


# Check Alert Profile(s)
@tree.command(name = "check_alert", description = "Check all alert profiles")
@discord.app_commands.describe(alert_profile_name='alert profile name')
async def _checkAlertProfile(interaction, alert_profile_name: str):
    # TODO - Check alert profile
    await interaction.response.send_message("Check alert profile is not yet implemented!")

@tree.command(name = "check_all_alerts", description = "Check all alert profiles")
async def _checkAllAlertProfiles(interaction):
    # TODO - Check all alert profiles
    await interaction.response.send_message("Check all alert profiles not yet implemented!")


def main():
    client.run(TOKEN)

if __name__ == '__main__':
    main()