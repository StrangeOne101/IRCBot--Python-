import socket
import os
from Config import *
from Commands import *

sock = socket.socket()

accountdb = {}

"""Send message to server"""
def send(string):
    if (string != ""):
        sock.send((string + "\r\n").encode("UTF-8"))
        print("[OUT] " + string)

"""Parse messages from irc"""
def handleMessage(message):
    try:
        if message[0] == ":":
            message = message[1:]
        msg = user_ = nick_ = command = host = channel = ""
        if (len(message.split()) < 3): #If short command. E.g the PINg command
            command = message.split()[0]
            msg = message.split()[1].split(":", 2)[1] 
        else:
            command = message.split()[1]
            if ("!" in message and "@" in message and (command.lower() == "privmsg" or command.lower() == "nick")):    
                user_ = message.split()[0].split("!")[1].split("@")[0]
                host = message.split()[0].split("@")
                nick_ = message.split()[0].split("!")[0]
            else:
                host = message.split()[0]
            channel = message.split()[2]
            msg = message.split(" ", 3)[3] #So we can have messages with spaces
            if (msg[0] == ":"):
                msg = msg[1:] #Cut the extra : off the start
    except IndexError as e:
        print("[WARNING] IndexError occured: " + str(e))
    if (command == "PING"):
        send("PONG :{}".format(msg))
    elif (command == "MODE"):
        if (channel == nickname):
            if ("+i" in msg):
                onConnect()
        elif ("+V" in msg or "+v" in msg):
                send("PRIVMSG {} :I got voice? :o".format(channel))
    elif (command == "JOIN"):
        send("WHO " + channel + " %na")
    elif (command == "NICK"):
        if (nick_ == nick):
            nick = msg
        elif (nick_ in accountdb.keys()):
            value = accountdb[nick_]
            accountdb.remove(nick_)
            accountdb[msg] = value
    elif (command == "354"): #Permissions from /who #chan
        accountdb[msg.split()[0]] = msg.split()[1]
        print("[DEBUG] " + msg.split()[0] + " = " + msg.split()[1])
    elif (command == "PRIVMSG"):
        onMessage(msg.replace("\n", "").replace("\r", ""), nick_, channel)

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
    return nick in accountdb.keys() and accountdb[nick] != "0" and accountdb[nick] in operators  
        
       
"""When the bot connects"""
def onConnect():
    for chan_ in channels:
        send("JOIN {}".format(chan_))
        send("WHO " + chan_ + " %na")  

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
    s = str(sock.recv(4096).decode("UTF-8"))
    if (s != "" and s != None):
        print("[IN] " + s.replace("\n", "")) 
        for s1 in s.split("\n"):
            if (s1 != "" and s1 != None):
                handleMessage(s1)
    else:
        sock.close()
   
        





