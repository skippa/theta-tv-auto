#!/bin/python

from operator import itemgetter
from os import getxattr
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from datetime import datetime
import random

options = Options()
options.binary_location = '/usr/bin/brave'
#options.add_argument("--no-sandbox")
driver_path = '/usr/local/bin/chromedriver'
drvr = webdriver.Chrome(options = options, executable_path = driver_path)

drvr.set_page_load_timeout(90)


def loginTheta():
    drvr.get("http://theta.tv")
    wait = WebDriverWait(drvr, 30)
    #click login link
    loginLink = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "header-login")))
    loginLink.click()

    #find email input
    wait = WebDriverWait(drvr, 30)
    inputEmail = wait.until(EC.visibility_of_element_located((By.TAG_NAME, "input")))
    #input email
    inputEmail.send_keys("cmskipsey@gmail.com")
    #find password input
    inputPassword = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@type='password']")))
    #input password
    inputPassword.send_keys("13klarica")

    loginLink = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "login-btn")))
    loginLink.click()
    time.sleep(5)


def getMostViewedChannel():
    drvr.get("http://theta.tv/discover")

    wait = WebDriverWait(drvr, 30)
    
    liveChannels = wait.until(EC.visibility_of_element_located((By.ID, "react-tabs-0")))
    liveChannels.click()

    
    thetaChannels = []
    channels = []
    viewCounts = []
    channelNames = []

    #channelCards = wait.until(EC.visibility_of_any_elements_located((By.CLASS_NAME, "g-channel-card")))
    
    for channel in wait.until(EC.visibility_of_any_elements_located((By.CLASS_NAME, "g-channel-card"))):
        channels.append(channel)
        
    for viewCount in wait.until(EC.visibility_of_any_elements_located((By.CLASS_NAME, "count"))):
        viewCounts.append(int(viewCount.text))

    for channelName in wait.until(EC.visibility_of_any_elements_located((By.CLASS_NAME, "username"))):
        channelNames.append(channelName.text)

    i = 0
    

    while (i < len(channels)):
        thetaChannels.append({"URL": channels[i], "viewCount": viewCounts[i], "channelName": channelNames[i]})
        i+=1

    thetaChannelsSorted = []
    thetaChannelsSorted = sorted(thetaChannels, key=itemgetter('viewCount'), reverse=True)


    #drvr.get(thetaChannelsSorted[0]["URL"])

    return(thetaChannelsSorted[0]["URL"], thetaChannelsSorted[0]["viewCount"], thetaChannelsSorted[0]["channelName"])


def getCurrentViewers():
    wait = WebDriverWait(drvr, 30)
    currentViewers = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "count")))
    currentChannelName = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "username")))
    return int(currentViewers.text), currentChannelName.text.upper()


def switchTab(index):
    drvr.switch_to.window(drvr.window_handles[index])

loginTheta()
mostViewedChannel = getMostViewedChannel()[0]

mostViewedChannel.click()


#got to most viewed channel
#drvr.get(getMostViewedChannel())

#open new tab
drvr.execute_script("window.open('');")
switchTab(0)

timeLastCheck = time.time()

while True:
    timeNow = time.time()
    if timeNow - timeLastCheck > 10: #every 1 min
        print(datetime.now())
        #switch to tab
        switchTab(1)
        #get latest channel stats
        try:
            channelInfo = getMostViewedChannel()
            mostViewedChannel = channelInfo[0]
            mostViewedChannelviewCount = channelInfo[1]
            mostViewedChannelName = channelInfo[2]
            print("Most Viewed Channel ", mostViewedChannelName)
            print("Most Viewed Channel viewCount ", mostViewedChannelviewCount, "\n")
        except:
            print("timeout getting most viewed channels")

        #go back to main tab
        switchTab(0)
        #wait
        time.sleep(5)
        #get current channel info
        try:
            currentInfo = getCurrentViewers()
            currentViewers = currentInfo[0]
            currentChannelName = currentInfo[1]
            print("Current Channel ", currentChannelName)
            if currentChannelName != mostViewedChannelName:
                try:
                    getMostViewedChannel()[0].click()
                except:
                    print("error loading mostViewedChanenl")

            print("Current viewCount ", currentViewers, "\n")
        except:
            print("timeout getting current channel info")
            getMostViewedChannel()[0].click()


        timeLastCheck = time.time()        

        timeLastCheck = time.time()


# g-tfuel-wallet click
# class = label -> text is "Peers" then next class=value text is number of peers
