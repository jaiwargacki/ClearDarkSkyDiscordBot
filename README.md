# Clear Dark Sky Discord Bot

## About

This is a Discord bot that allows user to create alter profiles for locations 
on [Clear Dark Sky](https://www.cleardarksky.com/csk/). The bot will then
periodically check the weather forecast for the location and send a message
to the user if the forecast meets the user's criteria.

Special thanks to Attilla Danko for creating Clear Dark Sky and allowing me to
use the data from the site. If you want to run this bot yourself, please 
reach out to him first. This repository requires env variables that are not
included in the repository, and will not work without information and approval
from Attilla.

That being said, if you want to use the bot (which I host), you can! See below.

## Usage

### Getting access to the bot

Join this server to get access to the bot: https://discord.gg/8EVZpMDaND
Once you have access to the bot, you can dm the bot to get started.

### Commands

#### `/create_alert`
Create a new alert profile. The command takes the following arguments:
- `location`: the location key from the url of the location for this alert profile. For example, if the url is `https://www.cleardarksky.com/c/AlbanyNYkey.html`, the location key is `AlbanyNY`.
- `alert_profile_name`: The name of the alert profile. This is what you will use to reference the alert profile in other commands.
- `duration`: The minimum duration of the weather forecast that you want to be alerted for. For example, if you want to be alerted if the forecast meets your criteria for at least 3 hours in a row, you would enter `3`.

#### `/delete_alert`
Delete an alert profile. The command takes an argument `alert_profile_name` for the name of the alert profile to delete.

#### `/list_alerts`
List all alert profiles you currently have.

#### `/update_alert`
Update an alert profile. The command takes an argument `alert_profile_name` for the name of the alert profile to update. Once the command is run, the bot will prompt you what you want to update.

#### `/check_alert`
Check the weather forecast for a particular profile. The command takes an argument `alert_profile_name` for the name of the alert profile to check. This is the same check that is run periodically.
