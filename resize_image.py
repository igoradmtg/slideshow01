import sys
from PIL import Image,ImageDraw,ImageFont,ImageFilter,ImageEnhance
reklamFont = "lcdnova.ttf"

def main(imageJpg,imagePng,reklamText,reklamFontSize,basewidth, baseheight, addBgImage):
    original = Image.open(imageJpg)
    try:
        original.verify()
    except Exception as er:
        print("Error open image ")
        print(er)
        return False
    original = Image.open(imageJpg)
    imageBg = Image.new('RGB', (basewidth, baseheight), (255, 255, 255))
    wpercent = (basewidth/float(original.size[0]))
    hpercent = (baseheight/float(original.size[1]))
    hsize = int((float(original.size[1])*float(wpercent)))
    wsize = int((float(original.size[0])*float(hpercent)))
    if (hsize<=baseheight):
        newWidth = basewidth
        newHeight = hsize
    else:
        newWidth = wsize
        newHeight = baseheight
    if (hsize<=baseheight):
        newWidthBg = wsize
        newHeightBg = baseheight
    else:
        newWidthBg = basewidth
        newHeightBg = hsize
    print(f"{wpercent} {hpercent} {wsize} {hsize} Base: {basewidth} x {baseheight}")
    if (addBgImage=="1"):
        try:    
            enhancer = ImageEnhance.Brightness(original)
            imgBgBrigtness = enhancer.enhance(1.5)
            imgBg = imgBgBrigtness.filter(ImageFilter.GaussianBlur(radius = 30)) 
            imgBgResize = imgBg.resize((newWidthBg,newHeightBg), Image.Resampling.LANCZOS)
        except Exception as er:
            print(er)
            return False
        
    try:    
        img = original.resize((newWidth,newHeight), Image.Resampling.LANCZOS)
    except Exception as er:
        print(er)
        return False
    if (addBgImage == "1"):    
        imageBg.paste(imgBgResize,(int(basewidth / 2 - newWidthBg / 2),int(baseheight / 2 - newHeightBg / 2)))    
        
    imageBg.paste(img,(int(basewidth / 2 - newWidth / 2),int(baseheight / 2 - newHeight / 2)))
    if (len(reklamText))>0:
        d1 = ImageDraw.Draw(imageBg)
        myFont = ImageFont.truetype(reklamFont, reklamFontSize)
        d1.text((10, 10), reklamText, fill =(255, 255, 255),font=myFont)
    imageBg.save(imagePng, format="png")
    return True

def resize_width_height(imageJpg,imagePng,reklamText,reklamFontSize,basewidth, baseheight, addBgImage):
    original = Image.open(imageJpg)
    try:
        original.verify()
    except Exception as er:
        print("Error open image ")
        print(er)
        return False
    original = Image.open(imageJpg)
    
    wpercent = (basewidth/float(original.size[0]))
    hpercent = (baseheight/float(original.size[1]))
    
    if (wpercent<=hpercent):
        hsize = int((float(original.size[1])*float(hpercent))) # 100
        wsize = int((float(original.size[0])*float(hpercent))) # 200
        basewidth = wsize
        baseheight = hsize
    else:
        hsize = int((float(original.size[1])*float(wpercent))) # 100
        wsize = int((float(original.size[0])*float(wpercent))) # 200

    basewidth = wsize
    baseheight = hsize
    newWidth = basewidth
    newHeight = baseheight
    
    imageBg = Image.new('RGB', (basewidth, baseheight), (255, 255, 255))
    print(f"{wpercent} {hpercent} {wsize} {hsize} Base: {basewidth} x {baseheight}")
    if (addBgImage=="1"):
        try:    
            enhancer = ImageEnhance.Brightness(original)
            imgBgBrigtness = enhancer.enhance(1.5)
            imgBg = imgBgBrigtness.filter(ImageFilter.GaussianBlur(radius = 30)) 
            imgBgResize = imgBg.resize((newWidthBg,newHeightBg), Image.Resampling.LANCZOS)
        except Exception as er:
            print(er)
            return False
        
    try:    
        img = original.resize((newWidth,newHeight), Image.Resampling.LANCZOS)
    except Exception as er:
        print(er)
        return False
    if (addBgImage == "1"):    
        imageBg.paste(imgBgResize,(int(basewidth / 2 - newWidthBg / 2),int(baseheight / 2 - newHeightBg / 2)))    
        
    imageBg.paste(img,(int(basewidth / 2 - newWidth / 2),int(baseheight / 2 - newHeight / 2)))
    if (len(reklamText))>0:
        d1 = ImageDraw.Draw(imageBg)
        myFont = ImageFont.truetype(reklamFont, reklamFontSize)
        d1.text((10, 10), reklamText, fill =(255, 255, 255),font=myFont)
    imageBg.save(imagePng, format="png")
    return True

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6]), str(sys.argv[7]))
