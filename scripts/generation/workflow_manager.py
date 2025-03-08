#!/usr/bin/env python3
"""
Workflow Manager for Cozy Anime Project

This script coordinates the entire workflow for creating a lo-fi video:
1. Music Management - Adding raw music files
2. Music Production - Creating production music files
3. Video Management - Adding raw video files
4. Video Production Prep - Creating production video files
5. Final Video Production - Combining production music and video files
6. Metadata Generation - Creating metadata for YouTube
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

def run_music_manager(channel_id, action):
    """Run the music_manager.py script with the specified action."""
    script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "music_manager.py")
    
    if not os.path.exists(script_path):
        print(f"Error: Script {script_path} not found.")
        return False
    
    # Make sure the script is executable
    os.chmod(script_path, 0o755)
    
    # Build the command
    cmd = [
        "python",
        script_path,
        action,
        str(channel_id)
    ]
    
    # Run the command
    try:
        result = subprocess.run(cmd, check=True)
        return result.returncode == 0
    except subprocess.CalledProcessError:
        return False

def run_music_production(channel_id, duration_minutes, exclude_track=None):
    """Run the music_production.py script to create production music files."""
    script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "music_production.py")
    
    if not os.path.exists(script_path):
        print(f"Error: Script {script_path} not found.")
        return False
    
    # Make sure the script is executable
    os.chmod(script_path, 0o755)
    
    # Build the command
    cmd = [
        "python",
        script_path,
        "create",
        str(channel_id),
        str(duration_minutes)
    ]
    
    if exclude_track:
        cmd.extend(["--exclude", exclude_track])
    
    # Run the command
    try:
        result = subprocess.run(cmd, check=True)
        return result.returncode == 0
    except subprocess.CalledProcessError:
        return False

def run_video_manager(channel_id, action):
    """Run the video_manager.py script with the specified action."""
    script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "video_manager.py")
    
    if not os.path.exists(script_path):
        print(f"Error: Script {script_path} not found.")
        return False
    
    # Make sure the script is executable
    os.chmod(script_path, 0o755)
    
    # Build the command
    cmd = [
        "python",
        script_path,
        action,
        str(channel_id)
    ]
    
    # Run the command
    try:
        result = subprocess.run(cmd, check=True)
        return result.returncode == 0
    except subprocess.CalledProcessError:
        return False

def run_video_production_prep(channel_id, duration_minutes):
    """Run the video_production_prep.py script to create production video files."""
    script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "video_production_prep.py")
    
    if not os.path.exists(script_path):
        print(f"Error: Script {script_path} not found.")
        return False
    
    # Make sure the script is executable
    os.chmod(script_path, 0o755)
    
    # Build the command
    cmd = [
        "python",
        script_path,
        "create",
        str(channel_id),
        str(duration_minutes)
    ]
    
    # Run the command
    try:
        result = subprocess.run(cmd, check=True)
        return result.returncode == 0
    except subprocess.CalledProcessError:
        return False

def run_video_production(channel_id, duration_minutes, exclude_track=None):
    """Run the video_production.py script to create the final video."""
    script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "video_production.py")
    
    if not os.path.exists(script_path):
        print(f"Error: Script {script_path} not found.")
        return False
    
    # Make sure the script is executable
    os.chmod(script_path, 0o755)
    
    # Build the command
    cmd = [
        "python",
        script_path,
        "create",
        str(channel_id),
        str(duration_minutes)
    ]
    
    if exclude_track:
        cmd.extend(["--exclude", exclude_track])
    
    # Run the command
    try:
        result = subprocess.run(cmd, check=True)
        return result.returncode == 0
    except subprocess.CalledProcessError:
        return False

def run_metadata_generator(channel_id, duration_minutes):
    """Run the metadata_generator.py script to generate metadata for YouTube."""
    script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "metadata_generator.py")
    
    if not os.path.exists(script_path):
        print(f"Error: Script {script_path} not found.")
        return False
    
    # Make sure the script is executable
    os.chmod(script_path, 0o755)
    
    # Build the command
    cmd = [
        "python",
        script_path,
        "generate",
        str(channel_id),
        str(duration_minutes)
    ]
    
    # Run the command
    try:
        result = subprocess.run(cmd, check=True)
        return result.returncode == 0
    except subprocess.CalledProcessError:
        return False

def run_workflow(channel_id, duration_minutes, exclude_track=None):
    """Run the entire workflow for creating a lo-fi video."""
    # Load channel concepts
    concepts = load_channel_concepts()
    if not concepts:
        return False
    
    # Get channel info
    channel = get_channel_info(channel_id, concepts)
    if not channel:
        return False
    
    # Validate channel directory
    if not validate_channel_directory(channel_id, concepts):
        # Create channel directory if it doesn't exist
        print(f"Channel directory for {channel['name']} does not exist. Creating it now...")
        
        # Run the channel_manager.py script to create the directory
        try:
            cmd = [
                "python",
                "channel_manager.py",
                "create",
                str(channel_id)
            ]
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError:
            print("Error: Failed to create channel directory.")
            return False
    
    # Update channel structure to include raw and production folders
    try:
        update_script = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "utils", "update_channel_structure.py")
        if os.path.exists(update_script):
            cmd = [
                "python",
                update_script,
                "--channel",
                str(channel_id)
            ]
            subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError:
        print("Warning: Failed to update channel structure. Continuing anyway...")
    
    print("\n" + "="*80)
    print(f"WORKFLOW INITIATED: {channel['name']}")
    print(f"Duration: {duration_minutes} minutes")
    print(f"Channel ID: {channel_id}")
    print(f"Music Genre: {channel['music_genre']}")
    print(f"Vibe: {channel['vibe']}")
    print("="*80)
    
    # Step 1: Music Management
    print("\n" + "="*80)
    print("STEP 1: MUSIC MANAGEMENT")
    print("="*80)
    
    # Show instructions for music generation
    print("\nGenerating music instructions...")
    run_music_manager(channel_id, "instructions")
    
    # Ask user if they have added music files
    while True:
        response = input("\nHave you added raw music files to the channel? (y/n): ").lower()
        if response == 'y':
            break
        elif response == 'n':
            print("Please add raw music files before continuing.")
            print(f"Add them to: channels/{channel['name'].replace(' ', '_')}/music/raw/")
            response = input("Would you like to continue without adding music files? (y/n): ").lower()
            if response == 'y':
                break
            else:
                return False
    
    # Validate music files
    print("\nValidating music files...")
    if not run_music_manager(channel_id, "validate"):
        print("Warning: Music validation failed. Continuing anyway...")
    
    # Step 2: Music Production
    print("\n" + "="*80)
    print("STEP 2: MUSIC PRODUCTION")
    print("="*80)
    
    # Create production music file
    print("\nCreating production music file...")
    if not run_music_production(channel_id, duration_minutes, exclude_track):
        print("Error: Failed to create production music file.")
        return False
    
    # Step 3: Video Management
    print("\n" + "="*80)
    print("STEP 3: VIDEO MANAGEMENT")
    print("="*80)
    
    # Show instructions for video generation
    print("\nGenerating video instructions...")
    run_video_manager(channel_id, "instructions")
    
    # Ask user if they have added video files
    while True:
        response = input("\nHave you added raw video files to the channel? (y/n): ").lower()
        if response == 'y':
            break
        elif response == 'n':
            print("Please add raw video files before continuing.")
            print(f"Add them to: channels/{channel['name'].replace(' ', '_')}/videos/raw/")
            response = input("Would you like to continue without adding video files? (y/n): ").lower()
            if response == 'y':
                break
            else:
                return False
    
    # Validate video files
    print("\nValidating video files...")
    if not run_video_manager(channel_id, "validate"):
        print("Warning: Video validation failed. Continuing anyway...")
    
    # Step 4: Video Production Prep
    print("\n" + "="*80)
    print("STEP 4: VIDEO PRODUCTION PREPARATION")
    print("="*80)
    
    # Create production video file
    print("\nCreating production video file...")
    if not run_video_production_prep(channel_id, duration_minutes):
        print("Error: Failed to create production video file.")
        return False
    
    # Step 5: Final Video Production
    print("\n" + "="*80)
    print("STEP 5: FINAL VIDEO PRODUCTION")
    print("="*80)
    
    # Ask user if they want to proceed with video production
    response = input("\nDo you want to proceed with creating the final video? (y/n): ").lower()
    if response != 'y':
        print("Video production skipped.")
        return False
    
    # Create final video
    print("\nCreating final video...")
    if not run_video_production(channel_id, duration_minutes, exclude_track):
        print("Error: Failed to create final video.")
        return False
    
    # Step 6: Metadata Generation
    print("\n" + "="*80)
    print("STEP 6: METADATA GENERATION")
    print("="*80)
    
    # Ask user if they want to generate metadata
    response = input("\nDo you want to generate metadata for YouTube? (y/n): ").lower()
    if response != 'y':
        print("Metadata generation skipped.")
        return True
    
    # Generate metadata
    print("\nGenerating metadata...")
    if not run_metadata_generator(channel_id, duration_minutes):
        print("Error: Failed to generate metadata.")
        return False
    
    # Generate thumbnail instructions
    print("\nGenerating thumbnail instructions...")
    script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "metadata_generator.py")
    if os.path.exists(script_path):
        cmd = [
            "python",
            script_path,
            "thumbnail",
            str(channel_id)
        ]
        try:
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError:
            print("Warning: Failed to generate thumbnail instructions.")
    
    print("\n" + "="*80)
    print("WORKFLOW COMPLETED SUCCESSFULLY!")
    print("="*80)
    
    print(f"\nYour {duration_minutes}-minute video for {channel['name']} has been created.")
    print(f"You can find it in: channels/{channel['name'].replace(' ', '_')}/final/")
    print(f"Metadata is available in: channels/{channel['name'].replace(' ', '_')}/metadata/")
    
    return True

def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Workflow Manager for Cozy Anime Project")
    parser.add_argument("channel_id", type=int, help="Channel ID")
    parser.add_argument("duration", type=int, help="Duration in minutes")
    parser.add_argument("--exclude", help="Track to exclude (optional)")
    
    args = parser.parse_args()
    
    run_workflow(args.channel_id, args.duration, args.exclude)

if __name__ == "__main__":
    main() 