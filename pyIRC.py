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




"""# Asks user for input.
host = '' #input("Enter IRC server [Freenode]: ")
port = '' #input("Enter port [6697]: ")
nick = '' #input("Enter nick [PythonIRCBot]: ")
chan = '' #input("Enter channel [#temp]: ")
Ssl = '' #input("Do you want to use SSL? [Y/n]: ")
logging = '' #input("Do you want to enable logging? [Y/n]: ")"""
log = './'

HOST='irc.freenode.net'
PORT=6697
NICK='DovahBot'
CHANNEL=['##isso-tutorials', '#temp']
LOG = ''
logFile = open('%s.log' % LOG, 'a')
sslEnable = 'y'
PASS = 'asdfghjkl'
IDENT='dovahkiin'
REALNAME='Python IRC Client'

ssL=socket.socket()
ssL.connect((HOST,PORT))

s = ssl.wrap_socket(ssL)

def connectToServer(passwd, nick, ident, host, realname):
    s.send(("PASS %s\r\n" % passwd).encode('utf-8'))
    s.send(('NICK %s\r\n' % nick).encode('utf-8'))
    s.send(('USER %s %s bla : %s\r\n' % (ident, host, realname)).encode('utf-8'))

def sendMessage(msg, CHAN):
    s.send(("PRIVMSG %s :%s\r\n" % (CHAN, msg)).encode('utf-8'))

def info(CHAN, NICK):
    sendMessage(("I'm %s, written by JakkinStewart on GitHub. Right now I can dispense advice using the adviceslip.com API. Hopefully, I will be extended to help train new ISSO members.\r\n" % NICK), CHAN)

def helpMe(CHAN):
    sendMessage(("'advice': Mentioning the word 'advice' to me will cause me to give you advice.\r\n"), CHAN)
    sendMessage(("'info'  : Mentioning the word 'info' to me will give general info on me. (Not much yet.)\r\n"), CHAN)
    sendMessage(("'Hello' : Saying hi to me will make me say hi back.\r\n"), CHAN)
    sendMessage(("'help'  : Using the word 'help' with my name will give you this message.\r\n"), CHAN)

def aircrack(CHAN):
    sendMessage(("Aircrack-ng is a complete suite of tools to assess WiFi network Security.\r\n"), CHAN)

    sendMessage(("Requirements: WiFi card. (Can be USB, as long as Aircrack-ng can see it.) | Helpful tutor. (I haven't been coded to be helpful yet.)"), CHAN)

    sendMessage(("airmon-ng check kill"), CHAN)
    sleep(1)
    sendMessage(("airmon-ng start \x035[interface]\x03"), CHAN)

    sendMessage(("airodump-ng [interface]mon"), CHAN)

    sendMessage(("airodump-ng -c [channel] --bssid [BSSID] -w dump [interface]mon"), CHAN)

    sendMessage(("airocrack-ng --bssid [BSSID] dump-*.cap"), CHAN)

    sendMessage(("Presto! You just cracked the key!"), CHAN)

def advice(CHAN):
    os.system("curl -s http://api.adviceslip.com/advice > .advice")
    inFile = open('.advice', 'r')
    jsonAttempt = inFile.read()
    parsed_json = json.loads(jsonAttempt)
    sendMessage("%s\r\n" % (parsed_json['slip']['advice']), CHAN)
    os.system('rm .advice')

def insult(CHAN, insulter, insultee):
    os.system('curl -s http://quandyfactory.com/insult/json > .insult')
    #os.system("""curl -s http://www.randominsults.net/ | grep -a '<td bordercolor="#FFFFFF"><font face="Verdana" size="4"><strong><i>' | sed 's/<td bordercolor="#FFFFFF"><font face="Verdana" size="4"><strong><i>//' | sed 's|</i></strong></font>&nbsp;</td>||' | sed 's/^......//' > .insult""")
    inFile = open('.insult', 'r')
    #insult = inFile.read()
    jsonAttempt = inFile.read()
    parsed_json = json.loads(jsonAttempt)
    sendMessage('%s, %s would like you to know something. %s ' % (insultee, insulter, parsed_json['insult']), CHAN)
    os.system('rm .insult')


# Begins readbuffer.
# Taken from http://archive.oreilly.com/pub/h/1968:
# You need a readbuffer because your might not always be able to read complete IRC commands from the server (due to a saturated Internet connection, operating system limits, etc).
#print("Connecting...")





readbuffer=''

# If SSL was enabled, wrap the socket in SSL.
#if sslEnable.lower() == 'y':

# Otherwise, don't wrap anything.
#elif sslEnable.lower() == 'n':
#    s=socket.socket()
#    s.connect((HOST,PORT))

# Send messages to the server containing the nick, identity, server, and realname. All messages must be encoded in utf-8.
#s.send(('PRIVMSG nickserv identify %s %s\r\n' % (NICK, PASS)).encode('utf-8'))
# Enter an infinite loop.

connectToServer(PASS, NICK, IDENT, HOST, REALNAME)
userList = []
count = 0
chanCount = -1
counter = 0
for a in CHANNEL:
    counter += 1

for i in range(counter):
    users = [] * counter
    userList.append(users)

while 1:
    try:
    # Read 1024 bytes from the server and append it to the readbuffer.
        readbuffer=readbuffer + s.recv(1024).decode()
        temp=readbuffer.split('\n')
        readbuffer=temp.pop()
        for line in temp:
            line=line.rstrip()
            line=line.split()
            #print(line)
            if line[0]=='PING':
                s.send(("PONG %s\r\n" % line[1]).encode('utf-8'))
            if (line[1]=='MODE'):
                for channel in CHANNEL:
                    s.send(("JOIN %s\r\n" % channel).encode('utf-8'))
                print("Connected!")

            try:
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
                #print(line)
                if line[2] != '##isso-tutorials':
                    sendMessage('Please join me in ##isso-tutorials.', line[2])
                    #pass
                stringy = line[0]
                temporary = stringy.split('!')
                user = str(temporary[0])[1:]
                y = line[3:]
                for x in y:
                    if x[0] == ':':
                        message += x[1:] + ' '
                    else: message += x + ' '

                y = [''.join(c for c in s if c not in punctuation) for s in y]

                if line[2] == '##isso-tutorials':
                    if NICK in message and ('Hello' or 'hello' or 'hi' or 'Hi' or 'HI') in message:
                        sendMessage(("Hello, %s\r\n" % user), line[2])

                    if NICK in message and 'advice' in message:
                        advice(line[2])

                    elif NICK in message and 'help' in message:
                        helpMe(line[2])

                    elif NICK in message and 'info' in message:
                        info(line[2], NICK)

                    elif NICK in message and 'tutorial' in message and ('WEP' or 'wep') in message:
                        aircrack(line[2])

                    elif NICK in message and 'insult' in message:
                        for users in userList:
                            for nickname in users:
                                if nickname in message and nickname != NICK and nickname != user:
                                    insult(line[2], user, nickname)


                printOut = user + ' | ' + message
                ircChat = printOut +'\n'
                print(printOut)
                logFile.write(ircChat)
                logFile.flush()

    except KeyboardInterrupt:
        s.send(("QUIT").encode("utf-8"))
        logFile.write('\nClosed\n')
        logFile.flush()
        print()
        exit('Closing')
