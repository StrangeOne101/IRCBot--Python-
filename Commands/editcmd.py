import os

if len(args) < 2:
    sender.reply(sender.nick + ": Not enough parameters! Usage is !editcmd <command> <code>")
elif not isCommand(args[0].lower()):
    sender.reply(sender.nick + ": Command does not exist!")
else:
    text = ""
    for t in args[1:]:
        if t == args[1]:
            text = t
        else:
            text = text + " " + t
    with open("Commands\\" + args[0].lower() + ".py","w+") as f:
        for text1 in text.split("\\n"):
            f.write(text1.replace("\\t", "\t") + "\n")    
        f.close()
    sender.reply(sender.nick + ": Command edited!")
