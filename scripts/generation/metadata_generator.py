#!/usr/bin/env python3
"""
Metadata Generator

This script handles the generation of thumbnails and metadata for YouTube.
It provides utilities for:
1. Generating title suggestions based on channel keywords
2. Creating description templates
3. Generating tag lists
4. Providing instructions for thumbnail creation

Usage:
    python metadata_generator.py generate CHANNEL_ID DURATION_MINUTES
    python metadata_generator.py thumbnail CHANNEL_ID
"""

import os
import sys
import json
import argparse
from datetime import datetime

# Add the parent directory to the path so we can import common modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.channel_utils import load_channel_concepts, get_channel_info

def generate_metadata(channel_id, duration_minutes, concepts):
    """
    Generate metadata for YouTube, including title, description, and tags.
    """
    channel = get_channel_info(channel_id, concepts)
    if not channel:
        return False
    
    channel_name = channel['name'].replace(' ', '_')
    
    print(f"\n=== Generating YouTube Metadata for {channel['name']} ===")
    print(f"Duration: {duration_minutes} minutes")
    
    # Create metadata directory if it doesn't exist
    metadata_dir = f"channels/{channel_name}/metadata"
    os.makedirs(metadata_dir, exist_ok=True)
    
    # Format duration string
    if duration_minutes >= 60:
        hours = duration_minutes // 60
        duration_str = f"{hours} hour{'s' if hours > 1 else ''}"
    else:
        duration_str = f"{duration_minutes} minutes"
    
    # Generate title suggestions
    title_suggestions = []
    print("\nTitle Suggestions:")
    
    for keyword in channel['target_keywords']:
        # Replace [Month] with current month if present
        if "[Month]" in keyword:
            current_month = datetime.now().strftime("%B")
            keyword = keyword.replace("[Month]", current_month)
        
        title = f"{keyword.capitalize()} | {duration_str}"
        print(f"• {title}")
        title_suggestions.append(title)
        
        # For longer videos, add "no ads" variant
        if duration_minutes >= 60:
            title_with_no_ads = f"{keyword.capitalize()} | {duration_str} (No Ads)"
            print(f"• {title_with_no_ads}")
            title_suggestions.append(title_with_no_ads)
    
    # Generate additional title variations
    print("\nAdditional Title Variations:")
    
    additional_titles = [
        f"{duration_str} of {channel['music_genre']} for {channel['vibe']}",
        f"{channel['music_genre']} for {channel['vibe']} | {duration_str}",
        f"{channel['vibe']} with {channel['music_genre']} | {duration_str}"
    ]
    
    for title in additional_titles:
        print(f"• {title}")
        title_suggestions.append(title)
    
    # Generate description template
    print("\nDescription Template:")
    print("=" * 50)
    
    description = f"{channel['music_genre']} music for {channel['vibe'].lower()}. Perfect for studying, relaxing, or focusing.\n\n"
    description += f"Enjoy {duration_str} of uninterrupted {channel['music_genre'].lower()} music with {channel['vibe'].lower()} visuals.\n\n"
    description += "Timestamps:\n"
    description += "00:00 - Introduction\n"
    description += "00:30 - First Track\n"
    description += "...\n\n"
    description += "#lofi #relaxing #study #music"
    
    print(description)
    print("=" * 50)
    
    # Generate tags
    tags = [
        channel['music_genre'].lower(),
        channel['vibe'].lower(),
        "lofi", "relaxing", "study music", "focus music",
        f"{duration_str} music", "no ads", "background music",
        "concentration", "ambient", "chill"
    ]
    
    # Add channel-specific tags
    for keyword in channel['target_keywords']:
        if "[Month]" in keyword:
            current_month = datetime.now().strftime("%B")
            keyword = keyword.replace("[Month]", current_month)
        tags.append(keyword.lower())
    
    # Print unique tags
    unique_tags = list(set(tags))
    print("\nRecommended Tags:")
    print(", ".join(unique_tags))
    
    # Save metadata to file
    metadata_file = f"{metadata_dir}/youtube_metadata_{datetime.now().strftime('%Y%m%d')}.txt"
    
    with open(metadata_file, 'w') as f:
        f.write(f"=== YouTube Metadata for {channel['name']} ===\n\n")
        
        f.write("Title Suggestions:\n")
        for title in title_suggestions:
            f.write(f"• {title}\n")
        
        f.write("\nDescription Template:\n")
        f.write("=" * 50 + "\n")
        f.write(description + "\n")
        f.write("=" * 50 + "\n")
        
        f.write("\nRecommended Tags:\n")
        f.write(", ".join(unique_tags) + "\n")
    
    print(f"\nMetadata saved to: {metadata_file}")
    
    # Save metadata as JSON for programmatic use
    metadata_json = {
        "channel_id": channel_id,
        "channel_name": channel['name'],
        "duration_minutes": duration_minutes,
        "duration_string": duration_str,
        "title_suggestions": title_suggestions,
        "description": description,
        "tags": unique_tags,
        "generation_date": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    json_file = f"{metadata_dir}/youtube_metadata_{datetime.now().strftime('%Y%m%d')}.json"
    with open(json_file, 'w') as f:
        json.dump(metadata_json, f, indent=2)
    
    print(f"Metadata JSON saved to: {json_file}")
    
    return True

def generate_thumbnail_instructions(channel_id, concepts):
    """
    Provide instructions for creating thumbnails for YouTube videos.
    """
    channel = get_channel_info(channel_id, concepts)
    if not channel:
        return False
    
    channel_name = channel['name'].replace(' ', '_')
    
    print(f"\n=== Thumbnail Creation Instructions for {channel['name']} ===")
    
    # Create thumbnails directory if it doesn't exist
    thumbnails_dir = f"channels/{channel_name}/thumbnails"
    os.makedirs(thumbnails_dir, exist_ok=True)
    
    print("\nThumbnail Creation Steps:")
    print("1. Create a 1280x720 image that represents your video")
    print("2. Include text that matches your video title")
    print("3. Use bold, readable fonts and high contrast")
    print(f"4. Save the thumbnail to: {thumbnails_dir}/")
    
    print("\nRecommended Elements:")
    print("- Include duration in the thumbnail (e.g., '3 HOURS')")
    print("- Use consistent branding elements for your channel")
    print("- Include visual elements that match your channel's vibe")
    
    # Provide vibe-specific tips
    vibe = channel['vibe']
    print("\nVibe-Specific Tips:")
    
    if "Cabin" in vibe or "Cozy" in vibe or "Fireplace" in vibe:
        print("- Use warm, inviting colors (oranges, reds, browns)")
        print("- Include elements like fireplaces, soft lighting, or rain on windows")
        print("- Consider adding a subtle glow effect to emphasize coziness")
    elif "Jazz" in vibe or "Piano" in vibe:
        print("- Use elegant, sophisticated colors (deep blues, purples, golds)")
        print("- Include elements like pianos, jazz instruments, or music notes")
        print("- Consider a vintage or film grain effect for added atmosphere")
    elif "ASMR" in vibe:
        print("- Use calming, soft colors (pastels, light blues, soft greens)")
        print("- Include elements that suggest sound (e.g., headphones, microphones)")
        print("- Consider adding visual sound wave elements")
    elif "Urban" in vibe or "City" in vibe:
        print("- Use modern, sleek colors (neon accents, dark backgrounds)")
        print("- Include elements like city skylines, neon lights, or urban textures")
        print("- Consider adding rain or snow effects for added atmosphere")
    elif "Nature" in vibe:
        print("- Use natural, earthy colors (greens, blues, browns)")
        print("- Include elements like forests, mountains, or water")
        print("- Consider adding subtle weather effects like fog or light rays")
    else:
        print("- Use colors that match the mood of your channel's vibe")
        print("- Include visual elements that represent your channel's concept")
        print("- Maintain consistency across all your thumbnails")
    
    # Provide example thumbnail file
    example_file = f"{thumbnails_dir}/example_thumbnail.txt"
    with open(example_file, 'w') as f:
        f.write(f"=== Example Thumbnail Structure for {channel['name']} ===\n\n")
        f.write("Resolution: 1280x720 pixels\n")
        f.write("Format: JPG or PNG\n\n")
        f.write("Elements:\n")
        f.write("- Background image matching the '{vibe}' vibe\n")
        f.write("- Title text: Large, bold, easy to read\n")
        f.write("- Duration: Prominently displayed (e.g., '3 HOURS')\n")
        f.write("- Channel branding: Consistent logo or visual style\n\n")
        f.write("Tips:\n")
        f.write("- Use high contrast between text and background\n")
        f.write("- Keep it simple and clear\n")
        f.write("- Make sure text is readable at small sizes\n")
        f.write("- Use consistent style across all your videos\n")
    
    print(f"\nExample thumbnail structure saved to: {example_file}")
    
    return True

def main():
    parser = argparse.ArgumentParser(description="Generate metadata for YouTube videos")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Generate metadata command
    generate_parser = subparsers.add_parser("generate", help="Generate metadata for YouTube")
    generate_parser.add_argument("channel_id", type=int, help="Channel ID")
    generate_parser.add_argument("duration", type=int, help="Video duration in minutes")
    
    # Thumbnail instructions command
    thumbnail_parser = subparsers.add_parser("thumbnail", help="Get instructions for thumbnail creation")
    thumbnail_parser.add_argument("channel_id", type=int, help="Channel ID")
    
    args = parser.parse_args()
    
    # Load channel concepts
    concepts = load_channel_concepts()
    if not concepts:
        return
    
    # Execute the appropriate command
    if args.command == "generate":
        generate_metadata(args.channel_id, args.duration, concepts)
    elif args.command == "thumbnail":
        generate_thumbnail_instructions(args.channel_id, concepts)
    else:
        parser.print_help()

if __name__ == "__main__":
    main() 