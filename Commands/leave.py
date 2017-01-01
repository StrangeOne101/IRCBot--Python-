if len(args) == 0:
	sender.reply("Command usage is !leave <channel>")
else:
	if args[0][0] == "#":
		args[0] = args[0][1:]
	sender.quote("PART #" + args[0])
