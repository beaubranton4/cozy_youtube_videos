#!/usr/bin/env python3
"""
Video Production Script

This script creates a final video by combining production music and video files.
It checks if production files are available and creates a final video of the specified duration.
"""

import os
import sys
import json
import argparse
import subprocess
from datetime import datetime

# Add parent directory to path to import channel_utils
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.channel_utils import load_channel_concepts, get_channel_info, validate_channel_directory

def check_assets(channel_id, concepts):
    """Check if production music and video files are available for a channel."""
    channel = get_channel_info(channel_id, concepts)
    if not channel:
        return False, False
    
    channel_name = channel['name'].replace(' ', '_')
    music_dir = f"channels/{channel_name}/music/production"
    videos_dir = f"channels/{channel_name}/videos/production"
    
    # Check if production directories exist
    if not os.path.exists(music_dir):
        print(f"Error: Production music directory {music_dir} does not exist.")
        print("Please run the music_production.py script to create production music files.")
        return False, False
    
    if not os.path.exists(videos_dir):
        print(f"Error: Production video directory {videos_dir} does not exist.")
        print("Please run the video_production_prep.py script to create production video files.")
        return False, False
    
    # Check if production files exist
    music_files = [f for f in os.listdir(music_dir) if f.endswith(('.mp3', '.wav', '.flac', '.ogg')) and f.startswith('production_')]
    video_files = [f for f in os.listdir(videos_dir) if f.endswith(('.mp4', '.mov', '.avi', '.mkv')) and f.startswith('production_')]
    
    has_music = len(music_files) > 0
    has_videos = len(video_files) > 0
    
    if not has_music:
        print(f"No production music files found in {music_dir}")
        print("Please run the music_production.py script to create production music files.")
    else:
        print(f"Found {len(music_files)} production music files in {music_dir}")
        for i, file in enumerate(music_files, 1):
            print(f"  {i}. {file}")
    
    if not has_videos:
        print(f"No production video files found in {videos_dir}")
        print("Please run the video_production_prep.py script to create production video files.")
    else:
        print(f"Found {len(video_files)} production video files in {videos_dir}")
        for i, file in enumerate(video_files, 1):
            print(f"  {i}. {file}")
    
    return has_music, has_videos

def get_latest_production_file(directory, file_type):
    """Get the latest production file from a directory."""
    if not os.path.exists(directory):
        return None
    
    files = [f for f in os.listdir(directory) if f.endswith(file_type) and f.startswith('production_')]
    if not files:
        return None
    
    # Sort files by modification time (newest first)
    files.sort(key=lambda x: os.path.getmtime(os.path.join(directory, x)), reverse=True)
    return os.path.join(directory, files[0])

def create_final_video(channel_id, duration_minutes, exclude_track, concepts):
    """Create a final video by combining production music and video files."""
    channel = get_channel_info(channel_id, concepts)
    if not channel:
        return False
    
    # Validate channel directory
    if not validate_channel_directory(channel_id, concepts):
        return False
    
    channel_name = channel['name'].replace(' ', '_')
    music_dir = f"channels/{channel_name}/music/production"
    videos_dir = f"channels/{channel_name}/videos/production"
    final_dir = f"channels/{channel_name}/final"
    
    # Ensure final directory exists
    os.makedirs(final_dir, exist_ok=True)
    
    # Check if production files exist
    has_music, has_videos = check_assets(channel_id, concepts)
    if not has_music or not has_videos:
        print("\nError: Missing production files. Please create them first.")
        return False
    
    # Get the latest production files
    music_file = get_latest_production_file(music_dir, '.mp3')
    video_file = get_latest_production_file(videos_dir, '.mp4')
    
    if not music_file or not video_file:
        print("\nError: Could not find latest production files.")
        return False
    
    print(f"\nUsing music file: {os.path.basename(music_file)}")
    print(f"Using video file: {os.path.basename(video_file)}")
    
    # Create output file name
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"{final_dir}/final_{duration_minutes}min_{timestamp}.mp4"
    
    # Use ffmpeg to combine music and video
    try:
        cmd = [
            'ffmpeg',
            '-i', video_file,
            '-i', music_file,
            '-map', '0:v',
            '-map', '1:a',
            '-c:v', 'copy',
            '-c:a', 'aac',
            '-b:a', '192k',
            '-shortest',
            output_file
        ]
        
        print(f"\nCreating final video: {output_file}")
        print(f"This may take a while depending on the file sizes...")
        
        subprocess.run(cmd, check=True)
        
        # Verify the output file exists
        if os.path.exists(output_file):
            print(f"\nFinal video created successfully: {os.path.basename(output_file)}")
            
            # Create a metadata file
            metadata_file = f"{final_dir}/metadata_{os.path.basename(output_file).replace('.mp4', '.txt')}"
            with open(metadata_file, 'w') as f:
                f.write(f"Final Video: {os.path.basename(output_file)}\n")
                f.write(f"Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Channel: {channel['name']}\n")
                f.write(f"Duration: {duration_minutes} minutes\n")
                f.write(f"Music File: {os.path.basename(music_file)}\n")
                f.write(f"Video File: {os.path.basename(video_file)}\n")
                f.write(f"Music Genre: {channel['music_genre']}\n")
                f.write(f"Vibe: {channel['vibe']}\n")
            
            print(f"Metadata saved to: {metadata_file}")
            return output_file
        else:
            print(f"Error: Failed to create final video")
            return False
    
    except Exception as e:
        print(f"Error creating final video: {e}")
        return False

def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Create final videos by combining production music and video files")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Check command
    check_parser = subparsers.add_parser("check", help="Check if production files are available")
    check_parser.add_argument("channel_id", type=int, help="Channel ID")
    
    # Create command
    create_parser = subparsers.add_parser("create", help="Create a final video")
    create_parser.add_argument("channel_id", type=int, help="Channel ID")
    create_parser.add_argument("duration", type=int, help="Duration in minutes")
    create_parser.add_argument("--exclude", help="Track to exclude (optional)")
    
    args = parser.parse_args()
    
    # Load channel concepts
    concepts = load_channel_concepts()
    if not concepts:
        return
    
    # Execute the appropriate command
    if args.command == "check":
        check_assets(args.channel_id, concepts)
    
    elif args.command == "create":
        result = create_final_video(args.channel_id, args.duration, args.exclude, concepts)
        if result:
            print(f"\nFinal video created successfully: {os.path.basename(result)}")
            print(f"You can find it in the channel's final directory.")
        else:
            print("\nFailed to create final video")
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main() 