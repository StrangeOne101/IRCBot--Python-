if len(args) == 0:
    sender.reply(sender.nick + ": Command usage is !viewcmd <command>")
elif not isCommand(args[0].lower()):
    sender.reply(sender.nick + ": Command not found!")
else:
    with open("Commands\\" + args[0].lower() + ".py", "r") as file:
        sender.pm(file.read().replace("\n", "\\n").replace("\t", "\\t").replace("    ", "\\t"))
