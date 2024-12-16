import moviepy.editor as mp

file = mp.VideoFileClip('blesk/res/r2.mp4')
file.write_videofile('blesk/res/r3.mp4')