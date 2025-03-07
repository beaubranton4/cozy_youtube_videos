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

We've defined 12 YouTube channel concepts, each with a unique music genre and visual vibe:

1. **Cozy Cabin Oldies** (@vintagecabinradio) - Vintage Oldies + Cabin Comforts
2. **Jewelry Store Jazz** (@jewelrystorejazz) - Tender Piano Jazz + Elegant & Luxurious Ambiance
3. **Retro Radio Archives** (@midnightradiovibes) - Vintage Radio Broadcasts + ASMR Radio Experience
4. **Seasonal Lofi Rhythms** (@lofiseasons) - Lofi Hip Hop + Monthly Seasonal Changes
5. **Deep Future Garage** (@neonmindtapes) - Future Garage + Immersive Soundscapes for Focus
6. **Midnight Auto Beats** (@midnightautowaves) - Future Garage x Industrial Ambient + Late Night Mechanic Shop
7. **Camp Fire Radio** (@mistyforestcamp) - ASMR x Nature x Vintage Radio + Campfire in a Foggy Forest
8. **Anime Jazz Club** (@animejazzclub) - Smooth Jazz x Anime Soundtracks + Retro Anime Lounge
9. **Ethereal Space Beats** (@etherealspacebeats) - Atmospheric Space Beats + Cinematic Cosmic Exploration
10. **Culinary Lofi Bakery** (@lofibakery) - Gentle Lofi + ASMR Culinary Experiences
11. **Grand Library Archives** (@grandlibraryradio) - Vintage Radio x Classical Jazz + Historic Library Ambiance
12. **Desert Lofi Mirage** (@desertlofimirage) - Lofi x Desert Ambience + Vast Open Desert Soundscapes

## For More Information

See the `PROJECT_GUIDE.md` file for a comprehensive guide to using this project.