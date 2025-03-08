#!/bin/bash

# Script to preview video and audio files before processing
# This helps you check the files and their durations

WORK_DIR="library/lo-fi/video_0"

# Function to display file information
display_info() {
    echo "===== File Information ====="
    echo "File: $1"
    
    # Get duration and other info
    ffprobe -v error -select_streams a:0 -show_entries stream=codec_name,duration,bit_rate -show_entries format=duration -of default=noprint_wrappers=1 "$1"
    
    echo "=========================="
    echo ""
}

# Create a directory for thumbnails
mkdir -p thumbnails

# Display video file info
echo "===== VIDEO FILE ====="
VIDEO_FILE="$WORK_DIR/Anime Cabin with Furnace.mp4"

if [ -f "$VIDEO_FILE" ]; then
    echo "Found video: $VIDEO_FILE"
    display_info "$VIDEO_FILE"
    
    # Generate a thumbnail
    ffmpeg -y -i "$VIDEO_FILE" -ss 00:00:01 -vframes 1 "thumbnails/video_thumbnail.jpg"
    echo "Thumbnail created: thumbnails/video_thumbnail.jpg"
else
    echo "Video file not found: $VIDEO_FILE"
fi

# Display audio file info
echo "===== AUDIO FILES ====="
AUDIO_FILES=$(find "$WORK_DIR" -name "*.mp3" | sort)

# Count the number of audio files
AUDIO_COUNT=$(find "$WORK_DIR" -name "*.mp3" | wc -l)

echo "Found $AUDIO_COUNT audio files"

# Display info for each audio file
for file in $AUDIO_FILES; do
    echo "Found audio: $file"
    display_info "$file"
done

# Get video duration
VIDEO_DURATION=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$VIDEO_FILE" 2>/dev/null)

echo "===== SUMMARY ====="
echo "Total number of audio files: $AUDIO_COUNT"
echo "Video duration: $VIDEO_DURATION seconds"

echo ""
echo "To play the video file:"
echo "ffplay \"$VIDEO_FILE\""
echo ""
echo "To play an audio file:"
echo "ffplay \"$WORK_DIR/Elysium.mp3\"" 