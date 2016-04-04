#! /usr/bin/python3
# Written by Joshua Jordi

# This program is designed to be a simple demonstration of a Python IRC client with SSL capabilities.
# From http://tools.ietf.org/html/rfc1459#section-3.3.2:
# The IRC protocol is a text-based protocol, with the simplest client being any socket program capable of connecting to the server.

# In its current stage, this IRC client fulfills the "simplest client" criteria. In the future, it will be updated to follow IRC client protocol and parse messages from IRC servers more cleanly.

import socket
import ssl
import os
import json
from string import punctuation
from time import sleep
from time import time
import re

# Opens settings file and reads it.
settingsFile = open("./settings.conf", "r")
config = json.loads(settingsFile.read())
settings = config['settings']

# Connections. Reads whether or not to connect through SSL. 
# Might just make it a class, but don't want to deal with it right now.
ssL=socket.socket()
ssL.connect((settings['host'], settings['port']))

if settings['ssl'] == 'yes':
    s = ssl.wrap_socket(ssL)
else:
    pass

# Sends the required stuffs to the server. Password, nickname, etc.
def connectToServer(passwd, nick, ident, host, realname):
    s.send(("PASS %s\r\n" % passwd).encode('utf-8'))
    s.send(('NICK %s\r\n' % nick).encode('utf-8'))
    s.send(('USER %s %s bla : %s\r\n' % (ident, host, realname)).encode('utf-8'))

# This simplifies sending messages. Its a pain to type in everything over and over.
def sendMessage(msg, CHAN):
    s.send(("PRIVMSG %s :%s\r\n" % (CHAN, msg)).encode('utf-8'))

    for a in logList:

        if CHAN in a:
            i = open(a, "a")
            i.write(NICK + ' | ' + msg + '\n')
            i.close()

# Prints out basic info on the bot
def info(CHAN, NICK):
    sendMessage(("I'm %s, written by JakkinStewart on GitHub (https://github.com/JakkinStewart). Right now I can dispense advice using the adviceslip.com API and insult other users with the quandyfactory insult generator. I have a simple WEP tutorial at the moment. Hopefully, I will be updated to include more tutorials.\r\n" % NICK), CHAN)

# Prints out the commands people can send to the bot.
def helpMe(CHAN):
    sendMessage(("'advice'  : Mentioning the word 'advice' to me will cause me to give you advice.\r\n"), CHAN)
    sendMessage(("'info'    : Mentioning the word 'info' to me will give general info on me. (Not much yet.)\r\n"), CHAN)
    sendMessage(("'Hello'   : Saying hi to me will make me say hi back.\r\n"), CHAN)
    sendMessage(("'help'    : Using the word 'help' with my name will give you this message.\r\n"), CHAN)
    sendMessage(("'insult'  : Saying insult to me and the nick of the person you want insulted will make me send an insulting message to them."), CHAN)
    sendMessage(("'tutorial': Saying 'tutorial' and 'wep' to me will give you a short tutorial on cracking wep with aircrack. I'm hoping to add more tutorials in the future."), CHAN)
    sendMessage(("'!ip'     : Use !ip <ip address/url> to locate an IP. Uses ip-api.com."), CHAN)
    sendMessage(("I will automatically print out the titles of any URL in the channel that I am in."), CHAN)

# Prints out a simple aircrack tutorial. Requires you to have a tutor on hand to explain it.
def aircrack(CHAN):
    sendMessage(("Aircrack-ng is a complete suite of tools to assess WiFi network Security.\r\n"), CHAN)

    sendMessage(("Requirements: WiFi card. (Can be USB, as long as Aircrack-ng can see it.) | Helpful tutor. (I haven't been coded to be helpful yet.)"), CHAN)

    sendMessage(("airmon-ng check kill"), CHAN)

    sendMessage(("airmon-ng start \x035[interface]\x03"), CHAN)

    sendMessage(("airodump-ng [interface]mon"), CHAN)

    sendMessage(("airodump-ng -c [channel] --bssid [BSSID] -w dump [interface]mon"), CHAN)

    sendMessage(("airocrack-ng --bssid [BSSID] dump-*.cap"), CHAN)

    sendMessage(("Presto! You just cracked the key!"), CHAN)

# Prints out random advice
def advice(CHAN):
    os.system("curl -s http://api.adviceslip.com/advice > .advice")
    inFile = open('.advice', 'r')
    parsed_json = json.loads(inFile.read())
    sendMessage("%s\r\n" % (parsed_json['slip']['advice']), CHAN)
    os.system('rm .advice')

# Prints out random insults
def insult(CHAN, insultee): #, insultee):
    os.system('curl -s http://quandyfactory.com/insult/json > .insult')
    inFile = open('.insult', 'r')
    jsonAttempt = inFile.read()
    parsed_json = json.loads(jsonAttempt)
    sendMessage('%s, %s ' % (insultee, parsed_json['insult']), CHAN)
    os.system('rm .insult')

# Detects if a url is present and returns true if they are
def urls(message):
    url = message
    urlHttp = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', url)
    urlWWW = re.findall('www.(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', url)

    if urlHttp != []:
        urlList.append(urlHttp)

    elif urlWWW != []:
        urlList.append(urlWWW)

    if urlList != []:
        return True

    else:
        return False

# Finds the title of the web page and prints it out. Trying to add a tinyurl to the title as well.
def printUrls(urls, CHAN):
    #print(urls)

    for websites in urls:

        for web in websites:
            #print(web)
            os.system("curl -s %s | grep -iPo '(?<=<title>)(.*)(?=</title>)' > .url" % web)
            inFile = open('.url')
            printUrls = inFile.read()
            tinyurl = os.system("""curl -s curl 'https://www.googleapis.com/urlshortener/v1/url?key=AIzaSyAYRyJuXmfWHgc6_lWjmJ8tpE8A932y9i8' -H 'Content-Type: application/json' -d '{"longUrl": "%s"}' > .tinyurl""" % web)
            tinyInFile = open('.tinyurl')
            jsonAttempt = tinyInFile.read()

            try:
                tinyurl = json.loads(jsonAttempt)

                if '&#x27;' in printUrls:
                    printUrls = re.sub('&#x27;', "'", printUrls)

                if '&#171;' in printUrls:
                    printUrls = re.sub('&#171;', '«', printUrls)

                if '&mdash;' in printUrls:
                    printUrls = re.sub('&mdash;', '-', printUrls)

                sendMe = '%s - %s' % (printUrls.strip(), tinyurl['id'])
                sendMessage(('^ %s ^' % sendMe), CHAN)

            except KeyError:
                pass

    del urlList[:]

# Searches ips with ip-api.com
def findIP(ips, CHAN):
    os.system('curl -s http://ip-api.com/json/%s > .ip' % ips)
    tempIPs = open('.ip', 'r')
    jsonRead = json.loads(tempIPs.read())

    if jsonRead['status'] == 'success':
        sendMessage('ISP:           %s' % jsonRead['isp'], CHAN)
        sendMessage('Country:       %s' % jsonRead['country'], CHAN)
        sendMessage('Region:        %s' % jsonRead['regionName'], CHAN)
        sendMessage('City:          %s' % jsonRead['city'], CHAN)
        sendMessage('Zipcode:       %s' % jsonRead['zip'], CHAN)
        sendMessage('Lat/Lon:       %s/%s' % (jsonRead['lat'], jsonRead['lon']), CHAN)
        sendMessage('Timezone:      %s' % jsonRead['timezone'], CHAN)
        sendMessage('Organizaton:   %s' % jsonRead['org'], CHAN)

    elif jsonRead['status'] == 'fail':
        sendMessage(jsonRead['message'], CHAN)

# Bothers Ohelig
def botherOhelig(msg, chan):
    sendMessage('%s' % msg, chan)

# Begins readbuffer.
# Taken from http://archive.oreilly.com/pub/h/1968:
# You need a readbuffer because your might not always be able to read complete IRC commands from the server (due to a saturated Internet connection, operating system limits, etc).
readbuffer=''

# Saves a debug log.
debug = "debug.log"

# Connects to server (as stated by the function name)
connectToServer(settings['pass'],
                settings['nick'],
                settings['ident'],
                settings['host'],
                settings['realname'])

# Creates empty list. Will be populated with users in the channels.
userList = []

# Forgot what this does. Will find out later.
logList = []

# Creates a counter. Don't remember what this does either.
#count = 0

# Sets nick to user's selected nickname
NICK = settings['nick']

# Makes a counter. Counter used to seperate channels into seperate lists. Makes life easier.
counter = 0

# Counts how many channels. Makes a list of users with these channels.
chanCount = -1

print("Connecting...")

# For every channel, make a <channel>.log file. Also, I found the counter thing.
for a in settings['channel']:
    counter += 1
    logList.append("%s.log" % a)

# For as many counts in the counter variable, make a list. Add users to that list. 
for i in range(counter):
    users = [] * counter
    userList.append(users)

# Here's the fun part! This part starts the infinite loop.
# The infinite loop will run certain things according to certain triggers. (No, its not a feminist.)
while 1:
    try:
        # Read 4096 bytes from the server and append it to the readbuffer.
        readbuffer=readbuffer + s.recv(4096).decode()
        temp=readbuffer.split('\n')
        readbuffer=temp.pop()

        # The program receives everything as a list. This will go through the list and allow us to manipulate it.
        # It also makes things easier to read when things are printed.
        for line in temp:
            line=line.rstrip()
            line=line.split()
            dbg = open(debug, "a")

            # Sometimes the debug writer doesn't like certain characters. So I'll just skip over them.
            # They aren't important (just things like \x02 and stuff like that).
            try:

                for i in line:
                    dbg.write(i + ' ')
                dbg.write('\n')
                dbg.close()

            except UnicodeEncodeError:
                pass

            # If the server pings, reply. (That way you don't get booted off the server.
            if line[0]=='PING':
                s.send(("PONG %s\r\n" % line[1]).encode('utf-8'))

            # If the line equals "mode", then join channels. It won't work otherwise.
            if (line[1]=='MODE'):
                for channel in settings['channel']:
                    s.send(("JOIN %s\r\n" % channel).encode('utf-8'))
                print("Connected!")

            try:

                # Lines containing "=" in them contain the list of users in the channel.
                if line[3] == '=':

                    for channels in line[4:]:

                        if channels[0] == '#':
                            chanCount += 1
                            userList[chanCount].append(channels)

                        elif channels[0] == ':':
                            userList[chanCount].append(channels[1:])

                        else: userList[chanCount].append(channels)

            except IndexError:
                pass

            message = ''
            user = ''

            if line[1] == 'PRIVMSG':
                stringy = line[0]
                temporary = stringy.split('!')
                user = str(temporary[0])[1:]
                y = line[3:]

                for x in y:

                    if x[0] == ':':
                        message += x[1:] + ' '

                    else: message += x + ' '

                printOut = user + " | " + message

                for a in logList:

                    if line[2] in a:
                        i = open(a, 'a')
                        i.write(printOut + '\n')
                        i.close()

                #if urls(message):
                    #print(urlList)
                    #printUrls(urlList, line[2])
                    #print(urlList)

                if '!ip' in message:
                    findIP(message[4:], line[2])

                if NICK.lower() in message.lower() and line[2] != '##isso-tutorials':

                    if line[2] == '##isso-mnsu':
                        pass

                    elif ('hello' in message.lower() or 'hi' in message.lower()):
                        sendMessage('Please join me in ##isso-tutorials. If you need help, mention my name and the word "help" the channel and I will print out a list of commands.\r\n', user)

                y = [''.join(c for c in s if c not in punctuation) for s in y]

                if line[2] == '##isso-tutorials' or line[2] == '##temp':

                    if NICK.lower() in message.lower() and ('hello' in message.lower() or 'hi' in message.lower()):
                        sendMessage(("Hello, %s\r\n" % user), line[2])

                    if NICK.lower() in message.lower() and 'advice' in message.lower():
                        advice(line[2])

                    elif NICK.lower() in message.lower() and 'help' in message.lower():
                        helpMe(line[2])

                    elif NICK.lower() in message.lower() and 'info' in message.lower():
                        info(line[2], NICK)

                    elif NICK.lower() in message.lower() and 'tutorial' in message.lower() and 'wep' in message.lower():
                        aircrack(line[2])

                    elif NICK.lower() in message.lower() and 'insult' in message.lower():

                        for users in userList:

                            for nickname in users:

                                if nickname.lower() in message.lower() and nickname != NICK and nickname != user:
                                    insult(line[2], nickname)


                ohelig = ''
                sentence = ''

                if NICK.lower() in message.lower() and ' say to' in message.lower():

                    for letter in message:
                        sentence += letter

                    name = message.split(' ')
                    ignore = len(NICK + ' say to ' + name[3] + ' ')

                    botherOhelig(sentence[ignore:], '##temp')

                if 'sleep()' in message.lower():
                    sleep(120)
                    botherOhelig("Ohelig, how could ", '##temp')
                    sleep(4)
                    botherOhelig('you want', '##temp')
                    sleep(7)
                    botherOhelig('to kill me?', '##temp')
                    sleep(10)
                    botherOhelig("OHELIG, I DON'T", '##temp')
                    sleep(10)
                    botherOhelig("WANT TO DIE!", '##temp')
                    sleep(20)
                    raise KeyboardInterrupt

                print(printOut)

    except KeyboardInterrupt:

        s.send(("QUIT \r\n").encode("utf-8"))

        for a in logList:
            i = open(a, "a")
            i.write('\nClosed\n')
            i.flush()
            i.close()

        print()

        exit('Closing')
