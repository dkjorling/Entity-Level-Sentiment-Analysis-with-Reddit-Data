import pandas as pd
import numpy as np
import json
import datetime as dt
import requests
import warnings
import re
import sys
from time import sleep
from nba_api.stats.static import players
from nba_api.stats.endpoints import commonplayerinfo, teamgamelog, boxscoretraditionalv2, boxscoreadvancedv2, teaminfocommon
from bs4 import BeautifulSoup


path = ("nba_data/")


### create list of players who played on lakers 2022-2023 season
player_list = [ 'Lebron James', 'Anthony Davis', 'D\'Angelo Russell', 'Dennis Schroder',
                'Austin Reaves', 'Russell Westbrook', 'Patrick Beverley', 'Troy Brown Jr.',
                'Jarred Vanderbilt', 'Malik Beasley', 'Lonnie Walker IV','Rui Hachimura',
                'Thomas Bryant', 'Wenyen Gabriel', 'Kendrick Nunn', 'Max Christie',
                'Juan Toscano-Anderson', 'Matt Ryan', 'Mo Bamba', 'Damian Jones',
                'Sterling Brown', 'Cole Swider', 'Scotty Pippen Jr.', 'Davon Reed'
              ]

other_team_ids = {'LAL':{'id':'1610612747', 'game_ids':[]},
                  'UTA':{'id':'1610612762', 'game_ids':[]},
                  'LAC':{'id':'1610612746', 'game_ids':[]}, 
                  'MIN':{'id':'1610612750', 'game_ids':[]},
                  'ORL':{'id':'1610612753', 'game_ids':[]},
                  'DEN':{'id':'1610612743', 'game_ids':[]},
                  'CHI':{'id':'1610612741', 'game_ids':[]},
                  'WAS':{'id':'1610612764', 'game_ids':[]}
                 }


def get_player_id_dict(player_list=player_list):
    """
    Given list of player names, fetches player ids and returns dict w player name and id.
    """
    player_dict = {}
    for p in player_list:
        try:
            p_info = players.find_players_by_full_name(p)
            player_dict[p] = p_info[0]['id']
        except:
            print("Could not fetch id for {}".format(p))
    return player_dict


def get_common_info(player_dict):
    """
    Given player dict with player name and id, returns df of common info for each player.
    
    Function also returns dictionary of player who were not loaded correctly.
    """
    common_info_dfs = []
    unsuccessful = {}
    for player, pid in player_dict.items():
        try:
            player_info = commonplayerinfo.CommonPlayerInfo(player_id=pid, timeout=2)
            common_info_dfs.append(player_info.get_data_frames()[0])
            print("{} successfully downloaded".format(player))
        except:
            print("{} failed to download!".format(player))
            unsuccessful[player] = pid
    
    return common_info_dfs, unsuccessful


def save_common_info(common_info_dfs):
    """
    Takes common_info_dfs list, concatenates them, and saves entire df to csv.
    """
    
    common_player_info = pd.concat(common_info_dfs)
    common_player_info = common_player_info[
    [
    'PLAYER_ID', 'FIRST_NAME', 'LAST_NAME', 'BIRTHDATE', 'SCHOOL',
    'HEIGHT', 'WEIGHT', 'SEASON_EXP', 'JERSEY', 'POSITION', 'DRAFT_YEAR',
    'DRAFT_ROUND', 'DRAFT_NUMBER'
    ]]
    
    common_player_info = common_player_info.reset_index().drop(columns='index')
    common_player_info.to_csv('common_player_info.csv')
    
    
def get_basic_game_logs(team_id, season=2022, season_type='Regular Season'):
    """
    Get basic game logs by team_id, beginning season year and season type.
    
    Parameters:
        team_id: nba.com team id; str
        season: year of beginning of season; int
        searon_type: one of: 'Regular Season', 'Playoffs', 'All-Star', 'All Star', 'Preseason'
    """
    if season_type not in ['Regular Season', 'Playoffs', 'All-Star', 'All Star', 'Preseason']:
        print("Invalid season type")
    else: 
        tgl = teamgamelog.TeamGameLog(team_id=team_id,
                                  season_type_all_star=season_type,
                                  season=season)
        columns = tgl.get_dict()['resultSets'][0]['headers']
        tgl = pd.DataFrame(tgl.get_dict()['resultSets'][0]['rowSet'], columns=columns)
        
    return tgl


def get_team_box_scores(team_id, season=2022, traditional=True):
    """
    Given team_id and season start year, returns all team box scores for year.
    Parameters:
        team_id: nba.com 10-digit team id
        season: starting year for desired season
        traditional: if true, returns traditional box scores, if false returns advanced; Default to True
    """
    ## get game ids ##
    try:
        tgl = get_basic_game_logs(team_id=team_id, season=season)
        game_ids = tgl['Game_ID'].astype(str) 
        print("game ids loaded")
    except ValueError:
        print("Could not load game ids, please try again.")
    sleep(3)
    
    # for traditional box score stats
    if traditional:
        # get cols and create empty df
        try:
            test = boxscoretraditionalv2.BoxScoreTraditionalV2(game_id=game_ids[0], timeout=3)
            columns = test.get_dict()['resultSets'][1]['headers']
            team_box_df = pd.DataFrame(columns=columns)
            print("Team box df created")
            
            # iterate through each game
            index = 0
            gid_no_load = []
            for gid in game_ids:
                try:
                    sleep(1)
                    game = boxscoretraditionalv2.BoxScoreTraditionalV2(game_id=gid, timeout=2)
                    teams = game.get_dict()['resultSets'][1]['rowSet']
                    
                    # only upload stats for desired team, not opponent
                    for team in teams:
                        if team[1] == team_id:
                            team_box_df.loc[index] = team
                            index += 1
                            print("{} successfully inserted for {}".format(team[2], gid))
                        else:
                            continue
                    print("Game {} complete".format(gid))
                except:
                    print("Could not load game_id: {}".format(gid))
                    gid_no_load.append(gid)
                sleep(3)
            return team_box_df, gid_no_load  
        except:
            print("Could not create team box df")
            return game_ids
    else:
        # for advanced box score stats
        try:
            # get cols and create empty df
            test = boxscoreadvancedv2.BoxScoreAdvancedV2(game_id=game_ids[0], timeout=3)
            columns = test.get_dict()['resultSets'][1]['headers']
            team_box_df = pd.DataFrame(columns=columns)
            print("Team box df created")
            
            # iterate through each game
            index = 0
            gid_no_load = []
            for gid in game_ids:
                try:
                    sleep(1)
                    game = boxscoreadvancedv2.BoxScoreAdvancedV2(game_id=gid, timeout=2)
                    teams = game.get_dict()['resultSets'][1]['rowSet']
                    
                    # only upload stats for desired team, not opponent
                    for team in teams:
                        if team[1] == team_id:
                            team_box_df.loc[index] = team
                            index += 1
                            print("{} successfully inserted for {}".format(team[2], gid))
                        else:
                            continue
                    print("Game {} complete".format(gid))
                except:
                    print("Could not load game_id: {}".format(gid))
                    gid_no_load.append(gid)
                sleep(3)
            return team_box_df, gid_no_load
        except:
            print("Could not create team box df")
            return game_ids


    
def get_player_box_scores(team_id, season=2022, traditional=True):
    """
    Given team_id and season start year, returns all player box score stats for year.
    
    Parameters:
        team_id: nba.com 10-digit team id
        season: starting year for desired season
        traditional: if true, returns traditional box scores, if false returns advanced; Default to True
    """
    ## get game ids ##
    try:
        tgl = get_basic_game_logs(team_id=team_id, season=season)
        game_ids = tgl['Game_ID'].astype(str) 
        print("game ids loaded")
    except ValueError:
        print("Could not load game ids, please try again.")
    sleep(3)
    if traditional:
        try:
            # get cols and create empty df
            test = boxscoretraditionalv2.BoxScoreTraditionalV2(game_id=game_ids[0], timeout=2)
            columns = test.get_dict()['resultSets'][0]['headers']
            player_box_df = pd.DataFrame(columns=columns)
            print("Player box df created")
            index = 0
            gid_no_load = []
            for gid in game_ids:
                try:
                    game = boxscoretraditionalv2.BoxScoreTraditionalV2(game_id=gid, timeout=2)
                    players = game.get_dict()['resultSets'][0]['rowSet']
                    for player in players:
                        if str(player[1]) == team_id:
                            player_box_df.loc[index] = player
                            index += 1
                            print("{} successfully inserted for {}".format(player[5], gid))
                        else:
                            continue
                    print("Game {} complete".format(gid))
                except:
                    print("Could not load game_id: {}".format(gid))
                    gid_no_load.append(gid)
                sleep(3)
            return player_box_df, gid_no_load  
        except:
            print("Could not create player box df")
            return game_ids
    else:
        try:
            # get cols and create empty df
            test = boxscoreadvancedv2.BoxScoreAdvancedV2(game_id=game_ids[0], timeout=2)
            columns = test.get_dict()['resultSets'][0]['headers']
            player_box_advanced_df = pd.DataFrame(columns=columns)
            print("Player box df created")
            index = 0
            gid_no_load = []
            for gid in game_ids:
                try:
                    game = boxscoreadvancedv2.BoxScoreAdvancedV2(game_id=gid, timeout=2)
                    players = game.get_dict()['resultSets'][0]['rowSet']
                    for player in players:
                        if str(player[1]) == team_id:
                            player_box_advanced_df.loc[index] = player
                            index += 1
                            print("{} successfully inserted for {}".format(player[5], gid))
                        else:
                            continue
                    print("Game {} complete".format(gid))
                except:
                    print("Could not load game_id: {}".format(gid))
                    gid_no_load.append(gid)
                sleep(3)
            return player_box_advanced_df, gid_no_load
        except:
            print("Could not create player box df")
            return game_ids

def get_common_team_info(teams):
    test = teaminfocommon.TeamInfoCommon(team_id=teams[0], season_nullable=2022).get_json()
    cols = json.loads(test)['resultSets'][0]['headers']
    
    tic_df = pd.DataFrame(columns=cols)
    index = 0
    for team in teams:
        js = teaminfocommon.TeamInfoCommon(team_id=team, season_nullable=2022).get_json()
        tic = json.loads(js)['resultSets'][0]
        tic_df.loc[index] = tic['rowSet'][0]
        
        index += 1
        
    
    return tic_df
              
        
def get_day_by_day_seedings(team, ew='w', start='2022-10-18', end='2023-04-09'):
    dt_start = dt.datetime.strptime(start, "%Y-%m-%d")
    dt_end = dt.datetime.strptime(end, "%Y-%m-%d")
    
    if ew == 'w':
        ew = 'Western Conference'
    else:
        ew = 'Eastern Conference'
    
    columns = [ew, 'W', 'L', 'W/L%', 'GB', 'PW', 'PL', 'PS/G', 'PA/G', 'RANK', 'DATE']
    
    current = dt_start
    seeding_on_date = pd.DataFrame(columns=columns)
    index = 0
    while current <= dt_end:
        url = "https://www.basketball-reference.com/friv/standings.fcgi?month={}&day={}&year={}&lg_id=NBA".format(current.month, current.day, current.year)
        x = requests.get(url)
        
        if str(x) == '<Response [429]>':
            print("Rate Limit Exceeded")
            return standings_on_date
            break
            

        soup = BeautifulSoup(x.content, "html.parser")
        tables = soup.find_all("table")
        
        if ew == 'Western Conference':
            standings = pd.read_html(str(tables[1]))[0]
        else:
            standings = pd.read_html(str(tables[0]))[0]
        
        standings[ew] = standings[ew].str.strip("*")
        
        
        team_row = standings[standings[ew] == team]
        rank = team_row.index[0] + 1
        date = dt.datetime.strftime(current, "%Y-%m-%d")
        
        insert = list(team_row.values[0])
        insert.append(rank)
        insert.append(date)
        
        seeding_on_date.loc[index] = insert
        
        current = current + dt.timedelta(days=1)
        index += 1
        
        print(str(date) + " complete")
        
        sleep(3)
    
    return seeding_on_date
        
        
def concat_all_team_data(abb, season, path=path):
    """
    Takes team info from tgl, traditional box and advanced box and concats into one df.
    """
    
    df = pd.read_csv(path + "tgl_{}.csv".format(abb), index_col=0)
    df2 = pd.read_csv(path + "team_box_traditional_{}.csv".format(abb), index_col=0)
    df3 = pd.read_csv(path + "team_box_advanced_{}.csv".format(abb), index_col=0)
    
    df4 = pd.concat([
    df[['GAME_DATE', 'MATCHUP', 'WL', 'W', 'L', 'W_PCT']],
    df2,
    df3.iloc[:, 6:]
    ],
    axis=1)
    
    df4['GAME_DATE'] = pd.to_datetime(df4['GAME_DATE'])

    df4 = df4.sort_values('GAME_DATE').reset_index().drop(columns=['index'])

    return df4


def concat_player_data(path):
    """
    Concatenate individual box score stats for any non-lakers stats \ 
    for players who played on the lakers at some point during the season
    """
    teams = ls.load_json_file('teams.json', path=path)
    
    pbtt = pd.read_csv(path + "player_box_traditional_total.csv", index_col=0)
    pbtt['GAME_ID'] = '00' + pbtt['GAME_ID'].astype(str)
    pbat = pd.read_csv(path + "player_box_advanced_total.csv", index_col=0)
    pbat['GAME_ID'] = '00' + pbat['GAME_ID'].astype(str)
    
    df_full = pd.merge(pbtt,
                       pbat,
                       how='inner',
                       on=['GAME_ID', 'TEAM_ID', 'PLAYER_ID',
                           'TEAM_ABBREVIATION', 'TEAM_CITY', 'PLAYER_NAME'])
    
    true_min = []
    for m in df_full['MIN_x']:
        if type(m) == float:
            true_min.append(m)
        else:
            reg = re.findall(r"^(\d+):(\d+)", m)
            if len(reg) > 0:
                mins = float(reg[0][0])
                secs = float(reg[0][1])
                true_min.append(mins + secs / 60)
            else:
                reg = re.findall(r"^(\d+)\.(\d+)", m)
                mins = float(reg[0][0])
                secs = float(reg[0][1])
                true_min.append(mins + secs)
    df_full['MIN'] = true_min
    
    drop_cols = ['NICKNAME_x', 'START_POSITION_x', 'COMMENT_x', 'MIN_x',
                 'NICKNAME_y', 'START_POSITION_y', 'COMMENT_y', 'MIN_y']
    
    df_full = df_full.drop(columns=drop_cols)
    
    files = ["tgl_{}.csv".format(x) for x in list(teams.keys())[1:]]
    tgl_dfs = [pd.read_csv(path + file, index_col=0) for file in files]
    tgls = pd.concat(tgl_dfs)
    tgls = tgls[['Game_ID', 'Team_ID', 'GAME_DATE', 'MATCHUP', 'WL']]
    tgls['Game_ID'] = '00' + tgls['Game_ID'].astype(str)
    
    df_fuller = pd.merge(
        df_full,
        tgls,
        how='left',
        left_on=['GAME_ID', 'TEAM_ID'],
        right_on=['Game_ID', 'Team_ID'])
    
    return df_fuller



















        
        
        
        
        
        