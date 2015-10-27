import os
from glob import glob

if __name__ == "__main__":
    raise Exception("Wrong module run! Run PyBot.py instead!")
if not os.path.exists("Commands"):
    os.mkdir("Commands")

files = glob("Commands/*.py")
for i in range(0, len(files)):
    files[i] = files[i][9:]
    if (files[i].lower() != files[i]):
        print("[FileIO] Converted " + files[i] + " command to lowercase.")
        os.rename("Commands/" + files[i], "Commands/" + files[i].lower())

def isCommand(command):
    print(str(os.path.isfile("Commands/" + command.replace(" ", "").lower() + ".py")) + "Commands/" + command.replace(" ", "").lower() + ".py")
    return os.path.isfile("Commands/" + command.replace(" ", "").lower() + ".py") and "." not in command and "/" not in command and "%" not in command

def execute(command, args, sender):
    #exec("import Commands." + command.replace(" ", "").lower())
    try:
        with open("Commands/" + command.replace(" ", "") + ".py") as f:
            code = compile(f.read(), "Commands/" + command.replace(" ", "") + ".py", 'exec')
            exec(code, globals(), locals())  
    except Exception as e:
        sender.reply("Error: " + str(e))
        
        