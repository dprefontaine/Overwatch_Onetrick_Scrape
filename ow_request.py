from over_json import overjson
import pandas as pd
import random
from ow_scrape import OwNameScrape
from time import strptime
from urllib.error import HTTPError


##FOR MAIN AND ARGUMENTS
import sys as s
import getopt as go

def main(argv):
	##for checking arguments
	argument_flag = True
	
	##ARGUMENTS SHOULD GO AS:
	##
	##ow_request.py -h -r (region name here) -pl (platform) -pa (pages) -max (max_one_trickers)
	##
	
	##argument variables
	region = 'en-us'
	platform = 'pc'
	pages = 1
	max_one_trickers = 100
	
	##random.randint(1,101)
	opts = None
	args = None
	
	##TESTING OUT THE ARGUMENTS
	try:
		opts, args = go.getopt(argv,"hi:o:",["region=","platform=","pages=","max_one_trickers="])
	except go.GetoptError:
		print("ERROR: arguments must be ow_request.py -h -r (region name here) -pl (platform) -pa (pages) -max (max_one_trickers)")
		argument_flag = False
	
	for opt, argument in opts:
			if (opt == '-h'):
				##PRINT OUT HELP
				print('ow_request.py -h -r (region name here) -pl (platform) -pa (pages) -max (max_one_trickers)')
			elif (opt == "-r"):
				region = argument
			elif (opt == "-pl"):
				platform = argument
			elif (opt == "-pa"):
				pages = argument
			elif (opt == "-max"):
				max_one_trickers = argument
				
	##DO THE FUNCTION IF ARGUMENTS ARE PROPER
	if argument_flag:
		##CRAWL THROUGH A BUNCH OF USERNAMES FIRST

		names = OwNameScrape(pages)

		##DO WHILE EITHER ONE-TRICKERS OR NOT ARE NOT SATISFIED YET (COUNT: 100)
		one_tricker_count = 0
	
		one_tricker_dataframe = pd.DataFrame(columns = ['Player', 'Winrate', 'AvgEliminations', 'AvgDeaths', 'TimeOnFire'])
		generalist_dataframe = pd.DataFrame(columns = ['Player', 'Winrate', 'AvgEliminations', 'AvgDeaths', 'TimeOnFire'])


		for name in names:
			if (one_tricker_count >= max_one_trickers):
				break
				
			try:
				player_obs = overjson(region, platform, name)
			
				##if (max_one_trickers > one_tricker_count and max_generalists > generalist_count):
				##    player_obs = overpy(region, platform, 'Player-1234')
			
				##SEE IF THEY QUALIFY FOR SURVEYING BY BEING OVER SOME PRESTIGE AND ARE PUBLIC
				if(player_obs["prestige"] >= 2 and not player_obs["private"] and player_obs["competitiveStats"]["games"]["played"] > 10):
					
					##IDEA HERE IS GET THE PROPORTIONS, AND IF ANY HERO GOES OVER 80, CONSIDERED ONE TRICKER
					hours = 0
					minutes = 0
					seconds = 0
					timeQuantity = 0
					timeList = []
					timeTotal = 0
					timeTest = False
					
					for hero, stats in player_obs["competitiveStats"]["topHeroes"].items():
						##print(stats["timePlayed"])
						try:
							hours, minutes, seconds = tuple(map(int, stats["timePlayed"].split(':')))
						except ValueError:
							try:
								hours = 0
								minutes, seconds = tuple(map(int, stats["timePlayed"].split(':')))
							except ValueError:
								hours = 0
								minutes = 0
								seconds = 0
						finally:
							timeQuantity = hours + minutes/60 + seconds/360
							timeList.append(timeQuantity)
							##print(timeQuantity)
					
					for i in timeList:
						timeTotal += i
						
					for j in timeList:
						##print(j/timeTotal)
						if j/timeTotal >= 0.6:
							timeTest = True
					
					if (timeTest):
						print("One Tricker Found")
						
						one_tricker_count += 1
						winrate = (player_obs["competitiveStats"]["games"]["won"] / player_obs["competitiveStats"]["games"]["played"])
						eliminations = (player_obs["competitiveStats"]["careerStats"]["allHeroes"]["combat"]["eliminations"]/player_obs["competitiveStats"]["games"]["played"])
						deaths = (player_obs["competitiveStats"]["careerStats"]["allHeroes"]["combat"]["deaths"]/player_obs["competitiveStats"]["games"]["played"])
						
						##processing timeOnFire
						timeOnFire = player_obs["competitiveStats"]["careerStats"]["allHeroes"]["combat"]["timeSpentOnFire"]
						timeOnFireQuantity = None
						tofHours = None
						tofMinutes = None
						tofSeconds = None
						
						try:
							tofHours, tofMinutes, tofSeconds = tuple(map(int, timeOnFire.split(':')))
						except ValueError:
							try:
								tofHours = 0
								tofMinutes, tofSeconds = tuple(map(int, timeOnFire.split(':')))
							except ValueError:
								tofHours = 0
								tofMinutes = 0
								tofSeconds = 0
						finally:
							timeOnFireQuantity = tofHours + tofMinutes/60 + tofSeconds/360
							##print(timeQuantity)
						
						#now append
						one_tricker_dataframe = one_tricker_dataframe.append({'Player': name, 'Winrate': winrate, 'AvgEliminations': eliminations, 'AvgDeaths': deaths, 'TimeOnFire': timeOnFireQuantity/player_obs["competitiveStats"]["games"]["played"]}, ignore_index=True)
					else:
						print("Generalist Found")
						
						winrate = (player_obs["competitiveStats"]["games"]["won"] / player_obs["competitiveStats"]["games"]["played"])
						eliminations = (player_obs["competitiveStats"]["careerStats"]["allHeroes"]["combat"]["eliminations"]/player_obs["competitiveStats"]["games"]["played"])
						deaths = (player_obs["competitiveStats"]["careerStats"]["allHeroes"]["combat"]["deaths"]/player_obs["competitiveStats"]["games"]["played"])
						
						##processing timeOnFire
						timeOnFire = player_obs["competitiveStats"]["careerStats"]["allHeroes"]["combat"]["timeSpentOnFire"]
						timeOnFireQuantity = None
						tofHours = None
						tofMinutes = None
						tofSeconds = None
						
						try:
							tofHours, tofMinutes, tofSeconds = tuple(map(int, timeOnFire.split(':')))
						except ValueError:
							try:
								tofHours = 0
								tofMinutes, tofSeconds = tuple(map(int, timeOnFire.split(':')))
							except ValueError:
								tofHours = 0
								tofMinutes = 0
								tofSeconds = 0
						finally:
							timeOnFireQuantity = tofHours + tofMinutes/60 + tofSeconds/360
							##print(timeQuantity)
							
						generalist_dataframe = generalist_dataframe.append({'Player': name, 'Winrate': winrate, 'AvgEliminations': eliminations, 'AvgDeaths': deaths, 'TimeOnFire': timeOnFireQuantity/player_obs["competitiveStats"]["games"]["played"]}, ignore_index=True)
						
						
					##TO SEE IF THEYRE A ONE TRICKER, THEY MUST HAVE AT LEAST 80% OF THEIR
					##PLAY TIME IN ONE HERO
					
					
					##TO DO THIS, HOURS WILL BE PARSED FOR THEIR HERO LIST, AND IF A HERO IS
					##OF 80% OR SOME THRESHOLD, THEY WILL BE CLASSIFIED AS A ONE TRICKER
			except HTTPError:
					print("Not found...")
					
		print(one_tricker_count)

		one_tricker_dataframe.to_csv("one_trickers.csv", index = None)
		generalist_dataframe.to_csv("generalists.csv", index = None)
	else:
		s.exit(2)
	
if __name__ == "__main__":
	main(s.argv[9:])