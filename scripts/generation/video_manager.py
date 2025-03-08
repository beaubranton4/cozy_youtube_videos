#!/usr/bin/env python3
"""
Video Manager

This script handles video-related operations for the cozy anime project.
It provides utilities for:
1. Listing available videos in a channel's video directory
2. Validating video files (checking format, duration, resolution, etc.)
3. Providing instructions for manual video generation

Usage:
    python video_manager.py list CHANNEL_ID
    python video_manager.py validate CHANNEL_ID
    python video_manager.py instructions CHANNEL_ID
"""

import os
import sys
import json
import argparse
import subprocess
from datetime import datetime

# Add the parent directory to the path so we can import common modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.channel_utils import load_channel_concepts, get_channel_info

def list_videos(channel_id, concepts):
    """
    List all video files in a channel's video directory.
    """
    channel = get_channel_info(channel_id, concepts)
    if not channel:
        return False
    
    channel_name = channel['name'].replace(' ', '_')
    video_dir = f"channels/{channel_name}/videos"
    
    if not os.path.exists(video_dir):
        print(f"Error: Video directory {video_dir} does not exist.")
        return False
    
    print(f"\n=== Video Files for {channel['name']} ===")
    
    video_files = []
    for file in os.listdir(video_dir):
        if file.endswith(('.mp4', '.mov', '.avi', '.mkv')):
            video_files.append(file)
    
    if not video_files:
        print("No video files found.")
        return False
    
    for i, file in enumerate(video_files, 1):
        print(f"{i}. {file}")
    
    print(f"\nTotal: {len(video_files)} video files")
    return True

def validate_videos(channel_id, concepts):
    """
    Validate video files in a channel's video directory.
    Check format, duration, resolution, and other properties.
    """
    channel = get_channel_info(channel_id, concepts)
    if not channel:
        return False
    
    channel_name = channel['name'].replace(' ', '_')
    video_dir = f"channels/{channel_name}/videos"
    
    if not os.path.exists(video_dir):
        print(f"Error: Video directory {video_dir} does not exist.")
        return False
    
    print(f"\n=== Validating Video Files for {channel['name']} ===")
    
    video_files = []
    for file in os.listdir(video_dir):
        if file.endswith(('.mp4', '.mov', '.avi', '.mkv')):
            video_files.append(os.path.join(video_dir, file))
    
    if not video_files:
        print("No video files found.")
        return False
    
    valid_files = 0
    
    for file in video_files:
        print(f"Checking: {os.path.basename(file)}")
        
        # Use ffprobe to get file information
        try:
            # Get duration
            duration_result = subprocess.run(
                ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 
                 'default=noprint_wrappers=1:nokey=1', file],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            if duration_result.returncode != 0:
                print(f"  Error: Could not analyze file. {duration_result.stderr.strip()}")
                continue
            
            duration = float(duration_result.stdout.strip())
            
            # Get resolution
            resolution_result = subprocess.run(
                ['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 
                 'stream=width,height', '-of', 'csv=s=x:p=0', file],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            if resolution_result.returncode != 0:
                print(f"  Error: Could not get resolution. {resolution_result.stderr.strip()}")
                resolution = "Unknown"
            else:
                resolution = resolution_result.stdout.strip()
            
            # Print information
            print(f"  Duration: {duration:.2f} seconds ({duration/60:.2f} minutes)")
            print(f"  Resolution: {resolution}")
            
            # Check if duration is reasonable (at least 30 seconds for looping)
            if duration < 30:
                print(f"  Warning: Video is very short for looping ({duration:.2f} seconds)")
            
            # Check if resolution is at least 720p
            if resolution != "Unknown":
                width, height = map(int, resolution.split('x'))
                if height < 720:
                    print(f"  Warning: Resolution is below 720p ({resolution})")
            
            valid_files += 1
            
        except Exception as e:
            print(f"  Error: {str(e)}")
    
    print(f"\nValidation complete: {valid_files}/{len(video_files)} files are valid")
    
    return valid_files > 0

def generate_video_instructions(channel_id, concepts):
    """
    Provide instructions for manually generating video content for a channel.
    """
    channel = get_channel_info(channel_id, concepts)
    if not channel:
        return False
    
    channel_name = channel['name'].replace(' ', '_')
    vibe = channel['vibe']
    
    print(f"\n=== Video Generation Instructions for {channel['name']} ===")
    print(f"Vibe: {vibe}")
    
    # Create the videos directory if it doesn't exist
    video_dir = f"channels/{channel_name}/videos"
    os.makedirs(video_dir, exist_ok=True)
    
    print("\nManual Video Creation Steps:")
    print(f"1. Create or collect video content that matches the '{vibe}' aesthetic")
    print(f"2. Videos should be at least 30 seconds long (longer is better for looping)")
    print(f"3. Use 1080p resolution or higher")
    print(f"4. Save the videos to: {video_dir}/")
    print(f"5. Use MP4 format with H.264 encoding")
    print(f"6. Name files descriptively (e.g., 'Cozy_Cabin_Fireplace.mp4')")
    
    print("\nRecommended Video Resources:")
    print("- Your own footage")
    print("- Stock video libraries (e.g., Pexels, Pixabay)")
    print("- AI-generated videos (e.g., Runway, Stable Diffusion)")
    
    # Provide vibe-specific tips
    if "Cabin" in vibe or "Cozy" in vibe or "Fireplace" in vibe:
        print("\nVibe-Specific Tips:")
        print("- Focus on warm, inviting interior spaces")
        print("- Include elements like fireplaces, soft lighting, or rain on windows")
        print("- Use slow, subtle movements (e.g., flickering fire, gentle rain)")
    elif "Jazz" in vibe or "Piano" in vibe:
        print("\nVibe-Specific Tips:")
        print("- Create elegant, sophisticated environments")
        print("- Consider jazz clubs, piano lounges, or intimate concert settings")
        print("- Use soft, warm lighting and subtle camera movements")
    elif "ASMR" in vibe:
        print("\nVibe-Specific Tips:")
        print("- Focus on visually satisfying, calming scenes")
        print("- Include elements that suggest sound (e.g., rain, typing, page turning)")
        print("- Use slow, deliberate movements")
    elif "Urban" in vibe or "City" in vibe:
        print("\nVibe-Specific Tips:")
        print("- Capture city scenes from relaxing perspectives")
        print("- Consider rooftop views, cafe windows, or cozy urban apartments")
        print("- Use rain or snow effects for added coziness")
    elif "Nature" in vibe:
        print("\nVibe-Specific Tips:")
        print("- Focus on peaceful natural landscapes")
        print("- Include gentle movement like swaying trees or flowing water")
        print("- Consider adding weather effects like light rain or snow")
    
    return True

def main():
    parser = argparse.ArgumentParser(description="Manage videos for cozy anime channels")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # List videos command
    list_parser = subparsers.add_parser("list", help="List video files for a channel")
    list_parser.add_argument("channel_id", type=int, help="Channel ID")
    
    # Validate videos command
    validate_parser = subparsers.add_parser("validate", help="Validate video files for a channel")
    validate_parser.add_argument("channel_id", type=int, help="Channel ID")
    
    # Generate instructions command
    instructions_parser = subparsers.add_parser("instructions", help="Get instructions for video generation")
    instructions_parser.add_argument("channel_id", type=int, help="Channel ID")
    
    args = parser.parse_args()
    
    # Load channel concepts
    concepts = load_channel_concepts()
    if not concepts:
        return
    
    # Execute the appropriate command
    if args.command == "list":
        list_videos(args.channel_id, concepts)
    elif args.command == "validate":
        validate_videos(args.channel_id, concepts)
    elif args.command == "instructions":
        generate_video_instructions(args.channel_id, concepts)
    else:
        parser.print_help()

if __name__ == "__main__":
    main() 