from PIL import Image;
import cv2;
import os;
import subprocess;
import math;
from moviepy.editor import *

import pandas as pd;

#change these variables for video cutting
INPUT_VIDEO_DIR = "./input";
OUTPUT_DIR_VIDEO= "output_clips";
OUTPUT_VIDEO_BASE_NAMES = "output";             # the output video name must start with the following nme 



def convert_into_format(number):
    if(number<10):
        return "0"+str(number);
    return str(number);

def get_duration_video(videopath):
    clip = VideoFileClip(videopath);
    seconds = math.floor(clip.duration)
    return seconds;


def convert_seconds_to_format(seconds):
    s = seconds;
    hours = math.floor(seconds/3600);
    s -= (hours * 3600);
    minutes = math.floor(s/60);
    s -= (minutes*60)

    hours_str = convert_into_format(hours);
    minutes_str = convert_into_format(minutes);
    seconds_str= convert_into_format(s);
    return "{}:{}:{}".format(hours_str , minutes_str , seconds_str);


    pass
def break_video_into_small_videos_from_utils(input_folder_path ,video_name , output_folder_path , basename , start=0 , duration=30, video_tag=0):
    
    cmd = ["ffmpeg" , 
    "-ss" , convert_seconds_to_format(start) , 
    "-t" , str(duration) , 
    "-i" , "./{}/{}".format(input_folder_path,video_name),
    "-acodec" , "copy",
    "./{}/{}.mp4".format(output_folder_path , basename.split(".")[0]+ str(start) )
    ];
    p = subprocess.Popen(cmd , shell=True);
    p.wait();

def break_video_into_small_videos_from_utils2(input_folder_path ,video_name , output_folder_path , basename , start , duration, video_tag=0):
    
    cmd = ["ffmpeg" , 
    "-ss" , str(start) , 
    "-t" , str(duration) , 
    "-i" , "{}/{}".format(input_folder_path,video_name),
    "-acodec" , "copy",
    "./{}/{}.mp4".format(output_folder_path , basename.split(".")[0] )
    ];
    p = subprocess.Popen(cmd , shell=True);
    p.wait();
#print(
# np.array(split_frames[0]).shape);
#make_video(split_frames[0])
def break_video_into_clips(input_folder_path ,video_name , output_folder_path , basename):
    start = 0;
    duration = 10;
    end = get_duration_video(input_folder_path + "/" + video_name);
    folder_path =output_folder_path + "/" + video_name.split(".")[0]; 
    if(not os.path.exists(folder_path)):

        os.mkdir(folder_path);
    while(start < end):

        break_video_into_small_videos_from_utils(input_folder_path , video_name , folder_path ,basename ,start , duration  );
        start += duration;


# video_n = os.listdir(INPUT_VIDEO_DIR);

# for video in video_n:
#     print("preapring video {}".format(video));
    
#     break_video_into_clips( INPUT_VIDEO_DIR, video , OUTPUT_DIR_VIDEO , OUTPUT_VIDEO_BASE_NAMES);

def runner_clip_maker():
    video_n = os.listdir(INPUT_VIDEO_DIR);

    for video in video_n:
        print("preapring video {}".format(video));
        
        break_video_into_clips( INPUT_VIDEO_DIR, video , OUTPUT_DIR_VIDEO , OUTPUT_VIDEO_BASE_NAMES);
def measure_duration(breakpoint):
    start = breakpoint[0];
    end = breakpoint[1];
    start_arr = [int(t) for t in start.split(":")];
    end_arr = [int(t) for t in end.split(":")];
    diff_arr = [  (end_arr[i] - start_arr[i])  for i in range(len(start_arr))]
    print(diff_arr)
    exp = 60;
    sum = 0;
    l = len(start_arr);
    for i in range(l):
        sum += (int)(math.pow(exp , i) * diff_arr[l-i-1]);
    return sum;

def data_generator(load_file_path):
    video_names = [];
    video_intervals = [];
    df = pd.read_csv(load_file_path , names=["videos" , "start" , "end"]);
    for i in range(len(df)):
        video_names.append(df["videos"][i]);
        video_intervals.append([df["start"][i] , df["end"][i]])
    return video_names , video_intervals;
def runner_clip_fetcher():
    videos , breakpoints = data_generator("./intervals.csv");
    print(videos , breakpoints);
    for i in range(len(videos)):
        duration = measure_duration(breakpoints[i]);
        print(videos[i]);
        break_video_into_small_videos_from_utils2(INPUT_VIDEO_DIR  ,videos[i] , OUTPUT_DIR_VIDEO , videos[i].split(".")[0]+"_"+str(i) , breakpoints[i][0] , duration   );
       
# measure_duration(["01:10:20", "02:02:10"]);
runner_clip_fetcher();