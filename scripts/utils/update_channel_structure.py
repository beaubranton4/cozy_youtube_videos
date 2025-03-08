#!/usr/bin/env python3
"""
Update Channel Structure

This script updates the directory structure for all channels to include raw and production folders
for both music and video content. It moves existing files to the raw folders.
"""

import os
import json
import shutil
from datetime import datetime

def load_channel_concepts():
    """Load channel concepts from JSON file."""
    try:
        # Try to load from current directory
        if os.path.exists('channel_concepts.json'):
            with open('channel_concepts.json', 'r') as f:
                return json.load(f)
        # Try to load from project root
        elif os.path.exists(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'channel_concepts.json')):
            with open(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'channel_concepts.json'), 'r') as f:
                return json.load(f)
        else:
            print("Error: channel_concepts.json not found.")
            return None
    except json.JSONDecodeError:
        print("Error: Invalid JSON in channel_concepts.json.")
        return None

def update_channel_structure(channel_id=None):
    """Update the directory structure for a specific channel or all channels."""
    concepts = load_channel_concepts()
    if not concepts:
        return
    
    channels = concepts['channels']
    if channel_id:
        channels = [c for c in channels if c['id'] == channel_id]
        if not channels:
            print(f"Error: Channel ID {channel_id} not found.")
            return
    
    for channel in channels:
        channel_name = channel['name'].replace(' ', '_')
        base_path = f"channels/{channel_name}"
        
        if not os.path.exists(base_path):
            print(f"Warning: Channel directory {base_path} does not exist. Skipping.")
            continue
        
        print(f"\nUpdating structure for channel: {channel['name']}")
        
        # Update music directory
        music_path = f"{base_path}/music"
        if os.path.exists(music_path):
            # Create raw and production folders
            os.makedirs(f"{music_path}/raw", exist_ok=True)
            os.makedirs(f"{music_path}/production", exist_ok=True)
            
            # Move existing files to raw folder
            files = [f for f in os.listdir(music_path) if os.path.isfile(os.path.join(music_path, f))]
            for file in files:
                if file.endswith(('.mp3', '.wav', '.flac', '.ogg')):
                    src = os.path.join(music_path, file)
                    dst = os.path.join(music_path, 'raw', file)
                    shutil.move(src, dst)
                    print(f"  Moved {file} to {music_path}/raw/")
        
        # Update videos directory
        videos_path = f"{base_path}/videos"
        if os.path.exists(videos_path):
            # Create raw and production folders
            os.makedirs(f"{videos_path}/raw", exist_ok=True)
            os.makedirs(f"{videos_path}/production", exist_ok=True)
            
            # Move existing files to raw folder
            files = [f for f in os.listdir(videos_path) if os.path.isfile(os.path.join(videos_path, f))]
            for file in files:
                if file.endswith(('.mp4', '.mov', '.avi', '.mkv')):
                    src = os.path.join(videos_path, file)
                    dst = os.path.join(videos_path, 'raw', file)
                    shutil.move(src, dst)
                    print(f"  Moved {file} to {videos_path}/raw/")
        
        # Create a log file
        log_file = f"{base_path}/metadata/structure_update_{datetime.now().strftime('%Y%m%d')}.txt"
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        with open(log_file, 'w') as f:
            f.write(f"Channel structure updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Added raw and production folders to music and videos directories.\n")
        
        print(f"  Structure update completed for {channel['name']}")

def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Update channel directory structure")
    parser.add_argument("--channel", type=int, help="Channel ID to update (default: all channels)")
    
    args = parser.parse_args()
    
    update_channel_structure(args.channel)
    
    print("\nChannel structure update completed.")
    print("Raw files are now in the 'raw' subdirectory of music and videos folders.")
    print("Production files should be placed in the 'production' subdirectory.")

if __name__ == "__main__":
    main() 