from configparser import ConfigParser

if __name__ == "__main__":
    raise Exception("Wrong module run! Run PyBot.py instead!")

config = ConfigParser()
config.read("config.ini")
if "PROPERTIES" not in config.sections():
    config.add_section("PROPERTIES")
    
IP = config["PROPERTIES"].get("IP", "irc.esper.net")
port = int(config["PROPERTIES"].get("Port", 6667))
nickname = config["PROPERTIES"].get("Nickname", "Riyo")
username = config["PROPERTIES"].get("Username", "Riyo")
nickpass = config["PROPERTIES"].get("NickServ Password", "") #Optional
passwd = config["PROPERTIES"].get("Server Password", "")     #Optional
root = "Strange"
hiddenmsg = config["PROPERTIES"].get("MOTD", "IRCBot made in Python by Strange.")
channels = config["PROPERTIES"].get("Channels", "#StrangeOne101").replace(" ", "").split(",")
operators = config["PROPERTIES"].get("Operators", "Strange").replace(" ", "").split(",")

config["PROPERTIES"]["IP"] = IP
config["PROPERTIES"]["Port"] = str(port)
config["PROPERTIES"]["Nickname"] = nickname
config["PROPERTIES"]["Username"] = username
config["PROPERTIES"]["NickServ Password"] = nickpass
config["PROPERTIES"]["Server Password"] = passwd
config["PROPERTIES"]["MOTD"] = hiddenmsg

chans = ""
for chan in channels:
    if chan == channels[0]:
        chans = chan
    else:
        chans = chans + ", " + chan
        
ops = ""        
for op in operators:
    if op == operators[0]:
        ops = op
    else:
        ops = ops + ", " + op        
config["PROPERTIES"]["Operators"] = ops
with open("config.ini", "w") as file:   
    config.write(file)