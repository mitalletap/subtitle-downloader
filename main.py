from subtitle_bot import SubtitleBot

def readFile(input_file_name):
    file = open(input_file_name, "r")

def parseLine(line):
    colon = line.find(": ")
    return str(line[colon+2:len(line)])

def addToList(movieName):
    with open("need_to_redo.txt", "a") as ntr:
        ntr.write(movieName)
        ntr.close()

input_file_name = input("Enter the file name: ")
input_file_name = "movies.txt"
bot = SubtitleBot()
try:
    readFile(input_file_name)
except FileNotFoundError:
    print("Invalid File Name or Type")

with open(input_file_name) as f:
    line = f.readline()
    cnt = 1
    while line:
        parsed = parseLine(line)
        bot.searchForMovie(parsed)
        value = bot.changeLanguage()
        print(value)
        if value is True:
            bot.selectSubtitle()
            status = bot.downloadSelectedSubtitle(parsed)
            if status == False:
                addToList(parsed)
                print("Failed to Download")
        else:
            addToList(parsed)
            print("Failed to Download")
        line = f.readline()
        cnt +=1 

f.close()