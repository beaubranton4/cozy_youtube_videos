#!/bin/bash

# Script to create a normal lofi video with ping-pong looping and audio crossfades
# This script stitches all audio files together with crossfades, then loops the combined audio with a slowed video

# Default values
DURATION_MINUTES=240
CHANNEL_NAME="Midnight Auto Beats"
SLOWDOWN_FACTOR=2.0
RANDOMIZE_MUSIC=false
CROSSFADE_DURATION=3  # Crossfade duration in seconds

# Convert channel name to directory format (replace spaces with underscores)
CHANNEL_DIR_NAME=$(echo "$CHANNEL_NAME" | tr ' ' '_')

# Generate timestamp for unique filenames
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

# Set paths based on channel name
CHANNEL_DIR="channels/$CHANNEL_DIR_NAME"
MUSIC_DIR="${CHANNEL_DIR}/music/raw"
VIDEO_DIR="${CHANNEL_DIR}/videos/raw"
OUTPUT_DIR="${CHANNEL_DIR}/final"
OUTPUT_FILE="${OUTPUT_DIR}/${CHANNEL_DIR_NAME}_${DURATION_MINUTES}min_${SLOWDOWN_FACTOR}x_${TIMESTAMP}.mp4"

# Calculate target duration in seconds
TARGET_DURATION=$((DURATION_MINUTES * 60))

# Create output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"

echo "=== Creating ${DURATION_MINUTES}-Minute ${SLOWDOWN_FACTOR}x Slower Video for $CHANNEL_NAME ==="
echo "Target duration: $TARGET_DURATION seconds ($DURATION_MINUTES minutes)"
echo "Music directory: $MUSIC_DIR"
echo "Video directory: $VIDEO_DIR"
echo "Output file: $OUTPUT_FILE"
echo "Audio crossfade: $CROSSFADE_DURATION seconds"
if [ "$RANDOMIZE_MUSIC" = true ]; then
    echo "Music tracks will be randomized"
else
    echo "Music tracks will play in alphabetical order"
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

# Step 3: Create a complex filter for audio crossfades
echo "Step 2: Creating audio with crossfades..."

# Create a temporary directory for individual audio files
AUDIO_TEMP_DIR="$TEMP_DIR/audio"
mkdir -p "$AUDIO_TEMP_DIR"

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
    
    # Use the shuffled array
    FINAL_MP3_FILES=("${SHUFFLED_MP3_FILES[@]}")
else
    # Use the original sorted array
    FINAL_MP3_FILES=("${MP3_FILES[@]}")
fi

# First, normalize all audio files to ensure consistent volume
echo "Step 3: Normalizing audio files..."
for i in "${!FINAL_MP3_FILES[@]}"; do
    echo "Normalizing: ${FINAL_MP3_FILES[$i]}"
    ffmpeg -i "${FINAL_MP3_FILES[$i]}" -af "loudnorm=I=-16:TP=-1.5:LRA=11" -ar 44100 "$AUDIO_TEMP_DIR/norm_$i.mp3" -y
done

# Now create the crossfaded audio file by concatenating files one by one
echo "Step 4: Creating crossfaded audio..."
if [ ${#FINAL_MP3_FILES[@]} -gt 1 ]; then
    echo "Creating crossfades between ${#FINAL_MP3_FILES[@]} tracks..."
    
    # Start with the first file
    cp "$AUDIO_TEMP_DIR/norm_0.mp3" "$TEMP_DIR/current.mp3"
    
    # Add each subsequent file with a crossfade
    for i in $(seq 1 $((${#FINAL_MP3_FILES[@]}-1))); do
        echo "Adding track $i with crossfade..."
        
        # Create a crossfade between current.mp3 and the next file
        ffmpeg -i "$TEMP_DIR/current.mp3" -i "$AUDIO_TEMP_DIR/norm_$i.mp3" \
            -filter_complex "[0:a][1:a]acrossfade=d=$CROSSFADE_DURATION:c1=tri:c2=tri[out]" \
            -map "[out]" -c:a libmp3lame -b:a 192k "$TEMP_DIR/crossfaded_$i.mp3" -y
        
        # Update current.mp3 for the next iteration
        mv "$TEMP_DIR/crossfaded_$i.mp3" "$TEMP_DIR/current.mp3"
    done
    
    # The final result is in current.mp3
    mv "$TEMP_DIR/current.mp3" "$TEMP_DIR/all_songs.mp3"
else
    # Only one file, no need for crossfade
    echo "Only one audio file found, no crossfade needed."
    cp "$AUDIO_TEMP_DIR/norm_0.mp3" "$TEMP_DIR/all_songs.mp3"
fi

# Check if the combined audio was created successfully
if [ ! -f "$TEMP_DIR/all_songs.mp3" ] || [ ! -s "$TEMP_DIR/all_songs.mp3" ]; then
    echo "Error: Failed to create combined audio file."
    exit 1
fi

# Get the duration of the combined audio
AUDIO_DURATION=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$TEMP_DIR/all_songs.mp3")
echo "Combined audio duration: $AUDIO_DURATION seconds"

# Step 5: Create a loop file for the combined audio
echo "Step 5: Creating a loop file for the combined audio..."
LOOP_LIST="$TEMP_DIR/loop.txt"
rm -f "$LOOP_LIST"

# Calculate how many times we need to loop the audio
LOOP_COUNT=$(echo "scale=0; $TARGET_DURATION / $AUDIO_DURATION + 1" | bc)
echo "Will loop audio $LOOP_COUNT times to reach target duration"

# Create a file with the audio repeated
for i in $(seq 1 $LOOP_COUNT); do
    # Use absolute path for the audio file
    echo "file '$PWD/$TEMP_DIR/all_songs.mp3'" >> "$LOOP_LIST"
done

# Debug: Print the content of the loop list file
echo "Loop list file content:"
cat "$LOOP_LIST"

# Step 6: Create the extended audio by concatenating the loops
echo "Step 6: Creating extended audio by concatenating loops..."
ffmpeg -f concat -safe 0 -i "$LOOP_LIST" -c:a libmp3lame -b:a 192k -t $TARGET_DURATION "$TEMP_DIR/extended_audio.mp3" -y

# Step 7: Find the video file directly in the raw folder (not in subdirectories)
echo "Step 7: Finding video file..."
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

# Step 8: Slow down the video
echo "Step 8: Slowing down the video (${SLOWDOWN_FACTOR}x slower)..."
ffmpeg -i "$VIDEO_FILE" -filter:v "setpts=${SLOWDOWN_FACTOR}*PTS" -c:v libx264 -crf 18 -preset slow "$TEMP_DIR/slowed_video.mp4" -y

# Step 9: Create a reversed version of the slowed video
echo "Step 9: Creating reversed version of the video..."
ffmpeg -i "$TEMP_DIR/slowed_video.mp4" -vf reverse -c:v libx264 -crf 18 -preset slow "$TEMP_DIR/reversed_video.mp4" -y

# Step 10: Create a concat file for the ping-pong loop
echo "Step 10: Creating ping-pong loop..."
PINGPONG_LIST="$TEMP_DIR/pingpong.txt"
rm -f "$PINGPONG_LIST"

# Use absolute paths for the video files
echo "file '$PWD/$TEMP_DIR/slowed_video.mp4'" >> "$PINGPONG_LIST"
echo "file '$PWD/$TEMP_DIR/reversed_video.mp4'" >> "$PINGPONG_LIST"

# Debug: Print the content of the pingpong list file
echo "Pingpong list file content:"
cat "$PINGPONG_LIST"

# Create a single ping-pong cycle
ffmpeg -f concat -safe 0 -i "$PINGPONG_LIST" -c copy "$TEMP_DIR/pingpong_cycle.mp4" -y

# Step 11: Create the extended video by looping the ping-pong cycle
echo "Step 11: Creating extended video by looping the ping-pong cycle..."
ffmpeg -stream_loop -1 -i "$TEMP_DIR/pingpong_cycle.mp4" -c copy -t $TARGET_DURATION "$TEMP_DIR/extended_video.mp4" -y

# Step 12: Combine extended video with extended audio
echo "Step 12: Combining video and audio..."
ffmpeg -i "$TEMP_DIR/extended_video.mp4" -i "$TEMP_DIR/extended_audio.mp3" -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest "$OUTPUT_FILE" -y

# Clean up temporary files
rm -rf "$TEMP_DIR"

echo "Process completed successfully!"
echo "Your ${SLOWDOWN_FACTOR}x slower ${DURATION_MINUTES}-minute video for $CHANNEL_NAME is ready at: $OUTPUT_FILE"
echo "To play the video: ffplay \"$OUTPUT_FILE\"" 