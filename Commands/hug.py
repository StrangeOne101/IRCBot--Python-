if len(args) > 0:
	text = ""
	for i in range(0, len(args)):
		if i == 0:
			text = args[0]
		else:
			text = text + " " + args[i]
	sender.reply("\x01ACTION hugs " + text + "\x01")
else:
	sender.reply("\x01ACTION hugs " + sender.nick + "\x01")

		

