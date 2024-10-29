#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import pandas as pd
import time
from bs4 import BeautifulSoup
from io import StringIO
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

years= list(range(1991,2024))
url_start='https://www.basketball-reference.com/awards/awards_{}.html'


# In[5]:


for year in years:
    url=url_start.format(year)
    data=requests.get(url)
    
    with open("mvp/{}.html".format(year), "w+",encoding='utf-8') as f:
        f.write(data.text)


# In[10]:


with open("mvp/1991.html", encoding='utf-8') as f:
    page=f.read()


# In[15]:


soup=BeautifulSoup(page,'html.parser')


# In[14]:


soup.find('tr', class_="over_header").decompose()


# In[18]:


mvp_table=soup.find(id='mvp')


# In[24]:


mvp_1991=pd.read_html(StringIO(str(mvp_table)))[0]


# In[32]:


dfs=[]
for year in years:
    with open("mvp/{}.html".format(year),encoding="utf-8") as f:
        page=f.read()
    soup=BeautifulSoup(page,'html.parser')
    soup.find('tr', class_="over_header").decompose()
    mvp_table=soup.find(id='mvp')
    mvp=pd.read_html(StringIO(str(mvp_table)))[0]
    mvp["Year"]=year
    dfs.append(mvp)


# In[33]:


mvps=pd.concat(dfs)


# In[38]:


mvps.to_csv("mvps.csv")


# In[7]:


player_stats_url="https://www.basketball-reference.com/leagues/NBA_{}_per_game.html"
url=player_stats_url.format(1991)
data=requests.get(url)
with open("player/1991.html","w+",encoding='utf-8') as f:
    f.write(data.text)


# In[ ]:


# Assuming you have defined player_stats_url and year earlier
driver = webdriver.Chrome()
year=1991
url = player_stats_url.format(year)
driver.get(url)

# Use WebDriverWait to wait for the presence of an element before scrolling
wait = WebDriverWait(driver, 10)  # Maximum wait time of 10 seconds
element_to_wait_for = wait.until(EC.presence_of_element_located((By.ID, "some_element_id")))

# Scroll to the bottom of the page
#driver.execute_script("arguments[0].scrollIntoView();", element_to_wait_for)

# If the above doesn't work, try using window.scrollTo directly
driver.execute_script("window.scrollTo(1, 10000)")

# Give some time for the scrolling to take effect
time.sleep(2)

# Continue with the rest of your code
html = driver.page_source
with open("player/{}.html".format(year),"w+", encoding='utf-8') as f:
    f.write(html)


# In[2]:


team_stats_url="https://www.basketball-reference.com/leagues/NBA_{}_standings.html"


# In[ ]:


for year in years:
    url=team_stats_url.format(year)
    data=requests.get(url)
    with open("team/{}.html".format(year), "w+",encoding="utf-8") as f:
        f.write(data.text)


# In[30]:


dfs=[]
for year in years:
    with open("team/{}.html".format(year),encoding='utf-8') as f:
        page=f.read()
    
    soup=BeautifulSoup(page,"html.parser")
    soup.find("tr", class_="thead").decompose()
    team_table=soup.find(id="divs_standings_E")
    team=pd.read_html(StringIO(str(team_table)))[0]
    team["Year"]=year
    team["Team"]=team["Eastern Conference"]
    del team['Eastern Conference']
    dfs.append(team)
    
    soup=BeautifulSoup(page,"html.parser")
    soup.find("tr", class_="thead").decompose()
    team_table=soup.find(id="divs_standings_W")
    team=pd.read_html(StringIO(str(team_table)))[0]
    team["Year"]=year
    team["Team"]=team["Western Conference"]
    del team['Western Conference']
    dfs.append(team)


# In[31]:


teams=pd.concat(dfs)


# In[32]:


teams


# In[33]:


teams.to_csv("teams.csv")

