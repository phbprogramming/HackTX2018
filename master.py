from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename,askdirectory
from PIL import ImageTk,Image
from os import listdir
from os.path import isfile, join
from uszipcode import SearchEngine, SimpleZipcode, Zipcode
from scrapeImages import run
import imghdr

class Main:
    def askFolderName(self):
        global fileName
        global tkvar
        global root
        global popupMenu

        filePath = askdirectory()
        fileName = filePath
        # self.filePath.set(filePath)
        print(filePath)
        onlyfiles = [f for f in listdir(filePath) if (isfile(join(filePath, f)) and imghdr.what(join(filePath,f)) != None )]
        choices = onlyfiles
        tkvar.set(onlyfiles[0])
        if(popupMenu != None):
            popupMenu.destroy()
        popupMenu = OptionMenu(root, tkvar,*choices)
        popupMenu.grid(row=3,column=1)
        # link function to change dropdown
        tkvar.trace('w', change_dropdown)
        self.fileName = onlyfiles

    def begin(self):
        search = SearchEngine()
        ans = dict()
        ans['name'] = self.e1.get()
        ans['ageRange'] = [self.e2.get(),self.e3.get()]
        ans['fileName'] = self.fileName
        # converts zip code to long/lat */
        zipcode = search.by_zipcode(self.e5.get())
        ans['location'] = [zipcode.lat, zipcode.lng]
        ans['radius'] = self.e6.get()
        answer = run(ans)
        messagebox.showinfo("Results", answer)
        # print(ans)

    def __init__(self, master):
        global tkvar
        master.title("New Redcat Search:")
        self.filePath = StringVar()
        self.filePath.set("")
        Label(master, text="Enter Potential Name:").grid(row=1)
        Label(master, text="Enter Potential Age Range:").grid(row=2)
        Button(master, text ="Select Photos to Search by", command = self.askFolderName).grid(row=3)
        Label(master, textvariable=self.filePath).grid(row=3,column=1)

        Label(master, text="Select Potential Zip Code").grid(row=4)
        Label(master, text="Enter Radius of Search(km)").grid(row=5)
        Button(master, text ="Begin Search", command = self.begin).grid(row=6)

        self.e1 = Entry(master)
        self.e2 = Entry(master)
        self.e3 = Entry(master)
        self.e4 = Entry(master)
        self.e5 = Entry(master)
        self.e6 = Entry(master)

        self.e1.grid(row=1, column=1)

        self.e2.grid(row=2, column=1)
        self.e3.grid(row=2, column=2)

        self.e5.grid(row=4, column=1)
        self.e6.grid(row=5, column=1)

def change_dropdown(*args):
    global root
    global tkvar
    global img
    global fileName
    img = Image.open(join(fileName,tkvar.get()))
    img = img.resize((210, 300), Image.ANTIALIAS) #The (250, 250) is (height, width)
    img = ImageTk.PhotoImage(img)
    canvas = Canvas(root, width = img.width(), height = img.height())
    canvas.grid(row = 8)
    canvas.create_image(0, 0, anchor=NW, image=img)
    # panel = Label(root, image = img)
    # panel.grid(row=8)
    # print( tkvar.get() )
fileName = ""
img = None
popupMenu = None
root = Tk()
tkvar = StringVar(root)
root.geometry("720x460")
my_gui = Main(root)
root.mainloop()
