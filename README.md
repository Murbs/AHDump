# AHDump

AHDump is a personal project to teach myself how to use the [Blizzard API](https://develop.battle.net/) in conjunction with python scripting.

TODO
---
 - Implement task scheduler, to collect data on refresh
 - Coordinate itemID with lookups for item names
 - Sort data into structured categories
 - Display text while tool is retrieving data

Other things you could do past that, would be graphing/heatmaps similar to [The Undermine Journal](https://theunderminejournal.com/). 

REQUIREMENTS
---
To use this tool you need the following:
 - A blizzard account
 - An OAuth client
 - ClientID and secret
 - Something that can read .CSV files
 - Python

DEPENDENCIES
---
 - [Pandas](https://pandas.pydata.org/)
 - [Requests](https://pypi.org/project/requests/)

All other modules are included with python 3.x, or this repo.

HOW TO USE
---

Edit CRS.py, store your clientID and secret in their respective variables 'token_client_id'/'token_secret'

Run AHdump.py from terminal, and enter a realm name when prompted. If the realm name can be matched to its corresponding slug, the auction data for that realm will be saved as a .csv file with the current date.
