from PIL import Image,ImageDraw,ImageFont
import os
import mp3mixer
import secrets
import numpy as np
import async_resize
import sys

dirNameBase = "3000x2000-b" # Имя файла на выходе
dirName = r"z:\001\img" # Каталог где расположены каталоги с файлами JPG
# Каталог с файлами музыка
dirMusic = [r"Z:\music\muz1", 
    r"Z:\music\muz2", 
    r"Z:\music\muz3", 
    r"Z:\music\muz4", 
    r"Z:\music\muz5"] 
fileNameMp3 = r"output.m4a" # Файл для добавления звука
dirNameOut = r"z:\001\Out_slide"
timeSeconds = 5 # Просмотр слайдшоу в секундах на 5 фото
reklamTexts = []

reklamText = ""
reklamFont = "lcdnova.ttf"
reklamFontSize = 32
fileName = "" # Имя файла в который сохранять видео MP4
fileNameSnd = "" # Имя файла в который сохранять видео MP4
fullNameOut = "" # Полное имя файла
fullNameOutSnd = "" # Полное имя файла
kResize = 1
maxThreads = 4 # Количество потоков преобразования файлов

maxWidth = 1920 # Ширина видео
maxHeight = 1080 # Высота видео

async_task = [] # Список для асинхронного изменения размеров

# ffmpeg -r 1/5 -i %05d.png -c:v libx264 -vf "fps=25,format=yuv420p" SecretStars-MichelleSS-011-slide.mp4
def setFileName():
    global dirNameBase,fileName,fileNameSnd,fullNameOut,fullNameOutSnd
    fileName = dirNameBase + "_nosound.mp4" # Имя файла в который сохранять видео MP4
    fileNameSnd = dirNameBase + "_sl.mp4" # Имя файла в который сохранять видео MP4
    fullNameOut = os.path.join(dirNameOut,fileName)
    fullNameOutSnd = os.path.join(dirNameOut,fileNameSnd)


def saveImagePng(imageJpg,imagePng,reklamText,reklamFontSize):
    original = Image.open(imageJpg)
    try:
        original.verify()
    except Exception as er:
        print("Error open image ")
        print(er)
        return False
    original = Image.open(imageJpg)
    imageBg = Image.new('RGB', (basewidth, baseheight), (0, 0, 0))
    wpercent = (basewidth/float(original.size[0]))
    hpercent = (baseheight/float(original.size[1]))
    hsize = int((float(original.size[1])*float(wpercent)))
    wsize = int((float(original.size[0])*float(hpercent)))
    print(f"{wpercent} {hpercent} {wsize} {hsize} Base: {basewidth} x {baseheight}")
    if (hsize<=baseheight):
        newWidth = basewidth
        newHeight = hsize
    else:
        newWidth = wsize
        newHeight = baseheight
    try:    
        img = original.resize((newWidth,newHeight), Image.ANTIALIAS)
    except Exception as er:
        print(er)
        return False
    imageBg.paste(img,(int(basewidth / 2 - newWidth / 2),int(baseheight / 2 - newHeight / 2)))
    if (len(reklamText))>0:
        d1 = ImageDraw.Draw(imageBg)
        # Font selection from the downloaded file
        myFont = ImageFont.truetype(reklamFont, reklamFontSize)
        # Decide the text location, color and font
        d1.text((10, 10), reklamText, fill =(255, 255, 255),font=myFont)
    imageBg.save(imagePng, format="png")
    return True
    
def saveImagePngAsync(imageJpg,imagePng,reklamText,reklamFontSize,basewidth, baseheight, saveBgImage):
    global async_task
    async_task.append(('python resize_image.py "'+imageJpg+'" "'+imagePng+'" "'+reklamText+'" '+str(reklamFontSize)+' '+str(basewidth)+' '+str(baseheight)+' '+str(saveBgImage),))

def saveAllFilesJPGtoPNG(dirNameFiles):
    global async_task,dirNameBase,basewidth, baseheight, reklamText 

    listDirs = os.listdir(dirNameFiles)
    cntDir = 1
    names3 = []
    names2 = []
    for dirName in listDirs:
        dirNameFull = os.path.join(dirNameFiles,dirName) # Полное имя каталога
        if not os.path.isdir(dirNameFull):
            print(f"Not dir: {dirNameFull}")
            continue
        listDirs2 = os.listdir(dirNameFull)
        numDir = 1
        countFilesInDir1 = 0 # Количество файлов в первом каталоге
        listFiles1 = [] # Список файлов в первом каталоге
        nameDir1 = '' # Имя первого каталога
        nameDir1Base = ''
        countFilesInDir2 = 0 # Количество файлов во втором каталоге
        listFiles2 = [] # Список файлов во втором каталоге
        nameDir2 = '' # Имя второго каталога
        nameDir2Base = ''
        for dirName2 in listDirs2:
            if len(reklamTexts)>0:
                cntReklam = secrets.randbelow(len(reklamTexts))         
                reklamText = reklamTexts[cntReklam]

            dirNameFull2 = os.path.join(dirNameFull,dirName2) # Полное имя каталога
            if not os.path.isdir(dirNameFull2):
                continue
            os.system("del /Q "+dirNameOut+"\\*.png") # Delete all files in a directory
            listDirName = dirName2.split("x")
            if len(listDirName)<2:
                print(f"Error dir name: {dirNameFull2}")
                continue
            kResizeW = maxWidth / int(listDirName[0]) # Коэффициент по ширине 2000 / 1000 = 2 2000 / 3000 = 0,667 
            kResizeH = maxHeight / int(listDirName[1]) # Коэффициент по ширине 2000 / 1000 = 2 2000 / 3000 = 0,667 
            if kResizeW<kResizeH:
                kResize = kResizeW # По ширине
            else:
                kResize = kResizeH # По высоте
            if kResize>1:
                kResize=1 # Уменьшать можно, увеличивать нельзя
            basewidth = int(int(listDirName[0]) * kResize) # Коэффициент уменьшения
            baseheight = int(int(listDirName[1]) * kResize) # Коэффициент уменьшения
            if (basewidth % 2) > 0:
                basewidth -= 1
            if (baseheight % 2) > 0:
                baseheight -= 1
            print(f"Dir name: {dirNameFull2} Size: {basewidth} x {baseheight} Reklam: {reklamText}")    
            dirNameBase = dirName + "_" + str(basewidth) + "x" + str(baseheight)
            setFileName()
            print(f"File save: {fullNameOutSnd}")
            cntDir += 1
            if os.path.isfile(fullNameOutSnd):
                print(f"File exists: {fullNameOutSnd}")
                continue
            names = os.listdir(dirNameFull2)
            names.sort()
            if numDir == 1:
                countFilesInDir1 = len(names) # Количество файлов в первом каталоге
                listFiles1 = names[:]
                nameDir1 = dirNameFull2
                nameDir1Base = dirName2 
                numDir = 2
            elif numDir == 2:
                countFilesInDir2 = len(names) # Количество файлов во втором каталоге
                listFiles2 = names[:]
                nameDir2 = dirNameFull2
                nameDir2Base = dirName2 
                numDir = 3
                    
            cntFiles = len(names) # Количество файлов
            durationVideo = cntFiles * timeSeconds # Длительность видео в секундах
            #if mp3mixer.mixingMp3Files(dirMusic,fileNameMp3,durationVideo) == False:
            #    print("Error save mp3 file")
            #    return False
            cntFile = 1
            names2 = []
            names3.clear()
            cntNames3 = 0
            for name in names:
                fullName = os.path.join(dirNameFull2,name)
                if not os.path.isfile(fullName):
                    continue
                fileName, fileExtension = os.path.splitext(name)
                if fileExtension.lower() != ".jpg" and fileExtension.lower() != ".png" and fileExtension.lower() != ".jpeg":
                    continue
                names3.append(name)
                cntNames3 += 1
                if cntNames3 >= maxThreads:
                    cntNames3 = 0
                    names2.append(names3.copy())
                    names3.clear()
            if len(names3)>0:
                names2.append(names3.copy())
                names3.clear()
            print(names2)        
            for listNames in names2:     
                async_task.clear()
                for name in listNames:
                    fullName = os.path.join(dirNameFull2,name)
                    if not os.path.isfile(fullName):
                        continue
                    fileName, fileExtension = os.path.splitext(name)
                    if fileExtension.lower() != ".jpg" and fileExtension.lower() != ".png" and fileExtension.lower() != ".jpeg":
                        continue
                    print(f"File: {fullName}")
                    fullNamePng = os.path.join(dirNameOut,str(cntFile).zfill(5) + ".png")
                    print(f"File PNG: {fullNamePng}")
                    #if saveImagePng(fullName,fullNamePng,reklamText,reklamFontSize)==True:
                    #    cntFile += 1
                    saveImagePngAsync(fullName,fullNamePng,reklamText,reklamFontSize,basewidth, baseheight,"0")
                    cntFile += 1
                async_resize.async_resize_run(async_task)
            
            # Конвертировать в MP4    
            strExec = "ffmpeg -y -r 1/"+str(timeSeconds)+" -i "+dirNameOut+"\\%05d.png -c:v libx264 -preset medium -b:v 8192k -maxrate 8192k -bufsize 8192k -vf \"fps=60,format=yuv420p\" "+fullNameOut
            print(f"Execute: {strExec}")
            os.system(strExec) 
            
            # Delete all files in a directory
            strExec = "del /Q "+dirNameOut+"\\*.png"
            print(f"Execute: {strExec}")
            os.system(strExec) 
            
            if os.path.isfile(fileNameMp3):
                os.system("ffmpeg -y -i "+fullNameOut+" -i "+fileNameMp3+" -codec copy -shortest "+fullNameOutSnd) # Добавить звук в MP4
                if os.path.isfile(fullNameOutSnd):
                    os.remove(fullNameOut)
            if numDir == 3:
                if countFilesInDir1>countFilesInDir2:
                    listDirName = nameDir1Base.split("x")
                else:
                    listDirName = nameDir2Base.split("x")
                    
                if len(listDirName)<2:
                    print(f"Error dir name: {nameDir1Base} {nameDir2Base}")
                    continue
                kResizeW = maxWidth / int(listDirName[0]) # Коэффициент по ширине 2000 / 1000 = 2 2000 / 3000 = 0,667 
                kResizeH = maxHeight / int(listDirName[1]) # Коэффициент по ширине 2000 / 1000 = 2 2000 / 3000 = 0,667 
                if kResizeW<kResizeH:
                    kResize = kResizeW # По ширине
                else:
                    kResize = kResizeH # По высоте
                if kResize>1:
                    kResize=1 # Уменьшать можно, увеличивать нельзя
                basewidth = int(int(listDirName[0]) * kResize) # Коэффициент уменьшения
                baseheight = int(int(listDirName[1]) * kResize) # Коэффициент уменьшения
                if (basewidth % 2) > 0:
                    basewidth -= 1
                if (baseheight % 2) > 0:
                    baseheight -= 1
                print(f"Dir name: {dirNameFull2} Size: {basewidth} x {baseheight} Reklam: {reklamText}")    
                dirNameBase = dirName + "_" + str(basewidth) + "x" + str(baseheight) + "fl"
                setFileName()
                print(f"File save: {fullNameOut} {fullNameOutSnd}")
                cntFiles = len(listFiles1) + len(listFiles2) # Количество файлов
                durationVideo = cntFiles * timeSeconds # Длительность видео в секундах
                if mp3mixer.mixingMp3Files(dirMusic,fileNameMp3,durationVideo) == False:
                    print("Error save mp3 file")
                    return False
                cntFile = 1
                listFilesAll = listFiles1 + listFiles2
                listFilesAll.sort()
                names2.clear()
                names3.clear()
                cntNames3 = 0
                for name in listFilesAll:
                    fileName, fileExtension = os.path.splitext(name)
                    if fileExtension.lower() != ".jpg" and fileExtension.lower() != ".png" and fileExtension.lower() != ".jpeg":
                        continue
                    fullName = os.path.join(nameDir1,name)
                    if os.path.isfile(fullName):
                        names3.append(name)
                        cntNames3 += 1
                    fullName = os.path.join(nameDir2,name)
                    if os.path.isfile(fullName):
                        names3.append(name)
                        cntNames3 += 1
                    if cntNames3 >= maxThreads:
                        cntNames3 = 0
                        names2.append(names3.copy())
                        names3.clear()
                if len(names3)>0:
                    names2.append(names3.copy())
                    names3.clear()
                print(names2)        
                
                for listNames in names2:
                    async_task.clear()
                    for name in listNames:
                        fullName = os.path.join(nameDir1,name)
                        if os.path.isfile(fullName):
                            fileName, fileExtension = os.path.splitext(name)
                            if fileExtension.lower() != ".jpg" and fileExtension.lower() != ".png" and fileExtension.lower() != ".jpeg":
                                continue
                            print(f"File: {fullName}")
                            fullNamePng = os.path.join(dirNameOut,str(cntFile).zfill(5) + ".png")
                            print(f"File PNG: {fullNamePng}")
                            saveImagePngAsync(fullName,fullNamePng,reklamText,reklamFontSize,basewidth, baseheight, "1")
                            cntFile += 1
                        fullName = os.path.join(nameDir2,name)
                        if os.path.isfile(fullName):
                            fileName, fileExtension = os.path.splitext(name)
                            if fileExtension.lower() != ".jpg" and fileExtension.lower() != ".png" and fileExtension.lower() != ".jpeg":
                                continue
                            print(f"File: {fullName}")
                            fullNamePng = os.path.join(dirNameOut,str(cntFile).zfill(5) + ".png")
                            print(f"File PNG: {fullNamePng}")
                            saveImagePngAsync(fullName,fullNamePng,reklamText,reklamFontSize,basewidth, baseheight, "1")
                            cntFile += 1
                    async_resize.async_resize_run(async_task)    
                
                # Конвертировать в MP4
                strExec = "ffmpeg -y -r 1/"+str(timeSeconds)+" -i "+dirNameOut+"\\%05d.png -c:v libx264 -preset medium -b:v 8192k -maxrate 8192k -bufsize 8192k -vf \"fps=60,format=yuv420p\" "+fullNameOut    
                print(f"Execute: {strExec}")
                os.system(strExec) 
                
                # Delete all files in a directory
                strExec = "del /Q "+dirNameOut+"\\*.png"
                print(f"Execute: {strExec}")
                os.system(strExec) 
                if os.path.isfile(fileNameMp3):
                    os.system("ffmpeg -y -i "+fullNameOut+" -i "+fileNameMp3+" -codec copy -shortest "+fullNameOutSnd) # Добавить звук в MP4
                    if os.path.isfile(fullNameOutSnd):
                        os.remove(fullNameOut)
                
                    
                    
if __name__ == '__main__':
    maxWidth = int(sys.argv[1]) # Ширина видео
    maxHeight = int(sys.argv[2]) # Высота видео
    saveAllFilesJPGtoPNG(dirName)

    