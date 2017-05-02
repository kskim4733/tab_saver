from subprocess import Popen, PIPE
import os
import webbrowser
from tkinter import *
import tkinter.messagebox
from tkinter import filedialog

def create_raw_list():
    cmd = "/usr/bin/osascript -e 'tell application \"Safari\"' -e 'get URL of every tab of every window' -e 'end tell'"
    pipe = Popen(cmd, shell=True, stdout=PIPE).stdout
    raw = pipe.readlines()
    urls = str(raw)
    urls = (urls.split(","))
    url_list=[]
    #filter
    for url in urls:
        if "http" in url:
            if "[b'" in url:
                url_list.append(url[3:])
            else:
                if "\n']" in url:
                    url_list.append(url[1:].strip("\n']"))
                url_list.append(url[1:])


    return url_list
def create_file(tabs):
    current_directory = os.getcwd()
    if not os.path.exists(current_directory+"/saved_tabs"):
        os.makedirs((current_directory+"/saved_tabs"))

    urls = tabs
    textfile = tkinter.filedialog.asksaveasfile(mode='w', defaultextension=".txt")
    for item in urls:
        textfile.writelines(item)
        textfile.writelines("\n")
    textfile.close()
    tkinter.messagebox.showinfo("Tabs Saved", "Tabs are now Saved")
def save_tabs():
    urls = create_raw_list()
    create_file(urls)
def reopen_tabs():
    chosen_file = tkinter.filedialog.askopenfilename()
    print(chosen_file)
    saved_tabs = open((chosen_file),"r")
    saved_tabs = saved_tabs.readlines()
    tabs_list=[]
    #putting tabs into arrays
    for url in saved_tabs:
        if url != "\n":
            tabs_list.append(url.strip("\n"))
    #reopening tabs
    for tab in tabs_list:
        webbrowser.get('safari').open_new_tab(tab)

def graphic():
    master = Tk()
    master.title("Web Tabs Saver")
    master.call('wm', 'attributes', '.', '-topmost', '1')
    #^put my app on top
    save_button = Button(master, text="Save Current Tabs", command=save_tabs)
    reopen_button = Button(master, text="Reopen Saved Tabs", command=reopen_tabs)
    save_button.pack()
    reopen_button.pack()


    mainloop()



graphic()

