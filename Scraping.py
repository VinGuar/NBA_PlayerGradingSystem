import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrapeURL(player1, season1):

    #remove punctuation for full name
    def nopunct(word):

        punctuations = '''!()-[];:'"\,<>./?@#$%^&*_~'''

        no_punct = ""
        for char in word:
            if char not in punctuations:
                no_punct = no_punct + char

        return no_punct

    player1 = nopunct(player1)

    #creating first and last name variables for player
    names = player1.split()
    firstName = names[0]
    lastName = names[1]


    url = "https://www.basketball-reference.com/players/"


    #insert the player name part of the url
    url += (lastName[0].lower() + "/")
    for num in range(5):
        url += lastName[num].lower()
    for num in range (2):
        url += firstName[num].lower()

    codeNum1 = 0
    codeNum2 = 2


    url += "01.html"

    #Finding name of player to check validity
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    player_name = soup.find('h1').text
    player_name = player_name.strip()
    player_name = nopunct(player_name)

    index = url.index("01")
    
    print(player_name.lower(), player1.lower())

    #url construction with potential ability to have the same base code.
    while True:
        if player_name.lower() == player1.lower():
            break
        else:
            url = url[:index]
            url = url + str(codeNum1) + str(codeNum2) + ".html"

            #redo player name with the new url
            page = requests.get(url)
            soup = BeautifulSoup(page.content, 'html.parser')

            player_name = soup.find('h1').text
            player_name = player_name.strip()

            player_name = nopunct(player_name)

            codeNum2 += 1

            if codeNum2>5:
                break

            if (codeNum2 % 10)==0:
                codeNum1 += 1
                codeNum2 = codeNum2 - 10
    return url



def scrapeStats(url, season1):
    #Making table with soup and pandas
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    table = soup.find_all("table")
    dfs = pd.read_html(str(table))[0]
    dfs = dfs.fillna(0)

    #print(dfs.to_dict('index'))

    newDFS = dfs.to_dict('index')

    listThrees = ["MP", "FG", "FGA", "FG%", "3P", "3PA", "3P%", "2P", "2PA", "2P%", "eFG%", "FT", "FTA", "FT%", "ORB", "DRB", "TRB", "AST", "STL", "BLK", "TOV", "PF", "PTS"]

    listID = 0

    while True:
        while True:
            try:
                seas = newDFS[listID]["Season"]
            except:
                listID += 1
            else:
                break
            
            if listID>100:
                print("Error. listID too high.")
                exit()
        
        if seas == season1:
            break
        else:
            listID += 1
    

    dictionary = {}

    for stat in listThrees:
        dictionary[stat] = newDFS[listID][stat]


    #newDFS = newDFS[0]["eFG%"]

    return dictionary

#team array for url
teams = ["MIL", "BOS", "PHI", "CLE", "NYK", "BRK", "MIA", "ATL", "TOR", "WAS", "CHI", "IND", "ORL", "CHO", "DET", "DEN", "MEM", "SAC", "PHO", "GSW", "LAC", "MIN", "OKC", "DAL", "LAL", "UTA", "NOP", "POR", "SAS", "HOU"]
teams.sort()
players = []
   
def scrapeRosterURL(teamNum):
    url = "https://www.basketball-reference.com/teams/"
    url = url + teams[teamNum] + "/2023.html"
    return url

def scrapeActivePlayers():
    
    for n in range (30):

        url = scrapeRosterURL(n)

        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        table = soup.find_all("table")
        df1 = pd.read_html(str(table))[0]
        df1 = df1.fillna(0)

        df1 = df1.to_dict('index')


        for x in range(len(df1)):

            player = df1[x]["Player"]

            if " (TW)" in player:
                player = player.replace(' (TW)', '') 

            players.append(player)
            
    return players







 

