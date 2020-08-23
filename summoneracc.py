from riotwatcher import LolWatcher, ApiError, RateLimiter
from settings import API_KEY, SUMMONER_NAME, DB_IP, DB_PASS
import pandas as pd
import mysql.connector

region = 'na1'
def connect_to_database():
     connector = mysql.connector.connect(user='root', password=DB_PASS, host=DB_IP, database='Matches')
     cursor = connector.cursor()
     return cursor

def get_watcher():
     lol_watcher = LolWatcher(API_KEY)
     return lol_watcher 

def get_summoner(lol_watcher):
     summoner = lol_watcher.summoner.by_name(region, SUMMONER_NAME)
     print(summoner)
     return summoner

def get_spell_dict(lol_watcher):
     latest = lol_watcher.data_dragon.versions_for_region(region)['n']['summoner']
     static_spells_list = lol_watcher.data_dragon.summoner_spells(latest, 'en_US')
     print(static_spells_list)
     spell_dict = {}
     for key in static_spells_list['data']:
          row = static_spells_list['data'][key]
          spell_dict[row['key']] = row['name']
     print(spell_dict)
     return spell_dict

def get_item_dict(lol_watcher):
     latest = lol_watcher.data_dragon.versions_for_region(region)['n']['item']
     static_items_list = lol_watcher.data_dragon.items(latest, 'en_US')
     item_dict = {}
     for key in static_items_list['data']:
          row = static_items_list['data'][key]
          item_dict[key] = row['name']
     return item_dict

def get_champ_dict(lol_watcher):
     latest = lol_watcher.data_dragon.versions_for_region(region)['n']['champion']
     static_champ_list = lol_watcher.data_dragon.champions(latest, False, 'en_US')
     champ_dict = {}
     for key in static_champ_list['data']:
          row = static_champ_list['data'][key]
          champ_dict[row['key']] = row['id']
     #print(champ_dict)
     return champ_dict

def get_item(item_dict, itemId):
     if itemId == 0:
          return "N/A"
     return item_dict[str(itemId)]

def get_champion(champ_dict, championId):
     return champ_dict[str(championId)]

def get_champion1(champ_dict, participants):
     print(champ_dict)
     print(champ_dict['69'])
     for row in participants:
          print(str(row['champion']) + ' ' + champ_dict[str(row['champion'])])
          """ row['championName'] = champ_dict[str(row['champion'])] """

def print_ranked_stats(lol_watcher, summoner, region):
     my_ranked_stats = lol_watcher.league.by_summoner(region, summoner['id'])
     print(my_ranked_stats)

def get_matchlist(lol_watcher, summoner, region, champ_dict, item_dict):
     #pd.set_option("display.max_rows", None, "display.max_columns", None)
     pd.set_option('display.max_rows', None)
     pd.set_option('display.max_columns', None)
     pd.set_option('display.width', None)
     pd.set_option('display.max_colwidth', 40)
     my_matches = lol_watcher.match.matchlist_by_account(region, summoner['accountId'], None, None, None, 1)
     # fetch last match detail
     last_match = my_matches['matches'][0]
     #print(last_match)
     match_detail = lol_watcher.match.by_id(region, last_match['gameId'])
     gameId = match_detail['gameId']
     participants = []
     stats = []
     full = []
     #print(match_detail['participantIdentities']['participantId'])
     """ for row in match_detail:
          participants1 = row['participants']
          participantIdentities = row['participantIdentities']
          participants_row = {}
          participants_row['participantId'] = participantIdentities['participantId']
          player = participantIdentities['player']
          participants_row['summonerName'] = player['summonerName']
          participants_row['champion'] = get_champion(champ_dict, participants1['championId'])
          participants_row['spell1'] = participants1['spell1Id']
          participants_row['spell2'] = participants1['spell2Id']
          participants_row['win'] = participants1['stats']['win']
          participants_row['kills'] = participants1['stats']['kills']
          participants_row['deaths'] = participants1['stats']['deaths']
          participants_row['assists'] = participants1['stats']['assists']
          full.append(participants_row) """
     for row in match_detail['participantIdentities']:
          participants_row = {}
          participants_row['gameId'] = gameId
          participants_row['participantId'] = row['participantId']
          print(row)
          player = row['player']
          
          participants_row['summonerName'] = player['summonerName']
          participants.append(participants_row)
     
     for row in match_detail['participants']:
          participants_row = {}
          participants_row['gameId'] = gameId
          participants_row['participantId'] = row['stats']['participantId']
          participants_row['champion'] = get_champion(champ_dict, row['championId'])
          participants_row['spell1'] = row['spell1Id']
          participants_row['spell2'] = row['spell2Id']
          participants_row['win'] = row['stats']['win']
          participants_row['kills'] = row['stats']['kills']
          participants_row['deaths'] = row['stats']['deaths']
          participants_row['assists'] = row['stats']['assists']
          """ participants_row['totalDamageDealt'] = row['stats']['totalDamageDealt']
          participants_row['goldEarned'] = row['stats']['goldEarned']
          participants_row['champLevel'] = row['stats']['champLevel']
          participants_row['totalMinionsKilled'] = row['stats']['totalMinionsKilled'] """
          participants_row['item0'] = get_item(item_dict, row['stats']['item0'])
          participants_row['item1'] = get_item(item_dict, row['stats']['item1'])
          participants_row['item2'] = get_item(item_dict, row['stats']['item2'])
          participants_row['item3'] = get_item(item_dict, row['stats']['item3'])
          participants_row['item4'] = get_item(item_dict, row['stats']['item4'])
          participants_row['item5'] = get_item(item_dict, row['stats']['item5'])
          participants_row['item6'] = get_item(item_dict, row['stats']['item6'])
          stats.append(participants_row)
     df1 = pd.DataFrame(participants)
     df2 = pd.DataFrame(stats)
     #df3 = pd.DataFrame(full)
     print(df1)
     print(df2.to_string())
     #print(df3)
     
     return stats

def main():
     cursor = connect_to_database()
     lol_watcher = get_watcher()
     summoner = get_summoner(lol_watcher)
     champ_dict = get_champ_dict(lol_watcher)
     item_dict = get_item_dict(lol_watcher)
     spell_dict = get_spell_dict(lol_watcher)
     stats = get_matchlist(lol_watcher, summoner, region, champ_dict, item_dict)
     #get_champion(get_champ_dict(lol_watcher), stats)

if __name__ == "__main__":
     main()
