#!/usr/bin/env python3
"""
Channel Utilities

This module contains common functions used by all scripts in the Cozy YouTube Videos project.
It provides utilities for:
1. Loading channel concepts from the JSON file
2. Getting channel information by ID
3. Validating channel directories
4. Other common operations
"""

import os
import json
from datetime import datetime

def load_channel_concepts():
    """
    Load channel concepts from the JSON file.
    Returns the concepts dictionary or None if an error occurs.
    """
    try:
        # Try to load from the current directory first
        if os.path.exists('channel_concepts.json'):
            with open('channel_concepts.json', 'r') as f:
                return json.load(f)
        
        # If not found, try to load from the project root
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        concepts_path = os.path.join(project_root, 'channel_concepts.json')
        
        if os.path.exists(concepts_path):
            with open(concepts_path, 'r') as f:
                return json.load(f)
        
        print("Error: channel_concepts.json not found.")
        return None
    except FileNotFoundError:
        print("Error: channel_concepts.json not found.")
        return None
    except json.JSONDecodeError:
        print("Error: Invalid JSON in channel_concepts.json.")
        return None

def get_channel_info(channel_id, concepts):
    """
    Get channel information by ID.
    Returns the channel dictionary or None if not found.
    """
    channel = next((c for c in concepts['channels'] if c['id'] == channel_id), None)
    if not channel:
        print(f"Error: Channel ID {channel_id} not found.")
        return None
    return channel

def validate_channel_directory(channel_id, concepts):
    """
    Validate that a channel directory exists and has the required subdirectories.
    Returns True if valid, False otherwise.
    """
    channel = get_channel_info(channel_id, concepts)
    if not channel:
        return False
    
    channel_name = channel['name'].replace(' ', '_')
    channel_dir = f"channels/{channel_name}"
    
    if not os.path.exists(channel_dir):
        print(f"Error: Channel directory {channel_dir} does not exist.")
        return False
    
    required_dirs = [
        'music/raw', 
        'music/production', 
        'videos/raw', 
        'videos/production', 
        'final', 
        'thumbnails', 
        'metadata'
    ]
    missing_dirs = []
    
    for dir_name in required_dirs:
        dir_path = os.path.join(channel_dir, dir_name)
        if not os.path.exists(dir_path):
            missing_dirs.append(dir_name)
    
    if missing_dirs:
        print(f"Error: The following directories are missing: {', '.join(missing_dirs)}")
        print(f"Run 'python channel_manager.py create {channel_id}' to create them.")
        print(f"Then run 'python scripts/utils/update_channel_structure.py --channel {channel_id}' to update the structure.")
        return False
    
    return True

def format_duration(duration_minutes):
    """
    Format duration in minutes to a human-readable string.
    """
    if duration_minutes >= 60:
        hours = duration_minutes // 60
        return f"{hours} hour{'s' if hours > 1 else ''}"
    else:
        return f"{duration_minutes} minutes"

def get_current_month():
    """
    Get the current month name.
    """
    return datetime.now().strftime("%B")

def replace_month_placeholder(text):
    """
    Replace month placeholders with the current month name.
    Handles [Month], [Current Month], and [Insert Current Month] placeholders.
    """
    current_month = get_current_month()
    
    if "[Month]" in text:
        text = text.replace("[Month]", current_month)
    
    if "[Current Month]" in text:
        text = text.replace("[Current Month]", current_month)
    
    if "[Insert Current Month]" in text:
        text = text.replace("[Insert Current Month]", current_month)
    
    return text

def create_channel_folders(channel_id, concepts):
    """
    Create folder structure for a specific channel.
    Returns True if successful, False otherwise.
    """
    channel = get_channel_info(channel_id, concepts)
    if not channel:
        return False
    
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
    return True

def list_channels(concepts):
    """
    List all available channel concepts.
    """
    print("\n=== Available Channel Concepts ===\n")
    for channel in concepts['channels']:
        print(f"{channel['id']}. {channel['name']} ({channel['youtube_handle']})")
        print(f"   Music: {channel['music_genre']}")
        print(f"   Vibe: {channel['vibe']}")
        print(f"   Keywords: {', '.join(channel['target_keywords'])}")
        print()
    
    return True 