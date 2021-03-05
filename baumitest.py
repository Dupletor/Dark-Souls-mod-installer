path = "A:/SteamLibrary/steamapps/common/Dark Souls Prepare to Die Edition/"
path = "C:/Program Files (x86)/Steam/steamapps/common/Dark Souls Prepare to Die Edition/"

import cv2
import numpy as np
import os
import zipfile
import shutil
from shutil import copyfile
from shutil import copyfileobj

# initialize the list of reference points and boolean indicating
# whether cropping is being performed or not
refPt = []
cropping = False

buttons = []
names = []

def extract(p, head, location, depth):
        if depth <= 3:
                if os.path.isdir(location + p):
                        files = os.listdir(location + p)
                        for file in files:
                                if not os.path.isfile(file):
                                        if((location + p)[-1] != '/'):
                                                extract(file, head, location + p + '/', depth+1)
                                        else:
                                                extract(file, head, location + p, depth+1)                                        #try:
                                        if(not os.path.exists(head + p)):                                                #if(depth != 0):
                                                shutil.copytree(location + p, head + p, depth+1)
                                        #except:
                                                #        print(location + p)
                                        #        continue
                else:
                        shutil.copy(location + p, head)
        

def click(event, x, y, flags, param):
        # grab references to the global variables
        global refPt, cropping
	# if the left mouse button was clicked, record the starting
	# (x, y) coordinates and indicate that cropping is being
        # performed
        if event == cv2.EVENT_LBUTTONDOWN:
                for button in range(len(buttons)):
                        if(x >= 5 and x <= 50 and y >= button*50+5 and y <= button*50 + 45):
                                buttons[button] = not buttons[button]
                                zip_ref = zipfile.ZipFile("mods/" + names[button], 'r')
                                zip_names = []
                                
                                print(zip_ref.namelist())
                                
                                for name in zip_ref.namelist():
                                        if not name.endswith('/'):
                                                i = len(name) - 2
                                                while(i >= 0):
                                                        if(name[i] == "/"):
                                                                zip_names.append(name[i+1:])
                                                                break
                                                        i-=1
                                #print(zip_names)
                                
                                if(buttons[button]):

                                        files_to_backup = os.listdir(path + "DATA")
                                        if(not os.path.exists(path + "backup")):
                                                os.mkdir(path + "backup")
                                        
                                        for file in files_to_backup:
                                                if(file in zip_names):
                                                        copyfile(path + "DATA/" + file, path + "backup/" + file)
                                        for name in zip_names:
                                                for file in zip_ref.namelist():
                                                        if name in file:
                                                                target = open(path + "DATA/" + name, "wb")
                                                                copyfileobj(zip_ref.open(file), target)
                                                                target.close()
                                        zip_ref.extractall(path + "DATA/")
                                        extract(zip_ref.namelist()[0], path + "DATA/", path + "DATA/", 0)
                                        #for file in zip_ref.namelist():
                                        #        for name in zip_names:
                                        #                if name in file:
                                        #                        copyfile(path + "DATA/" + names[button] + "/" + file, path + "DATA/" + name)
                                else:
                                        #print(zip_ref.namelist())
                                        for file in (os.listdir(path + "DATA/")):
                                                #print(file)
                                                
                                                for name in zip_ref.namelist():
                                                        if(file in name):
                                                                try:
                                                                        os.remove(path + "DATA/" + file)
                                                                except:
                                                                        try:
                                                                                shutil.rmtree(path + "DATA/" + file + "/")
                                                                        except:
                                                                                continue
                                                                        continue
                                        files_to_backup = os.listdir(path + "backup")
                                        for file in files_to_backup:
                                                copyfile(path + "backup/" + file, path + "DATA/" + file)
                                                os.remove(path + "backup/" + file)
                                        
                
                                        
	# check to see if the left mouse button was released
img = np.ones([50, 500, 3],dtype=np.uint8)*255
cv2.namedWindow('Dark Souls mod installer')
cv2.setMouseCallback('Dark Souls mod installer', click)
cv2.imshow('Dark Souls mod installer', img)
cv2.waitKey(1)


font                   = cv2.FONT_HERSHEY_SIMPLEX
fontScale              = 1
fontColor              = (0,0,0)
lineType               = 2

buttons = []
names = []
while(True):
        files = os.listdir("mods")
        img = np.ones([50*len(files), 500, 3],dtype=np.uint8)*255

        for file in range(len(files)):
                if(not files[file] in names):
                        buttons.insert(file, False)
                        names.insert(file, files[file])
                if(not buttons[file]):
                        cv2.rectangle(img, (5, file*50 + 5), (50, file*50 + 45), (0,0,255), -1)
                else:
                        cv2.rectangle(img, (5, file*50 + 5), (50, file*50 + 45), (0,255,0), -1)
                
                bottomLeftCornerOfText = (50,file*50 + 35)
                cv2.putText(img, files[file], 
                            bottomLeftCornerOfText, 
                            font, 
                            fontScale,
                            fontColor,
                            lineType)
        if(cv2.getWindowProperty('Dark Souls mod installer', 0) >= 0):
                cv2.imshow('Dark Souls mod installer', img)
        else:
                cv2.destroyAllWindows()
                break
                
        cv2.waitKey(1)

