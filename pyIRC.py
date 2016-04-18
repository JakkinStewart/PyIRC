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


    # Sends the required stuffs to the server. Password, nickname, etc.
def connectToServer(passwd, nick, ident, host, realname): #ident, host, realname):
    s.send(('USER %s %s bla : %s\r\n' % (ident, host, realname)).encode('utf-8'))
    s.send(("PASS %s \r\n" % str(passwd)).encode('utf-8'))
    s.send(('NICK %s \r\n' % nick).encode('utf-8'))
    #s.send(('USER %s bla : %s\r\n' % (host, realname)).encode('utf-8')) #ident, host, realname)).encode('utf-8'))

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
var = open(debug, "w")
var.write("")
var.flush()
var.close()
# Connects to server (as stated by the function name)
# Creates empty list. Will be populated with users in the channels.
userList = []

# Makes a list of channel logs
logList = []

# Sets nick to user's selected nickname
NICK = settings['nick']

# Makes a counter. Counter used to seperate channels into seperate lists. Makes life easier.
counter = 0

# Counts how many channels. Makes a list of users with these channels.
chanCount = -1

# For every channel, make a <channel>.log file. Also, I found the counter thing.
for a in settings['channel']:
    counter += 1
    logList.append("%s.log" % a)

# For as many counts in the counter variable, make a list. Add users to that list. 
for i in range(counter):
    users = [] * counter
    userList.append(users)

firstConnection = True

# Here's the fun part! This part starts the infinite loop.
# The infinite loop will run certain things according to certain triggers. (No, its not a feminist.)
while True:

    if firstConnection == True:
        ssL=socket.socket()
        ssL.connect((settings['host'], settings['port']))
        ssL.settimeout(60)
        if settings['ssl'] == 'yes':
            s = ssl.wrap_socket(ssL)
        else:
            s = ssL

        firstConnection = False
        print("Connecting...")

    else:
        #ssL.shutdown(SHUT_RDWR)
        ssL.close()
        ssL=socket.socket()
        ssL.connect((settings['host'], settings['port']))
        ssL.settimeout(60)
        if settings['ssl'] == 'yes':
            s = ssl.wrap_socket(ssL)

        else:
            s = ssL

        print("Reconnecting...")

    connectToServer(settings['pass'],
                    settings['nick'],
                    settings['ident'],
                    settings['host'],
                    settings['realname'])

    timeEnd = time() + 60

    while True:

        try:
            #if len(s.recv(4096)) == 0:
                #break
                #print("Disconnected....")
                #s.send(("QUIT \r\n").encode('utf-8'))
                #connectToServer(settings['pass'],
                                #settings['nick'],
                                #settings['ident'],
                                #settings['host'],
                                #settings['realname'])
            # Read 4096 bytes from the server and append it to the readbuffer.
            readbuffer=readbuffer + s.recv(4096).decode(errors='ignore')
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
                    # Writes to the debug log. Not sure if its actually useful.
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
                #sleep(5)
                if (line[1]=='MODE'):
                    for channel in settings['channel']:
                        s.send(("JOIN %s\r\n" % channel).encode('utf-8'))
                    print("Connected!")

                try:

                    # Lines containing "=" in them contain the list of users in the channel.
                    if line[3] == '=':

                        # Iterates throught the messages sent by the server. Cuts out the useless junk.
                        for channels in line[4:]:

                            # Channel names start with "#" and also lead the list of users
                            if channels[0] == '#':
                                chanCount += 1
                                userList[chanCount].append(channels)

                            # Anything else after the channel name will start with a ":".
                            # Cut out the colon and add it to the list.
                            elif channels[0] == ':':
                                userList[chanCount].append(channels[1:])

                            # Otherwise, just add it to the list.
                            else: userList[chanCount].append(channels)

                # If an index error occurs (sometimes the server will send a line shorter than expected), ignore.
                except IndexError:
                    pass

                # Message and user will be populated later.
                message = ''
                user = ''

                # PRIVMSG is the only thing you care about if you want to see people talking.
                if line[1] == 'PRIVMSG':

                    # Temporary variable stringy (quite original)
                    stringy = line[0]
                    #print(stringy)
                    # Another temporary variable. It splits everything by "!". 
                    # For some reason, users always seem to start with "!"\
                    # This almost doesn't seem necessary.... Grr.
                    temporary = stringy.split('!')

                    # User is finally discovered. (Unfortunately, I have to coverty it to string before its useable.)
                    user = str(temporary[0])[1:]

                    # y (an insanely clear variable name) saves the rest of the line (ignoring the nicks)
                    y = line[3:]

                    # Iterate through y.
                    for x in y:

                        # Ignoring any colons in the variable, save the rest of the data in the message variable
                        if x[0] == ':':
                            message += x[1:] + ' '

                        # Save everything without cutting colons or anything weird.
                        else: message += x + ' '

                    # Save the user and their messages in the printOut variable
                    printOut = user + " | " + message

                    # Iterate through the channel log files and save to each file.
                    for a in logList:

                        try:
                            if line[2] in a:
                                i = open(a, 'a')
                                i.write(printOut + '\n')
                                i.close()

                        except UnicodeEncodeError:
                            pass

                    #if urls(message):
                        #print(urlList)
                        #printUrls(urlList, line[2])
                        #print(urlList)

                    # Runs the findIP function to find geolocations of IP addresses
                    if '!ip' in message:
                        findIP(message[4:], line[2])

                    # If stuff isn't in the channel ##isso-tutorials, do the stuffs.
                    if NICK.lower() in message.lower() and line[2] != '##isso-tutorials':

                        # If the stuff is in ##isso-mnsu, don't do shit
                        if line[2] == '##isso-mnsu':
                            pass

                        # Otherwise, if a greeting exists in the message, send user a PM saying to not talk to you here
                        elif ('hello' in message.lower() or 'hi' in message.lower()):
                            sendMessage('Please join me in ##isso-tutorials. If you need help, mention my name and the word "help" the channel and I will print out a list of commands.\r\n', user)

                    # Get rid of all punctuation... Not sure why. Will find out later.
                    y = [''.join(c for c in s if c not in punctuation) for s in y]

                    # If message sent in either channel ##isso-tutorials or channel ##temp, do the stuffs!
                    if line[2] == '##isso-tutorials' or line[2] == '##temp':

                        # Checks if bot's nick is in the message and if a greeting is in the message.
                        # If yes, say hi back.
                        if NICK.lower() in message.lower() and ('hello' in message.lower() or 'hi' in message.lower()):
                            sendMessage(("Hello, %s\r\n" % user), line[2])

                        # If bot's nick and the word advice in the message, give some advice from the advice function.
                        if NICK.lower() in message.lower() and 'advice' in message.lower():
                            advice(line[2])

                        # If nick and "help" in the message, send the help message.
                        elif NICK.lower() in message.lower() and 'help' in message.lower():
                            helpMe(line[2])

                        # Again, if nick is in the message and "info" in the message, send the info message.
                        elif NICK.lower() in message.lower() and 'info' in message.lower():
                            info(line[2], NICK)

                        # Please tell me you get the idea.
                        # Runs the aircrack function.
                        elif NICK.lower() in message.lower() and 'tutorial' in message.lower() and 'wep' in message.lower():
                            aircrack(line[2])

                        # Insults the damn user. (Only insults people who exist.)
                        elif NICK.lower() in message.lower() and 'insult' in message.lower():

                        # Runs through all the users
                            for users in userList:

                                # Runs through the two lists to find the user
                                for nickname in users:

                                    # Does some checking, and insults the person.
                                    if nickname.lower() in message.lower() and nickname != NICK and nickname != user:
                                        insult(line[2], nickname)

                    # Initializes empty variables.
                    # This was designed to annoy one of the mods in my channel.
                    ohelig = ''
                    sentence = ''

                    # Checks to see if someone is asking bot to say something to someone.
                    if NICK.lower() in message.lower() and ' say to' in message.lower():

                        # Apparently, the for loop will look at every letter rather than do what I want.
                        # (Shows my lack of knowledge in python.)
                        for letter in message:
                            sentence += letter

                        # Finds the name (spoiler, its in the third position in the list)
                        name = message.split(' ')
                        ignore = len(NICK + ' say to ' + name[3] + ' ')

                        # Bothers Ohelig
                        botherOhelig(sentence[ignore:], '##temp')

                    # Prints the printOut variable.
                    print(printOut)

        except socket.timeout:
            break

        # If some fucker decides to interrupt the program, do this shit.
        except KeyboardInterrupt:

            # Tell the server that the bot quits.
            s.send(("QUIT \r\n").encode("utf-8"))

            # Write "Closed" in each logfile.
            for a in logList:
                i = open(a, "a")
                i.write('\nClosed\n')
                i.flush()
                i.close()

            # Makes screen look prettier.
            print()

            # Exits the program.
            exit('Closing')
