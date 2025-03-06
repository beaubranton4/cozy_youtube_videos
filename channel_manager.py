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
        print(f"{channel['id']}. {channel['name']}")
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
        f.write(f"Music Genre: {channel['music_genre']}\n")
        f.write(f"Vibe: {channel['vibe']}\n")
        f.write(f"Target Keywords: {', '.join(channel['target_keywords'])}\n")
        f.write(f"Concept: {channel['concept']}\n")
        f.write(f"\nCreated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    print(f"\nChannel folder structure created for: {channel['name']}")

def main():
    parser = argparse.ArgumentParser(description="Manage YouTube channel concepts and content")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # List channels command
    list_parser = subparsers.add_parser("list", help="List all channel concepts")
    
    # Create folders command
    create_parser = subparsers.add_parser("create", help="Create folder structure for a channel")
    create_parser.add_argument("channel_id", type=int, help="Channel ID to create folders for")
    
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
    else:
        parser.print_help()

if __name__ == "__main__":
    main()