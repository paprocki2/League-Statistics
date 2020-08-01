from riotwatcher import LolWatcher, ApiError, RateLimiter
from settings import API_KEY, SUMMONER_NAME, DB_IP, DB_PASS
import pandas as pd
import mysql.connector

def connect_to_database():
     connector = mysql.connector.connect(user='root', password=DB_PASS, host=DB_IP, database='Matches')
     cursor = connector.cursor()
     return cursor

def get_summoner():
     lol_watcher = LolWatcher(API_KEY)
     region = 'na1'
     ddragon = LolWatcher.data_dragon
     ddragon
     me = lol_watcher.summoner.by_name(region, SUMMONER_NAME)
     print(me)

def print_ranked_stats(region, summoner, lol_watcher):
     my_ranked_stats = lol_watcher.league.by_summoner(region, summoner['id'])
     print(my_ranked_stats)

def get_matchlist(lol_watcher, summoner, region):
     my_matches = lol_watcher.match.matchlist_by_account(region, summoner['accountId'], None, None, None, 1)
     # fetch last match detail
     last_match = my_matches['matches'][0]
     print(last_match)
     match_detail = lol_watcher.match.by_id(region, last_match['gameId'])
     participants = []
     for row in match_detail['participants']:
          participants_row = {}
          participants_row['champion'] = row['championId']
          participants_row['spell1'] = row['spell1Id']
          participants_row['spell2'] = row['spell2Id']
          participants_row['win'] = row['stats']['win']
          participants_row['kills'] = row['stats']['kills']
          participants_row['deaths'] = row['stats']['deaths']
          participants_row['assists'] = row['stats']['assists']
          participants_row['totalDamageDealt'] = row['stats']['totalDamageDealt']
          participants_row['goldEarned'] = row['stats']['goldEarned']
          participants_row['champLevel'] = row['stats']['champLevel']
          participants_row['totalMinionsKilled'] = row['stats']['totalMinionsKilled']
          participants_row['item0'] = row['stats']['item0']
          participants_row['item1'] = row['stats']['item1']
          participants_row['item2'] = row['stats']['item2']
          participants_row['item3'] = row['stats']['item3']
          participants_row['item4'] = row['stats']['item4']
          participants_row['item5'] = row['stats']['item5']
          participants_row['item6'] = row['stats']['item6']
          print(row['stats']['item4'])
     
          participants.append(participants_row)
     df = pd.DataFrame(participants)
     print(df)
