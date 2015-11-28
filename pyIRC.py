#! /usr/bin/env python
# Written by Joshua Jordi

import sys
import socket
import string
import ssl

host = input("Enter IRC server [freenode]: ")
port = input("Enter port [6667]: ")
nick = input("Enter nick [PyIRC]: ")
chan = input("Enter channel [#freenode]: ")
Ssl = input("Do you want to use SSL? [y/N]: ")
if host == '': HOST='irc.freenode.net'
elif host != '': HOST=host
if port == '': PORT=6667
elif port != '': PORT=int(port)
if nick == '': NICK='PyIRC'
elif nick != '': NICK=nick
if chan == '': CHANNEL='#freenode'
elif chan != '': CHANNEL=chan
if Ssl == '' or Ssl.lower() == 'n': sslEnable='n'
elif Ssl.lower() == 'y': sslEnable='y'
else: exit("This is an unusual error. Contact JakkinStewart at Github to solve this.")

IDENT='pyirc'
REALNAME='Python IRC Client'
readbuffer=''

#def SSL(HOST, PORT):
#    ssl_=socket.socket()
#    ssl_.connect((HOST,PORT))
#    s = ssl.wrap_socket(ssl_)

#def noSSL(HOST, PORT):
#    s=socket.socket()
#    s.connect((HOST,PORT))

if sslEnable.lower() == 'y': 
    ssL=socket.socket()
    ssL.connect((HOST,PORT))
    s = ssl.wrap_socket(ssL)

elif sslEnable.lower() == 'n': 
    s=socket.socket()
    s.connect((HOST,PORT))

s.send(('NICK %s\r\n' % NICK).encode('utf-8'))
s.send(('USER %s %s bla : %s\r\n' % (IDENT, HOST, REALNAME)).encode('utf-8'))
#s.send(('QUOTE PONG oxiDWBqeAK\r\n').encode('utf-8'))
#sleep(5)

while 1:
    readbuffer=readbuffer + s.recv(1024).decode()
    temp=readbuffer.split('\n')
    readbuffer=temp.pop()

    for line in temp:
        line=line.rstrip()
        line=line.split()

        if (line[0]=='PING'):
            s.send(("PONG %s\r\n" % line[1]).encode('utf-8'))
        if (line[1]=='MODE'):
            s.send(("JOIN %s\r\n" % CHANNEL).encode('utf-8'))
#        for word in line:
#             print(word[0], word[3], end=' ')
#        print()
#        print(line[3])
    try:
#        for word in line[3:]:
        for word in line:
            print(word, end=' ')
        print()
#        print(line[3:])
    except:
        pass


#while 1:
#    readbuffer=readbuffer+s.recv(1024).decode()
#    temp=readbuffer.split('\n')
#    readbuffer=temp.pop()
#
#    for line in temp:
#        line=line.rstrip()
#        line=line.split()
#
#        if (line[0]=='PING'):
#            s.send(("PONG %s\r\n" % line[1]).encode('utf-8'))
#        if (line[1]=='MODE'):
#            s.send(("JOIN %s\r\n" % CHANNEL).encode('utf-8'))
#        for word in line:
#            print(word, end=' ')
#        print()
#         print(line)

#elif useSSL == 'n':
#    s=socket.socket()
#    s.connect((HOST,PORT))
#    s.send(('NICK %s\r\n' % NICK).encode('utf-8'))
#    s.send(('USER %s %s bla : %s\r\n' % (IDENT, HOST, REALNAME)).encode('utf-8'))
#
#    while 1:
#        readbuffer=readbuffer+s.recv(1024).decode()
#        temp=readbuffer.split('\n')
#        readbuffer=temp.pop()
#    
#        for line in temp:
#            line=line.rstrip()
#            line=line.split()
#    
#            if (line[0]=='PING'):
#                s.send(("PONG %s\r\n" % line[1]).encode('utf-8'))
#            if (line[1]=='MODE'):
#                s.send(("JOIN %s\r\n" % CHANNEL).encode('utf-8'))
##            for word in line:
##                print(word, end=' ')
##            print()
##            print(line[3])
#        try:
#            for word in line[3:]:
#                print(word, end=' ')
##            print()
##            print(line[3:])
#
#        except:
#            pass
