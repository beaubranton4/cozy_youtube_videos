#!/bin/bash

# Final script to create a lofi video with all songs except the first one
# This script stitches all audio files together, then loops the combined audio with a video

# Default values
DURATION_MINUTES=${1:-180}
MUSIC_DIR=${2:-"../../library/lo-fi/video_0"}
VIDEO_DIR=${3:-"../../library/lo-fi/video_0"}
OUTPUT_FILE=${4:-"../../final/final_${DURATION_MINUTES}min_lofi.mp4"}

# Calculate target duration in seconds
TARGET_DURATION=$((DURATION_MINUTES * 60))

# Track to exclude (can be empty if no track should be excluded)
EXCLUDE_TRACK=${5:-"Drift (1).mp3"}

# Crossfade duration in seconds
CROSSFADE_DURATION=3

# Create output directory if it doesn't exist
OUTPUT_DIR=$(dirname "$OUTPUT_FILE")
mkdir -p "$OUTPUT_DIR"

echo "=== Creating ${DURATION_MINUTES}-Minute Lofi Video ==="
echo "Target duration: $TARGET_DURATION seconds ($DURATION_MINUTES minutes)"
echo "Music directory: $MUSIC_DIR"
echo "Video directory: $VIDEO_DIR"
echo "Output file: $OUTPUT_FILE"
if [ -n "$EXCLUDE_TRACK" ]; then
    echo "Excluding track: $EXCLUDE_TRACK"
fi
echo "Using crossfade duration: $CROSSFADE_DURATION seconds between tracks"

# Step 1: Create a temporary directory for processing
TEMP_DIR="$OUTPUT_DIR/temp"
mkdir -p "$TEMP_DIR"

# Step 2: Find all MP3 files except the excluded one
echo "Step 1: Finding all MP3 files..."
MP3_FILES=()
while IFS= read -r file; do
    # Skip the excluded track if specified
    if [ -z "$EXCLUDE_TRACK" ] || [[ "$(basename "$file")" != "$EXCLUDE_TRACK" ]]; then
        MP3_FILES+=("$file")
        echo "Found: $file"
    else
        echo "Excluded: $file"
    fi
done < <(find "$MUSIC_DIR" -name "*.mp3" | sort)

echo "Found ${#MP3_FILES[@]} MP3 files to include"

# Step 3: Create a concat file for ffmpeg
echo "Step 2: Creating concat file for ffmpeg..."
CONCAT_LIST="$TEMP_DIR/concat.txt"
rm -f "$CONCAT_LIST"

for file in "${MP3_FILES[@]}"; do
    echo "file '$(pwd)/$file'" >> "$CONCAT_LIST"
done

# Step 4: Stitch all audio files together
echo "Step 3: Stitching all audio files together..."
ffmpeg -f concat -safe 0 -i "$CONCAT_LIST" -c:a libmp3lame -b:a 192k "$TEMP_DIR/all_songs.mp3" -y

# Check if the combined audio was created successfully
if [ ! -f "$TEMP_DIR/all_songs.mp3" ] || [ ! -s "$TEMP_DIR/all_songs.mp3" ]; then
    echo "Error: Failed to create combined audio file."
    exit 1
fi

# Get the duration of the combined audio
AUDIO_DURATION=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$TEMP_DIR/all_songs.mp3")
echo "Combined audio duration: $AUDIO_DURATION seconds"

# Step 5: Create a loop file for the combined audio
echo "Step 4: Creating a loop file for the combined audio..."
LOOP_LIST="$TEMP_DIR/loop.txt"
rm -f "$LOOP_LIST"

# Calculate how many times we need to loop the audio
LOOP_COUNT=$(echo "scale=0; $TARGET_DURATION / $AUDIO_DURATION + 1" | bc)
echo "Will loop audio $LOOP_COUNT times to reach target duration"

# Create a file with the audio repeated
for i in $(seq 1 $LOOP_COUNT); do
    echo "file '$(pwd)/$TEMP_DIR/all_songs.mp3'" >> "$LOOP_LIST"
done

# Step 6: Create the extended audio by concatenating the loops
echo "Step 5: Creating extended audio by concatenating loops..."
ffmpeg -f concat -safe 0 -i "$LOOP_LIST" -c:a libmp3lame -b:a 192k -t $TARGET_DURATION "$TEMP_DIR/extended_audio.mp3" -y

# Step 7: Find the video file
echo "Step 6: Finding video file..."
VIDEO_FILE=""
while IFS= read -r file; do
    if [[ "$file" == *".mp4" ]]; then
        VIDEO_FILE="$file"
        echo "Found video: $file"
        break
    fi
done < <(find "$VIDEO_DIR" -type f | sort)

if [ -z "$VIDEO_FILE" ]; then
    echo "Error: No video file found in $VIDEO_DIR"
    exit 1
fi

# Step 8: Create the extended video by looping
echo "Step 7: Creating extended video..."
ffmpeg -stream_loop -1 -i "$VIDEO_FILE" -c:v copy -t $TARGET_DURATION "$TEMP_DIR/extended_video.mp4" -y

# Step 9: Combine extended video with extended audio
echo "Step 8: Combining video and audio..."
ffmpeg -i "$TEMP_DIR/extended_video.mp4" -i "$TEMP_DIR/extended_audio.mp3" -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest "$OUTPUT_FILE" -y

# Clean up temporary files
rm -rf "$TEMP_DIR"

echo "Process completed successfully!"
echo "Your ${DURATION_MINUTES}-minute lofi video is ready at: $OUTPUT_FILE"
echo "To play the video: ffplay \"$OUTPUT_FILE\"" 