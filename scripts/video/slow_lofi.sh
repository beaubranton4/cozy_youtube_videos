#!/bin/bash

# Script to create a 3x slower lofi video with ping-pong looping
# This script stitches all audio files together, then loops the combined audio with a slowed video

# Default values
DURATION_MINUTES=240
CHANNEL_NAME="Midnight Auto Beats"
RANDOMIZE_MUSIC=true

# Convert channel name to directory format (replace spaces with underscores)
CHANNEL_DIR_NAME=$(echo "$CHANNEL_NAME" | tr ' ' '_')

# Generate timestamp for unique filenames
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

# Set paths based on channel name
CHANNEL_DIR="channels/$CHANNEL_DIR_NAME"
MUSIC_DIR="${CHANNEL_DIR}/music/raw"
VIDEO_DIR="${CHANNEL_DIR}/videos/raw"
OUTPUT_DIR="${CHANNEL_DIR}/final"
OUTPUT_FILE="${OUTPUT_DIR}/${CHANNEL_DIR_NAME}_${DURATION_MINUTES}min_3x_slower_${TIMESTAMP}.mp4"

# Calculate target duration in seconds
TARGET_DURATION=$((DURATION_MINUTES * 60))

# Create output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"

echo "=== Creating ${DURATION_MINUTES}-Minute 3x Slower Video for $CHANNEL_NAME ==="
echo "Target duration: $TARGET_DURATION seconds ($DURATION_MINUTES minutes)"
echo "Music directory: $MUSIC_DIR"
echo "Video directory: $VIDEO_DIR"
echo "Output file: $OUTPUT_FILE"
if [ "$RANDOMIZE_MUSIC" = true ]; then
    echo "Music tracks will be randomized"
fi

# Step 1: Create a temporary directory for processing
TEMP_DIR="$OUTPUT_DIR/temp"
mkdir -p "$TEMP_DIR"

# Step 2: Find all MP3 files
echo "Step 1: Finding all MP3 files..."
MP3_FILES=()
while IFS= read -r file; do
    MP3_FILES+=("$file")
    echo "Found: $file"
done < <(find "$MUSIC_DIR" -name "*.mp3" | sort)

if [ ${#MP3_FILES[@]} -eq 0 ]; then
    echo "Error: No MP3 files found in $MUSIC_DIR"
    exit 1
fi

echo "Found ${#MP3_FILES[@]} MP3 files to include"

# Step 3: Create a concat file for ffmpeg
echo "Step 2: Creating concat file for ffmpeg..."
CONCAT_LIST="$TEMP_DIR/concat.txt"
rm -f "$CONCAT_LIST"

# If randomize is enabled, shuffle the array of MP3 files
if [ "$RANDOMIZE_MUSIC" = true ]; then
    echo "Randomizing music track order..."
    # Create a temporary array for shuffling
    SHUFFLED_MP3_FILES=()
    
    # Copy the original array to avoid modifying it
    for file in "${MP3_FILES[@]}"; do
        SHUFFLED_MP3_FILES+=("$file")
    done
    
    # Fisher-Yates shuffle algorithm
    for ((i=${#SHUFFLED_MP3_FILES[@]}-1; i>0; i--)); do
        # Generate a random index between 0 and i
        j=$(($RANDOM % (i+1)))
        
        # Swap elements at indices i and j
        temp="${SHUFFLED_MP3_FILES[i]}"
        SHUFFLED_MP3_FILES[i]="${SHUFFLED_MP3_FILES[j]}"
        SHUFFLED_MP3_FILES[j]="$temp"
    done
    
    # Use the shuffled array for the concat file
    for file in "${SHUFFLED_MP3_FILES[@]}"; do
        echo "Adding to playlist: $file"
        echo "file '$(pwd)/$file'" >> "$CONCAT_LIST"
    done
else
    # Use the original sorted array
    for file in "${MP3_FILES[@]}"; do
        echo "file '$(pwd)/$file'" >> "$CONCAT_LIST"
    done
fi

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

# Step 7: Find the video file directly in the raw folder (not in subdirectories)
echo "Step 6: Finding video file..."
VIDEO_FILES=()
# Use -maxdepth 1 to only search in the specified directory, not in subdirectories
while IFS= read -r file; do
    if [[ "$file" == *".mp4" ]]; then
        VIDEO_FILES+=("$file")
        echo "Found video: $file"
    fi
done < <(find "$VIDEO_DIR" -maxdepth 1 -name "*.mp4" | sort)

if [ ${#VIDEO_FILES[@]} -eq 0 ]; then
    echo "Error: No video files found directly in $VIDEO_DIR"
    echo "Please make sure there is at least one .mp4 file in this directory (not in subdirectories)"
    exit 1
fi

# Use the first video file found (or the only one)
VIDEO_FILE="${VIDEO_FILES[0]}"
echo "Selected video: $VIDEO_FILE"

# Step 8: Slow down the video (3x slower)
echo "Step 7: Slowing down the video (3x slower)..."
ffmpeg -i "$VIDEO_FILE" -filter:v "setpts=3.0*PTS" -c:v libx264 -crf 18 -preset slow "$TEMP_DIR/slowed_video.mp4" -y

# Step 9: Create a reversed version of the slowed video
echo "Step 8: Creating reversed version of the video..."
ffmpeg -i "$TEMP_DIR/slowed_video.mp4" -vf reverse -c:v libx264 -crf 18 -preset slow "$TEMP_DIR/reversed_video.mp4" -y

# Step 10: Create a concat file for the ping-pong loop
echo "Step 9: Creating ping-pong loop..."
PINGPONG_LIST="$TEMP_DIR/pingpong.txt"
rm -f "$PINGPONG_LIST"

echo "file '$(pwd)/$TEMP_DIR/slowed_video.mp4'" >> "$PINGPONG_LIST"
echo "file '$(pwd)/$TEMP_DIR/reversed_video.mp4'" >> "$PINGPONG_LIST"

# Create a single ping-pong cycle
ffmpeg -f concat -safe 0 -i "$PINGPONG_LIST" -c copy "$TEMP_DIR/pingpong_cycle.mp4" -y

# Step 11: Create the extended video by looping the ping-pong cycle
echo "Step 10: Creating extended video by looping the ping-pong cycle..."
ffmpeg -stream_loop -1 -i "$TEMP_DIR/pingpong_cycle.mp4" -c copy -t $TARGET_DURATION "$TEMP_DIR/extended_video.mp4" -y

# Step 12: Combine extended video with extended audio
echo "Step 11: Combining video and audio..."
ffmpeg -i "$TEMP_DIR/extended_video.mp4" -i "$TEMP_DIR/extended_audio.mp3" -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest "$OUTPUT_FILE" -y

# Clean up temporary files
rm -rf "$TEMP_DIR"

echo "Process completed successfully!"
echo "Your 3x slower ${DURATION_MINUTES}-minute video for $CHANNEL_NAME is ready at: $OUTPUT_FILE"
echo "To play the video: ffplay \"$OUTPUT_FILE\"" 