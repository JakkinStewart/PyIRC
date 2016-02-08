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

# Asks user for input.
host = '' #input("Enter IRC server [Freenode]: ")
port = '' #input("Enter port [6697]: ")
nick = '' #input("Enter nick [PythonIRCBot]: ")
chan = '' #input("Enter channel [#temp]: ")
Ssl = '' #input("Do you want to use SSL? [Y/n]: ")
logging = '' #input("Do you want to enable logging? [Y/n]: ")
if logging.lower() == 'y':
    log = input("Where do you want save the log file? (Default is in currect directory.) ")
elif logging == '':
    log = './'
prevtime = 0

# If an input was left blank, use defaults.
if host == '': HOST='irc.freenode.net'
elif host != '': HOST=host
if port == '': PORT=6697
elif port != '': PORT=int(port)
if nick == '': NICK='DovahBot'
elif nick != '': NICK=nick
if chan == '': CHANNEL='#temp'
elif chan != '': CHANNEL=chan
if Ssl == '' or Ssl.lower() == 'y': sslEnable='y'
elif Ssl.lower() == 'n': sslEnable='n'
if logging.lower() == '': logFile = open('%s.log' % CHANNEL, 'a')
elif logging.lower() == 'y':
    logFile = open(log + '%s.log' % CHANNEL, 'a')
elif logging.lower() == 'n':
    pass
else: exit("This is an unusual error. Contact JakkinStewart at Github to solve this.")

PASS = 'asdfghjkl'

# Sets identity and realname for the IRC server.
IDENT='dovahkiin'
REALNAME='Python IRC Client'

print("Connecting...")

# Begins readbuffer.
# Taken from http://archive.oreilly.com/pub/h/1968:
# You need a readbuffer because your might not always be able to read complete IRC commands from the server (due to a saturated Internet connection, operating system limits, etc).
#print("Connecting...")
readbuffer=''

# If SSL was enabled, wrap the socket in SSL.
if sslEnable.lower() == 'y':
    ssL=socket.socket()
    ssL.connect((HOST,PORT))
    s = ssl.wrap_socket(ssL)

# Otherwise, don't wrap anything.
elif sslEnable.lower() == 'n':
    s=socket.socket()
    s.connect((HOST,PORT))

# Send messages to the server containing the nick, identity, server, and realname. All messages must be encoded in utf-8.
s.send(("PASS %s\r\n" % PASS).encode('utf-8'))
s.send(('NICK %s\r\n' % NICK).encode('utf-8'))
s.send(('USER %s %s bla : %s\r\n' % (IDENT, HOST, REALNAME)).encode('utf-8'))
#s.send(('PRIVMSG nickserv identify %s %s\r\n' % (NICK, PASS)).encode('utf-8'))
# Enter an infinite loop.

while 1:
    try:
    # Read 1024 bytes from the server and append it to the readbuffer.
        readbuffer=readbuffer + s.recv(1024).decode()
        temp=readbuffer.split('\n')
        readbuffer=temp.pop()
        for line in temp:
            line=line.rstrip()
            line=line.split()
            print(line)
            if 'JOIN' in line and CHANNEL in line:
                s.send(("PRIVMSG %s :Hi, I'm %s. If you ever need advice, just ask!\r\n" % (CHANNEL, NICK)).encode('utf-8'))
            if (line[0]=='PING'):
                s.send(("PONG %s\r\n" % line[1]).encode('utf-8'))
            if (line[1]=='MODE'):
                s.send(("JOIN %s\r\n" % CHANNEL).encode('utf-8'))
                print("Connected!")

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

                y = [''.join(c for c in s if c not in punctuation) for s in y]

                if NICK in y and 'advice' in y:
                    os.system("curl -s http://api.adviceslip.com/advice > .file")
                    inFile = open('.file', 'r')
                    jsonAttempt = inFile.read()
                    parsed_json = json.loads(jsonAttempt)
                    #print(parsed_json['slip']['advice'])
                    s.send(("PRIVMSG %s :%s\r\n" % (CHANNEL, parsed_json['slip']['advice'])).encode('utf-8'))


                elif NICK in y and 'Hello' in y or 'hello' in y or 'hi' in y or 'Hi' in y or 'HI' in y:
                    s.send(("PRIVMSG %s :Hello, %s\r\n" % (CHANNEL, user)).encode('utf-8'))

                elif NICK in y and 'info' in y:
                    s.send((("PRIVMSG %s :I'm %s, written by JakkinStewart on GitHub. Right now I can dispense advice using the adviceslip.com API. Hopefully, I will be extended to help train new ISSO members.\r\n") % (CHANNEL, NICK)).encode('utf-8'))

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
