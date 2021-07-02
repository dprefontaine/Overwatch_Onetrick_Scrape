import requests
import logging

from bs4 import BeautifulSoup
import pandas as pd
import re

def OwNameScrape(iterations):
    name_data = []
    i = 1

    while i < iterations:
        ##url <- paste0("https://overwatchtracker.com/leaderboards/pc/global/CompetitiveRank?page=",paste0(i,sep=""),"mode=1") 
        url = "https://overwatchtracker.com/leaderboards/pc/en-us/CompetitiveRank?country=United States&page=" + str(i) + "&mode=1"
        soup = None
        
        ##tried specifying this more because global also introduces another variable
        pattern = re.compile(f"profile/pc/global/*")
        pattern2 = re.compile('p')
        
        ##theHTML <- tryCatch({read_html(url)}, error=function(err) "Error")
        
        try:
            html = requests.get(url)
        except Exception:
            logging.exception(f'Failed to crawl: {url}')
        finally:
            soup = BeautifulSoup(html.text, "html.parser")
        
        ##Nodes <- theHTML %>% xml_nodes("a") %>% xml_attr("href") %>% as.data.frame
        
        names = soup.find_all("a", href=pattern)
        
        ##Nodes[,1] <- as.character(Nodes[,1])
        ##Nodes_2 <- as.data.frame(matrix(NA,50,1))
        ##Nodes_2[,1] <- Nodes[grep("profile",Nodes[,1]),]
        ##Nodes_2[,1] <- sub(".*global/", "", Nodes_2[,1])
        
        ##nameframe <- rbind(nameframe, Nodes_2)
        
        if names is not None:
            for toAppend in names:
                print(toAppend['href'][19:])
                name_data.append(toAppend['href'][19:])
        
        i += 1

    return name_data