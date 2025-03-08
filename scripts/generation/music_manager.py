#!/usr/bin/env python3
"""
Music Manager

This script handles music-related operations for the cozy anime project.
It provides utilities for:
1. Listing available music in a channel's music directory
2. Validating music files (checking format, duration, etc.)
3. Providing instructions for manual music generation

Usage:
    python music_manager.py list CHANNEL_ID
    python music_manager.py validate CHANNEL_ID
    python music_manager.py instructions CHANNEL_ID
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

def list_music(channel_id, concepts):
    """
    List all music files in a channel's music directory.
    """
    channel = get_channel_info(channel_id, concepts)
    if not channel:
        return False
    
    channel_name = channel['name'].replace(' ', '_')
    music_dir = f"channels/{channel_name}/music"
    
    if not os.path.exists(music_dir):
        print(f"Error: Music directory {music_dir} does not exist.")
        return False
    
    print(f"\n=== Music Files for {channel['name']} ===")
    
    music_files = []
    for file in os.listdir(music_dir):
        if file.endswith(('.mp3', '.wav', '.flac')):
            music_files.append(file)
    
    if not music_files:
        print("No music files found.")
        return False
    
    for i, file in enumerate(music_files, 1):
        print(f"{i}. {file}")
    
    print(f"\nTotal: {len(music_files)} music files")
    return True

def validate_music(channel_id, concepts):
    """
    Validate music files in a channel's music directory.
    Check format, duration, and other properties.
    """
    channel = get_channel_info(channel_id, concepts)
    if not channel:
        return False
    
    channel_name = channel['name'].replace(' ', '_')
    music_dir = f"channels/{channel_name}/music"
    
    if not os.path.exists(music_dir):
        print(f"Error: Music directory {music_dir} does not exist.")
        return False
    
    print(f"\n=== Validating Music Files for {channel['name']} ===")
    
    music_files = []
    for file in os.listdir(music_dir):
        if file.endswith(('.mp3', '.wav', '.flac')):
            music_files.append(os.path.join(music_dir, file))
    
    if not music_files:
        print("No music files found.")
        return False
    
    valid_files = 0
    total_duration = 0
    
    for file in music_files:
        print(f"Checking: {os.path.basename(file)}")
        
        # Use ffprobe to get file information
        try:
            result = subprocess.run(
                ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 
                 'default=noprint_wrappers=1:nokey=1', file],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            if result.returncode != 0:
                print(f"  Error: Could not analyze file. {result.stderr.strip()}")
                continue
            
            duration = float(result.stdout.strip())
            total_duration += duration
            
            # Check if duration is reasonable (between 2 and 10 minutes)
            if duration < 120:
                print(f"  Warning: File is very short ({duration:.2f} seconds)")
            elif duration > 600:
                print(f"  Warning: File is very long ({duration:.2f} seconds)")
            else:
                print(f"  Duration: {duration:.2f} seconds ({duration/60:.2f} minutes)")
            
            valid_files += 1
            
        except Exception as e:
            print(f"  Error: {str(e)}")
    
    print(f"\nValidation complete: {valid_files}/{len(music_files)} files are valid")
    print(f"Total music duration: {total_duration:.2f} seconds ({total_duration/60:.2f} minutes)")
    
    return valid_files > 0

def generate_music_instructions(channel_id, concepts):
    """
    Provide instructions for manually generating music for a channel.
    """
    channel = get_channel_info(channel_id, concepts)
    if not channel:
        return False
    
    channel_name = channel['name'].replace(' ', '_')
    music_genre = channel['music_genre']
    
    print(f"\n=== Music Generation Instructions for {channel['name']} ===")
    print(f"Genre: {music_genre}")
    
    # Create the music directory if it doesn't exist
    music_dir = f"channels/{channel_name}/music"
    os.makedirs(music_dir, exist_ok=True)
    
    print("\nManual Music Creation/Collection Steps:")
    print(f"1. Create or collect 6-8 tracks in the '{music_genre}' style")
    print(f"2. Each track should be 3-4 minutes long")
    print(f"3. Save the tracks to: {music_dir}/")
    print(f"4. Use MP3 format with 192kbps or higher bitrate")
    print(f"5. Name files descriptively (e.g., 'Gentle_Rain_Piano.mp3')")
    
    print("\nRecommended Music Resources:")
    print("- Your own compositions")
    print("- Royalty-free music libraries (e.g., Epidemic Sound, Artlist)")
    print("- AI music generation tools (e.g., Mubert, AIVA, Soundraw)")
    
    # Provide genre-specific tips
    if "Jazz" in music_genre or "Piano" in music_genre:
        print("\nGenre-Specific Tips:")
        print("- Focus on smooth, melodic piano pieces")
        print("- Include gentle percussion and bass")
        print("- Aim for a relaxed, contemplative mood")
    elif "Lofi" in music_genre or "Hip Hop" in music_genre:
        print("\nGenre-Specific Tips:")
        print("- Use dusty drum samples and vinyl crackle")
        print("- Include mellow chord progressions")
        print("- Add subtle bass lines and gentle melodies")
    elif "Oldies" in music_genre or "Vintage" in music_genre:
        print("\nGenre-Specific Tips:")
        print("- Look for tracks with a nostalgic quality")
        print("- Consider adding subtle vinyl crackle or room ambience")
        print("- Focus on warm, inviting tones")
    
    return True

def main():
    parser = argparse.ArgumentParser(description="Manage music for cozy anime channels")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # List music command
    list_parser = subparsers.add_parser("list", help="List music files for a channel")
    list_parser.add_argument("channel_id", type=int, help="Channel ID")
    
    # Validate music command
    validate_parser = subparsers.add_parser("validate", help="Validate music files for a channel")
    validate_parser.add_argument("channel_id", type=int, help="Channel ID")
    
    # Generate instructions command
    instructions_parser = subparsers.add_parser("instructions", help="Get instructions for music generation")
    instructions_parser.add_argument("channel_id", type=int, help="Channel ID")
    
    args = parser.parse_args()
    
    # Load channel concepts
    concepts = load_channel_concepts()
    if not concepts:
        return
    
    # Execute the appropriate command
    if args.command == "list":
        list_music(args.channel_id, concepts)
    elif args.command == "validate":
        validate_music(args.channel_id, concepts)
    elif args.command == "instructions":
        generate_music_instructions(args.channel_id, concepts)
    else:
        parser.print_help()

if __name__ == "__main__":
    main() 