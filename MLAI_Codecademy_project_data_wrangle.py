#!/usr/bin/env python
# coding: utf-8

# In[74]:


#Consult the livescore-api.com API to obtain the LigaMX data
#The API serves a JSON file, but divides it in several pages.
#So, I have to consult how many pages it is, to go through each in order to create a single database, stored in a list called "games"
#To do this, I made a while loop that loops to each page, from 1 to "total_pages", and appends the data from each page to the "games" list.
#The database is a list of dictionaries, each containing information from each match played since 2017 for all leage matches, of all teams in the league.

import requests
import json
api_key = 'DEGlErxbRH0HdPay'
api_secret = 'BzxFxodQ03sVf8xSNedrFLDwsDdFsne4'
api_url = 'https://livescore-api.com/api-client/scores/history.json?competition_id=45&key=' + api_key + '&secret=' + api_secret
pageNum = 1
parameters = {"page": pageNum}
data_request = requests.get(api_url, params=parameters)
totalPages = data_json.get("data").get("total_pages")


games = []

while pageNum <= totalPages:
    parameters = {"page": pageNum}
    data_request = requests.get(api_url, params=parameters)
    data_json = data_request.json()
    matchData = data_json.get("data").get('match')
    for m in matchData:
        games.append(m)
    pageNum += 1
    
#Once the database is created and stored in the games list, it is time to consult only the information to be analyzed.
#First, I define the variable "team" which stores the name of the team to be analyzed.
#Then, I create two empty lists: "results" and "location".
#The for loop iterates through each match and obtains the name of the home and away teams, as well as the score of the match.
#We then assign how many goals where scored by the home team, and how many by the away team.
#Finally, we focus only on the team we're studying. If the home or away team is the team we're studying, we proceed. Else, we go to the next match.
#If our team played at home, we append "H" to the location, else we append "A".
#IF our team won, we append "W" to the results. Else, we append "T" for a Tie, or "L" for a loss.

team = "Tigres"

results = []
location = []

for game in games:
    homeTeam = game.get("home_name")
    awayTeam = game.get("away_name")
    gameScore = game.get("score")
    homeGoals = gameScore[0]
    awayGoals = gameScore[-1]
    if homeTeam == team or awayTeam == team:       
        if homeTeam == team:
            location.append("H")
            if awayGoals < homeGoals:
                results.append("W")
            elif homeGoals < awayGoals:
                results.append("L")
            else:
                results.append("T")
        elif awayTeam == team:
            location.append("A")
            if homeGoals < awayGoals:
                results.append("W")
            elif awayGoals < homeGoals:
                results.append("L")
            else:
                results.append("T")

#We now collect both lists, location and results, into a dictionary of matches
matchDict = {}
for n in range(0, (len(location)-1)):
    l = location[n]
    r = results[n]
    m = "match" + str(n+1)
    matchDict[m] = {l:r}

#And convert it to a json Object called jsonResults
jsonResults = json.dumps(matchDict, indent = 4) 

#Finally, we export the information to a new file
with open("matchResults.json", "w") as outfile:
    outfile.write(jsonResults)

#This will let me know in the console when the process is finished, so I can consult the file using a text editor.
#I will use this file in the next script, in which I will write the statistical analysis functions.
print("Done")


# In[ ]:




