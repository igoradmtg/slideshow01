import subprocess
import os
import secrets

# Create loop file mp3
def saveFile(fileName,strSave):
    with open(fileName, mode = "w", encoding='utf-8', newline="\r\n") as fout:
        fout.write(strSave)

# Get leng file mp3
def getLength(inputFile):
    result = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', inputFile], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return float(result.stdout)
    
def mixingMp3Files(listDirNameFiles, fileMp3, duration = 100):
    fileList = []
    if os.path.isfile(fileMp3):
        os.remove(fileMp3)
    for dirNameFiles in listDirNameFiles:   
        listDirs = os.listdir(dirNameFiles)
        for dirFile in listDirs:
            dirFileFull = os.path.join(dirNameFiles,dirFile) # Полное имя каталога
            if os.path.isfile(dirFileFull):
                fileList.append(dirFileFull)
    randomNum = secrets.randbelow(len(fileList))        
    randomFile = fileList[randomNum]
    print(f"File random: {randomFile}")
    mp3Duration = getLength(randomFile)
    loop = int(int(duration) / mp3Duration)+2
    print(f"Video duration: {duration} File duration: {mp3Duration} Loop: {loop}")
    strSave = ""
    for i in range(0,loop):
        strSave += "file '"+randomFile+"'" + "\n"
    saveFile("files.txt",strSave)
    execCmd = "ffmpeg -y -f concat -safe 0 -i files.txt -c:a aac -vn " + fileMp3
    print(execCmd)
    os.system(execCmd)
    if os.path.isfile(fileMp3):
        return True
    else:
        return False
    
