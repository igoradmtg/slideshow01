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
 
def set_video_size(width, height):
    """
    Set the video size.

    Args:
        width (int): The width of the video.
        height (int): The height of the video.
    """
    # Set the width and height of the video
    global W, H, SIZE, K_W_H
    W = width
    H = height
    
    # Calculate the aspect ratio of the video
    K_W_H = W / H  # Aspect ratio of width / height
    
    # Set the size of the video
    SIZE = (W, H)  # Size of the video
    
    # Print the video size
    print("Video size: {} {}".format(W, H))

def intro() :
    """
    Create an intro clip with two text clips.

    Returns:
        CompositeVideoClip: The concatenated intro clip.
    """
    # Set the duration of each text clip
    duration_intro = 2 # Duration of each text clip
    
    # Create the first text clip
    logo1 = (TextClip(txt=text_logo,color="#0000AA", align='West',fontsize=fontSizeIntro,font = 'Arial')  # Create the text clip
              .set_duration(duration_intro)  # Set the duration
              .margin(right=8, top=8, opacity=0)  # Set the margin and opacity
              .set_pos(("center","center")))  # Set the position
    logo1_clip = CompositeVideoClip([logo1.fadein(0.5,initial_color=[255,255,255]).fadeout(0.5,final_color=[255,255,255])], size=SIZE, bg_color = [255,255,255])  # Add fade-in and fade-out effects
    
    # Create the second text clip
    logo2 = (TextClip(txt="present",color="#0000AA", align='West',fontsize=fontSizeIntro,font = 'Arial')  # Create the text clip
              .set_duration(duration_intro)  # Set the duration
              .margin(right=8, top=8, opacity=0)  # Set the margin and opacity
              .set_pos(("center","center")))  # Set the position
    logo2_clip = CompositeVideoClip([logo2.fadein(0.5,initial_color=[255,255,255]).fadeout(0.5,final_color=[255,255,255])], size=SIZE, bg_color = [255,255,255])  # Add fade-in and fade-out effects
    
    # Concatenate the text clips
    return concatenate_videoclips([logo1_clip,logo2_clip])
  
def outro() :
    """
    Create an outro clip with a single text clip.

    Returns:
        CompositeVideoClip: The outro clip.
    """
    # Set the duration of the text clip
    duration_intro = 4  # Duration of the text clip

    # Create the text clip
    logo1 = (TextClip(txt=text_logo,color="#0000AA", align='West',fontsize=fontSizeIntro,font = 'Arial')  # Create the text clip
              .set_duration(duration_intro)  # Set the duration
              .margin(right=8, top=8, opacity=0)  # Set the margin and opacity
              .set_pos(("center","center")))  # Set the position
              
    # Add fade-in and fade-out effects
    return CompositeVideoClip([logo1.fadein(0.5,initial_color=[255,255,255]).fadeout(0.5,final_color=[255,255,255])], size=SIZE, bg_color = [255,255,255])
    
def calc_rotate(t, angle):
    """
    Calculate the rotational angle based on the given parameters.

    Args:
        t (float): The time value.
        angle (float): The initial angle.

    Returns:
        float: The calculated rotational angle.
    """
    # If time value is greater than 1, return 0.
    if t > 1:
        return 0
    
    # If the angle is greater than 0, calculate the rotational angle.
    if angle > 0:
        # Return the angle minus the product of time and angle.
        return angle - (t * angle)
    
    # If the angle is less than 0, calculate the rotational angle.
    elif angle < 0:
        # Return the angle minus the product of time and angle.
        return angle - (t * angle)
    
    # If the angle is 0, return 0.
    return 0
        
    

def calc_resize(t):
    """
    Calculate the resize value based on the given time value.

    Args:
        t (float): The time value.

    Returns:
        float: The calculated resize value.
    """
    # If time value is greater than 1, return 0.125.
    if (t > 1):
        return 0.125
    # Otherwise, calculate the resize value.
    else:
        # Return the difference between 0.125*2 and the product of t and 0.125.
        return (0.125 * 2) - (t * 0.125)
    
def save_clip() :
    """
    Save the clip to a file.

    This function saves the clip to a file based on the given parameters.
    It creates a list of video clips, sorts the file names, calculates the time durations,
    and appends the image clips to the clip list. If a text file is provided, it appends the
    text clips to the clip list. If a logo is provided, it appends the logo clip to the clip list.
    Finally, it saves the final clip to a file.
    """
    global dir_name, fnamemp4 , SIZE , H, image_duration , ffmpeg_params , file_name_text, text_duration
    
    clip_list = [] # Video clip
    file_names = [] # Full file names
    
    # Get file names and sort them
    names = os.listdir(dir_name)
    names.sort()
    
    # Initialize time durations
    time_start = 0 # Start clip
    time_for_image = image_duration # Time image
    time_video = 0 # Time video
    
    # Append image clips to the clip list
    for name in names:
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
    
    # Append text clips to the clip list
    if len(file_name_text)>0:
        if os.path.isfile(file_name_text) :   
            time_start = 0 # Time video
            current_h = 0
            last_h = 0
            with open(file_name_text, 'r', encoding='utf8') as fp:
                for line in fp:
                    if ((current_h+last_h)>H) :
                        current_h = 0
                    print("current_h: {} Time: {} Text: {}".format(current_h, time_start,line.strip()))
                    clip_text = (TextClip(txt=line.strip(),color="#0000AA",bg_color="rgba(255, 255, 255, 0.5)", align='West', fontsize=fontSizeIntro, font = 'Arial')
                        .set_duration(text_duration*1.8)
                        .margin(right=8, top=8, opacity=0)
                        .set_pos((text_x,current_h))
                        .set_start(time_start)
                        .crossfadein(0.5)
                        .crossfadeout(0.5)    )
                    time_start += text_duration
                    last_h = clip_text.h
                    current_h += last_h
                    clip_list.append(clip_text)
    
    # Append logo clip to the clip list
    if text_logo:
        logo = (TextClip(txt=text_logo, color='white', align='West',fontsize=fontSizeLogo,font = 'Arial-Bold').set_duration(max_time).margin(right=8, top=8, opacity=0).set_pos(("right","top")))
        clip_list.append(logo)
    
    # Create the final clip and save it to a file
    final_clip_f2 = CompositeVideoClip(clip_list, size=SIZE, bg_color = [255,255,255]).set_duration(max_time)
    
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
    """
    Main function to execute the slideshow script.

    This function sets the global variables based on the command line arguments,
    checks the number of arguments, and calls the save_clip function to create 
    and save the slideshow video.
    """
    global dir_name, fnamemp4, text_logo, file_name_text, image_duration, text_duration, save_gif

    # Check the number of arguments
    if len(sys.argv)<9:
        print("Error params")
        return

    # Set the global variables based on the command line arguments
    dir_name = sys.argv[1]
    fnamemp4 = sys.argv[2]
    text_logo = sys.argv[3]
    file_name_text = sys.argv[4]
    set_video_size(int(sys.argv[5]),int(sys.argv[6]))
    image_duration = int(sys.argv[7])
    text_duration = int(sys.argv[8])
    print("Argument:",len(sys.argv))

    # Check if the optional argument is provided
    if (len(sys.argv)>9):
        if sys.argv[9] == "gif":
            save_gif = True

    # Create and save the slideshow video
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