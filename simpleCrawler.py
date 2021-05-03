# Website change finder v0.4.2
# created by Anhat Singh
# Last modified: 09:15:00 18/12/2020
#
# Simple Python Program to find if anything has changed at all on a website, automatically after a set amount of time.
# Primary use: To check if things have changed on gndu Online Website
# Primary drawback: currently only works on PC and in windows enviornment, will add support later
#
# Requirements:
# Python 3.x+
# The following libraries installed: requests, time, sys, hashlib, datetime, argparse, colorama, urllib.request, bs4
#
# If you want to know its working, try running it on your PC with CMD
# If you want to contribute to this program, feel free to message me
#
# To use it, in cmd type the following after fulfilling the above requirements:
# py Crawler.py url <your_website_url> -t <time in seconds> -a <max number of attempts> -sh <boolean; whether to show debug info or not>
#
# if you only type py Crawler.py without any arguements, it defaults to the following parameters.
#
defaultUrl = "http://online.gndu.ac.in/"            # The URL of the page where we have to detect changes
defaultTimeInterval = 1                             # Time Interval in seconds for re-checking
defaultNumberOfAttempts = 120                       # Maximum number of times to check the webpage
defaultWhetherToShowHashAndPercent = False          # Sometimes program misses the changes on a page, this will show debug info side-by-side on the pc

# =================================================================================================================================================================================================================================================
# Importing all the libraries required
import requests, time, sys, hashlib, datetime, argparse
from colorama import init
init(autoreset=True)
from urllib.request import urlopen
from bs4 import BeautifulSoup
from colorama import Fore, Back, Style
# =================================================================================================================================================================================================================================================
#
# get the arguements from the user, if no arguements, it will default to above declared variables.
#
parser = argparse.ArgumentParser(description='Website')
parser.add_argument('url', metavar='url', type=str, help='Webpage Address to check for changes',nargs='?', default=defaultUrl)
parser.add_argument('-t', metavar='seconds',nargs='?', type=int, help='Time in seconds before re-checking the page (default = '+ str(defaultTimeInterval) +' sec)', default=defaultTimeInterval)
parser.add_argument('-a', metavar='number_of_attempts',nargs='?', type=int, help='Number of Attempts to check (default = '+str(defaultNumberOfAttempts)+')', default=defaultNumberOfAttempts)
parser.add_argument('-sh', metavar='True',nargs='?', type=bool, help='(True/False) Whether to show Hash values and percent change (default = '+str(defaultWhetherToShowHashAndPercent)+')', default=defaultWhetherToShowHashAndPercent)

# parse_args() simply gives us the args as an object, assign args to different variables.
# This can be shortened, as i have used this for backwards compatibility!
args = parser.parse_args()
url = str(args.url)
sleepTime = int(args.t)
numberOfAttempts = int(args.a)


# To give a general estimate of the time it will take to run our commands, it test-runs the benchmark, simply makes 1 crawl to website, and notes the approx time and gives us that.
global lineToPrint
def connect(host=url):
    try:
        try:
            urlopen(host, timeout=5)
            return True
        except:
            return False
    except KeyboardInterrupt:
        pass

def timeToFetchResult():
    start = time.time()
    testConnection = connect()
    if(testConnection):
        response1 = requests.get(url).text
        stripHtml1 = BeautifulSoup(response1, "lxml").text
        hashOfHtml1 = hashlib.md5(stripHtml1.encode('utf-16')).hexdigest()
    end = time.time()
    if(testConnection):
        return ((end - start)*2) + 0.75
    else:
        return int(-1)


# Simple messages to show to user
    
print("\n====================================================================================================================")
print("Website Change Finder v0.4.2")
print("created by Anhat Singh")
print("Last modified: 09:15:00 18/12/2020")
print("====================================================================================================================", end = "\n\n")
print("Webpage to Check: \t\t" + Back.WHITE + Fore.RED + " " + url + "\t\t\t\t\t\t")
print("Interval before check: \t\t" + Back.WHITE + Fore.RED + " " + str(sleepTime) + " seconds" + "\t\t\t\t\t\t\t")
print("Total Attempts to perform: \t" + Back.WHITE + Fore.RED + " " + str(numberOfAttempts) + "\t\t\t\t\t\t\t\t")
print("Show detailed attempt: \t\t" + Back.WHITE + Fore.RED + " " + (str(args.sh) if args.sh != None else "True") + "\t\t\t\t\t\t\t\t")
print("Please wait.... Establishing Connection", end = "\r")
print("Estimated Program Run-time: \t" + Back.WHITE + Fore.RED + " " + str(datetime.timedelta(seconds=round(defaultNumberOfAttempts*(defaultTimeInterval + timeToFetchResult())))) + " (H:m:s), finishing at [" +time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time() + defaultNumberOfAttempts*(defaultTimeInterval + timeToFetchResult())))+ "]\t\t", end="\n\n")

#actual code starts here, will update it's working later.

x = 1
try:
    while x <= numberOfAttempts:
        x = x + 1
        getTheTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print("Attempt " + str(x - 1) + " ["+ str(getTheTime) +"]: "+Fore.BLUE+"Establishing Connection", end="\r")
        if(connect()):
            print("Attempt " + str(x - 1) + " ["+ str(getTheTime) +"]: Connection Established... "+Fore.BLUE+"Fetching First Copy", end="\r")
            #response1 = urlopen(url).read().decode('utf-8')
            response1 = requests.get(url).text
            stripHtml1 = BeautifulSoup(response1, "lxml").text
            hashOfHtml1 = hashlib.md5(stripHtml1.encode('utf-16')).hexdigest()
            #time.sleep(sleepTime)
            for i in range(int(sleepTime),0,-1):
                print ("Attempt " + str(x - 1) + " ["+ str(getTheTime) +"]: First Copy Fetched...." + Fore.BLUE + "Waiting " + Fore.YELLOW + str(datetime.timedelta(seconds=i)) + Fore.BLUE + " Hours" + Fore.RESET + " for second copy", end = "\r")
                #sys.stdout.write(str(i)+' ')
                #sys.stdout.flush()
                time.sleep(1)
            #response2 = urlopen(url).read().decode('utf-8')
            print ("Attempt " + str(x - 1) + " ["+ str(getTheTime) +"]: Wait Time Over...."+Fore.BLUE+"Fetching the second copy                        ", end = "\r")
            if(connect()):
                pass
            else:
                for i2 in range(int(sleepTime),0,-1):
                    print("Attempt " + str(x - 1) + " ["+ str(getTheTime) +"]: "+Fore.RED+"Unable to establish connection " + Fore.BLUE + "Waiting " + Fore.YELLOW + str(datetime.timedelta(seconds=i2)) + Fore.BLUE + " Hours" + Fore.RESET + " to retry   ", end = "\r")
                    time.sleep(1)
                print("Attempt " + str(x - 1) + " ["+ str(getTheTime) +"]: "+Fore.RED+"Unable to establish connection                                                                                              ")
                continue
            response2 = requests.get(url).text
            stripHtml2 = BeautifulSoup(response2, "lxml").text
            hashOfHtml2 = hashlib.md5(stripHtml2.encode('utf-16')).hexdigest()
            percentChange = ((len(response2) - len(response1)) / len(response1))*100
            if (hashOfHtml1 == hashOfHtml2):
                if(args.sh == True or args.sh == None):
                    printStatement = "Attempt " + str(x - 1) + " ["+ str(getTheTime) +"]: " + Fore.GREEN + "No changes... " + Fore.RESET + "  H_1=" + hashOfHtml1 + ", H_2=" + hashOfHtml2
                else:
                    printStatement = "Attempt " + str(x - 1) + " ["+ str(getTheTime) +"]: " + Fore.GREEN + "No changes found" + Fore.RESET + "                                                  "
                print(printStatement)
                # print(percentChange)
                # time.sleep(60)
                continue

            else:
                if(args.sh == True or args.sh == None):
                    printStatement2 = Fore.RED + Back.WHITE + "Attempt " + str(x - 1) + " ["+ str(getTheTime) +"]: SOMETHING CHANGED..... R1_Len=" + str(len(response1)) + ", R2_Len="+ str(len(response2)) + ", Change=" + str(percentChange) + "%, H_1=" + hashOfHtml1 + ", H_2=" + hashOfHtml2
                else:
                    printStatement2 = Fore.RED + Back.WHITE + "Attempt " + str(x - 1) + " ["+ str(getTheTime) +"]: SOMETHING CHANGED " + Back.RESET + "                                                     "
                print(printStatement2)
                #print(percentChange)
                continue
            continue
        else:
            for i3 in range(int(sleepTime),0,-1):
                print("Attempt " + str(x - 1) + " ["+ str(getTheTime) +"]: "+Fore.RED+"Unable to establish connection " + Fore.BLUE + "Waiting " + Fore.YELLOW + str(datetime.timedelta(seconds=i3)) + Fore.BLUE + " Hours" + Fore.RESET + " to retry   ", end = "\r")
                time.sleep(1)
            print("Attempt " + str(x - 1) + " ["+ str(getTheTime) +"]: "+Fore.RED+"Unable to establish connection                                                                                              ")
            continue
except KeyboardInterrupt:
    pass

if(numberOfAttempts == x - 1):
    print("\n\nProgram Finished Successfully at " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + " time")
else:
    pass
print("\n\n")
k = input("Press Enter to Close")