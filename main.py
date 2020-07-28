import requests
from bs4 import BeautifulSoup
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
import time
import fileinput
import matplotlib.dates
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
pd.options.mode.chained_assignment = None

URL = input("Enter a Twitter link: ")


def get_data():
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    now = datetime.now()
    results = soup.find_all('strong')
    retweets = str(results[1])
    likes = str(results[2])
    retweets = retweets[8:-9]
    retweets = retweets.replace(',', '')
    retweets = int(retweets)
    likes = likes[8:-9]
    likes = likes.replace(',', '')
    likes = int(likes)
    sheet = open("data.csv", "a")
    sheet.write(now.strftime('%H:%M:%S,'))
    sheet.write("{},{},,\n".format(retweets, likes))
    sheet.close()

def display():
    choice = input("Likes or Retweets vs Time? ")
    choice = choice.upper()
    df = pd.read_csv('data.csv')
    plt.xlabel("Time")
    dates = []
    for index in range(0, len(df['Time'])):
        df['Time'][index] = datetime.strptime(df['Time'][index], "%H:%M:%S")
    if choice == "LIKES":
        plt.ylabel("Likes")
        plt.plot_date(df['Time'], df['Likes'], 'ro')
        plt.title("Likes vs Time")
    else:
        plt.ylabel("Retweets")
        plt.plot_date(df['Time'], df['Retweets'], 'o')
        plt.title("Retweets vs Time")

    plt.tick_params(axis='x', labelrotation=90, labelsize=6)
    plt.show()
def mine():
    secs = input('How many seconds between gets? (seconds) ')
    while True:
        print('Getting Data...')
        get_data()
        time.sleep(int(secs))
def smooth_data():
    lines = []
    for line in open("data.csv"):
        if line == "Time,Retweets,Likes,,\n":
            lines.append(line)
            continue
        if len(lines) == 0:
            lines.append(line)
            continue
        prev = lines[-1]
        one = prev.index(",")
        two = prev.index(",", 1)
        three = prev.index(",", two+1)
        prev_num = prev[two+1:three]
        one = line.index(",")
        two = line.index(",", 1)
        three = line.index(",", two+1)
        num = line[two+1:three]
        if prev_num != num:
            lines.append(line)
    f = open("data.csv", "w")
    for line in lines:
        f.write(line)
    f.close()

def clear():
    choice = input("Are you sure? This will delete all existing data and is irreversible. (y/n) ")
    if choice.lower() == "n":
        return
    f = open("data.csv", "w")
    f.write("Time,Retweets,Likes,,\n")
    f.close()

while True:
    action = input('What would you like to do? [MINE, SMOOTH, DISPLAY, GET, CLEAR, EXIT] ')
    action = action.upper()
    print(action)
    if action == 'DISPLAY':
        display()
    if action == 'MINE':
        mine()
    if action == 'GET':
        get_data()
    if action == 'SMOOTH':
        smooth_data()
    if action == 'CLEAR':
        clear()
    if action == 'EXIT':
        break
