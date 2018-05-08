import urllib.request
from bs4 import BeautifulSoup

def search(key,string):
    for i in range(len(string)):
        check = string[i:i+(len(key))]
        if check == key:
            return True
    return False

# imports source data from website (link) and saves as fileName (.txt)
def getData(link,fileName):
    site = urllib.request.urlopen(link)
    data = site.read()
    file = open(fileName,'wb')
    file.write(data)
    file.close()

# Determines name, age, and place of profile User
def nap(fileName):
    readFile = open(fileName,'r',encoding='utf8')
    readData = readFile.read()
    parse = BeautifulSoup(readData,'html.parser')
    meta = parse.find_all('meta')

    napLine = str(meta[9])
    napLine = napLine.split()
    addInfoLoc = []
    age = 'unk'
    addInfo = []
    
    for i in range(len(napLine)):
        if napLine[i][0] == '(' and napLine[i][-1:] == '.':
            addInfoLoc.append(i)
            addInfo.append(napLine[i][:-1])

        try:
            age = int(napLine[i])
            break
        except ValueError:
            if age == 'unk':
                age = 'unk'

    newLine = []
    if len(addInfoLoc) > 0:
        for i in range(len(napLine)):
           testFor = 0
           for n in addInfoLoc:
                if i != n and testFor == 0:
                    testFor = 1
                    newLine.append(napLine[i])
    else:
        newLine = napLine

    try:
        FN = newLine[1].split('"')
    except len(FN) == 1:
        FN = newLine[1].split("'")
    FN = FN[1]
    LN = newLine[2]
    if LN[-1] == '.':
        LN = LN[:-1]
    if len(addInfo)>=1:
        name = [LN,addInfo,FN]
    else:
        name = [LN,FN]
    
    location = ''
    for i in range(len(napLine)-2,7,-1):
        location = napLine[i] + ' ' + location
    location = location.split(',')
    location = location[-1]
    location = location[:-2]

    nal = [name,age,location]
    return nal

def jobEdu(fileName):
    readFile = open(fileName,'r',encoding='utf8')
    readData = readFile.read()
    parse = BeautifulSoup(readData,'html.parser')
    # searches for tags that start with span
    # main listing has <span title
    # date listing has <span class but immediately follows main listing it is relevant to
    span = parse("span")
    workDates = []
    workLocs = []
    eduDates = []
    eduLocs = []
    check = 0
    work = []
    higherEd = []
    for i in span:
        
        i = str(i)
        if search('job',i):
            job = True
            school = False
        if search('uni',i) or search('college',i):
            job = False
            school = True
        if search('school',i):
            job = False
            school = False
        # checks for employer
        if i[:11] == '<span title' and job:
            check = 1
            workLocs.append(i)
        # checks for dates worked for employer
        if check == 1 and i[:11] != '<span title' and job:
            workDates.append(i)
            check = 0
        # checks for educator (higher ed only, college/university)
        if i[:11] == '<span title' and school:
            check = 1
            eduLocs.append(i)
        # checks dates spent at educational institution
        if check == 1 and i[:11] != '<span title' and school:
            eduDates.append(i)
            check = 0
    # trims irrelevant information from the main listing
    for i in range(len(workLocs)):
        workLocs[i] = workLocs[i].split('"')
        workLocs[i] = workLocs[i][1:-1]
        temp = ''
        for n in range(len(workLocs[i])):
            temp = temp + workLocs[i][n]
        workLocs[i] = temp
    for i in range(len(eduLocs)):
        eduLocs[i] = eduLocs[i].split('"')
        eduLocs[i] = eduLocs[i][1:-1]
        temp = ''
        for n in range(len(eduLocs[i])):
            temp = temp + eduLocs[i][n]
        eduLocs[i] = temp
    # trims irrelevant information from the date listing
    for i in range(len(workDates)):
        
        workDates[i] = workDates[i].split('>')
        workDates[i] = workDates[i][1].split('<')
        workDates[i] = workDates[i][0].split()
                
        if len(workDates[i]) > 4:
            field = ''
            for l in workDates[i][4:]:
                field = field + ' ' + l
            try:
                workDates[i] = workDates[i][1] + ' - ' + workDates[i][3] + ' ' + field
            except IndexError:
                workDates[i] = workDates[i][1] + ' - Present' + ' ' + field
        else:
            try:
                workDates[i] = workDates[i][1] + ' - ' + workDates[i][3]
            except IndexError:
                workDates[i] = workDates[i][1] + ' - Present'
    for i in range(len(eduDates)):
        eduDates[i] = eduDates[i].split('>')
        eduDates[i] = eduDates[i][1].split('<')
        eduDates[i] = eduDates[i][0].split()
        try:
            eduDates[i] = eduDates[i][1] + ' - ' + eduDates[i][3]
        except IndexError:
            eduDates[i] = eduDates[i][1]
    #compiles dates and locations lists into one to produce the result that will be returned
    for i in range(len(workDates)):
        work.append([workLocs[i],workDates[i]])
    for i in range(len(eduDates)):
        higherEd.append([eduLocs[i],eduDates[i]])
    return [work,higherEd]
        
def main(link):
    fileName = 'okData.txt'
    getData(link,fileName)
    nalList = nap(fileName)
    history = jobEdu(fileName)
    historyWork = history[0]
    historyEdu = history[1]
    name = nalList[0]
    try:
        name = str(name[0]+name[1][0]+', '+name[2])
    except IndexError:
        name=str(name[0]+', '+name[1])
    age = nalList[1]
    loc = nalList[2]

    result = [name,age,loc,historyEdu,historyWork]
    return result
