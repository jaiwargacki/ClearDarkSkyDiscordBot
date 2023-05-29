import os

import discord
from discord.ext import tasks as discordTasks
from dotenv import load_dotenv

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

import clearDarkSkyModel as cds
import clearDarkSkyWeb as cds_web

from clearDarkSkyConstants import *

# Bot Setup

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)

@client.event
async def on_ready():
    await tree.sync()
    print(f'{client.user} has connected to Discord!')

    scheduler = AsyncIOScheduler()
    scheduler.add_job(checkAlerts, CronTrigger(hour=7, minute=0, second=0))
    scheduler.start()


# Classes

class UpdateAttribute(discord.ui.View):
    def __init__(self, alert_profile_name: str, attributeKey: str):
        super().__init__()
        self.alert_profile_name = alert_profile_name
        self.attribute = WeatherAttribute(int(attributeKey))
        lookup = OPTIONS_LOOKUP[self.attribute]
        select = discord.ui.Select(placeholder = lookup[0], options = lookup[1], \
            min_values=lookup[2], max_values=lookup[3])
        select.callback = self.callback
        self.add_item(select)

    async def callback(self, interaction):
        profile = cds.AlertProfile(interaction.user.id, self.alert_profile_name)
        try:
            profile.load()
        except FileNotFoundError:
            await interaction.response.send_message(f"Alert profile {self.alert_profile_name} does not exist!")
            return
        if self.attribute == WeatherAttribute.CLOUD_COVER:
            profile.add(WeatherAttribute.CLOUD_COVER, int(interaction.data['values'][0]))
        elif self.attribute == WeatherAttribute.TRANSPARENCY:
            profile.add(WeatherAttribute.TRANSPARENCY, Transparency(int(interaction.data['values'][0])))
        elif self.attribute in [WeatherAttribute.SEEING, WeatherAttribute.DARKNESS, WeatherAttribute.SMOKE, WeatherAttribute.WIND, WeatherAttribute.HUMIDITY]:
            profile.add(self.attribute, float(interaction.data['values'][0]))
        elif self.attribute == WeatherAttribute.TEMPERATURE:
            temps = [float(x) for x in interaction.data['values']]
            profile.add(WeatherAttribute.TEMPERATURE, (min(temps), max(temps)))
        profile.save()
        await interaction.response.send_message("Successfully updated!")

class UpdateSelectAttribute(discord.ui.View):
    def __init__(self, alert_profile_name: str):
        super().__init__()
        self.alert_profile_name = alert_profile_name

    @discord.ui.select(
        placeholder = "Select an attribute to update",
        options = ATTRIBUTE_OPTIONS
    )
    async def select_callback(self, interaction, select):
        await interaction.response.send_message("Update...", view=UpdateAttribute(self.alert_profile_name, select.values[0]))


# Commands

@tree.command(name = "create_alert", description = "Create an alert profile")
@discord.app_commands.describe(location='location name (example: AlbanyNY)')
@discord.app_commands.describe(alert_profile_name='alert profile name')
@discord.app_commands.describe(duration='min duration in hours')
async def _createAlertProfile(interaction, location: str, alert_profile_name: str, duration: int):
    await interaction.response.defer()
    if not cds_web.validateLocationKey(location):
        await interaction.followup.send("Invalid location! (examples: AlbanyNY, BttlRvr0AB, NrthCpPE, etc)\n \
            Find you location key from the url of your location and try again.")
        return

    profile = cds.AlertProfile(interaction.user.id, alert_profile_name, location)
    profile.setDuration(duration)
    profile.save()

    response = f"Successfully created alert profile {alert_profile_name} for {location}!"
    response += f"\nUse the `update_alert` command to set alert profile attributes."
    await interaction.followup.send(response)


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
    

@tree.command(name = "delete_alert", description = "Delete an alert profile")
@discord.app_commands.describe(alert_profile_name='alert profile name')
async def _deleteAlertProfile(interaction, alert_profile_name: str):
    profile = cds.AlertProfile(interaction.user.id, alert_profile_name)
    if profile.delete():
        await interaction.response.send_message(f"Successfully deleted alert profile {alert_profile_name}!")
    else:
        await interaction.response.send_message(f"Failed to delete alert profile {alert_profile_name}!")


@tree.command(name = "list_alerts", description = "List all of your alert profiles")
async def _listAlertProfile(interaction):
    profiles = cds.AlertProfile.getAllForUser(interaction.user.id)
    if len(profiles) == 0:
        await interaction.response.send_message("You have no alert profiles!")
        return
    response = "Here are your alert profiles:\n"
    for profile in profiles:
        response += f"{profile.name} for {profile.get(cds.AlertProfile.LOCATION)}\n"
    await interaction.response.send_message(response)


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


async def checkAlerts():
    print("Checking alerts...")
    for profile in cds.AlertProfile.getAll():
        profile.load()
        location = profile.get(cds.AlertProfile.LOCATION)
        weatherData = cds_web.extractWeatherData(location)
        print(f"Checking {location}...")
        if weatherData is None:
            continue
        result = profile.checkForAlert(weatherData)
        if len(result) == 0:
            continue
        response = f"For {location}..."
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
        userId = profile.username
        print(f"Sending alert to {userId}...")
        user = await client.fetch_user(userId)
        await user.send(response)


def main():
    client.run(TOKEN)


if __name__ == '__main__':
    main()