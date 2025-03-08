#!/usr/bin/env python3
"""
Video Production Preparation Script

This script combines multiple raw video files into a single production video file.
It can create production files of specific durations by looping and concatenating raw files.
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

def list_raw_videos(channel_id, concepts):
    """List all raw video files for a channel."""
    channel = get_channel_info(channel_id, concepts)
    if not channel:
        return []
    
    channel_name = channel['name'].replace(' ', '_')
    raw_video_dir = f"channels/{channel_name}/videos/raw"
    
    if not os.path.exists(raw_video_dir):
        print(f"Error: Raw video directory {raw_video_dir} does not exist.")
        return []
    
    video_files = []
    for file in os.listdir(raw_video_dir):
        if file.endswith(('.mp4', '.mov', '.avi', '.mkv')):
            video_files.append(os.path.join(raw_video_dir, file))
    
    return video_files

def get_video_duration(file_path):
    """Get the duration of a video file in seconds using ffprobe."""
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

def get_video_resolution(file_path):
    """Get the resolution of a video file using ffprobe."""
    try:
        cmd = [
            'ffprobe',
            '-v', 'error',
            '-select_streams', 'v:0',
            '-show_entries', 'stream=width,height',
            '-of', 'csv=s=x:p=0',
            file_path
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.stdout.strip()
    except Exception as e:
        print(f"Error getting resolution for {file_path}: {e}")
        return "unknown"

def create_production_video(channel_id, duration_minutes, concepts=None):
    """Create a production video file by combining and looping raw video files."""
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
    raw_video_dir = f"channels/{channel_name}/videos/raw"
    production_dir = f"channels/{channel_name}/videos/production"
    
    # Ensure production directory exists
    os.makedirs(production_dir, exist_ok=True)
    
    # Get all raw video files
    video_files = list_raw_videos(channel_id, concepts)
    if not video_files:
        print(f"Error: No raw video files found in {raw_video_dir}")
        return False
    
    # Calculate total duration needed in seconds
    target_duration = duration_minutes * 60
    
    # Get durations and resolutions of all files
    file_info = {}
    for file in video_files:
        duration = get_video_duration(file)
        resolution = get_video_resolution(file)
        if duration > 0:
            file_info[file] = {'duration': duration, 'resolution': resolution}
    
    if not file_info:
        print("Error: Could not determine durations of video files")
        return False
    
    # Find the most common resolution to standardize output
    resolutions = [info['resolution'] for info in file_info.values()]
    if resolutions:
        # Count occurrences of each resolution
        resolution_counts = {}
        for res in resolutions:
            if res in resolution_counts:
                resolution_counts[res] += 1
            else:
                resolution_counts[res] = 1
        
        # Find the most common resolution
        target_resolution = max(resolution_counts, key=resolution_counts.get)
        print(f"Using target resolution: {target_resolution}")
    else:
        target_resolution = "1920x1080"  # Default to 1080p if no resolution found
    
    # Create a timestamp for the output file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"{production_dir}/production_{duration_minutes}min_{timestamp}.mp4"
    
    # Create a temporary directory for processed files
    temp_dir = f"{production_dir}/temp_{timestamp}"
    os.makedirs(temp_dir, exist_ok=True)
    
    processed_files = []
    
    # Process each file to match the target resolution and create looped versions if needed
    for i, (file, info) in enumerate(file_info.items()):
        file_basename = os.path.basename(file)
        file_duration = info['duration']
        file_resolution = info['resolution']
        
        # Calculate how many times to loop this video to contribute to the target duration
        # We'll aim for each video to contribute roughly equal portions of the total duration
        portion_duration = target_duration / len(file_info)
        loops_needed = max(1, round(portion_duration / file_duration))
        
        print(f"\nProcessing file {i+1}/{len(file_info)}: {file_basename}")
        print(f"  Duration: {file_duration:.2f} seconds")
        print(f"  Resolution: {file_resolution}")
        print(f"  Loops needed: {loops_needed}")
        
        # Create a processed version with the target resolution
        processed_file = f"{temp_dir}/processed_{i}_{file_basename}"
        
        # If the file needs to be looped, create a looped version
        if loops_needed > 1:
            # Create a temporary file with the file repeated multiple times
            temp_list = f"{temp_dir}/loop_list_{i}.txt"
            with open(temp_list, 'w') as f:
                for _ in range(loops_needed):
                    f.write(f"file '{os.path.abspath(file)}'\n")
            
            # Use ffmpeg to concatenate the file with itself multiple times
            try:
                cmd = [
                    'ffmpeg',
                    '-f', 'concat',
                    '-safe', '0',
                    '-i', temp_list,
                    '-c', 'copy',
                    processed_file
                ]
                
                subprocess.run(cmd, check=True)
                processed_files.append(processed_file)
                
                # Clean up the temporary file
                os.remove(temp_list)
                
            except Exception as e:
                print(f"Error creating looped version: {e}")
                continue
        else:
            # Just use the original file
            processed_files.append(file)
    
    if not processed_files:
        print("Error: No processed files created")
        return False
    
    # Shuffle the processed files to create variety
    random.shuffle(processed_files)
    
    # Create a file list for concatenation
    concat_list = f"{temp_dir}/concat_list.txt"
    with open(concat_list, 'w') as f:
        for file in processed_files:
            f.write(f"file '{os.path.abspath(file)}'\n")
    
    # Use ffmpeg to concatenate all processed files
    try:
        cmd = [
            'ffmpeg',
            '-f', 'concat',
            '-safe', '0',
            '-i', concat_list,
            '-c', 'copy',
            output_file
        ]
        
        print(f"\nCreating production video file: {output_file}")
        print(f"Target duration: {duration_minutes} minutes ({target_duration} seconds)")
        print(f"Combining {len(processed_files)} processed video files...")
        
        subprocess.run(cmd, check=True)
        
        # Clean up temporary files
        os.remove(concat_list)
        for file in processed_files:
            if file.startswith(temp_dir) and os.path.exists(file):
                os.remove(file)
        os.rmdir(temp_dir)
        
        # Verify the output file exists and get its duration
        if os.path.exists(output_file):
            actual_duration = get_video_duration(output_file)
            print(f"Production video file created successfully!")
            print(f"Actual duration: {actual_duration/60:.2f} minutes ({actual_duration:.2f} seconds)")
            
            # Create a metadata file
            metadata_file = f"{production_dir}/metadata_{os.path.basename(output_file).replace('.mp4', '.txt')}"
            with open(metadata_file, 'w') as f:
                f.write(f"Production Video File: {os.path.basename(output_file)}\n")
                f.write(f"Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Target Duration: {duration_minutes} minutes\n")
                f.write(f"Actual Duration: {actual_duration/60:.2f} minutes\n")
                f.write(f"Target Resolution: {target_resolution}\n")
                f.write(f"Number of Source Videos: {len(file_info)}\n\n")
                f.write("Videos Used:\n")
                for i, file in enumerate(video_files, 1):
                    f.write(f"{i}. {os.path.basename(file)}\n")
            
            print(f"Metadata saved to: {metadata_file}")
            return output_file
        else:
            print(f"Error: Failed to create production video file")
            return False
    
    except Exception as e:
        print(f"Error creating production video file: {e}")
        # Clean up temporary files if they exist
        if os.path.exists(concat_list):
            os.remove(concat_list)
        for file in processed_files:
            if file.startswith(temp_dir) and os.path.exists(file):
                os.remove(file)
        if os.path.exists(temp_dir):
            os.rmdir(temp_dir)
        return False

def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Create production video files by combining raw video files")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # List command
    list_parser = subparsers.add_parser("list", help="List raw video files for a channel")
    list_parser.add_argument("channel_id", type=int, help="Channel ID")
    
    # Create command
    create_parser = subparsers.add_parser("create", help="Create a production video file")
    create_parser.add_argument("channel_id", type=int, help="Channel ID")
    create_parser.add_argument("duration", type=int, help="Duration in minutes")
    
    args = parser.parse_args()
    
    # Load channel concepts
    concepts = load_channel_concepts()
    if not concepts:
        return
    
    # Execute the appropriate command
    if args.command == "list":
        video_files = list_raw_videos(args.channel_id, concepts)
        if video_files:
            print(f"\nRaw video files for channel {args.channel_id}:")
            for i, file in enumerate(video_files, 1):
                print(f"{i}. {os.path.basename(file)}")
        else:
            print(f"No raw video files found for channel {args.channel_id}")
    
    elif args.command == "create":
        result = create_production_video(args.channel_id, args.duration, concepts)
        if result:
            print(f"\nProduction video file created successfully: {os.path.basename(result)}")
        else:
            print("\nFailed to create production video file")
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main() 