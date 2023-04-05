from PIL import Image
import numpy, cv2
# Imports can be found in the "Imports" section above

# Load up the first and second demo images, assumed is that image1 and image2 both share the same height and width
image1 = Image.open("001.png")
image2 = Image.open("002.png")
image3 = Image.open("003.png")
maxtime = 200
# Grab the stats from image1 to use for the resultant video
height, width, layers =  numpy.array(image1).shape
print(height, width)
# Create the OpenCV VideoWriter
fourcc_str="mp4v"
fourcc = cv2.VideoWriter_fourcc(*fourcc_str)
video = cv2.VideoWriter("demo001_002.mp4", # Filename
                        fourcc, # Negative 1 denotes manual codec selection. You can make this automatic by defining the "fourcc codec" with "cv2.VideoWriter_fourcc"
                        10, # 10 frames per second is chosen as a demo, 30FPS and 60FPS is more typical for a YouTube video
                        (width,height) # The width and height come from the stats of image1
                        )

# We'll have 30 frames be the animated transition from image1 to image2. At 10FPS, this is a whole 3 seconds
for i in range(0,maxtime):
    imagestmp = Image.blend(image1, image2, i/maxtime)
    # Conversion from PIL to OpenCV from: http://blog.extramaster.net/2015/07/python-converting-from-pil-to-opencv-2.html
    video.write(cv2.cvtColor(numpy.array(imagestmp), cv2.COLOR_RGB2BGR))

for i in range(0,maxtime):
    video.write(cv2.cvtColor(numpy.array(image2), cv2.COLOR_RGB2BGR))
    
# And back from image2 to image3
for i in range(0,maxtime):
    imagestmp = Image.blend(image2, image3, i/maxtime)
    video.write(cv2.cvtColor(numpy.array(imagestmp), cv2.COLOR_RGB2BGR))

for i in range(0,maxtime):
    video.write(cv2.cvtColor(numpy.array(image3), cv2.COLOR_RGB2BGR))
    
# And back from image3 to image1...
for i in range(0,maxtime):
    imagestmp = Image.blend(image3, image1, i/maxtime)
    video.write(cv2.cvtColor(numpy.array(imagestmp), cv2.COLOR_RGB2BGR))
    
# Release the video for it to be committed to a file
video.release()