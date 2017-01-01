#!/usr/bin/python3

import socket
import os
import re
from Config import *
from Commands import *

sock = socket.socket()

accountdb = {}

irc_prefix_rem = re.compile(r'(.*?) (.*?) (.*)').match
irc_noprefix_rem = re.compile(r'()(.*?) (.*)').match
irc_netmask_rem = re.compile(r':?([^!@]*)!?([^@]*)@?(.*)').match
irc_param_ref = re.compile(r'(?:^|(?<= ))(:.*|[^ ]+)').findall  

"""Send message to server"""
def send(string):
    if (string != ""):
        sock.send((string + "\r\n").encode("UTF-8"))
        print("[OUT] " + string)

"""Parse messages from irc"""
def handleMessage(message):
    global nickname
    try:    
        if message.startswith(":"):  # has a prefix
            prefix, command, params = irc_prefix_rem(message).groups()
        else:
            prefix, command, params = irc_noprefix_rem(message).groups()
        nick, user, host = irc_netmask_rem(prefix).groups()
        paramlist = irc_param_ref(params.replace("\n", "").replace("\r", ""))
        lastparam = ""
        if paramlist:
            if paramlist[-1].startswith(':'):
                paramlist[-1] = paramlist[-1][1:]
            lastparam = paramlist[-1]
            
        msg = paramlist[-1]
        channel = None
        if len(paramlist) > 1:
            channel = paramlist[-2]                   
    except IndexError as e:
        print("[WARNING] IndexError occured: " + str(e))
    except AttributeError as e:
        print("[WARNING] Recieved line that couldn't be processed: " + str(e))
        return
    if (command == "PING"):
        send("PONG :{}".format(msg))
    elif (command == "MODE"):
        print("[DEBUG] Msg = " + msg)
        if (channel == nickname):
            if ("+i" in msg):
                onConnect()
    elif (command == "JOIN"):
        if nick == nickname:
            send("WHO " + msg + " %na")
        else:    
            send("WHO " + nick + " %na")
    elif (command == "NICK"):
        if (nick == nickname):
            nickname = msg
        elif (nick.lower() in accountdb.keys()):
            value = accountdb[nick.lower()].lower()
            accountdb.remove(nick.lower())
            accountdb[msg.lower()] = value
    elif (command == "354"): #Permissions from /who #chan
        accountdb[channel.lower()] = msg.lower()
    elif (command == "PART" or command == "QUIT"):    
        if accountdb.has_key(nick.lower()):
            del accountdb[nick.lower()]
    elif (command == "PRIVMSG"):
        onMessage(msg.replace("\n", "").replace("\r", ""), nick, channel)

"""When a message is received"""
def onMessage(message, nick, channel):
    """if ("<3" in message):
        if ("anna" in nick.lower()):
            send("PRIVMSG {} :No Anna. No <3 for you.".format(channel))
        else:
            send("PRIVMSG {} :<3")"""
    if (nick == root):
        if ("#kill" in message):
            kill()
        elif (message.split()[0] == "#eval"):
            exec(message[6:])
    if (message[0] == "!" and isCommand(message.split(" ")[0][1:])):
        print("[DEBUG] COMMAND EXECUTED")
        sender = Sender(nick, "<UNKNOWN>", channel)
        args = message.split(" ")[1:]
        execute(message.split(" ")[0][1:], args, sender) 
        
"""Is the user an operator of the bot?"""
def isOperator(nick):
    print(str(operators))
    return nick.lower() in accountdb.keys() and accountdb[nick.lower()] != "0" and accountdb[nick.lower()] in operators  
        
       
"""When the bot connects"""
def onConnect():
    for chan_ in channels:
        send("JOIN {}".format(chan_))

"""Kill the bot"""
def kill():
    send("QUIT :{} dies".format(nickname))
    
class Sender:
    
    def __init__(self, nickname, username, channel):
        self.nick = nickname
        self.user = username
        self.channel = channel
        
    def reply(self, message):
        send("PRIVMSG " + self.channel + " :" + message)
        
    def pm(self, message):
        send("PRIVMSG " + self.nick + " :" + message)
    
    def quote(self, message):
        send(message)
        
    def isOp(self):
        return isOperator(self.nick)

sock.connect((IP, port))
send("NICK " + nickname)
send("USER " + username + " 0 * :" + hiddenmsg)

if (passwd != ""):
    send("PASS " + passwd)
if (nickpass != ""):
    send("PRIVMSG NickServ identify " + nickpass)

while (sock != None):
    for codec in ('utf-8', 'iso-8859-1', 'shift_jis', 'cp1252'):
        try:
            s = str(sock.recv(4096).decode(codec))
            if (s != "" and s != None):
                print("[IN] " + s.replace("\n", "")) 
                for s1 in s.split("\n"):
                    if (s1 != "" and s1 != None):
                        handleMessage(s1)
            else:
                sock.close()
        except UnicodeDecodeError:
            continue
   
        





