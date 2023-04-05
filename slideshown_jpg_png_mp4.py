from PIL import Image,ImageDraw,ImageFont
import os
import mp3mixer
import secrets
import numpy as np
import async_resize
import config

dirNameBase = "3000x2000-b" # Имя файла на выходе
dirName = config.dirName # Каталог где расположены каталоги с файлами JPG
dirMusic = config.dirMusic # Каталог с файлами музыкального фона
fileNameMp3 = config.fileNameMp3 # Файл для добавления музыкального фона
dirNameOut = config.dirNameOut # Каталог для сохранения данных
timeSeconds = config.timeSeconds # Просмотр слайдшоу в секундах на 1 фото
reklamTexts = config.reklamTexts # Рекламный текст список выбирается один текст в случайном порядке
reklamText = ""
reklamFont = "lcdnova.ttf"
reklamFontSize = 32
fileName = "" # Имя файла в который сохранять видео MP4
fileNameSnd = "" # Имя файла в который сохранять видео MP4
fullNameOut = "" # Полное имя файла
fullNameOutSnd = "" # Полное имя файла
kResize = 1

maxWidth = 2160 # Ширина видео
maxHeight = 2160 # Высота видео

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
    
def saveImagePngAsync(imageJpg,imagePng,reklamText,reklamFontSize,basewidth, baseheight):
    global async_task
    async_task.append(('python resize_image.py "'+imageJpg+'" "'+imagePng+'" "'+reklamText+'" '+str(reklamFontSize)+' '+str(basewidth)+' '+str(baseheight),))

def saveAllFilesJPGtoPNG(dirNameFiles):
    global async_task,dirNameBase,basewidth, baseheight, reklamText 

    listDirs = os.listdir(dirNameFiles)
    cntDir = 1
    for dirName in listDirs:
        dirNameFull = os.path.join(dirNameFiles,dirName) # Полное имя каталога
        if not os.path.isdir(dirNameFull):
            print(f"Not dir: {dirNameFull}")
            continue
        listDirs2 = os.listdir(dirNameFull)
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
                basewidth += 1
            if (baseheight % 2) > 0:
                baseheight += 1
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
            cntFiles = len(names) # Количество файлов
            durationVideo = cntFiles * timeSeconds # Длительность видео в секундах
            if mp3mixer.mixingMp3Files(dirMusic,fileNameMp3,durationVideo) == False:
                print("Error save mp3 file")
                return False
            cntFile = 1
            async_task.clear()
            for name in names:
                fullName = os.path.join(dirNameFull2,name)
                if not os.path.isfile(fullName):
                    continue
                fileName, fileExtension = os.path.splitext(name)
                if fileExtension.lower() != ".jpg":
                    continue
                print(f"File: {fullName}")
                fullNamePng = os.path.join(dirNameOut,str(cntFile).zfill(5) + ".png")
                print(f"File PNG: {fullNamePng}")
                #if saveImagePng(fullName,fullNamePng,reklamText,reklamFontSize)==True:
                #    cntFile += 1
                saveImagePngAsync(fullName,fullNamePng,reklamText,reklamFontSize,basewidth, baseheight)
                cntFile += 1
            async_resize.async_resize_run(async_task)    
            os.system("ffmpeg -y -r 1/"+str(timeSeconds)+" -i "+dirNameOut+"\\%05d.png -c:v libx264 -preset medium -b:v 1984k -maxrate 1984k -bufsize 3968k -vf \"fps=25,format=yuv420p\" "+fullNameOut) # Конвертировать в MP4
            os.system("del /Q "+dirNameOut+"\\*.png") # Delete all files in a directory
            if os.path.isfile(fileNameMp3):
                os.system("ffmpeg -y -i "+fullNameOut+" -i "+fileNameMp3+" -codec copy -shortest "+fullNameOutSnd) # Добавить звук в MP4
                if os.path.isfile(fullNameOutSnd):
                    os.remove(fullNameOut)
if __name__ == '__main__':
    saveAllFilesJPGtoPNG(dirName)

    