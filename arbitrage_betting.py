#Things to do:
#- Bet365 class
#- if bets empty then remove game Betway 
#- open all drop down menus tab: event-list__event-header__sport-name

import selenium 
import os
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time 
import re

driver = webdriver.Chrome('/Users/allyhassell/.wdm/drivers/chromedriver/mac64/103.0.5060.53/chromedriver')

class TAB:
    '''TAB class calculations and objects'''
    
    def __init__(self):
        '''Initialising'''
        
    def driver_setup(self, sport):
        '''Driver url'''
        sports_number = {'american-football' : 3, 'australian-rules' : 5, 'baseball' : 7, 'basketball' : 8, 'boxing' : 11, 'cricket' : 12, 'cycling' : 14, 'darts' : 15, 'football': 16, 'golf': 17, 'hockey': 20, 'ice-hockey': 21, 'mixed-martial-arts': 22, 'motor-racing': 23, 'motorcycling':24, 'netball': 25, 'rugby-league': 26, 'rugby-union': 27, 'snooker': 30, 'surfing': 34, 'table-tennis':36, 'tennis':37, 'volleyball': 40}
        number = sports_number[sport]
        driver.get(f'https://www.tab.co.nz/sport/{number}/{sport}/matches')
        time.sleep(30) 
         
       
    def teams(self):
        '''Names and odds of games'''
        web_teams = driver.find_elements_by_xpath("//*[@class='heading__no-grouping' or @class='button--outcome__text-title']")
        web_teams = [element.text for element in web_teams if element.text != '' and element.text != 'Over' and element.text != 'Under' and element.text != 'Draw']
        '''Remove any games not reasonably far in the future'''
        if len(web_teams) > 1:
            i = 0
            terminate = False
            future_days = ['Tomorrow', 'Later', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            teams_future = []
            while terminate == False and i < len(web_teams):
                if web_teams[i] in future_days:
                    teams_future = web_teams[i:]
                    terminate = True
                i += 1
            if len(teams_future) == 0:
                teams = []
            else:            
                teams = [team for team in teams_future if team not in future_days and team != 'Outrights & Futures']
        else:
            teams = []
        return teams
    
    def odds(self, sport):
        '''Odds from website'''
        web_odds = driver.find_elements_by_xpath("//*[@class='heading__no-grouping' or @class='button--outcome__price']")
        web_odds = [element.text for element in web_odds if element.text != '']
        '''Remove any games not reasonably far in the future'''
        if len(web_odds) > 1:
            i = 0
            terminate = False
            future_days = ['Tomorrow', 'Later', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            odds_future = []
            while terminate == False and i < len(web_odds):
                if web_odds[i] in future_days:
                    odds_future = web_odds[i:]
                    terminate = True
                i += 1
            if len(odds_future) == 0:
                all_odds = []
            else:
                all_odds = [odd for odd in odds_future if odd not in future_days and odd != 'Outrights & Futures']
            '''Where on the site the odds are located'''
            if sport in ['american-football', 'australian-rules', 'rugby-league', 'table-tennis']:
                index_odds1 = [i*6 for i in range(0,20)]
                index_odds2 = [i*6+1 for i in range(0,20)]
            elif sport in ['boxing', 'football', 'hockey', 'rugby-union', 'snooker']:
                index_odds1 = [i*3 for i in range(0,20)]
                index_odds2 = [i*3+2 for i in range(0,20)]
            elif sport in ['darts', 'mixed-martial-arts', 'tennis']:
                index_odds1 = [i*2 for i in range(0,20)]
                index_odds2 = [i*2+1 for i in range(0,20)]
            else:
                index_odds1 = [i*2 for i in range(0,20)]
                index_odds2 = [i*2+1 for i in range(0,20)]            
            index_odds = sorted(index_odds1 + index_odds2)
            odds = []
            for index in range(0, len(all_odds)):
                if index in index_odds:
                    odds.append(all_odds[index])
        else:
            odds = []
        return odds
    
    def dictionary(self, sport):
        '''TAB sport dict'''
        self.driver_setup(sport)
        teams = self.teams()
        odds = self.odds(sport)   
        game_dict = {}
        if len(teams) >= len(odds):
            short_len = len(odds)
        elif len(odds) > len(teams):
            short_len = len(teams)
        for i in range(0, short_len, 2):
            team1 = teams[i]
            team2 = teams[i+1]
            both_teams = [team1, team2]
            sorted_teams = sorted(both_teams)
            odds1 = odds[i]
            odds2 = odds[i+1]
            game = sorted_teams[0] + ' - ' + sorted_teams[1]
            game_dict[game] = {team1 : odds1, team2: odds2}
        return game_dict
            
class Betway:
    '''Betway objects and calcs'''
    
    def __init__(self):
        '''Initialising'''
        
    def driver_setup(self, sport):
        '''Driver'''
        driver.get(f'https://betway.com/en/sports/cat/{sport}')
        time.sleep(30)  

    def teams(self, sport):
        '''Names and odds of games'''
        web_hometeams = driver.find_elements_by_xpath("//*[@class='teamNameFirstPart teamNameHomeTextFirstPart smallFont' or @class='teamNameFirstPart teamNameHomeTextFirstPart' or @class='titleText']")
        web_awayteams = driver.find_elements_by_xpath("//*[@class='teamNameFirstPart teamNameAwayTextFirstPart smallFont' or @class='teamNameFirstPart teamNameAwayTextFirstPart'or @class='titleText']")
        teams1 = [element.text for element in web_hometeams]
        teams2 = [element.text for element in web_awayteams]
        web_teams = []
        for i in range(0, len(teams1)):
            web_teams.append(teams1[i])
            web_teams.append(teams2[i])
        '''Remove any games not reasonably far in the future'''
        if len(web_teams) > 1:
            i = 0
            terminate = False
            future_days = ('Tomorrow', 'Mon', 'Tue', 'Wed', 'Thur', 'Fri', 'Sat', 'Sun')
            teams_future = []
            while terminate == False and i < len(web_teams):
                if web_teams[i].startswith(future_days):
                    teams_future = web_teams[i:]
                    terminate = True
                i += 1
            if len(teams_future) == 0:
                teams = []
            else:
                teams_future = [team for team in teams_future if team.startswith(future_days) ==  False]
                teams = [re.sub('(B.C.)', 'British Columbia', team) for team in teams_future]
        else:
            teams = []
        return teams
    
    def odds(self, sport):
        '''Odds in list'''
        web_odds = driver.find_elements_by_xpath("//*[@class='titleText' or @class='odds' or @class='button']")
        web_odds = [element.text for element in web_odds if element != '']
        more_bets_indexes = [i+1 for i in range(0, len(web_odds)) if web_odds[i] == 'More Bets']
        web_odds = [re.sub('More Bets', '0', odd) for odd in web_odds]
        for index_toadd in more_bets_indexes:
            web_odds.insert(index_toadd, '0')
        web_odds = [element for element in web_odds if element != '']
        '''Remove any games not reasonably far in the future'''
        if len(web_odds) > 1:
            i = 0
            terminate = False
            future_days = ('Tomorrow', 'Mon', 'Tue', 'Wed', 'Thur', 'Fri', 'Sat', 'Sun')
            odds_future = []
            while terminate == False and i < len(web_odds):
                if web_odds[i].startswith(future_days):
                    odds_future = web_odds[i:]
                    terminate = True
                i += 1
            if len(odds_future) == 0:
                all_odds = []
            else:
                all_odds = [odd for odd in odds_future if str(odd).startswith(future_days) ==  False]
            '''Where on the site the odds are found'''
            if sport in ['football', 'basketball']:
                index_odds1 = [i*3 for i in range(0,20)]
                index_odds2 = [i*3+2 for i in range(0,20)]
            elif sport in ['tennis', 'baseball']:
                index_odds1 = [i*2 for i in range(0,20)]
                index_odds2 = [i*2+1 for i in range(0,20)]        
            index_odds = sorted(index_odds1 + index_odds2)
            odds = []
            for index in range(0, len(all_odds)):
                if index in index_odds:
                    odds.append(all_odds[index])
        else:
            odds = []
        return odds    
    
    def dictionary(self, sport):
        '''Betway sport dict'''
        self.driver_setup(sport)
        teams = self.teams(sport)
        odds = self.odds(sport)
        game_dict = {}
        if len(teams) >= len(odds):
            short_len = len(odds)
        elif len(odds) > len(teams):
            short_len = len(teams)
        for i in range(0, short_len, 2):
            team1 = teams[i]
            team2 = teams[i+1]
            both_teams = [team1, team2]
            sorted_teams = sorted(both_teams)                  
            odds1 = odds[i]
            odds2 = odds[i+1]
            game = sorted_teams[0] + ' - ' + sorted_teams[1]
            game_dict[game] = {team1 : odds1, team2: odds2}
        return game_dict
    
class Bet365:
    '''Bet365 objects and calcs'''
    
    def __init__(self):
        '''Initialising'''
        
    def driver_setup(self, sport):
        '''Driver url'''
        sports_number = {'basketball' : 'B18', 'football': 'B1', 'ice-hockey': 'B17', 'tennis':'B13'}
        number = sports_number[sport]
        driver.get(f'https://www.bet365.com/#/AS/{number}/')
        time.sleep(30) 
        
    def teams(self):
        '''Names and odds of games'''
        web_leagues = driver.find_elements_by_xpath("//*[@class='sm-SplashMarketGroupButton_Text ']")
        leagues = [element.text for element in web_leagues]
        game_lines = driver.find_elements_by_xpath("//*[@class='sm-CouponLink ']")
        print(game_lines)
        all_teams = []
        print(leagues)
        for i in range(0, len(leagues)):
            game_lines[i].click()
            web_teams = driver.find_elements_by_xpath("//*[@class='hscb-ParticipantFixtureDetailsHigherBasketball_Team ' or @class='rcl-MarketHeaderLabel rcl-MarketHeaderLabel-isdate']")  
            web_teams = [element.text for element in web_teams]
            print(web_teams)
            '''Remove any games not reasonably far in the future'''
            if len(web_teams) > 1:
                i = 0
                terminate = False
                future_days = ('Tomorrow', 'Mon', 'Tue', 'Wed', 'Thur', 'Fri', 'Sat', 'Sun')
                teams_future = []
                while terminate == False and i < len(web_teams):
                    if web_teams[i].startswith(future_days):
                        teams_future = web_teams[i:]
                        terminate = True
                    i += 1
                print(teams_future)
                if len(teams_future) == 0:
                    teams = []
                else:
                    teams_future = [team for team in teams_future if team.startswith(future_days) ==  False]
            else:
                teams = []
            all_teams.append(teams)
        return all_teams

    
    def odds(self, sport):
        '''Odds from website'''
        web_odds = driver.find_elements_by_xpath("//*[@class='heading__no-grouping' or @class='button--outcome__price']")
        web_odds = [element.text for element in web_odds if element.text != '']
        '''Remove any games not reasonably far in the future'''
        if len(web_odds) > 1:
            i = 0
            terminate = False
            future_days = ['Tomorrow', 'Later', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            odds_future = []
            while terminate == False and i < len(web_odds):
                if web_odds[i] in future_days:
                    odds_future = web_odds[i:]
                    terminate = True
                i += 1
            if len(odds_future) == 0:
                all_odds = []
            else:
                all_odds = [odd for odd in odds_future if odd not in future_days and odd != 'Outrights & Futures']
            '''Where on the site the odds are located'''
            if sport in ['american-football', 'australian-rules', 'rugby-league', 'table-tennis']:
                index_odds1 = [i*6 for i in range(0,20)]
                index_odds2 = [i*6+1 for i in range(0,20)]
            elif sport in ['boxing', 'football', 'hockey', 'rugby-union', 'snooker']:
                index_odds1 = [i*3 for i in range(0,20)]
                index_odds2 = [i*3+2 for i in range(0,20)]
            elif sport in ['darts', 'mixed-martial-arts', 'tennis']:
                index_odds1 = [i*2 for i in range(0,20)]
                index_odds2 = [i*2+1 for i in range(0,20)]
            else:
                index_odds1 = [i*2 for i in range(0,20)]
                index_odds2 = [i*2+1 for i in range(0,20)]            
            index_odds = sorted(index_odds1 + index_odds2)
            odds = []
            for index in range(0, len(all_odds)):
                if index in index_odds:
                    odds.append(all_odds[index])
        else:
            odds = []
        return odds
    
    def dictionary(self, sport):
        '''TAB sport dict'''
        self.driver_setup(sport)
        teams = self.teams()
        odds = self.odds(sport)   
        game_dict = {}
        if len(teams) >= len(odds):
            short_len = len(odds)
        elif len(odds) > len(teams):
            short_len = len(teams)
        for i in range(0, short_len, 2):
            team1 = teams[i]
            team2 = teams[i+1]
            both_teams = [team1, team2]
            sorted_teams = sorted(both_teams)
            odds1 = odds[i]
            odds2 = odds[i+1]
            game = sorted_teams[0] + ' - ' + sorted_teams[1]
            game_dict[game] = {team1 : odds1, team2: odds2}
        return game_dict
            
class Calculations:
    '''Calculations'''
    
    def __init__(self, sites, sports, site_sports, site_classes):
        '''Initialsiing'''
        self.sites = sites
        self.sports = sports
        self.site_sports = site_sports
        self.site_classes = site_classes
        
    def bet_dict(self):
        '''Bet dictionary'''
        site_sports = self.site_sports
        site_classes = self.site_classes
        sports = self.sports
        bet_dict = {}
        for sport in sports:
            bet_dict[sport] = {}
            for website in self.sites:
                if website == 'Betway' and sport == 'australian-rules':
                    site_class = site_classes[website]
                    site_dict = site_class.dictionary('aussie-rules')
                    bet_dict['australian-rules'][website] = site_dict                    
                elif sport in site_sports[website]:
                    site_class = site_classes[website]
                    site_dict = site_class.dictionary(sport)
                    bet_dict[sport][website] = site_dict
        return bet_dict
    
    def good_odds(self):
        '''Good odds'''
        bet_dict = self.bet_dict()
        sites = self.sites
        sites2 = self.sites
        sports = self.sports
        for sport in sports:
            for site in sites:
                if sport in self.site_sports[site]:
                    sport_dict = bet_dict[sport]
                    site_value = sport_dict[site]
                    for game_key, odds_value in site_value.items():
                        for team_key, odd_value in odds_value.items():
                            for site2 in sites2: 
                                if site2 != site:
                                    site_dict = sport_dict[site2]
                                    if game_key in site_dict:
                                        game = site_dict[game_key]
                                        for team_key2, odd_value2 in game.items():
                                            if team_key2 != team_key:
                                                x = float(odd_value)
                                                y = float(odd_value2)
                                                xy = x * y
                                                if x + y < xy:
                                                    print(f'Good odds: {site_key} {team_key} at {x} and {site_key2} {team_key2} at {y}.')
                    

def main():
    '''Main function which calls calculations and classes'''
    '''Sites'''
    sites = ['TAB', 'Betway']
    '''Sports'''
    sports_suggested = ['basketball', 'football', 'ice-hockey', 'tennis']
    sports = ['football']
    '''Sports by site'''
    tab_sports = ['basketball', 'football', 'ice-hockey', 'tennis']
    betway_sports = ['basketball', 'football', 'ice-hockey', 'tennis']
    site_sports = {'TAB' : tab_sports, 'Betway': betway_sports}
    '''Classes'''
    site_classes = {'TAB': TAB(), 'Betway': Betway()}    
    '''Calculations'''
    calcs = Calculations(sites, sports, site_sports, site_classes)
    calcs.good_odds()

main()

        