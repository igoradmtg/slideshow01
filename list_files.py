import os
dirName = "z:\\003" # Каталог для обработки файлов
textBanner = "https://github.com/igoradmtg" # Текстовый баннер
fnameCmd = "slideshow01.cmd"

def write_file_str(str) :
    global fnameCmd
    f = open(fnameCmd, 'a')
    f.write(str + '\n')
    f.close()

names = os.listdir(dirName)
# Sort file names 
names.sort()

for name in names:
    #print("File ",name)
    fullName = os.path.join(dirName,name)
    if not os.path.isdir(fullName):
        continue
    names2 = os.listdir(fullName)
    for name2 in names2:
        fullName2 = os.path.join(fullName,name2)
        if not os.path.isdir(fullName2):
            continue
        if name2.lower().find("x") == -1 :
            continue
        fileNameMp4 = name + "_" + name2 + ".mp4"
        sizeList = name2.split("x")
        widthMp4 = sizeList[0]
        heightMp4 = sizeList[1]
        strSave = f'slideshow01.py "{fullName2}" "{fileNameMp4}" "{textBanner}" "" {widthMp4} {heightMp4} 3 2'
        print(strSave)
        write_file_str(strSave)
