#!/bin/bash

# Quick script to generate a lo-fi video with default settings
# Just run this script without any parameters

# Create output directory
mkdir -p final

# One-line command to loop video and add audio
ffmpeg -stream_loop 10 -i "library/lo-fi/video_0/Anime Cabin with Furnace.mp4" -i "library/lo-fi/video_0/Elysium.mp3" -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest "final/quick_lofi.mp4"

echo "Quick lo-fi video created at: final/quick_lofi.mp4" 