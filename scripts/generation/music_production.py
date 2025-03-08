#!/usr/bin/env python3
"""
Music Production Script

This script combines multiple raw music files into a single production music file.
It can create production files of specific durations by concatenating raw files.
"""

import os
import sys
import json
import argparse
import subprocess
import random
from datetime import datetime

# Add parent directory to path to import channel_utils
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.channel_utils import load_channel_concepts, get_channel_info, validate_channel_directory

def list_raw_music(channel_id, concepts):
    """List all raw music files for a channel."""
    channel = get_channel_info(channel_id, concepts)
    if not channel:
        return []
    
    channel_name = channel['name'].replace(' ', '_')
    raw_music_dir = f"channels/{channel_name}/music/raw"
    
    if not os.path.exists(raw_music_dir):
        print(f"Error: Raw music directory {raw_music_dir} does not exist.")
        return []
    
    music_files = []
    for file in os.listdir(raw_music_dir):
        if file.endswith(('.mp3', '.wav', '.flac', '.ogg')):
            music_files.append(os.path.join(raw_music_dir, file))
    
    return music_files

def get_audio_duration(file_path):
    """Get the duration of an audio file in seconds using ffprobe."""
    try:
        cmd = [
            'ffprobe', 
            '-v', 'error', 
            '-show_entries', 'format=duration', 
            '-of', 'default=noprint_wrappers=1:nokey=1', 
            file_path
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        return float(result.stdout.strip())
    except Exception as e:
        print(f"Error getting duration for {file_path}: {e}")
        return 0

def create_production_music(channel_id, duration_minutes, exclude_track=None, concepts=None):
    """Create a production music file by combining raw music files."""
    if not concepts:
        concepts = load_channel_concepts()
        if not concepts:
            return False
    
    channel = get_channel_info(channel_id, concepts)
    if not channel:
        return False
    
    # Validate channel directory
    if not validate_channel_directory(channel_id, concepts):
        return False
    
    channel_name = channel['name'].replace(' ', '_')
    raw_music_dir = f"channels/{channel_name}/music/raw"
    production_dir = f"channels/{channel_name}/music/production"
    
    # Ensure production directory exists
    os.makedirs(production_dir, exist_ok=True)
    
    # Get all raw music files
    music_files = list_raw_music(channel_id, concepts)
    if not music_files:
        print(f"Error: No raw music files found in {raw_music_dir}")
        return False
    
    # Filter out excluded track if specified
    if exclude_track:
        music_files = [f for f in music_files if exclude_track not in f]
    
    if not music_files:
        print(f"Error: No music files left after excluding '{exclude_track}'")
        return False
    
    # Calculate total duration needed in seconds
    target_duration = duration_minutes * 60
    
    # Get durations of all files
    file_durations = {}
    for file in music_files:
        duration = get_audio_duration(file)
        if duration > 0:
            file_durations[file] = duration
    
    if not file_durations:
        print("Error: Could not determine durations of music files")
        return False
    
    # Create a playlist of files to reach the target duration
    playlist = []
    current_duration = 0
    
    # Keep adding files until we reach the target duration
    available_files = list(file_durations.keys())
    while current_duration < target_duration and available_files:
        # Shuffle the available files to get a random order
        random.shuffle(available_files)
        
        # Add the next file to the playlist
        next_file = available_files.pop(0)
        playlist.append(next_file)
        current_duration += file_durations[next_file]
        
        # If we've used all files but still need more duration, reset the available files
        if not available_files and current_duration < target_duration:
            available_files = list(file_durations.keys())
            # Remove the last added file to avoid immediate repetition
            if len(available_files) > 1 and next_file in available_files:
                available_files.remove(next_file)
    
    # Create a temporary file with the list of files to concatenate
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"{production_dir}/production_{duration_minutes}min_{timestamp}.mp3"
    temp_list = f"{production_dir}/temp_list_{timestamp}.txt"
    
    with open(temp_list, 'w') as f:
        for file in playlist:
            f.write(f"file '{os.path.abspath(file)}'\n")
    
    # Use ffmpeg to concatenate the files
    try:
        cmd = [
            'ffmpeg',
            '-f', 'concat',
            '-safe', '0',
            '-i', temp_list,
            '-c', 'copy',
            output_file
        ]
        
        print(f"\nCreating production music file: {output_file}")
        print(f"Target duration: {duration_minutes} minutes ({target_duration} seconds)")
        print(f"Combining {len(playlist)} raw music files...")
        
        subprocess.run(cmd, check=True)
        
        # Clean up the temporary file
        os.remove(temp_list)
        
        # Verify the output file exists and get its duration
        if os.path.exists(output_file):
            actual_duration = get_audio_duration(output_file)
            print(f"Production music file created successfully!")
            print(f"Actual duration: {actual_duration/60:.2f} minutes ({actual_duration:.2f} seconds)")
            
            # Create a metadata file
            metadata_file = f"{production_dir}/metadata_{os.path.basename(output_file).replace('.mp3', '.txt')}"
            with open(metadata_file, 'w') as f:
                f.write(f"Production Music File: {os.path.basename(output_file)}\n")
                f.write(f"Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Target Duration: {duration_minutes} minutes\n")
                f.write(f"Actual Duration: {actual_duration/60:.2f} minutes\n")
                f.write(f"Number of Tracks: {len(playlist)}\n\n")
                f.write("Tracks Used:\n")
                for i, file in enumerate(playlist, 1):
                    f.write(f"{i}. {os.path.basename(file)}\n")
            
            print(f"Metadata saved to: {metadata_file}")
            return output_file
        else:
            print(f"Error: Failed to create production music file")
            return False
    
    except Exception as e:
        print(f"Error creating production music file: {e}")
        # Clean up the temporary file if it exists
        if os.path.exists(temp_list):
            os.remove(temp_list)
        return False

def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Create production music files by combining raw music files")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # List command
    list_parser = subparsers.add_parser("list", help="List raw music files for a channel")
    list_parser.add_argument("channel_id", type=int, help="Channel ID")
    
    # Create command
    create_parser = subparsers.add_parser("create", help="Create a production music file")
    create_parser.add_argument("channel_id", type=int, help="Channel ID")
    create_parser.add_argument("duration", type=int, help="Duration in minutes")
    create_parser.add_argument("--exclude", help="Track to exclude (optional)")
    
    args = parser.parse_args()
    
    # Load channel concepts
    concepts = load_channel_concepts()
    if not concepts:
        return
    
    # Execute the appropriate command
    if args.command == "list":
        music_files = list_raw_music(args.channel_id, concepts)
        if music_files:
            print(f"\nRaw music files for channel {args.channel_id}:")
            for i, file in enumerate(music_files, 1):
                print(f"{i}. {os.path.basename(file)}")
        else:
            print(f"No raw music files found for channel {args.channel_id}")
    
    elif args.command == "create":
        result = create_production_music(args.channel_id, args.duration, args.exclude, concepts)
        if result:
            print(f"\nProduction music file created successfully: {os.path.basename(result)}")
        else:
            print("\nFailed to create production music file")
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main() 