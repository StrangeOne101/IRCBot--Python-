if len(args) == 0:
        sender.reply("Command usage is !join <channel>")
else:
        if args[0][0] == "#":
                args[0] = args[0][1:]
        sender.quote("JOIN #" + args[0])
