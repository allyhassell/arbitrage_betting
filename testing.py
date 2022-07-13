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

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(chrome_options=options, executable_path='/Users/allyhassell/.wdm/drivers/chromedriver/mac64/103.0.5060.53/chromedriver')
sport = 'basketball'
sports_number = {'basketball' : 'B18', 'football': 'B1', 'ice-hockey': 'B17', 'tennis':'B13'}
number = sports_number[sport]
driver.get(f'https://www.bet365.com/#/AS/{number}/')
time.sleep(10)





web_leagues = driver.find_elements_by_xpath("//*[@class='sm-SplashMarketGroupButton_Text']")
time.sleep(10)

game_lines = driver.find_elements_by_xpath("//*[@class='sm-CouponLink_Title']")
time.sleep(10)

for i in range(0, len(web_leagues)):
    league = web_leagues[i]
    game_line = game_lines[i]
    print('made it this far')
    game_line.click()
    time.sleep(5)
    






def tab_check():
    '''Checking functions'''
    tab = TAB()
    tab.driver_setup('basketball')
    teams = tab.teams()
    odds = tab.odds('basketball')
    tab_dict = tab.dictionary('basketball')
    print(teams)
    print(odds)
    print(tab_dict)
    print(len(tab_dict))
    
def betway_check():
    '''Checking functions'''
    betway = Betway()
    betway.driver_setup('tennis')
    teams = betway.teams('tennis')
    odds = betway.odds('tennis')
    tab_dict = betway.dictionary('tennis')
    print(teams)
    print(odds)
    print(tab_dict)('american-football')
    print(tab_odds)

def check_dict():
    '''Check bet dict'''
    sites = ['TAB', 'Betway']
    sports = ['american-football', 'volleyball']
    tab_sports = ['american-football']
    betway_sports = ['american-football']
    site_sports = {'TAB' : tab_sports, 'Betway': betway_sports}
    site_classes = {'TAB':TAB(), 'Betway': Betway()}    
    calcs = Calculations(sites, sports, site_sports, site_classes)
    bet_dict = calcs.bet_dict()
    print(bet_dict)
    
def check_bet365():
    '''Check Bet365 code'''
    bet365 = Bet365()
    bet365.driver_setup('basketball')
    teams = bet365.teams()
    odds = bet365.odds('basketball')
    bet365_dict = bet365.dictionary('basketball')
    print(teams)
    print(odds)
    print(bet365_dict)
    
