import pandas as pd
import numpy as np
import json
import re
import datetime as dt
import sys
from time import sleep



### load data ###
path = "nba_data/"
# player dict with names and ids 
f = open(path + 'players.json')
player_dict = json.load(f)
# transaction dict with transaction info for players
f = open(path + 'transactions.json')
transactions_dict = json.load(f)
# teams dict contains lakers and teams laker players played for in 2022-23 w id and all game ids
f = open(path + 'teams.json')
team_dict = json.load(f)

def load_json_file(file, path=path):
    f = open(path + file)
    return json.load(f)


def find_nearest_date(df, column, date):
    """
    Given a df with a string date column, returns string date of nearest date that does not go past that date.
    Note: date must be inh '%Y-%m-%d' format
    Parameters:
        df: dataframe to reference
        column: df column to reference
        date: string format date 
    """
    
    dt_date = dt.datetime.strptime(date, "%Y-%m-%d") # define date in dt format
    
    string_dates = list(df[column])
    dates = list(pd.to_datetime(df[column]))
    diffs = [dt_date - x for x in dates]
    idx = diffs.index(min([d for d in diffs if d.days >=0]))
    date = string_dates[idx]
    
    return date

def gmas(stat, stat_df):
    """
    Advanced stats are calculated using number of possessions so simple mean will not \
    calculate proper value. This function takes possessions into account to return the \
    correct average advanced stat
    """
    product = stat_df[stat] * stat_df['POSS']
    mean_stat = product.sum() / stat_df['POSS'].sum()
    return mean_stat


def get_cum_stats_any(df, x=None, n=None, laker_only=False, team=False):
        """
        Returns player's cumulative stats throughout season. /
        Can specify last x games/or n days and also whether to include all stats or laker only
        Parameters:
            x_games: if set, gets cum stats last x games; default=None
            n_days: if set, gets cum stats last n days; default=None
        """
        if (x != None) & (n != None):
            raise ValueError("Can only specify either x games or n days, not both!")
        
        # define stats
        if laker_only:
            df = df[df['TEAM_ABBREVIATION'] == 'LAL']

            
        # drop games with 0 minutes played:
        df = df[~df['MIN'].isna()].reset_index().drop(columns=("index"))
                    
        last_date = df['GAME_DATE'].iloc[-1]
        
        # filter last x games if x specified
        if x != None:
            if type(x) != int:
                raise TypeError("Invalid Value Type. Must be int")
            idx_first = df.shape[0] - x
            if idx_first < 0:
                idx_first = 0
            df = df.iloc[idx_first:]
            
        # filter last n days if n specified
        elif n != None:
            if type(n) != int:
                raise TypeError("Invalid Value Type. Must be int")
            date_dt = dt.datetime.strptime(last_date, "%Y-%m-%d")
            date_dt_first = date_dt - dt.timedelta(days=n)
            date_first = dt.datetime.strftime(date_dt_first, "%Y-%m-%d")
            df = df[df['GAME_DATE'] > date_first]
            
        
        # drop columns that are not cumulative
        drop_columns = ['GAME_ID', 'TEAM_ID', 'TEAM_ABBREVIATION', 'TEAM_CITY',
                        'PLAYER_ID', 'PLAYER_NAME', 'FG_PCT', 'FG3_PCT', 'FT_PCT',
                        'GAME_DATE', 'MATCHUP', 'WL', 'TM_TOV_PCT']
        
        df = df.drop(columns=drop_columns)
        
        
        
        # filter our advanced columns that use special mean function
        adv_cols = list(df.columns[16:36])
        remove = ['AST_TOV', 'NET_RATING', 'E_NET_RATING', 'POSS']
        adv_cols = [x for x in adv_cols if x not in remove]
        
        
        # calculate mean traditional stats
        totals = df.sum(axis=0)
        totals['GAMES'] = df.shape[0]
        totals['FG_PCT'] = totals.FGM / totals.FGA
        totals['FG3_PCT'] = totals.FG3M / totals.FG3A
        totals['FT_PCT'] = totals.FTM / totals.FTA
        
        # calculate mean advanced stats
        for col in adv_cols:
            totals[col] = gmas(col, df)
            
            
        # calc remaining adv stats
        totals.NET_RATING = totals.OFF_RATING - totals.DEF_RATING
        totals.E_NET_RATING = totals.E_OFF_RATING - totals.E_DEF_RATING
        totals.AST_TOV = totals.AST / totals.TO
        
        
        # format data and return
        for i in totals.index:
            if "PCT" in i:
                totals.loc[i] = totals.loc[i] * 100
            elif i == "PIE":
                totals.loc[i] = totals.loc[i] * 100
        return totals.round(1)
    
    
def get_per_game_stats_any(df, x=None, n=None, laker_only=False, team=False):
    cum_stats = get_cum_stats_any(df=df, x=x, n=n, laker_only=laker_only)

    divide_col_index = list(cum_stats.index[:16])
    divide_col_index.append("POSS") 
    divide_col_index.append("MIN") 

    for idx in divide_col_index:
        name = idx + "_PG"
        cum_stats[name] = cum_stats[idx] / cum_stats.GAMES
        cum_stats.drop(index=idx, inplace=True)

    per_game = cum_stats

    return per_game.round(1)

def get_per_m_minutes_stats_any(df, m=36, x=None, n=None, laker_only=False, team=False):
    cum_stats = get_cum_stats_any(df=df, x=x, n=n)

    divide_col_index = list(cum_stats.index[:16])
    divide_col_index.append("POSS") 
    divide_col_index.append("MIN") 
    total_min = cum_stats.MIN

    for idx in divide_col_index:
        name = idx + "_P{}M".format(m)
        cum_stats[name] = cum_stats[idx] / total_min * m
        cum_stats.drop(index=idx, inplace=True)

    per_minutes = cum_stats

    return per_minutes.round(1)
        
def get_per_p_possessions_stats_any(df, p=100, x=None, n=None, laker_only=False, team=False):
    cum_stats = get_cum_stats_any(df=df, x=x, n=n)

    divide_col_index = list(cum_stats.index[:16])
    divide_col_index.append("POSS") 
    divide_col_index.append("MIN") 
    total_poss = cum_stats.POSS

    for idx in divide_col_index:
        name = idx + "_P{}P".format(p)
        cum_stats[name] = cum_stats[idx] / total_poss * p
        cum_stats.drop(index=idx, inplace=True)

    per_possessions = cum_stats

    return per_possessions.round(1)

def get_cum_stats_any_team(df, x=None, n=None):
    if (x != None) & (n != None):
            raise ValueError("Can only specify either x games or n days, not both!")
    # get last date
    last_date = df['GAME_DATE'].iloc[-1]

    # filter last x games if x specified
    if x != None:
        if type(x) != int:
            raise TypeError("Invalid Value Type. Must be int")
        idx_first = df.shape[0] - x
        if idx_first < 0:
            idx_first = 0
        df = df.iloc[idx_first:]

    # filter last n days if n specified
    elif n != None:
        if type(n) != int:
            raise TypeError("Invalid Value Type. Must be int")
        date_dt = dt.datetime.strptime(last_date, "%Y-%m-%d")
        date_dt_first = date_dt - dt.timedelta(days=n)
        date_first = dt.datetime.strftime(date_dt_first, "%Y-%m-%d")
        df = df[df['GAME_DATE'] > date_first]

    # drop columns that are not cumulative
    drop_columns = ['GAME_DATE', 'MATCHUP', 'WL', 'W', 'L', 'W_PCT',
                   'GAME_ID', 'TEAM_NAME', 'TEAM_ID', 'TEAM_ABBREVIATION',
                    'TEAM_CITY', 'FG_PCT', 'FG3_PCT', 'FT_PCT',
                   ]
    df = df.drop(columns=drop_columns)

    # filter our advanced columns that use special mean function
    adv_cols = list(df.columns[17:])
    remove = ['AST_TOV', 'NET_RATING', 'E_NET_RATING', 'POSS']
    adv_cols = [x for x in adv_cols if x not in remove]


    # calculate mean traditional stats
    totals = df.sum(axis=0)
    totals['GAMES'] = df.shape[0]
    totals['FG_PCT'] = totals.FGM / totals.FGA
    totals['FG3_PCT'] = totals.FG3M / totals.FG3A
    totals['FT_PCT'] = totals.FTM / totals.FTA

    # calculate mean advanced stats
    for col in adv_cols:
        totals[col] = gmas(col, df)

    # calc remaining adv stats
    totals.NET_RATING = totals.OFF_RATING - totals.DEF_RATING
    totals.E_NET_RATING = totals.E_OFF_RATING - totals.E_DEF_RATING
    totals.AST_TOV = totals.AST / totals.TO

    for i in totals.index:
        if "PCT" in i:
            totals.loc[i] = totals.loc[i] * 100
        elif i == "PIE":
            totals.loc[i] = totals.loc[i] * 100


    return totals.round(1)
    
def get_per_game_stats_any_team(df, x=None, n=None):
    cum_stats = get_cum_stats_any_team(df=df, x=x, n=n)

    divide_col_index = list(cum_stats.index[:17])
    divide_col_index.append("POSS")

    for idx in divide_col_index:
        name = idx + "_PG"
        cum_stats[name] = cum_stats[idx] / cum_stats.GAMES
        cum_stats.drop(index=idx, inplace=True)

    per_game = cum_stats

    return per_game.round(1)
        
def get_per_p_possessions_stats_any_team(df, p=100, x=None, n=None):
    cum_stats = get_cum_stats_any_team(df=df, x=x, n=n)

    divide_col_index = list(cum_stats.index[:17])
    divide_col_index.append("POSS")
    total_poss = cum_stats.POSS

    for idx in divide_col_index:
        name = idx + "_P{}P".format(p)
        cum_stats[name] = cum_stats[idx] / total_poss * p
        cum_stats.drop(index=idx, inplace=True)

    per_possessions = cum_stats

    return per_possessions.round(1)

class TeamDate():
    """
    Create team date object. Note this is only valid for the 2022-23 season and only teams \
    where Laker players played on during the season. 
    """
    # set data path
    path = "nba_data/"
    
    def __init__(self, abb, date="2023-04-10"):
        self._set_abb(abb)
        self._set_date(date)
        self._set_stats(abb, date)
        self._set_common_info(abb)
        self._set_full_name()
        self._set_current_seed()
        self.id = load_json_file("teams.json", path=path)[abb]['id']
        self.game_ids = load_json_file("teams.json", path=path)[abb]['game_ids']
    
    def _set_abb(self, abb):
        if abb in load_json_file("teams.json", path=path).keys():
            self.abb = abb
        else:
            raise ValueError("Invalid Team Abbreviation, try again")
        
    def _set_date(self, date):
        match = re.findall(r"\d{4}-\d{2}-\d{2}", date)
        if len(match) == 1:
            if date < "2022-10-18":
                self.date = "beginning"
            else:
                self.date = date
        else:
            raise ValueError("Invalid Date Format; must be '%Y-%m-%d'")
        
    def _set_stats(self, abb, date):
        if self.date == "beginning":
            self.stats = "Date is prior to season started and therefore no stats exist"
            
        else:
            stats = pd.read_csv(path + "full_team_data_{}.csv".format(abb),
                                index_col=0,
                                parse_dates=['GAME_DATE'])
            stats['GAME_ID'] = '00' + stats['GAME_ID'].astype(str) 
            self.stats = stats[stats['GAME_DATE'] <= self.date]
            self.stats['MIN'] = [int(x[:3]) for x in self.stats['MIN']]
        
    def _set_common_info(self, abb):
        tic_df = pd.read_csv(path + "common_team_info.csv", index_col=0)
        ci = tic_df[tic_df['TEAM_ABBREVIATION'] == self.abb]
        
        self.common_info = ci
        
    def _set_full_name(self):
        ci = self.common_info
        full_name = ci['TEAM_CITY'] + " " + ci['TEAM_NAME']
        self.full_name = full_name[0]        
        
    def _set_current_seed(self):
        seeding = pd.read_csv(path + "seedings_data_{}.csv".format(self.abb), index_col=0)
        ci = self.common_info
        conf = ci['TEAM_CONFERENCE'].values[0]
        if self.date < '2022-10-18':
            self.current_seed = "No current seed! Season hasn't started!"
        elif self.date > '2023-04-09':
            team_seeding = seeding[seeding['DATE'] == '2023-04-09']
            seed = team_seeding.RANK.values[0]
            self.current_seed = conf + " Seed " + str(seed)
        else:
            team_seeding = seeding[seeding['DATE'] == self.date]
            seed = team_seeding.RANK.values[0]
            self.current_seed = conf + " Seed " + str(seed)
        
    def get_record(self, x=None, n=None):
        """
        Returns current record or record over last x games or record over last n days.
        """
        # make sure both x and n are not specified
        if (x != None) & (n != None):
            raise ValueError("Can only specify either x games or n days, not both!")
        
        stats=self.stats
        
        if x != None:
            if type(x) != int:
                raise TypeError("Invalid number, must be int")
                
            idx_first = stats.shape[0] - x
            if idx_first < 0:
                idx_first = 0
            stats = stats.iloc[idx_first:]
            
            wins = 0
            losses = 0
            for i, row in stats.iterrows():
                if row.WL == 'W':
                    wins += 1
                else:
                    losses += 1
            return "{}-{}".format(wins, losses)
        
        elif n != None:
            if type(n) != int:
                raise TypeError("Invalid number, must be int")
            
            date_dt = dt.datetime.strptime(self.date, "%Y-%m-%d")
            date_dt_first = date_dt - dt.timedelta(days=n)
            date_first = dt.datetime.strftime(date_dt_first, "%Y-%m-%d")
            stats = stats[stats['GAME_DATE'] > date_first]
            print(stats.shape[0])
            
            if len(stats) == 0:
                raise ValueError("No Data available between selected dates")
            
            wins = 0
            losses = 0
            for i, row in stats.iterrows():
                if row.WL == 'W':
                    wins += 1
                else:
                    losses += 1
            return "{}-{}".format(wins, losses)
        
        else:
            if self.date == "beginning":
                return "0-0"
            if self.date >= "2023-04-09":
                return "43-39"
            date = find_nearest_date(self.stats, 'GAME_DATE', self.date)
            row = self.stats[self.stats['GAME_DATE'] == date]
            return "{}-{}".format(row.W.values[0], row.L.values[0])
        
    def current_streak(self):
        if self.date == "beginning":
            return "W0"
        else:
            stats = self.stats
            
            stats = stats.sort_values('GAME_DATE', ascending=False)
            row1 = stats.iloc[0]
            win_or_loss = row1.WL
            streak = 0
            
            for _, row in stats.iterrows():
                if (win_or_loss == 'W') & (row.WL == 'W'):
                    streak += 1
                elif (win_or_loss == 'L') & (row.WL == 'L'):
                    streak += 1
                else:
                    break
            return win_or_loss + str(streak)
        
    def get_cum_stats(self, x=None, n=None):
        """
        Returns team's cumulative stats throughout season. Can specify last x games/or n days
        Parameters:
            x_games: if set, gets cum stats last x games; default=None
            n_days: if set, gets cum stats last n days; default=None
        """
        # make sure both x and n are not specified
        if (x != None) & (n != None):
            raise ValueError("Can only specify either x games or n days, not both!")
        
        # define stats
        stats = self.stats
        
        # filter last x games if x specified
        if x != None:
            if type(x) != int:
                raise TypeError("Invalid Value Type. Must be int")
            idx_first = stats.shape[0] - x
            if idx_first < 0:
                idx_first = 0
            stats = stats.iloc[idx_first:]
            
        # filter last n days if n specified
        elif n != None:
            if type(n) != int:
                raise TypeError("Invalid Value Type. Must be int")
            date_dt = dt.datetime.strptime(self.date, "%Y-%m-%d")
            date_dt_first = date_dt - dt.timedelta(days=n)
            date_first = dt.datetime.strftime(date_dt_first, "%Y-%m-%d")
            stats = stats[stats['GAME_DATE'] > date_first]
        
        # drop columns that are not cumulative
        drop_columns = ['GAME_DATE', 'MATCHUP', 'WL', 'W', 'L', 'W_PCT',
                       'GAME_ID', 'TEAM_NAME', 'TEAM_ID', 'TEAM_ABBREVIATION',
                        'TEAM_CITY', 'FG_PCT', 'FG3_PCT', 'FT_PCT',
                       ]
        stats = stats.drop(columns=drop_columns)
        
        # filter our advanced columns that use special mean function
        adv_cols = list(stats.columns[17:])
        remove = ['AST_TOV', 'NET_RATING', 'E_NET_RATING', 'POSS']
        adv_cols = [x for x in adv_cols if x not in remove]
        
        
        # calculate mean traditional stats
        totals = stats.sum(axis=0)
        totals['GAMES'] = stats.shape[0]
        totals['FG_PCT'] = totals.FGM / totals.FGA
        totals['FG3_PCT'] = totals.FG3M / totals.FG3A
        totals['FT_PCT'] = totals.FTM / totals.FTA
        
        # calculate mean advanced stats
        for col in adv_cols:
            totals[col] = gmas(col, stats)
        
        # calc remaining adv stats
        totals.NET_RATING = totals.OFF_RATING - totals.DEF_RATING
        totals.E_NET_RATING = totals.E_OFF_RATING - totals.E_DEF_RATING
        totals.AST_TOV = totals.AST / totals.TO
        
        for i in totals.index:
            if "PCT" in i:
                totals.loc[i] = totals.loc[i] * 100
            elif i == "PIE":
                totals.loc[i] = totals.loc[i] * 100
                
                
        return totals.round(1)
    
    def get_per_game_stats(self, x=None, n=None):
        cum_stats = self.get_cum_stats(x=x, n=n)
        
        divide_col_index = list(cum_stats.index[:17])
        divide_col_index.append("POSS")
        
        for idx in divide_col_index:
            name = idx + "_PG"
            cum_stats[name] = cum_stats[idx] / cum_stats.GAMES
            cum_stats.drop(index=idx, inplace=True)
        
        per_game = cum_stats
        
        return per_game.round(1)
        
    
    def get_per_m_minutes_stats(self, m=240, x=None, n=None):
        cum_stats = self.get_cum_stats(x=x, n=n)
        
        divide_col_index = list(cum_stats.index[:17])
        divide_col_index.append("POSS")
        total_min = cum_stats.MIN
        
        for idx in divide_col_index:
            name = idx + "_P{}M".format(m)
            cum_stats[name] = cum_stats[idx] / total_min * m
            cum_stats.drop(index=idx, inplace=True)
        
        per_minutes = cum_stats
        
        return per_minutes.round(1)
        
    def get_per_p_possessions_stats(self, p=100, x=None, n=None):
        cum_stats = self.get_cum_stats(x=x, n=n)
        
        divide_col_index = list(cum_stats.index[:17])
        divide_col_index.append("POSS")
        total_poss = cum_stats.POSS
        
        for idx in divide_col_index:
            name = idx + "_P{}P".format(p)
            cum_stats[name] = cum_stats[idx] / total_poss * p
            cum_stats.drop(index=idx, inplace=True)
        
        per_possessions = cum_stats
        
        return per_possessions.round(1)
    
    def get_trending_pg(self, x=10, x_comp=10, n=None, n_comp=None, full_szn=True):
        ### get latest stats ###
        stats = self.stats
        per_game = self.get_per_game_stats(x=x, n=n)
        
        
        if x != None:
            # get full comp group
            idx_first = stats.shape[0] - x
            if idx_first < 0:
                idx_first = 0
            comp = stats.iloc[:idx_first]
            
            if full_szn:
                x_comp=None
            comp_pg = get_per_game_stats_any_team(comp, x=x_comp)
            
        else:
            date_dt = dt.datetime.strptime(self.date, "%Y-%m-%d")
            date_dt_first = date_dt - dt.timedelta(days=n)
            date_first = dt.datetime.strftime(date_dt_first, "%Y-%m-%d")
            comp = stats[stats['GAME_DATE'] <= date_first]
            
            if full_szn:
                n_comp=None
                
            comp_pg = get_per_game_stats_any_team(comp, n=n_comp)
        
        ### compare groups and return groups and comp ###
        diff = (per_game.values - comp_pg.values) / comp_pg.values * 100
        diff = pd.DataFrame(diff, index=comp_pg.index, columns=['PERCENT_DIFF'])
        diff['RAW_DIFF'] = (per_game.values - comp_pg.values)
        
        return diff, per_game, comp_pg
    
    def get_trending_p100(self, x=10, x_comp=10, n=None, n_comp=None, full_szn=True):
        ### get latest stats ###
        stats = self.stats
        per100 = self.get_per_p_possessions_stats(x=x, n=n, p=100)
        
        if x != None:
            # get full comp group
            idx_first = stats.shape[0] - x
            if idx_first < 0:
                idx_first = 0
            comp = stats.iloc[:idx_first]
            
            if full_szn:
                x_comp=None
            comp_p100 = get_per_p_possessions_stats_any_team(comp, x=x_comp, p=100)
            
        else:
            date_dt = dt.datetime.strptime(self.date, "%Y-%m-%d")
            date_dt_first = date_dt - dt.timedelta(days=n)
            date_first = dt.datetime.strftime(date_dt_first, "%Y-%m-%d")
            comp = stats[stats['GAME_DATE'] <= date_first]
            
            if full_szn:
                n_comp=None
            comp_p100 = get_per_p_possessions_stats_any_team(comp, n=n_comp, p=100)
            
        
        diff = (per100.values - comp_p100.values) / comp_p100.values * 100
        diff = pd.DataFrame(diff, index=comp_p100.index, columns=['PERCENT_DIFF'])
        diff['RAW_DIFF'] = (per100.values - comp_p100.values)
        
        return diff, per100, comp_p100
        
        

class PlayerDate():
    # set data path
    path = "nba_data/"
    def __init__(self, name, date="2023-04-10"):
        self._set_name(name)
        self._set_date(date)
        self._set_pid()
        self._set_transactions()
        self._set_acquired()
        self._set_moved()
        self._set_waived()
        self._set_signed()
        self._set_traded_away()
        self._set_traded_for()
        self._set_other_teams()
        self._set_common_info()
        self._set_stats()
        self._set_laker_stats()
        self._set_non_laker_stats()

    def _set_name(self, name):
        if name in load_json_file("players.json", path=path).keys():
            self.name = name
        else:
            raise ValueError("Invalid player name, try again")
    
    def _set_date(self, date):
        match = re.findall(r"\d{4}-\d{2}-\d{2}", date)
        if len(match) == 1:
            if date < "2022-10-18":
                self.date = "beginning"
            else:
                self.date = date
        else:
            raise ValueError("Invalid Date Format; must be '%Y-%m-%d'")
            
    def _set_pid(self):
        players = load_json_file("players.json", path=path)
        self.pid = players[self.name]
    
    def _set_transactions(self):
        transactions = load_json_file("transactions.json", path=path)
        if self.name not in transactions.keys():
            self.transactions = None
        else:
            self.transactions = transactions[self.name]
    
    def _set_acquired(self):
        if self.transactions == None:
            self.acquired = False
        elif self.transactions['date_acquired'] == None:
            self.acquired = False
        else:
            self.acquired = self.transactions['date_acquired']
            
    def _set_moved(self):
        if self.transactions == None:
            self.moved = False
        elif self.transactions['date_moved'] == None:
            self.moved = False
        else:
            self.moved = self.transactions['date_moved']
            
    def _set_waived(self):
        if self.transactions == None:
            self.waived= False
        elif self.transactions['waived'] == False:
            self.waived = False
        else:
            self.waived = "Waived on {}".format(self.moved)
    
    def _set_signed(self):
        if self.transactions == None:
            self.signed= False
        elif self.transactions['signed'] == False:
            self.signed = False
        else:
            self.signed = "Signed on {}".format(self.acquired)
    
    def _set_traded_away(self):
        if self.transactions == None:
            self.traded_away = False
        elif self.transactions['traded_away'] == False:
            self.traded_away = False
        else:
            self.traded_away = "Traded on {}".format(self.moved)
    
    def _set_traded_for(self):
        if self.transactions == None:
            self.traded_for= False
        elif self.transactions['traded_for'] == False:
            self.traded_for = False
        else:
            self.traded_for = "Traded for on {}".format(self.acquired)
    
    def _set_other_teams(self):
        if self.transactions == None:
            self.other_teams = False
        else:
            self.other_teams = self.transactions['other_teams']
      
    def _set_common_info(self):
        pic_df = pd.read_csv(path + "common_player_info.csv", index_col=0)
        ci = pic_df[pic_df['PERSON_ID'] == self.pid]
        self.common_info = ci
        
    def _set_stats(self):
        if self.date == "beginning":
            self.stats = "Date is prior to season started and therefore no stats exist"
        else:
            stats = pd.read_csv(path + "player_total_total.csv",
                                index_col=0,
                                parse_dates=['GAME_DATE'])
            stats = stats.sort_values('GAME_DATE')
            stats = stats[stats['PLAYER_ID'] == self.pid].reset_index().drop(columns=('index'))
            stats = stats.drop(columns=['Game_ID', 'Team_ID', 'PACE_PER40'])
            self.stats = stats
        
    def _set_laker_stats(self):
        if self.transactions == None:
            self.laker_stats = self.stats
        else:
            stats = self.stats
            laker_stats = stats[stats['TEAM_ABBREVIATION'] == 'LAL']
            self.laker_stats = laker_stats.reset_index().drop(columns=('index'))
            
    def _set_non_laker_stats(self):
        if self.transactions == None:
            self.non_laker_stats = None
        
        else:
            stats = self.stats
            non_laker_stats = stats[stats['TEAM_ABBREVIATION'] != 'LAL']
            self.non_laker_stats = non_laker_stats
            
    def get_cum_stats(self, x=None, n=None, laker_only=False):
        """
        Returns player's cumulative stats throughout season. /
        Can specify last x games/or n days and also whether to include all stats or laker only
        Parameters:
            x_games: if set, gets cum stats last x games; default=None
            n_days: if set, gets cum stats last n days; default=None
        """
        if (x != None) & (n != None):
            raise ValueError("Can only specify either x games or n days, not both!")
        
        # define stats
        if laker_only:
            stats = self.laker_stats
        else:
            stats = self.stats
            
        # drop games with 0 minutes played:
        stats = stats[~stats['MIN'].isna()].reset_index().drop(columns=("index"))
        
        # filter last x games if x specified
        if x != None:
            if type(x) != int:
                raise TypeError("Invalid Value Type. Must be int")
            idx_first = stats.shape[0] - x
            if idx_first < 0:
                idx_first = 0
            stats = stats.iloc[idx_first:]
            
        # filter last n days if n specified
        elif n != None:
            if type(n) != int:
                raise TypeError("Invalid Value Type. Must be int")
            date_dt = dt.datetime.strptime(self.date, "%Y-%m-%d")
            date_dt_first = date_dt - dt.timedelta(days=n)
            date_first = dt.datetime.strftime(date_dt_first, "%Y-%m-%d")
            stats = stats[stats['GAME_DATE'] > date_first]
            
        
        # drop columns that are not cumulative
        drop_columns = ['GAME_ID', 'TEAM_ID', 'TEAM_ABBREVIATION', 'TEAM_CITY',
                        'PLAYER_ID', 'PLAYER_NAME', 'FG_PCT', 'FG3_PCT', 'FT_PCT',
                        'GAME_DATE', 'MATCHUP', 'WL', 'TM_TOV_PCT']
        
        stats = stats.drop(columns=drop_columns)

        # filter our advanced columns that use special mean function
        adv_cols = list(stats.columns[16:36])
        remove = ['AST_TOV', 'NET_RATING', 'E_NET_RATING', 'POSS']
        adv_cols = [x for x in adv_cols if x not in remove]

        # calculate mean traditional stats
        totals = stats.sum(axis=0)
        totals['GAMES'] = stats.shape[0]
        totals['FG_PCT'] = totals.FGM / totals.FGA
        totals['FG3_PCT'] = totals.FG3M / totals.FG3A
        totals['FT_PCT'] = totals.FTM / totals.FTA
        
        # calculate mean advanced stats
        for col in adv_cols:
            totals[col] = gmas(col, stats)

        # calc remaining adv stats
        totals.NET_RATING = totals.OFF_RATING - totals.DEF_RATING
        totals.E_NET_RATING = totals.E_OFF_RATING - totals.E_DEF_RATING
        totals.AST_TOV = totals.AST / totals.TO

        # format data and return
        for i in totals.index:
            if "PCT" in i:
                totals.loc[i] = totals.loc[i] * 100
            elif i == "PIE":
                totals.loc[i] = totals.loc[i] * 100
        return totals.round(1)

    def get_per_game_stats(self, x=None, n=None, laker_only=False):
        cum_stats = self.get_cum_stats(x=x, n=n, laker_only=laker_only)
        
        divide_col_index = list(cum_stats.index[:16])
        divide_col_index.append("POSS") 
        divide_col_index.append("MIN") 
        
        for idx in divide_col_index:
            name = idx + "_PG"
            cum_stats[name] = cum_stats[idx] / cum_stats.GAMES
            cum_stats.drop(index=idx, inplace=True)
        
        per_game = cum_stats
        
        return per_game.round(1)
    
    def get_per_m_minutes_stats(self, m=36, x=None, n=None, laker_only=False):
        cum_stats = self.get_cum_stats(x=x, n=n)
        divide_col_index = list(cum_stats.index[:16])
        divide_col_index.append("POSS") 
        divide_col_index.append("MIN") 
        total_min = cum_stats.MIN
        
        for idx in divide_col_index:
            name = idx + "_P{}M".format(m)
            cum_stats[name] = cum_stats[idx] / total_min * m
            cum_stats.drop(index=idx, inplace=True)
        
        per_minutes = cum_stats
        
        return per_minutes.round(1)
        
    def get_per_p_possessions_stats(self, p=100, x=None, n=None, laker_only=False):
        cum_stats = self.get_cum_stats(x=x, n=n)
        
        divide_col_index = list(cum_stats.index[:16])
        divide_col_index.append("POSS") 
        divide_col_index.append("MIN") 
        total_poss = cum_stats.POSS
        
        for idx in divide_col_index:
            name = idx + "_P{}P".format(p)
            cum_stats[name] = cum_stats[idx] / total_poss * p
            cum_stats.drop(index=idx, inplace=True)
        
        per_possessions = cum_stats
        
        return per_possessions.round(1)
    
    def get_trending_pg(self, x=10, x_comp=10, n=None, n_comp=None, laker_only=False, full_szn=True):
        ### get latest stats ###
        per_game = self.get_per_game_stats(x=x, n=n, laker_only=laker_only)
        
        if laker_only:
            stats = self.laker_stats
        else:
            stats = self.stats
        
        ### get compare group stats for x games ###
        if x != None:
            # get full comp group
            idx_first = stats.shape[0] - x
            if idx_first < 0:
                idx_first = 0
            comp = stats.iloc[:idx_first]
            
            if full_szn:
                x_comp=None
            
            comp_pg = get_per_game_stats_any(comp, x=x_comp)
                
        ### get compare group stats for n days ###      
        else:
            # get full comp group
            date_dt = dt.datetime.strptime(self.date, "%Y-%m-%d")
            date_dt_first = date_dt - dt.timedelta(days=n)
            date_first = dt.datetime.strftime(date_dt_first, "%Y-%m-%d")
            comp = stats[stats['GAME_DATE'] <= date_first]
            
            if full_szn:
                n_comp=None
            
            comp_pg = get_per_game_stats_any(comp, n=n_comp)
            
        
        ### compare groups and return groups and comp ###
        diff = (per_game.values - comp_pg.values) / comp_pg.values * 100
        diff = pd.DataFrame(diff, index=comp_pg.index, columns=['PERCENT_DIFF'])
        diff['RAW_DIFF'] = (per_game.values - comp_pg.values)
        
        return diff, per_game, comp_pg
               
    def get_trending_p36(self, x=10, x_comp=10, n=None, n_comp=None, laker_only=False, full_szn=True):
        ### get latest stats ###
        per36 = self.get_per_m_minutes_stats(x=x, n=n, laker_only=laker_only, m=36)
        
        if laker_only:
            stats = self.laker_stats
        else:
            stats = self.stats
    
        ### get compare group stats for x games ###
        if x != None:
            # get full comp group
            idx_first = stats.shape[0] - x
            if idx_first < 0:
                idx_first = 0
            comp = stats.iloc[:idx_first]
            
            if full_szn:
                x_comp=None
            
            comp_p36 = get_per_m_minutes_stats_any(comp, x=x_comp, m=36)
                
        ### get compare group stats for n days ###      
        else:
            # get full comp group
            date_dt = dt.datetime.strptime(self.date, "%Y-%m-%d")
            date_dt_first = date_dt - dt.timedelta(days=n)
            date_first = dt.datetime.strftime(date_dt_first, "%Y-%m-%d")
            comp = stats[stats['GAME_DATE'] <= date_first]
            
            if full_szn:
                n_comp=None
            
            comp_p36 = get_per_m_minutes_stats_any(comp, n=n_comp, m=36)

        ### compare groups and return comp ###
        diff = (per36.values - comp_p36.values) / comp_p36.values * 100
        diff = pd.DataFrame(diff, index=comp_p36.index, columns=['PERCENT_DIFF'])
        diff['RAW_DIFF'] = (per36.values - comp_p36.values)
        
        return diff, per36, comp_p36
    
    def get_trending_p100(self, x=10, x_comp=10, n=None, n_comp=None, laker_only=False, full_szn=True):
        ### get latest stats ###
        per100 = self.get_per_p_possessions_stats(x=x, n=n, laker_only=laker_only, p=100)
        
        if laker_only:
            stats = self.laker_stats
        else:
            stats = self.stats
        
        ### get compare group stats for x games ###
        if x != None:
            # get full comp group
            idx_first = stats.shape[0] - x
            if idx_first < 0:
                idx_first = 0
            comp = stats.iloc[:idx_first]
            
            if full_szn:
                x_comp=None
            
            comp_p100 = get_per_p_possessions_stats_any(comp, x=x_comp, p=100)
                
        ### get compare group stats for n days ###      
        else:
            # get full comp group
            date_dt = dt.datetime.strptime(self.date, "%Y-%m-%d")
            date_dt_first = date_dt - dt.timedelta(days=n)
            date_first = dt.datetime.strftime(date_dt_first, "%Y-%m-%d")
            comp = stats[stats['GAME_DATE'] <= date_first]
            
            if full_szn:
                n_comp=None
            
            comp_p100 = get_per_p_possessions_stats_any(comp, n=n_comp, p=100)            
        
        ### compare groups and return comp ###
        diff = (per100.values - comp_p100.values) / comp_p100.values * 100
        diff = pd.DataFrame(diff, index=comp_p100.index, columns=['PERCENT_DIFF'])
        diff['RAW_DIFF'] = (per100.values - comp_p100.values)
        
        return diff, per100, comp_p100   
    
    def get_trend_lal_non_lal_pg(self, x=10, xcomp=10, n=None, n_comp=None, full_szn_lal=True, full_szn_other=True):
        """
        Compare laker vs non-laker stats per game. Can compare last x games or n days of each.
        """
        # get lalppg
        if full_szn_lal:
            pglal = self.get_per_game_stats(laker_only=True)
            
        else:
            pglal = self.get_per_game_stats(x=x, n=n, laker_only=True)
            
        # get comp group
        nonlal = self.non_laker_stats
        
        if full_szn_other:
            comp = get_per_game_stats_any(nonlal)
        else:
            comp = get_per_game_stats_any(nonlal, x=xcomp, n=n_comp)
            
        ### compare groups and return groups and comp ###
        diff = (pglal.values - comp.values) / comp.values * 100
        diff = pd.DataFrame(diff, index=comp.index, columns=['PERCENT_DIFF'])
        diff['RAW_DIFF'] = (pglal.values - comp.values)
        
        return diff, pglal, comp
             
    def get_trend_lal_non_lal_p36(self, x=10, xcomp=10, n=None, n_comp=None, full_szn_lal=True, full_szn_other=True):
        """
        Compare laker vs non-laker stats per 36 min. Can compare last x games or n days of each.
        """
        # get lalp36
        if full_szn_lal:
            p36lal = self.get_per_m_minutes_stats(laker_only=True, m=36)
        else:
            p36lal = self.get_per_m_minutes_stats(x=x, n=n, laker_only=True, m=36)
            
        # get comp group
        nonlal = self.non_laker_stats
        
        if full_szn_other:
            comp = get_per_m_minutes_stats_any(nonlal, m=36)
        else:
            comp = get_per_m_minutes_stats_any(nonlal, x=x_comp, n=n_comp, m=36)
            
            
        ### compare groups and return groups and comp ###
        diff = (p36lal.values - comp.values) / comp.values * 100
        diff = pd.DataFrame(diff, index=comp.index, columns=['PERCENT_DIFF'])
        diff['RAW_DIFF'] = (p36lal.values - comp.values)
        
        return diff, p36lal, comp
                
    def get_trend_lal_non_lal_p100(self, x=10, xcomp=10, n=None, n_comp=None, full_szn_lal=True, full_szn_other=True):
        """
        Compare laker vs non-laker stats per 100 poss. Can compare last x games or n days of each.
        """
        # get lalp100
        if full_szn_lal:
            p100lal = self.get_per_p_possessions_stats(laker_only=True, p=100)
        else:
            p100lal = self.get_per_p_possessions_stats(x=x, n=n, laker_only=True, p=100)
        
        # get comp group
        nonlal = self.non_laker_stats
        
        if full_szn_other:
            comp = get_per_p_possessions_stats_any(nonlal, p=100)
        else:
            comp = get_per_p_possessions_stats_any(nonlal, x=x_comp, n=n_comp, p=100)
    
        ### compare groups and return groups and comp ###
        diff = (p100lal.values - comp.values) / comp.values * 100
        diff = pd.DataFrame(diff, index=comp.index, columns=['PERCENT_DIFF'])
        diff['RAW_DIFF'] = (p100lal.values - comp.values)
        
        return diff, p100lal, comp

    
    
    
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    