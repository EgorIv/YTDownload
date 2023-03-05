#!/usr/bin/env python3
import os
import argparse
from pytube import YouTube

def download(url, audio):
    print("\tProcessing: ", url)

    yt = YouTube(url)
    
    if audio is None:
        video = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
    else:
        video = yt.streams.filter(only_audio=True).first()

    print("\tTitle: " + yt.title)
    print("\tSize: " + str(video.filesize))

    out_file = video.download(output_path=".")
    if audio is None:
        return
    
    video_name, _ = os.path.splitext(out_file)
    new_filename = video_name + ".mp3"
    os.rename(out_file, new_filename)


def main():
    parser = argparse.ArgumentParser(
        prog = 'YTDownload',
        description = 'A simple program to download videos from Youtube')
    parser.add_argument('-u', help='Urls of a video', type=str, nargs='+')
    parser.add_argument('-l', help='Use urls from a file in the current directory', type=str, nargs='+')
    parser.add_argument('-d', help='Use urls from all files in the current directory', action='store_true')
    parser.add_argument('-a', help='Download only audio', action='store_true')
    args = parser.parse_args()

    if args.u is not None:
        for url in args.u:
            download(url, args.a)

    if args.l is not None:
        files = args.l
    elif args.d:
        files = os.listdir()
    else:
        return

    for file in files:
        _, ext = os.path.splitext(file)
        if ext != ".txt":
                continue
        f = open(file, "rt")
        urls = f.read().rstrip("\n").split("\n")
        f.close()

        for url in urls:
            download(url, args.a)


if __name__ == '__main__':
    main()
