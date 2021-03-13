import pandas as pd
import numpy as np
import time
from selenium import webdriver

driver = webdriver.Chrome()
link = 'https://www.cricbuzz.com/cricket-team/league'
driver.get(link)
# time.sleep(4)
element = driver.find_element_by_xpath("//div[@class = 'cb-col cb-col-100']")
string = element.text

teams_string = string.split('\n')


batsmen = list()
all_rounder = list()
wicket_keeper = list()
bowler = list()
num_of_batsmen = len(batsmen)
num_of_bowlers = len(bowler)
num_of_all_rounders = len(all_rounder)
num_of_wicket_keeper = len(wicket_keeper)
name = list()
role = list()
team = list()
hand = list()
bowl_type = list()
player_data = list()

# extracting only IPL teams data
for team_name in teams_string[:8]:
    
    bat_hand_type = ''
    bowl_type = ''
    group = 0
    
    team_link = driver.find_element_by_link_text(team_name)
    team_link.click()
    
    player_page = driver.find_element_by_link_text('Players')
    player_page.click()
    
    # getting all the players data and their roles
    player_names = driver.find_element_by_xpath('//div[@class = "cb-col-67 cb-col cb-left cb-top-zero"]')
    player_names = player_names.text
    player_names_list = player_names.split('\n')
    
    for i in player_names_list:
        if i not in ['BATSMEN', 'WICKET KEEPER', 'BOWLER' ,'ALL ROUNDER']:
            
            bowl_type = ''
            
            # clicking on the player links and getting their data
            player_info = driver.find_element_by_link_text(i)
            player_info.click()
            
            information = driver.find_element_by_xpath("//div[@class = 'cb-col cb-col-33 text-black']")
            information = information.text
                        
            if ('Left Handed Bat' in information):
                bat_hand_type = 'Left'
            else:
                bat_hand_type = 'Right'
            
            for bowling in ['Right-arm legbreak', 'Left-arm legbreak', 'Right-arm offbreak', 'Left-arm offbreak',
                'Right-arm fast', 'Left-arm fast', 'Right-arm medium', 'Left-arm medium', 
                'Right-arm fast-medium', 'Left-arm fast-medium', 'Right-arm orthodox', 'Left-arm orthodox',
                'Left-arm chinaman', 'Right-arm chinaman']:
                
                if bowling in information:
                    bowl_type = bowling
                    break
            
            information = driver.find_element_by_xpath("//div[@class = 'cb-hm-rght cb-player-bio']")
            information = information.text
            
            # getting all the statistics from the player bio
            if 'Batting Career Summary' not in information:
                
                # debut players will have no information
                batting_stats = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                bowling_stats = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            else:
                stats = list()
                count = 0
                string = information.split('\n')
                for s in string:
                    if s.startswith('IPL'):
                        count += 1
                        stats.append(s)
                        if count == 2:
                            break
                # debut player will have no information
                # this block will be used when the player has some description in the player bio
                if len(stats) != 0:
                    batting_stats = stats[0].split(' ')[1:]
                    bowling_stats = stats[1].split(' ')[1:]
                
        if i == 'BATSMEN':
            group = 1
            continue
        elif i == 'ALL ROUNDER':
            group = 2
            continue
        elif i == 'WICKET KEEPER':
            group = 3
            continue
        elif i == 'BOWLER':
            group = 4
            continue
        if group == 1:
            batsmen.append([i, team_name, bat_hand_type, bowl_type, batting_stats, bowling_stats])
        elif group == 2:
            all_rounder.append([i, team_name, bat_hand_type, bowl_type, batting_stats, bowling_stats])
        elif group == 3:
            wicket_keeper.append([i, team_name, bat_hand_type, bowl_type, batting_stats, bowling_stats])
        elif group == 4:
            bowler.append([i, team_name, bat_hand_type, bowl_type, batting_stats, bowling_stats])
            
        if i in ['BATSMEN', 'WICKET KEEPER', 'BOWLER' ,'ALL ROUNDER']:
            continue
        
        # navigate to previous page to move on to next team player
        driver.back()

            
    # go back to main page
    driver.get(link)

# structuring the data to put it in a data frame
for player in range(num_of_batsmen):
    if batsmen[player][0] != 'BATSMEN':
        temporary = list()
        temporary.extend(batsmen[player][:4])
        temporary.extend(['BATSMAN'])
        temporary.extend(batsmen[player][4])
        temporary.extend(batsmen[player][5])       
        name.append(temporary)
for player in range(num_of_bowlers):
    if bowler[player][0] != 'BOWLER':    
        temporary = list()
        temporary.extend(bowler[player][:4])
        temporary.extend(['BOWLER'])
        temporary.extend(bowler[player][4])
        temporary.extend(bowler[player][5])       
        name.append(temporary)
for player in range(num_of_wicket_keeper):
    if wicket_keeper[player][0] != 'WICKET KEEPER':    
        temporary = list()
        temporary.extend(wicket_keeper[player][:4])
        temporary.extend(['WICKET KEEPER'])
        temporary.extend(wicket_keeper[player][4])
        temporary.extend(wicket_keeper[player][5])       
        name.append(temporary)
for player in range(num_of_all_rounders):
    if all_rounder[player][0] != 'ALL ROUNDER':    
        temporary = list()
        temporary.extend(all_rounder[player][:4])
        temporary.extend(['ALL ROUNDER'])
        temporary.extend(all_rounder[player][4])
        temporary.extend(all_rounder[player][5])       
        name.append(temporary)

df = pd.DataFrame(
        name, columns=['Name', 'Team', 'Batting_Hand', 'Bowling_Type', 'Role', 'Matches','Innings', 'Not Outs', 'Runs', 'Highest', 'Average', 'BF', 'SR', '100', '200', '50', '4', '6', 'Matches', 'Innings', 'Balls', 'Runs', 'Wickets', 'BBI', 'BBM', 'Economy', 'Average', 'SR', '5W', '10W']
    )

df.to_csv('player_data.csv')