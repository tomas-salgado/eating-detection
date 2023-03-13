import cv2
import datetime
import calendar
import csv
import subprocess

#subprocess to extract creation time from metadata
command = "ffprobe -v quiet -select_streams v:0  -show_entries stream_tags=creation_time -of default=noprint_wrappers=1:nokey=1 video.mp4"
process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=None, shell=True)
output = process.communicate()[0]
output = output.decode("utf-8")

year = int(output[:4])
month = int(output[5:7])
date = int(output[8:10])
hour = int(output[11:13])
minute = int(output[14:16])
second = int(output[17:19]) #takes rounded int value for seconds
print(year, month, date, hour, minute, second)

t = datetime.datetime(year, month, date, hour, minute, second)
creation_time = float(calendar.timegm(t.timetuple()))


path_to_vid = ''
cap = cv2.VideoCapture(path_to_vid)


with open('timestamps.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)

    frame_no = 0
    total_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    
    while total_frames >= frame_no:
        frame_exists, curr_frame = cap.read()
        
        string = "frame : " + str(frame_no), "   timestamp: " + str(cap.get(cv2.CAP_PROP_POS_MSEC)/1000+creation_time)
        writer.writerow(string)
        


        frame_no += 1

    cap.release()