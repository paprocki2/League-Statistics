from riotwatcher import LolWatcher, ApiError
from settings import API_KEY, SUMMONER_NAME

lol_watcher = LolWatcher(API_KEY)
region = 'na1'

me = lol_watcher.summoner.by_name(region, SUMMONER_NAME)
print(me)

my_ranked_stats = lol_watcher.league.by_summoner(region, me['id'])
print(my_ranked_stats)


