import sys
from PIL import Image,ImageDraw,ImageFont
reklamFont = "lcdnova.ttf"
def main(imageJpg,imagePng,reklamText,reklamFontSize,basewidth, baseheight):
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
        img = original.resize((newWidth,newHeight), Image.Resampling.LANCZOS)
    except Exception as er:
        print(er)
        return False
    imageBg.paste(img,(int(basewidth / 2 - newWidth / 2),int(baseheight / 2 - newHeight / 2)))
    if (len(reklamText))>0:
        d1 = ImageDraw.Draw(imageBg)
        myFont = ImageFont.truetype(reklamFont, reklamFontSize)
        d1.text((10, 10), reklamText, fill =(255, 255, 255),font=myFont)
    imageBg.save(imagePng, format="png")
    return True

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6]))
