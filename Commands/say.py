if len(args) > 0:
    text = ""
    for i in range(0, len(args)):
        if i == 0:
            text = args[0]
        else:
            text = text + " " + args[i]
    sender.reply(text)
else:
    sender.reply("\x1DSay what?")

        
