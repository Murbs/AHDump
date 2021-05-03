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
 - Client id and secret
 - Something that can read .csv files
 - Python

DEPENDENCIES
---
 - [Pandas](https://pandas.pydata.org/)
 - [Requests](https://pypi.org/project/requests/)

All other modules are included with python 3.x, or this repo.

HOW TO USE
---

Store your client ID/secret as environment variables. Personally, I use [pipenv](https://pypi.org/project/pipenv/).

```PowerShell
cd <path to AHDump>

pipenv --python 3.x  # Change to whatever current compatible version of python
```

This should generate a pipfile and a .lock file, that houses venv data like python version, libraries etc.

If using pipenv, run AHdump.py from terminal.

```PowerShell
cd <path to AHDump>

pipenv run AHDump.py

#Loading .env environment variables...

Input realm name: Magtheridon #Replace with desired realm slug

#CSV file exports to cd
```

Enter a realm name when prompted. If the realm name can be matched to its corresponding slug, the auction data for that realm will be saved as a .csv file with the current date to your current directory. Refer to realm_slug.txt for a list of valid realm names.

DISCLAIMER: This is only setup for US realms. To setup for EU/OCE just swap the region and import your own realm list json file.
