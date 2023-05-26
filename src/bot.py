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
class UpdateAttribute(discord.ui.View):
    def __init__(self, alert_profile_name: str, attributeKey: str):
        super().__init__()
        self.alert_profile_name = alert_profile_name
        self.attribute = cds.WeatherAttribute(int(attributeKey))
        if self.attribute == cds.WeatherAttribute.CLOUD_COVER:
            select = discord.ui.Select(placeholder = "Maximum cloud cover", options = cdo.CLOUD_COVER_OPTIONS)
        elif self.attribute == cds.WeatherAttribute.TRANSPARENCY:
            select = discord.ui.Select(placeholder = "Worst transparency", options = cdo.TRANSPARENCY_OPTIONS)
        elif self.attribute == cds.WeatherAttribute.SEEING:
            select = discord.ui.Select(placeholder = "Worst seeing", options = cdo.SEEING_OPTIONS)
        elif self.attribute == cds.WeatherAttribute.DARKNESS:
            select = discord.ui.Select(placeholder = "Brightest", options = cdo.DARKNESS_OPTIONS)
        elif self.attribute == cds.WeatherAttribute.SMOKE:
            select = discord.ui.Select(placeholder = "Worst smoke", options = cdo.SMOKE_OPTIONS)
        elif self.attribute == cds.WeatherAttribute.WIND:
            select = discord.ui.Select(placeholder = "Worst wind", options = cdo.WIND_OPTIONS)
        elif self.attribute == cds.WeatherAttribute.HUMIDITY:
            select = discord.ui.Select(placeholder = "Worst humidity", options = cdo.HUMIDITY_OPTIONS)
        elif self.attribute == cds.WeatherAttribute.TEMPERATURE:
            select = discord.ui.Select(placeholder = "Temperature Min and Max", options = cdo.TEMPERATURE_OPTIONS)
        select.callback = self.callback
        self.add_item(select)

    async def callback(self, interaction):
        profile = cds.AlertProfile(interaction.user.id, self.alert_profile_name)
        try:
            profile.load()
        except FileNotFoundError:
            await interaction.response.send_message(f"Alert profile {self.alert_profile_name} does not exist!")
            return
        if self.attribute == cds.WeatherAttribute.CLOUD_COVER:
            profile.add(cds.WeatherAttribute.CLOUD_COVER, int(interaction.data['values'][0]))
        elif self.attribute == cds.WeatherAttribute.TRANSPARENCY:
            profile.add(cds.WeatherAttribute.TRANSPARENCY, cds.Transparency.getAttributeFromText(interaction.data['values'][0]))
        elif self.attribute in [cds.WeatherAttribute.SEEING, cds.WeatherAttribute.DARKNESS, cds.WeatherAttribute.SMOKE, cds.WeatherAttribute.WIND, cds.WeatherAttribute.HUMIDITY]:
            profile.add(self.attribute, float(interaction.data['values'][0]))
        elif self.attribute == cds.WeatherAttribute.TEMPERATURE:
            temps = [float(x) for x in interaction.data['values']]
            profile.add(cds.WeatherAttribute.TEMPERATURE, (min(temps), max(temps)))
        profile.save()
        await interaction.response.send_message("Successfully updated!")

class UpdateSelectAttribute(discord.ui.View):
    def __init__(self, alert_profile_name: str):
        super().__init__()
        self.alert_profile_name = alert_profile_name

    @discord.ui.select(
        placeholder = "Select an attribute to update",
        options = cdo.ATTRIBUTE_OPTIONS
    )
    async def select_callback(self, interaction, select):
        await interaction.response.send_message("Update...", view=UpdateAttribute(self.alert_profile_name, select.values[0]))

@tree.command(name = "update_alert", description = "Update an alert profile")
@discord.app_commands.describe(alert_profile_name='alert profile name')
async def _updateAlertProfile(interaction, alert_profile_name: str):
    profile = cds.AlertProfile(interaction.user.id, alert_profile_name)
    try:
        profile.load()
    except FileNotFoundError:
        await interaction.response.send_message(f"Alert profile {alert_profile_name} does not exist!")
        return
    response = f"Updating alert profile..."
    response += f"\n\nCurrent alert profile:{repr(profile)}"
    response += "\n\nSelect an attribute to update."
    await interaction.response.send_message(response, view=UpdateSelectAttribute(alert_profile_name))
    

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
    await interaction.response.defer()
    profile = cds.AlertProfile(interaction.user.id, alert_profile_name)
    try:
        profile.load()
    except FileNotFoundError:
        await interaction.followup.send(f"Alert profile {alert_profile_name} does not exist!")
        return
    location = profile.get(cds.AlertProfile.LOCATION)
    weatherData = cds_web.extractWeatherData(location)
    if weatherData is None:
        await interaction.followup.send(f"Failed to get weather data for {location}!")
        return
    response = f"For {location}..."
    result = profile.checkForAlert(weatherData)
    if len(result) == 0:
        response += "\nNo alerts!"
    else:
        response += "\nConditions met from "
        for i in range(len(result)):
            alert = result[i]
            if i > 0 and (i != len(result) - 1 or len(result) > 2):
                response += ", "
            elif i > 0:
                response += " and "
            time1 = alert[0]
            time2 = alert[1]
            if time1.day == time2.day:
                response += f"{time1.strftime('%B %d, %H:%M')} to {time2.strftime('%H:%M')}"
            else:
                response += f"{time1.strftime('%B %d, %H:%M')} to {time2.strftime('%B %d, %H:%M')}"
    await interaction.followup.send(response)


def main():
    client.run(TOKEN)

if __name__ == '__main__':
    main()