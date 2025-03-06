#!/usr/bin/env python3
"""
Workflow Manager

This script manages the entire workflow for creating lo-fi videos:
1. Music Management - List, validate, and provide instructions for raw music files
2. Music Production - Combine raw music files into production music files
3. Video Management - List, validate, and provide instructions for raw video files
4. Video Production Prep - Prepare raw video files for production
5. Final Video Production - Combine production music and video files into a final video
6. Metadata Generation - Generate metadata for YouTube
"""

import os
import sys
import argparse
import subprocess

# Add parent directory to path to import channel_utils
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.channel_utils import load_channel_concepts, get_channel_info, validate_channel_directory

def run_music_manager(channel_id, action):
    """
    Run the music manager script with the specified action.
    """
    script_path = os.path.join(os.path.dirname(__file__), 'music_manager.py')
    
    if not os.path.exists(script_path):
        print(f"Error: Music manager script not found at {script_path}")
        return False
    
    cmd = ['python', script_path, action, str(channel_id)]
    print(f"\nRunning: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True)
        return result.returncode == 0
    except subprocess.CalledProcessError:
        print("Error running music manager script")
        return False

def run_music_production(channel_id, duration_minutes, exclude_track=None):
    """
    Run the music production script to create a production music file.
    """
    script_path = os.path.join(os.path.dirname(__file__), 'music_production.py')
    
    if not os.path.exists(script_path):
        print(f"Error: Music production script not found at {script_path}")
        return False
    
    cmd = ['python', script_path, 'create', str(channel_id), str(duration_minutes)]
    
    if exclude_track:
        cmd.extend(['--exclude', exclude_track])
    
    print(f"\nRunning: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True)
        return result.returncode == 0
    except subprocess.CalledProcessError:
        print("Error running music production script")
        return False

def run_video_manager(channel_id, action):
    """
    Run the video manager script with the specified action.
    """
    script_path = os.path.join(os.path.dirname(__file__), 'video_manager.py')
    
    if not os.path.exists(script_path):
        print(f"Error: Video manager script not found at {script_path}")
        return False
    
    cmd = ['python', script_path, action, str(channel_id)]
    print(f"\nRunning: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True)
        return result.returncode == 0
    except subprocess.CalledProcessError:
        print("Error running video manager script")
        return False

def run_video_production_prep(channel_id, duration_minutes):
    """
    Run the video production prep script to create a production video file.
    """
    script_path = os.path.join(os.path.dirname(__file__), 'video_production_prep.py')
    
    if not os.path.exists(script_path):
        print(f"Error: Video production prep script not found at {script_path}")
        return False
    
    cmd = ['python', script_path, 'create', str(channel_id), str(duration_minutes)]
    print(f"\nRunning: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True)
        return result.returncode == 0
    except subprocess.CalledProcessError:
        print("Error running video production prep script")
        return False

def run_video_production(channel_id, duration_minutes, exclude_track=None):
    """
    Run the video production script to create a final video.
    """
    script_path = os.path.join(os.path.dirname(__file__), 'video_production.py')
    
    if not os.path.exists(script_path):
        print(f"Error: Video production script not found at {script_path}")
        return False
    
    cmd = ['python', script_path, 'create', str(channel_id), str(duration_minutes)]
    
    if exclude_track:
        cmd.extend(['--exclude', exclude_track])
    
    print(f"\nRunning: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True)
        return result.returncode == 0
    except subprocess.CalledProcessError:
        print("Error running video production script")
        return False

def run_metadata_generator(channel_id, duration_minutes):
    """
    Run the metadata generator script to generate metadata for YouTube.
    """
    script_path = os.path.join(os.path.dirname(__file__), 'metadata_generator.py')
    
    if not os.path.exists(script_path):
        print(f"Error: Metadata generator script not found at {script_path}")
        return False
    
    cmd = ['python', script_path, 'generate', str(channel_id), str(duration_minutes)]
    print(f"\nRunning: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True)
        return result.returncode == 0
    except subprocess.CalledProcessError:
        print("Error running metadata generator script")
        return False

def run_workflow(channel_id, duration_minutes, exclude_track=None):
    """
    Run the entire workflow for creating a lo-fi video.
    """
    # Load channel concepts
    concepts = load_channel_concepts()
    if not concepts:
        return False
    
    # Get channel info
    channel = get_channel_info(channel_id, concepts)
    if not channel:
        return False
    
    print(f"\n=== Starting Workflow for {channel['name']} ===")
    print(f"Duration: {duration_minutes} minutes")
    print(f"Channel ID: {channel_id}")
    print(f"Music Genre: {channel['music_genre']}")
    print(f"Vibe: {channel['vibe']}")
    
    # Validate channel directory
    if not validate_channel_directory(channel_id, concepts):
        print("\nCreating channel directory structure...")
        # Run channel_manager.py to create the directory structure
        cmd = ['python', 'channel_manager.py', 'create', str(channel_id)]
        try:
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError:
            print("Error creating channel directory structure")
            return False
    
    # Step 1: Music Management
    print("\n=== Step 1: Music Management ===")
    print("This step will help you manage raw music files for your channel.")
    
    # Provide instructions for music generation
    if not run_music_manager(channel_id, 'instructions'):
        return False
    
    # Ask user if they have added music files
    while True:
        response = input("\nHave you added music files to the channel? (y/n): ").lower()
        if response == 'y':
            break
        elif response == 'n':
            print("Please add music files before proceeding.")
            print("You can run this script again when you're ready.")
            return False
    
    # Validate music files
    if not run_music_manager(channel_id, 'validate'):
        return False
    
    # Step 2: Music Production
    print("\n=== Step 2: Music Production ===")
    print("This step will combine your raw music files into a production music file.")
    
    if not run_music_production(channel_id, duration_minutes, exclude_track):
        return False
    
    # Step 3: Video Management
    print("\n=== Step 3: Video Management ===")
    print("This step will help you manage raw video files for your channel.")
    
    # Provide instructions for video generation
    if not run_video_manager(channel_id, 'instructions'):
        return False
    
    # Ask user if they have added video files
    while True:
        response = input("\nHave you added video files to the channel? (y/n): ").lower()
        if response == 'y':
            break
        elif response == 'n':
            print("Please add video files before proceeding.")
            print("You can run this script again when you're ready.")
            return False
    
    # Validate video files
    if not run_video_manager(channel_id, 'validate'):
        return False
    
    # Step 4: Video Production Prep
    print("\n=== Step 4: Video Production Prep ===")
    print("This step will combine your raw video files into a production video file.")
    
    if not run_video_production_prep(channel_id, duration_minutes):
        return False
    
    # Step 5: Final Video Production
    print("\n=== Step 5: Final Video Production ===")
    print("This step will combine your production music and video files into a final video.")
    
    if not run_video_production(channel_id, duration_minutes, exclude_track):
        return False
    
    # Step 6: Metadata Generation
    print("\n=== Step 6: Metadata Generation ===")
    print("This step will generate metadata for YouTube.")
    
    if not run_metadata_generator(channel_id, duration_minutes):
        return False
    
    print("\n=== Workflow Complete ===")
    print(f"Your lo-fi video for {channel['name']} has been created successfully!")
    print("You can find the final video in the channel's final directory.")
    print("You can find the metadata in the channel's metadata directory.")
    
    return True

def main():
    parser = argparse.ArgumentParser(description="Manage the workflow for creating lo-fi videos")
    parser.add_argument("channel_id", type=int, help="Channel ID to create video for")
    parser.add_argument("duration", type=int, help="Video duration in minutes")
    parser.add_argument("--exclude", help="Track to exclude from the final video")
    
    args = parser.parse_args()
    
    run_workflow(args.channel_id, args.duration, args.exclude)

if __name__ == "__main__":
    main()