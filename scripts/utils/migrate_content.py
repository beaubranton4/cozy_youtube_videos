#!/usr/bin/env python3
"""
Content Migration Script

This script helps migrate existing content from the legacy structure to the new channel-based structure.
It provides utilities for:
1. Listing available content in the legacy structure
2. Copying content to channel directories
3. Organizing content by channel

Usage:
    python migrate_content.py list
    python migrate_content.py copy CHANNEL_ID CONTENT_TYPE SOURCE_DIR
"""

import os
import sys
import json
import argparse
import shutil
from datetime import datetime

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

# Get channel information
def get_channel_info(channel_id, concepts):
    channel = next((c for c in concepts['channels'] if c['id'] == channel_id), None)
    if not channel:
        print(f"Error: Channel ID {channel_id} not found.")
        return None
    return channel

# List available content in the legacy structure
def list_content():
    print("\n=== Available Content in Legacy Structure ===\n")
    
    # Check if library directory exists
    if not os.path.exists('library'):
        print("Error: 'library' directory not found.")
        return
    
    # List content in library directory
    print("Music Content:")
    for root, dirs, files in os.walk('library'):
        for file in files:
            if file.endswith('.mp3'):
                print(f"- {os.path.join(root, file)}")
    
    print("\nVideo Content:")
    for root, dirs, files in os.walk('library'):
        for file in files:
            if file.endswith('.mp4'):
                print(f"- {os.path.join(root, file)}")
    
    # Check if final directory exists
    if os.path.exists('final'):
        print("\nFinal Videos:")
        for root, dirs, files in os.walk('final'):
            for file in files:
                if file.endswith('.mp4'):
                    print(f"- {os.path.join(root, file)}")

# Copy content to channel directory
def copy_content(channel_id, content_type, source_dir, concepts):
    channel = get_channel_info(channel_id, concepts)
    if not channel:
        return
    
    channel_name = channel['name'].replace(' ', '_')
    
    # Validate content type
    if content_type not in ['music', 'videos', 'final']:
        print(f"Error: Invalid content type '{content_type}'. Must be 'music', 'videos', or 'final'.")
        return
    
    # Validate source directory
    if not os.path.exists(source_dir):
        print(f"Error: Source directory '{source_dir}' not found.")
        return
    
    # Create target directory
    target_dir = f"channels/{channel_name}/{content_type}"
    os.makedirs(target_dir, exist_ok=True)
    
    # Copy content
    print(f"\n=== Copying {content_type} content to {channel_name} ===\n")
    
    # Determine file extensions based on content type
    if content_type == 'music':
        extensions = ['.mp3']
    elif content_type in ['videos', 'final']:
        extensions = ['.mp4']
    else:
        extensions = ['.mp3', '.mp4']
    
    # Copy files
    files_copied = 0
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            if any(file.endswith(ext) for ext in extensions):
                source_file = os.path.join(root, file)
                target_file = os.path.join(target_dir, file)
                
                print(f"Copying: {source_file} -> {target_file}")
                shutil.copy2(source_file, target_file)
                files_copied += 1
    
    print(f"\nCopied {files_copied} files to {target_dir}")
    
    # Create metadata entry
    if files_copied > 0:
        metadata_dir = f"channels/{channel_name}/metadata"
        os.makedirs(metadata_dir, exist_ok=True)
        
        metadata_file = f"{metadata_dir}/migration_{datetime.now().strftime('%Y%m%d')}.txt"
        with open(metadata_file, 'w') as f:
            f.write(f"=== Content Migration for {channel['name']} ===\n\n")
            f.write(f"Content Type: {content_type}\n")
            f.write(f"Source Directory: {source_dir}\n")
            f.write(f"Target Directory: {target_dir}\n")
            f.write(f"Files Copied: {files_copied}\n")
            f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        print(f"Migration metadata saved to: {metadata_file}")

def main():
    parser = argparse.ArgumentParser(description="Migrate content from legacy structure to channel-based structure")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # List content command
    list_parser = subparsers.add_parser("list", help="List available content in legacy structure")
    
    # Copy content command
    copy_parser = subparsers.add_parser("copy", help="Copy content to channel directory")
    copy_parser.add_argument("channel_id", type=int, help="Channel ID to copy content to")
    copy_parser.add_argument("content_type", choices=['music', 'videos', 'final'], help="Type of content to copy")
    copy_parser.add_argument("source_dir", help="Source directory containing content to copy")
    
    args = parser.parse_args()
    
    # Execute the appropriate command
    if args.command == "list":
        list_content()
    elif args.command == "copy":
        # Load channel concepts
        concepts = load_channel_concepts()
        if not concepts:
            return
        
        copy_content(args.channel_id, args.content_type, args.source_dir, concepts)
    else:
        parser.print_help()

if __name__ == "__main__":
    main() 