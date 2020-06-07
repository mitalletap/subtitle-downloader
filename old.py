from selenium import webdriver

def readFile(input_file_name):
    file = open(input_file_name, "r")


def parseLine(line):
    colon = line.find(": ")
    # print(line[colon+2:len(line)])


input_file_name = input("Type the name of the text file: ")

try:
    readFile(input_file_name)
except FileNotFoundError:
    print("Invalid File Name or Type")

with open(input_file_name) as f:
    line = f.readline()
    cnt = 1
    while line:
        parseLine(line)
        line = f.readline()
        cnt +=1 


# webbrowser.open('https://www.opensubtitles.org/en/search/subs', new=1)
browser = webdriver.Chrome('C:\WebDrivers\chromedriver.exe')
