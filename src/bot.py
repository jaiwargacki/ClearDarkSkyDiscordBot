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
class UpdateCloudCover(discord.ui.View):
    def __init__(self, alert_profile_name: str):
        super().__init__()
        self.alert_profile_name = alert_profile_name

    @discord.ui.select(
        placeholder = "Maximium cloud cover",
        options = cdo.CLOUD_COVER_OPTIONS
    )
    async def select_callback(self, interaction, select):
        profile = cds.AlertProfile(interaction.user.id, self.alert_profile_name)
        try:
            profile.load()
        except FileNotFoundError:
            await interaction.response.send_message(f"Alert profile {self.alert_profile_name} does not exist!")
            return
        profile.add(cds.WeatherAttribute.CLOUD_COVER, int(select.values[0]))
        profile.save()
        await interaction.response.send_message("Successfully updated cloud cover!")

class UpdateTransparency(discord.ui.View):
    def __init__(self, alert_profile_name: str):
        super().__init__()
        self.alert_profile_name = alert_profile_name

    @discord.ui.select(
        placeholder = "Worst transparency",
        options = cdo.TRANSPARENCY_OPTIONS
    )
    async def select_callback(self, interaction, select):
        profile = cds.AlertProfile(interaction.user.id, self.alert_profile_name)
        try:
            profile.load()
        except FileNotFoundError:
            await interaction.response.send_message(f"Alert profile {self.alert_profile_name} does not exist!")
            return
        profile.add(cds.WeatherAttribute.TRANSPARENCY, cds.Transparency.getAttributeFromText(select.values[0]))
        profile.save()
        await interaction.response.send_message("Successfully updated transparency!")

class UpdateSeeing(discord.ui.View):
    def __init__(self, alert_profile_name: str):
        super().__init__()
        self.alert_profile_name = alert_profile_name

    @discord.ui.select(
        placeholder = "Worst seeing",
        options = cdo.SEEING_OPTIONS
    )
    async def select_callback(self, interaction, select):
        profile = cds.AlertProfile(interaction.user.id, self.alert_profile_name)
        try:
            profile.load()
        except FileNotFoundError:
            await interaction.response.send_message(f"Alert profile {self.alert_profile_name} does not exist!")
            return
        profile.add(cds.WeatherAttribute.SEEING, float(select.values[0]))
        profile.save()
        await interaction.response.send_message("Successfully updated seeing!")

class UpdateDarkness(discord.ui.View):
    def __init__(self, alert_profile_name: str):
        super().__init__()
        self.alert_profile_name = alert_profile_name

    @discord.ui.select(
        placeholder = "Brightest",
        options = cdo.DARKNESS_OPTIONS
    )
    async def select_callback(self, interaction, select):
        profile = cds.AlertProfile(interaction.user.id, self.alert_profile_name)
        try:
            profile.load()
        except FileNotFoundError:
            await interaction.response.send_message(f"Alert profile {self.alert_profile_name} does not exist!")
            return
        profile.add(cds.WeatherAttribute.DARKNESS, float(select.values[0]))
        profile.save()
        await interaction.response.send_message("Successfully updated darkness!")

class UpdateSmoke(discord.ui.View):
    def __init__(self, alert_profile_name: str):
        super().__init__()
        self.alert_profile_name = alert_profile_name

    @discord.ui.select(
        placeholder = "Worst smoke",
        options = cdo.SMOKE_OPTIONS
    )
    async def select_callback(self, interaction, select):
        profile = cds.AlertProfile(interaction.user.id, self.alert_profile_name)
        try:
            profile.load()
        except FileNotFoundError:
            await interaction.response.send_message(f"Alert profile {self.alert_profile_name} does not exist!")
            return
        profile.add(cds.WeatherAttribute.SMOKE, float(select.values[0]))
        profile.save()
        await interaction.response.send_message("Successfully updated smoke!")

class UpdateWind(discord.ui.View):
    def __init__(self, alert_profile_name: str):
        super().__init__()
        self.alert_profile_name = alert_profile_name

    @discord.ui.select(
        placeholder = "Worst wind",
        options = cdo.WIND_OPTIONS
    )
    async def select_callback(self, interaction, select):
        profile = cds.AlertProfile(interaction.user.id, self.alert_profile_name)
        try:
            profile.load()
        except FileNotFoundError:
            await interaction.response.send_message(f"Alert profile {self.alert_profile_name} does not exist!")
            return
        profile.add(cds.WeatherAttribute.WIND, float(select.values[0]))
        profile.save()
        await interaction.response.send_message("Successfully updated wind!")

class UpdateHumidity(discord.ui.View):
    def __init__(self, alert_profile_name: str):
        super().__init__()
        self.alert_profile_name = alert_profile_name

    @discord.ui.select(
        placeholder = "Worst humidity",
        options = cdo.HUMIDITY_OPTIONS
    )
    async def select_callback(self, interaction, select):
        profile = cds.AlertProfile(interaction.user.id, self.alert_profile_name)
        try:
            profile.load()
        except FileNotFoundError:
            await interaction.response.send_message(f"Alert profile {self.alert_profile_name} does not exist!")
            return
        profile.add(cds.WeatherAttribute.HUMIDITY, float(select.values[0]))
        profile.save()
        await interaction.response.send_message("Successfully updated humidity!")

class UpdateTemperature(discord.ui.View):
    def __init__(self, alert_profile_name: str):
        super().__init__()
        self.alert_profile_name = alert_profile_name

    @discord.ui.select(
        placeholder = "Temperature Min and Max",
        min_values=2,
        max_values=2,
        options = cdo.TEMPERATURE_OPTIONS
    )
    async def select_callback(self, interaction, select):
        profile = cds.AlertProfile(interaction.user.id, self.alert_profile_name)
        try:
            profile.load()
        except FileNotFoundError:
            await interaction.response.send_message(f"Alert profile {self.alert_profile_name} does not exist!")
            return
        temps = [float(x) for x in select.values]
        profile.add(cds.WeatherAttribute.TEMPERATURE, (min(temps), max(temps)))
        profile.save()
        await interaction.response.send_message("Successfully updated temperature!")

class UpdateSelectAttribute(discord.ui.View):
    def __init__(self, alert_profile_name: str):
        super().__init__()
        self.alert_profile_name = alert_profile_name

    @discord.ui.select(
        placeholder = "Select an attribute to update",
        options = cdo.ATTRIBUTE_OPTIONS
    )
    async def select_callback(self, interaction, select):
        if select.values[0] == str(cds.WeatherAttribute.CLOUD_COVER.value):
            await interaction.response.send_message("Update cloud cover...", view=UpdateCloudCover(self.alert_profile_name))
        elif select.values[0] == str(cds.WeatherAttribute.TRANSPARENCY.value):
            await interaction.response.send_message("Update transparency...", view=UpdateTransparency(self.alert_profile_name))
        elif select.values[0] == str(cds.WeatherAttribute.SEEING.value):
            await interaction.response.send_message("Update seeing...", view=UpdateSeeing(self.alert_profile_name))
        elif select.values[0] == str(cds.WeatherAttribute.DARKNESS.value):
            await interaction.response.send_message("Update darkness...", view=UpdateDarkness(self.alert_profile_name))
        elif select.values[0] == str(cds.WeatherAttribute.SMOKE.value):
            await interaction.response.send_message("Update smoke...", view=UpdateSmoke(self.alert_profile_name))
        elif select.values[0] == str(cds.WeatherAttribute.WIND.value):
            await interaction.response.send_message("Update wind...", view=UpdateWind(self.alert_profile_name))
        elif select.values[0] == str(cds.WeatherAttribute.HUMIDITY.value):
            await interaction.response.send_message("Update humidity...", view=UpdateHumidity(self.alert_profile_name))
        elif select.values[0] == str(cds.WeatherAttribute.TEMPERATURE.value):
            await interaction.response.send_message("Update temperature...", view=UpdateTemperature(self.alert_profile_name))
        else:
            await interaction.response.send_message("Invalid option selected!")

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