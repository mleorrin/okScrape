import tkinter
import okScrape2
from googletrans import Translator

def helpButton():
    helpWindow=tkinter.Tk()
    helpWindow.title('Help')
    helpText = 'Use CTRL+V and CTRL+C to paste and copy \nto the entry box and output boxes (respectively).\nTranslate checkbox will translate Name and Location only.\nUse clear button before running a new URL (or translating).'
    helpWid = tkinter.Label(helpWindow,text=helpText)
    helpWid.pack()
    
def clear():
    nBox.delete(0)
    aBox.delete(0)
    lBox.delete(0)
    edBox.delete(0,edBox.size())
    jobBox.delete(0,jobBox.size())
    e = entry.get()
    l = len(e)
    entry.delete(0,l)

    
def trans(words):
    translator = Translator()
    translated = translator.translate(words)
    return translated.text
def setWidget():
    lwid.grid(row=0,column=0,padx=5,pady=5)
    entry.grid(row=0,column=1,columnspan=2,padx=5,pady=5)
    rbut.grid(row=0,column=4,padx=5,pady=5)
    cbut.grid(row=0,column=5,padx=5,pady=5)
    cb.grid(row=0,column=3,padx=5,pady=5)
    hbut.grid(row=1,column=5,padx=5,pady=5)
    nFrame.grid(row=1,column=0,columnspan=5,sticky=W,padx=5,pady=5)
    nBox.grid(row=1,column=0,columnspan=5,sticky=W,padx=5,pady=5)
    aFrame.grid(row=2,column=0,columnspan=5,sticky=W,padx=5,pady=5)
    aBox.grid(row=2,column=0,columnspan=5,sticky=W,padx=5,pady=5)
    lFrame.grid(row=3,column=0,columnspan=5,sticky=W,padx=5,pady=5)
    lBox.grid(row=3,column=0,columnspan=5,sticky=W,padx=5,pady=5)
    edFrame.grid(row=4,column=0,columnspan=5,sticky=W,padx=5,pady=5)
    edBox.grid(row=4,column=0,columnspan=5,sticky=W,padx=5,pady=5)
    jobFrame.grid(row=5,column=0,columnspan=5,sticky=W,padx=5,pady=5)
    jobBox.grid(row=5,column=0,columnspan=5,sticky=W,padx=5,pady=5)


def showData(link):
    data = okScrape2.main(link)
    age = data[1]
    ed = data[3]
    job = data[4]
    if lang.get():
        name = trans(data[0])
        loc = trans(data[2])
    elif not lang.get():
        name = data[0]
        loc = data[2]
    count = 1
    nBox.insert(count,name)
    aBox.insert(count,age)
    lBox.insert(count,loc)
    if ed == []:
        ed = ['None Listed']
    edBox.config(height=len(ed))
    jobBox.config(height=len(job))
    for i in range(len(ed)):
        count += 1
        edBox.insert(count,ed[i])
    count = 1
    for i in range(len(job)):
        count += 1
        jobBox.insert(count,job[i])    

E = 'E'
W = 'W'
w = []
window = tkinter.Tk()
window.title("Scrape")
lang = tkinter.IntVar()

lwid = tkinter.Label(window,text='URL:')
entry = tkinter.Entry(window,width=50)
rbut = tkinter.Button(window,text='Run',
                      width=20,height=1,
                      command=lambda n = 0:showData(entry.get()))
cbut = tkinter.Button(window,text='Clear',
                      width=10,height=1,
                      command=clear)
hbut = tkinter.Button(window,text='Help',
                      width=10,height=1,
                      command=helpButton)
cb = tkinter.Checkbutton(window,text='Translate',variable=lang)
nFrame = tkinter.LabelFrame(window,text='Name',height=1,width=80)
nBox = tkinter.Listbox(nFrame,height=1,width=105)
aFrame = tkinter.LabelFrame(window,text='Age',height=1,width=80)
aBox = tkinter.Listbox(aFrame,height=1,width=105)
lFrame = tkinter.LabelFrame(window,text='Current Location',height=1,width=80)
lBox = tkinter.Listbox(lFrame,height=1,width=105)
edFrame = tkinter.LabelFrame(window,text='Education',height=1,width=105)
edBox = tkinter.Listbox(edFrame,height=1,width=105)
jobFrame = tkinter.LabelFrame(window,text='Employment',height=1,width=105)
jobBox = tkinter.Listbox(jobFrame,height=1,width=105)



setWidget()
window.mainloop()
