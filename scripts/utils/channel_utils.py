#!/usr/bin/env python3
"""
Channel Utilities

Common utility functions for working with channel concepts and directories.
"""

import os
import json
import sys

def load_channel_concepts():
    """
    Load channel concepts from the JSON file.
    Tries to find the file in the current directory or project root.
    """
    # Try current directory first
    if os.path.exists('channel_concepts.json'):
        try:
            with open('channel_concepts.json', 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print("Error: Invalid JSON in channel_concepts.json.")
            return None
    
    # Try project root
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    concepts_path = os.path.join(project_root, 'channel_concepts.json')
    
    if os.path.exists(concepts_path):
        try:
            with open(concepts_path, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print("Error: Invalid JSON in channel_concepts.json.")
            return None
    
    print("Error: channel_concepts.json not found.")
    return None

def get_channel_info(channel_id, concepts=None):
    """
    Get information about a specific channel.
    """
    if concepts is None:
        concepts = load_channel_concepts()
        if not concepts:
            return None
    
    channel = next((c for c in concepts['channels'] if c['id'] == channel_id), None)
    if not channel:
        print(f"Error: Channel ID {channel_id} not found.")
        return None
    
    return channel

def validate_channel_directory(channel_id, concepts=None):
    """
    Validate that the channel directory exists and has the expected structure.
    """
    if concepts is None:
        concepts = load_channel_concepts()
        if not concepts:
            return False
    
    channel = get_channel_info(channel_id, concepts)
    if not channel:
        return False
    
    channel_name = channel['name'].replace(' ', '_')
    base_path = os.path.join('channels', channel_name)
    
    if not os.path.exists(base_path):
        print(f"Error: Channel directory {base_path} not found.")
        return False
    
    required_dirs = [
        os.path.join(base_path, 'music', 'raw'),
        os.path.join(base_path, 'music', 'production'),
        os.path.join(base_path, 'videos', 'raw'),
        os.path.join(base_path, 'videos', 'production'),
        os.path.join(base_path, 'final'),
        os.path.join(base_path, 'thumbnails'),
        os.path.join(base_path, 'metadata')
    ]
    
    for directory in required_dirs:
        if not os.path.exists(directory):
            print(f"Warning: Directory {directory} not found.")
            os.makedirs(directory, exist_ok=True)
            print(f"Created: {directory}")
    
    return True

def get_channel_path(channel_id, concepts=None):
    """
    Get the path to a channel's directory.
    """
    if concepts is None:
        concepts = load_channel_concepts()
        if not concepts:
            return None
    
    channel = get_channel_info(channel_id, concepts)
    if not channel:
        return None
    
    channel_name = channel['name'].replace(' ', '_')
    return os.path.join('channels', channel_name)

if __name__ == "__main__":
    # This script is not meant to be run directly
    print("This script is a utility module and is not meant to be run directly.")
    print("Import it in your scripts to use its functions.")
    sys.exit(1)