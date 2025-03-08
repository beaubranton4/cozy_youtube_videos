#!/usr/bin/env python3
"""
Channel Manager for Cozy YouTube Videos

This script helps organize and manage content for different YouTube channel concepts.
It provides utilities for:
1. Listing available channel concepts
2. Creating folder structures for each channel
3. Suggesting video titles based on channel keywords
4. Tracking which content belongs to which channel
"""

import json
import os
import argparse
from datetime import datetime
import shutil

# Load channel concepts from JSON file
def load_channel_concepts():
    try:
        with open('channel_concepts.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Error: channel_concepts.json not found.")
        return None
    except json.JSONDecodeError:
        print("Error: Invalid JSON in channel_concepts.json.")
        return None

# List all available channel concepts
def list_channels(concepts):
    print("\n=== Available Channel Concepts ===\n")
    for channel in concepts['channels']:
        print(f"{channel['id']}. {channel['name']} ({channel['youtube_handle']})")
        print(f"   Music: {channel['music_genre']}")
        print(f"   Vibe: {channel['vibe']}")
        print(f"   Keywords: {', '.join(channel['target_keywords'])}")
        print()

# Create folder structure for a specific channel
def create_channel_folders(channel_id, concepts):
    channel = next((c for c in concepts['channels'] if c['id'] == channel_id), None)
    if not channel:
        print(f"Error: Channel ID {channel_id} not found.")
        return
    
    # Create base folder structure
    channel_name = channel['name'].replace(' ', '_')
    base_path = f"channels/{channel_name}"
    
    folders = [
        f"{base_path}/music/raw",
        f"{base_path}/music/production",
        f"{base_path}/videos/raw",
        f"{base_path}/videos/production",
        f"{base_path}/final",
        f"{base_path}/thumbnails",
        f"{base_path}/metadata"
    ]
    
    for folder in folders:
        os.makedirs(folder, exist_ok=True)
        print(f"Created: {folder}")
    
    # Create a channel info file
    with open(f"{base_path}/channel_info.txt", 'w') as f:
        f.write(f"Channel: {channel['name']}\n")
        f.write(f"YouTube Handle: {channel['youtube_handle']}\n")
        f.write(f"Music Genre: {channel['music_genre']}\n")
        f.write(f"Vibe: {channel['vibe']}\n")
        f.write(f"Target Keywords: {', '.join(channel['target_keywords'])}\n")
        f.write(f"Concept: {channel['concept']}\n")
        f.write(f"\nCreated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    print(f"\nChannel folder structure created for: {channel['name']} ({channel['youtube_handle']})")

# Generate video title suggestions based on channel keywords
def suggest_titles(channel_id, duration_minutes, concepts):
    channel = next((c for c in concepts['channels'] if c['id'] == channel_id), None)
    if not channel:
        print(f"Error: Channel ID {channel_id} not found.")
        return
    
    print(f"\n=== Title Suggestions for {channel['name']} ({channel['youtube_handle']}) ===\n")
    
    # Format duration string
    if duration_minutes >= 60:
        hours = duration_minutes // 60
        duration_str = f"{hours} hour{'s' if hours > 1 else ''}"
    else:
        duration_str = f"{duration_minutes} minutes"
    
    # Generate title variations
    for keyword in channel['target_keywords']:
        # Replace [Month] or [Current Month] with current month if present
        if "[Month]" in keyword or "[Current Month]" in keyword:
            current_month = datetime.now().strftime("%B")
            keyword = keyword.replace("[Month]", current_month).replace("[Current Month]", current_month)
        # Replace [Insert Current Month] with current month if present
        if "[Insert Current Month]" in keyword:
            current_month = datetime.now().strftime("%B")
            keyword = keyword.replace("[Insert Current Month]", current_month)
            
        print(f"• {keyword.capitalize()} | {duration_str}")
        print(f"• {duration_str} of {keyword.capitalize()}")
        
        # For longer videos, add "no ads" variant
        if duration_minutes >= 60:
            print(f"• {keyword.capitalize()} | {duration_str} (No Ads)")
    
    print("\nAdditional Variations:")
    print(f"• {channel['music_genre']} for {channel['vibe']} | {duration_str}")
    print(f"• {channel['vibe']} with {channel['music_genre']} | {duration_str}")

# Track which content belongs to which channel
def track_content(channel_id, video_path, concepts, move_file=False):
    channel = next((c for c in concepts['channels'] if c['id'] == channel_id), None)
    if not channel:
        print(f"Error: Channel ID {channel_id} not found.")
        return
    
    if not os.path.exists(video_path):
        print(f"Error: Video file {video_path} not found.")
        return
    
    channel_name = channel['name'].replace(' ', '_')
    base_path = f"channels/{channel_name}"
    
    # Create metadata entry
    metadata = {
        "channel_id": channel_id,
        "channel_name": channel['name'],
        "youtube_handle": channel['youtube_handle'],
        "file_name": os.path.basename(video_path),
        "original_path": os.path.abspath(video_path),
        "date_added": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "keywords": channel['target_keywords']
    }
    
    # Save metadata
    metadata_file = f"{base_path}/metadata/{os.path.splitext(os.path.basename(video_path))[0]}.json"
    os.makedirs(os.path.dirname(metadata_file), exist_ok=True)
    
    with open(metadata_file, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"Content tracked: {os.path.basename(video_path)} → {channel['name']} ({channel['youtube_handle']})")
    
    # Move file if requested
    if move_file:
        target_path = f"{base_path}/final/{os.path.basename(video_path)}"
        shutil.copy2(video_path, target_path)
        print(f"File copied to: {target_path}")

def main():
    parser = argparse.ArgumentParser(description="Manage YouTube channel concepts and content")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # List channels command
    list_parser = subparsers.add_parser("list", help="List all channel concepts")
    
    # Create folders command
    create_parser = subparsers.add_parser("create", help="Create folder structure for a channel")
    create_parser.add_argument("channel_id", type=int, help="Channel ID to create folders for")
    
    # Suggest titles command
    suggest_parser = subparsers.add_parser("suggest", help="Suggest video titles for a channel")
    suggest_parser.add_argument("channel_id", type=int, help="Channel ID to suggest titles for")
    suggest_parser.add_argument("duration", type=int, help="Video duration in minutes")
    
    # Track content command
    track_parser = subparsers.add_parser("track", help="Track which content belongs to which channel")
    track_parser.add_argument("channel_id", type=int, help="Channel ID the content belongs to")
    track_parser.add_argument("video_path", help="Path to the video file")
    track_parser.add_argument("--move", action="store_true", help="Move the file to the channel folder")
    
    args = parser.parse_args()
    
    # Load channel concepts
    concepts = load_channel_concepts()
    if not concepts:
        return
    
    # Execute the appropriate command
    if args.command == "list":
        list_channels(concepts)
    elif args.command == "create":
        create_channel_folders(args.channel_id, concepts)
    elif args.command == "suggest":
        suggest_titles(args.channel_id, args.duration, concepts)
    elif args.command == "track":
        track_content(args.channel_id, args.video_path, concepts, args.move)
    else:
        parser.print_help()

if __name__ == "__main__":
    main() 