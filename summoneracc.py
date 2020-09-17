from riotwatcher import LolWatcher, ApiError, RateLimiter
from settings import API_KEY, SUMMONER_NAME, DB_IP, DB_PASS
import pandas as pd
import mysql.connector
import requests
import time

region = 'na1'
def add_to_database(lol_watcher, my_matchlist, champ_dict, item_dict, spell_dict):
     connector = mysql.connector.connect(user='root', password=DB_PASS, host=DB_IP, database='Matches')
     cur = connector.cursor()
     insert = """INSERT INTO Matches(gameId, participantId, summoner, champion, spell1, spell2, win, kills, deaths, assists, 
     level, minionsKilled, item0, item1, item2, item3, item4, item5, trinket) 
     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
     """ for row in stats:
          summonerData = (row['gameId'], row['participantId'], row['summoner'], row['champion'], row['spell1'], row['spell2'],
          row['win'], row['kills'], row['deaths'], row['assists'], row['level'], row['minionsKilled'], row['item0'],
          row['item1'], row['item2'], row['item3'], row['item4'], row['item5'], row['trinket'])
          cur.execute(insert, summonerData)
     print("success")
     connector.commit() """
     return cur

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
     spell_dict = {}
     for key in static_spells_list['data']:
          row = static_spells_list['data'][key]
          spell_dict[row['key']] = row['name']
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

def get_spell(spell_dict, spellId):
     return spell_dict[str(spellId)]

def get_item(item_dict, itemId):
     if itemId == 0:
          return "N/A"
     return item_dict[str(itemId)]

def get_champion(champ_dict, championId):
     return champ_dict[str(championId)]

def print_ranked_stats(lol_watcher, summoner, region):
     my_ranked_stats = lol_watcher.league.by_summoner(region, summoner['id'])
     print(my_ranked_stats)

def get_matchlist(lol_watcher, region, summoner, index):
     my_matchlist = lol_watcher.match.matchlist_by_account(region, summoner['accountId'], None, 1578477600, None, index)
     return my_matchlist 

def get_match(lol_watcher, my_matchlist, champ_dict, item_dict, spell_dict):
     #pd.set_option("display.max_rows", None, "display.max_columns", None)
     pd.set_option('display.max_rows', None)
     pd.set_option('display.max_columns', None)
     pd.set_option('display.width', None)
     pd.set_option('display.max_colwidth', 40)
     last_match = my_matchlist['matches'][0]
     match_detail = lol_watcher.match.by_id(region, last_match['gameId'])
     gameId = match_detail['gameId']
     participants = []
     stats = []
     for row in match_detail['participantIdentities']:
          participants_row = {}
          participants_row['gameId'] = gameId
          participants_row['participantId'] = row['participantId']
          player = row['player']
          participants_row['summonerName'] = player['summonerName']
          participants.append(participants_row)
     #print(participants)
     for row in match_detail['participants']:
          participants_row = {}
          participants_row['gameId'] = gameId
          participants_row['participantId'] = row['stats']['participantId']
          participants_row['summoner'] = participants[participants_row['participantId'] - 1]['summonerName']
          participants_row['champion'] = get_champion(champ_dict, row['championId'])
          participants_row['spell1'] = get_spell(spell_dict, row['spell1Id'])
          participants_row['spell2'] = get_spell(spell_dict, row['spell2Id'])
          participants_row['win'] = row['stats']['win']
          participants_row['kills'] = row['stats']['kills']
          participants_row['deaths'] = row['stats']['deaths']
          participants_row['assists'] = row['stats']['assists']
          """ participants_row['totalDamageDealt'] = row['stats']['totalDamageDealt']
          participants_row['goldEarned'] = row['stats']['goldEarned']"""
          participants_row['level'] = row['stats']['champLevel']
          participants_row['minionsKilled'] = row['stats']['totalMinionsKilled'] 
          participants_row['item0'] = get_item(item_dict, row['stats']['item0'])
          participants_row['item1'] = get_item(item_dict, row['stats']['item1'])
          participants_row['item2'] = get_item(item_dict, row['stats']['item2'])
          participants_row['item3'] = get_item(item_dict, row['stats']['item3'])
          participants_row['item4'] = get_item(item_dict, row['stats']['item4'])
          participants_row['item5'] = get_item(item_dict, row['stats']['item5'])
          participants_row['trinket'] = get_item(item_dict, row['stats']['item6'])
          stats.append(participants_row)
     df1 = pd.DataFrame(participants)
     df2 = pd.DataFrame(stats)
     """ print(df1)
     print(df2.to_string())
     print(stats) """
     """insert = INSERT INTO Matches(gameId, participantId, summoner, champion, spell1, spell2, win, kills, deaths, assists, 
     level, minionsKilled, item0, item1, item2, item3, item4, item5, trinket) 
     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
     for row in stats:
          summonerData = (row['gameId'], row['participantId'], row['summoner'], row['champion'], row['spell1'], row['spell2'],
          row['win'], row['kills'], row['deaths'], row['assists'], row['level'], row['minionsKilled'], row['item0'],
          row['item1'], row['item2'], row['item3'], row['item4'], row['item5'], row['trinket'])
          cursor.execute(insert, summonerData) """
     return stats

def main():
     lol_watcher = get_watcher()
     summoner = get_summoner(lol_watcher)
     champ_dict = get_champ_dict(lol_watcher)
     item_dict = get_item_dict(lol_watcher)
     spell_dict = get_spell_dict(lol_watcher)

     connector = mysql.connector.connect(user='root', password=DB_PASS, host=DB_IP, database='Matches')
     cur = connector.cursor()
     insert = """INSERT INTO Matches(gameId, participantId, summoner, champion, spell1, spell2, win, kills, deaths, assists, 
     level, minionsKilled, item0, item1, item2, item3, item4, item5, trinket) 
     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
     index = 0
     range = 2000
     while index < range:
          try:
               my_matchlist = get_matchlist(lol_watcher, region, summoner, index)
               print(index)
               stats = get_match(lol_watcher, my_matchlist, champ_dict, item_dict, spell_dict)
               checkGame = """SELECT * FROM Matches WHERE gameId = %s """
               gameId = ((stats[0]['gameId']))
               print(gameId)
               cur.execute(checkGame, (gameId,))
               inDb = cur.fetchall()
               if len(inDb) > 1:
                    index += 1
                    continue
               for row in stats:
                    summonerData = (row['gameId'], row['participantId'], row['summoner'], row['champion'], row['spell1'], row['spell2'],
                    row['win'], row['kills'], row['deaths'], row['assists'], row['level'], row['minionsKilled'], row['item0'],
                    row['item1'], row['item2'], row['item3'], row['item4'], row['item5'], row['trinket'])
                    cur.execute(insert, summonerData)
                    print("success")
                    connector.commit()
               index += 1
          except requests.HTTPError as e:
               time.sleep(1)
               print(e.__class__.__name__)
               print(e)
               print("Something went wrong")
               if index > 0:
                    index -= 1
               continue
          except Exception as ex:
               print(ex.__class__.__name__)
               print(ex)
               break
     cur.execute("SELECT * FROM matches WHERE summoner LIKE 'Poprocks12' ")
     result = cur.fetchall()
     #for x in result:
          #print(x)
     
     

if __name__ == "__main__":
     main()
