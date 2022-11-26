import requests
import toml

CONFIG = toml.load("././tester.toml")
ROVER_CONFIG = CONFIG["RoVer"]
ROVER_GUILD_ID = ROVER_CONFIG["Id"]
ROBLOX_CONFIG = CONFIG["Roblox"]
ROBLOX_GROUP_ID = ROBLOX_CONFIG["Id"]
ROVER_URL = "registry.rover.link/api/guilds/"+ROVER_GUILD_ID+"/discord-to-roblox/{discordUserId}"
ROBLOX_URL = "groups.roblox.com/v1/groups/"+ROBLOX_GROUP_ID+"/users/{userId}"

# get tester ids
def getDiscordIds():
	return []

discordIds = getDiscordIds()

# assign roblox ids to discord
def getRobloxIds(dIds: list[int]):
	return []

robloxIds = getRobloxIds(discordIds)

# update user in Roblox group
def updateUserId(userId: int):
	print("Update", userId)

for robloxId in robloxIds:
	updateUserId(robloxId)