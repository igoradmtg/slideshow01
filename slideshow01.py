# -*- coding: utf-8 -*-
import os
import sys
from moviepy.editor import *
from moviepy.editor import TextClip,VideoFileClip, concatenate_videoclips

dir_name = "" 
fnamemp4 = "File.mp4"
text_logo = "" # Текст для интро и аутро
#fontSizeIntro = 80 # Размер шрифта для интро и аутро
#W = 1920 # clip width 1920
#H = 1080 # clip height 1080 
fontSizeIntro = 20 # Размер шрифта для интро и аутро
fontSizeLogo = 24 # Размер шрифта для логотипа вверхний правый угол
W = 1920 # Default clip width 1280
H = 1080 # Default clip height 720 
ffmpeg_params = ['-crf', '17']    
DW = 1 # 1 - Up  2 - Down
DH = 1 # 1 - Left 2 - Right
K_W_H = W / H # Коэффициент ширина и высота 1920 / 1080 = 1,77777
SIZE = (W, H) # Размер видео
IMAGE_CROSSFIDE = 0.4 # Количество секунд для эффекта перехода
image_duration = 2 # Image duration
text_duration = 2 # Text duration
file_name_text = "" # Text file 
text_x = 10 # Text position X, int or 'center'
save_gif = False
audio_file = "Z:/vid/m4a/tmp3.m4a" # Имя файла для добавления аудио
ffmpeg_cmd = "ffmpeg"
 
def set_video_size(width,height) :
    global W,H,SIZE,K_W_H
    W = width
    H = height
    K_W_H = W / H # Коэффициент ширина и высота 1920 / 1080 = 1,77777
    SIZE = (W, H) # Размер видео
    print("Video size ",W,H)

def intro() :
    global text_logo, SIZE, fontSizeIntro
    duration_intro = 2 # Длительность каждого текстового клипа
    logo1 = (TextClip(txt=text_logo,color="#0000AA", align='West',fontsize=fontSizeIntro,font = 'Arial').set_duration(duration_intro).margin(right=8, top=8, opacity=0).set_pos(("center","center"))) # (optional) logo-border padding.set_pos(("right","top")))
    logo1_clip = CompositeVideoClip([logo1.fadein(0.5,initial_color=[255,255,255]).fadeout(0.5,final_color=[255,255,255])], size=SIZE, bg_color = [255,255,255])  
    logo2 = (TextClip(txt="present",color="#0000AA", align='West',fontsize=fontSizeIntro,font = 'Arial').set_duration(duration_intro).margin(right=8, top=8, opacity=0).set_pos(("center","center"))) # (optional) logo-border padding.set_pos(("right","top")))
    logo2_clip = CompositeVideoClip([logo2.fadein(0.5,initial_color=[255,255,255]).fadeout(0.5,final_color=[255,255,255])], size=SIZE, bg_color = [255,255,255])  
    return concatenate_videoclips([logo1_clip,logo2_clip])
  
def outro() :
    global text_logo, SIZE, fontSizeIntro
    duration_intro = 4 # Длительность каждого текстового клипа
    logo1 = (TextClip(txt=text_logo,color="#0000AA", align='West',fontsize=fontSizeIntro,font = 'Arial').set_duration(duration_intro).margin(right=8, top=8, opacity=0).set_pos(("center","center"))) # (optional) logo-border padding.set_pos(("right","top")))
    return CompositeVideoClip([logo1.fadein(0.5,initial_color=[255,255,255]).fadeout(0.5,final_color=[255,255,255])], size=SIZE, bg_color = [255,255,255])
    
def calc_rotate(t,angle):
    if (t>1):
        return 0
    if angle>0:
        #print("1 ",angle-(t*angle))
        return angle-(t*angle)
    elif angle<0:
        #print("2 ",angle-(t*angle))
        return angle-(t*angle)
    return 0
        
    

def calc_resize(t):
    if (t>1):
        return 0.125
    else :
        return (0.125*2)-(t*0.125)
    
def save_clip() :
    global dir_name, fnamemp4 , SIZE , H, image_duration , ffmpeg_params , file_name_text, text_duration
    clip_list = [] # Video clip
    file_names = [] # Full file names
    names = os.listdir(dir_name)
    # Sort file names 
    names.sort()
    time_start = 0 # Start clip
    time_for_image = image_duration # Time image
    time_video = 0 # Time video
    for name in names:
        #print("File ",name)
        if name.lower().find(".jpg") == -1 :
            print("Continue ",name) # Continue
            continue
        fullname = os.path.join(dir_name, name) # Get full file name
        if not os.path.isfile(fullname) :
            print("Not found file ",fullname)
            continue
        print(fullname)
        file_names.append(fullname)
        
    time_video = time_for_image * (len(file_names) + 1)    
    for name in file_names:
        clip = ImageClip(name).set_duration(time_for_image + 1)
        clip_w = clip.w # Clip width
        clip_h = clip.h # Clip height
        clip = clip.resize(height=H).set_start(time_start).crossfadein(IMAGE_CROSSFIDE)
        clip_list.append(clip)
        time_start += time_for_image
    max_time = time_start
    
    if len(file_name_text)>0:
        if os.path.isfile(file_name_text) :    
            time_start = 0 # Time video
            current_h = 0
            last_h = 0
            with open(file_name_text, 'r', encoding='utf8') as fp:
                for line in fp:
                    #if not line :
                    #    continue
                    if ((current_h+last_h)>H) :
                        current_h = 0
                    print("current_h: {} Time: {} Text: {}".format(current_h, time_start,line.strip()))
                    clip_text = (TextClip(txt=line.strip(),color="#0000AA",bg_color="rgba(255, 255, 255, 0.5)", align='West', fontsize=fontSizeIntro, font = 'Arial')
                        .set_duration(text_duration*1.8)
                        .margin(right=8, top=8, opacity=0)
                        .set_pos((text_x,current_h))
                        .set_start(time_start)
                        #.resize(lambda t: calc_resize(t))
                        #.rotate(lambda t: calc_rotate(t,angle[cnt_angle]), resample = 'bilinear')
                        .crossfadein(0.5)
                        .crossfadeout(0.5)    )
                         # (optional) logo-border padding.set_pos(("right","top")))
                    time_start += text_duration
                    last_h = clip_text.h
                    current_h += last_h
                    clip_list.append(clip_text)
    # Add logo
    if text_logo:
        logo = (TextClip(txt=text_logo, color='white', align='West',fontsize=fontSizeLogo,font = 'Arial-Bold').set_duration(max_time).margin(right=8, top=8, opacity=0).set_pos(("right","top")))
        # Создаем клип с наложенным логотипом
        clip_list.append(logo)
    final_clip_f2 = CompositeVideoClip(clip_list, size=SIZE, bg_color = [255,255,255]).set_duration(max_time)         
    # Сохранение клипа в файл
    if save_gif == True:
        final_clip_f2.write_gif(fnamemp4, fps=10)
    else:
        final_clip_f2.write_videofile(fnamemp4, preset = "veryslow",  ffmpeg_params = ffmpeg_params, fps=30, threads=4, audio = False)
    if len(audio_file)>0:    
        fnamemp4Sound = fnamemp4.replace(".mp4","")+"_snd.mp4"
        myCmd = ffmpeg_cmd +' -y -i '+fnamemp4+' -i '+audio_file+' -codec copy -shortest '+fnamemp4Sound
        print(f"Execute: {myCmd}")
        os.system(myCmd)
        

def main() : 
    global dir_name, fnamemp4, text_logo, file_name_text, image_duration, text_duration, save_gif
    if len(sys.argv)<9:
        print("Error params")
        return
    dir_name = sys.argv[1]
    fnamemp4 = sys.argv[2]
    text_logo = sys.argv[3]
    file_name_text = sys.argv[4]
    set_video_size(int(sys.argv[5]),int(sys.argv[6]))
    image_duration = int(sys.argv[7])
    text_duration = int(sys.argv[8])
    print("Argument:",len(sys.argv))
    if (len(sys.argv)>9):
        if sys.argv[9] == "gif":
            save_gif = True
    save_clip()
  
if __name__ == "__main__":
    main()  
# slideshow.py dir_images filename.mp4 text_logo file_name_text width height image_duration text_duration
# slideshow.py img filename.mp4 "Hello world" text_video.txt 400 600 3 2
# slideshow.py img filename.mp4 "Hello world" text_video.txt 400 600 3 2
# slideshow.py img2 example.gif "igoradmtg" text_video.txt 300 200 3 2 gif
# slideshow.py "Z:\001\MonikaD09\1200x1800" example.mp4 "" "" 1200 1800 3 2
# Объединение файлов:
# file '/path/to/file1'
# file '/path/to/file2'
# file '/path/to/file3'
# ffmpeg -f concat -safe 0 -i mylist.txt -c copy output.mp4