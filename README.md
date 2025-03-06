# Cozy YouTube Videos

A comprehensive project for creating lo-fi music videos for YouTube, organized by channel concepts.

## Project Overview

This project is designed to help you create lo-fi music videos for multiple YouTube channels, each with a specific music genre and visual vibe. The project includes tools for:

- Managing different channel concepts
- Organizing content by channel
- Generating music and video content
- Creating final videos by combining music and video
- Generating metadata for YouTube

## Project Structure

The project is organized as follows:

```
cozy_youtube_videos/
├── channels/                  # Channel-specific content
│   ├── Channel_Name_1/        # Each channel has its own directory
│   │   ├── music/             # Music files for this channel
│   │   │   ├── raw/           # Raw music files (individual tracks)
│   │   │   └── production/    # Production music files (combined tracks)
│   │   ├── videos/            # Video files for this channel
│   │   │   ├── raw/           # Raw video files (individual clips)
│   │   │   └── production/    # Production video files (combined clips)
│   │   ├── final/             # Final rendered videos
│   │   ├── thumbnails/        # Thumbnail images
│   │   ├── metadata/          # Metadata for YouTube
│   │   └── channel_info.txt   # Information about the channel
│   └── ...
├── scripts/                   # Scripts for automation
│   ├── utils/                 # Utility scripts
│   │   ├── channel_utils.py   # Common channel utilities
│   │   ├── update_channel_structure.py # Update channel directory structure
│   │   └── migrate_content.py # Content migration utilities
│   ├── generation/            # Content generation scripts
│   │   ├── music_manager.py   # Raw music management utilities
│   │   ├── music_production.py # Production music creation
│   │   ├── video_manager.py   # Raw video management utilities
│   │   ├── video_production_prep.py # Production video creation
│   │   ├── video_production.py # Final video production utilities
│   │   ├── metadata_generator.py # Metadata generation utilities
│   │   └── workflow_manager.py # Unified workflow manager
│   └── video/                 # Video production scripts
│       └── create_final_lofi.sh # Script for creating final videos
├── channel_concepts.json      # Channel concepts in JSON format
├── channel_manager.py         # Script for managing channels
├── README.md                  # This file
└── PROJECT_GUIDE.md           # Comprehensive guide
```

## Available Channel Concepts

We've defined 12 YouTube channel concepts, each pairing a specific music genre with a complementary vibe:

1. **Vintage Cabin Retreats** - Vintage Oldies + Cabin Comforts
2. **Tranquil Corner Jazz** - Tender Piano Jazz + Perfect Relaxing Corner
3. **Atmospheric Radio Archives** - Vintage Radio Broadcasts + ASMR Radio Experience
4. **Seasonal Lofi Rhythms** - Lofi Hip Hop + Monthly Seasonal Changes
5. **Deep Focus Garage** - Future Garage + Focus Enhancing
6. **Whispered Beats Studio** - Atmospheric Beats + ASMR Lofi
7. **Melodic Trap Sanctuaries** - Melodic Trap/Drill + Urban Relaxation Spaces
8. **Accent Jazz Journeys** - International Jazz Variations + ASMR Accent Experiences
9. **Winter Oldies Hearth** - Winter-themed Oldies + Cozy Fireplace Settings
10. **Culinary Lofi Bakery** - Gentle Lofi + ASMR Culinary Experiences
11. **Tender Night Melodies** - Tender Piano Jazz + Night-time Relaxation
12. **Atmospheric Nature Beats** - Atmospheric Beats + Natural Landscapes

## For More Information

See the `PROJECT_GUIDE.md` file for a comprehensive guide to using this project.