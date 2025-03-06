# Cozy YouTube Videos Production Guide

This guide provides a comprehensive overview of how to use this project to create lo-fi music videos for different YouTube channels. It covers the entire workflow from project organization to video production and publishing.

## Table of Contents

1. [Project Overview](#project-overview)
2. [Project Structure](#project-structure)
3. [Channel Management](#channel-management)
4. [Manual Workflow](#manual-workflow)
5. [Automated Workflow](#automated-workflow)
6. [Video Production](#video-production)
7. [Publishing to YouTube](#publishing-to-youtube)
8. [Automation Tips](#automation-tips)

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
├── README.md                  # Main project documentation
└── PROJECT_GUIDE.md           # This guide
```

## Channel Management

### Available Channel Concepts

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

### Channel Manager Script

The `channel_manager.py` script helps you manage your YouTube channels and content. Here's how to use it:

#### List All Channel Concepts

```bash
python channel_manager.py list
```

This command displays all available channel concepts with their IDs, music genres, vibes, and target keywords.

#### Create Folder Structure for a Channel

```bash
python channel_manager.py create CHANNEL_ID
```

This command creates a folder structure for the specified channel ID.

#### Generate Video Title Suggestions

```bash
python channel_manager.py suggest CHANNEL_ID DURATION
```

This command generates title suggestions for a video of the specified duration (in minutes) based on the channel's target keywords.

#### Track Content for a Channel

```bash
python channel_manager.py track CHANNEL_ID VIDEO_PATH [--move]
```

This command tracks which content belongs to which channel by creating a metadata file. If the `--move` flag is provided, it also copies the file to the channel's final folder.

## Manual Workflow

The project now uses a modular approach with six separate steps that can be run individually:

### Step 1: Music Management

The `scripts/generation/music_manager.py` script handles raw music-related operations:

```bash
# Get instructions for music generation
python scripts/generation/music_manager.py instructions CHANNEL_ID

# List raw music files for a channel
python scripts/generation/music_manager.py list CHANNEL_ID

# Validate raw music files for a channel
python scripts/generation/music_manager.py validate CHANNEL_ID
```

#### Manual Music Creation/Collection

1. Create or collect 6-8 tracks in the channel's music genre
2. Each track should be 3-4 minutes long
3. Save the tracks to the channel's music/raw directory
4. Use MP3 format with 192kbps or higher bitrate
5. Name files descriptively (e.g., 'Gentle_Rain_Piano.mp3')

### Step 2: Music Production

The `scripts/generation/music_production.py` script handles production music creation:

```bash
# List raw music files for a channel
python scripts/generation/music_production.py list CHANNEL_ID

# Create a production music file
python scripts/generation/music_production.py create CHANNEL_ID DURATION_MINUTES [--exclude TRACK_NAME]
```

This step combines multiple raw music files into a single production music file of the specified duration. The production file is saved to the channel's music/production directory.

### Step 3: Video Management

The `scripts/generation/video_manager.py` script handles raw video-related operations:

```bash
# Get instructions for video generation
python scripts/generation/video_manager.py instructions CHANNEL_ID

# List raw video files for a channel
python scripts/generation/video_manager.py list CHANNEL_ID

# Validate raw video files for a channel
python scripts/generation/video_manager.py validate CHANNEL_ID
```

#### Manual Video Creation/Collection

1. Create or collect video content that matches the channel's vibe
2. Videos should be at least 30 seconds long (longer is better for looping)
3. Use 1080p resolution or higher
4. Save the videos to the channel's videos/raw directory
5. Use MP4 format with H.264 encoding
6. Name files descriptively (e.g., 'Cozy_Cabin_Fireplace.mp4')

### Step 4: Video Production Prep

The `scripts/generation/video_production_prep.py` script handles production video creation:

```bash
# List raw video files for a channel
python scripts/generation/video_production_prep.py list CHANNEL_ID

# Create a production video file
python scripts/generation/video_production_prep.py create CHANNEL_ID DURATION_MINUTES
```

This step combines multiple raw video files into a single production video file of the specified duration. The production file is saved to the channel's videos/production directory.

### Step 5: Final Video Production

The `scripts/generation/video_production.py` script handles the creation of final videos:

```bash
# Check if production music and video files are available
python scripts/generation/video_production.py check CHANNEL_ID

# Create a final video
python scripts/generation/video_production.py create CHANNEL_ID DURATION_MINUTES [--exclude TRACK_NAME]
```

This step combines a production music file and a production video file into a final video. The final video is saved to the channel's final directory.

### Step 6: Metadata Generation

The `scripts/generation/metadata_generator.py` script handles the generation of metadata for YouTube:

```bash
# Generate metadata for YouTube
python scripts/generation/metadata_generator.py generate CHANNEL_ID DURATION_MINUTES

# Get instructions for thumbnail creation
python scripts/generation/metadata_generator.py thumbnail CHANNEL_ID
```

## Automated Workflow

If you prefer to run all steps in sequence, you can use the workflow manager script:

```bash
python scripts/generation/workflow_manager.py CHANNEL_ID DURATION_MINUTES [--exclude TRACK_NAME]
```

This script will guide you through the entire workflow, from raw music and video management to production file creation, final video production, and metadata generation. It will:

1. Check if the channel directory exists and create it if necessary
2. Update the channel structure to include raw and production folders
3. Provide instructions for manually adding raw music files
4. Validate the raw music files you've added
5. Create a production music file by combining your raw music files
6. Provide instructions for manually adding raw video files
7. Validate the raw video files you've added
8. Create a production video file by combining your raw video files
9. Create a final video by combining your production music and video files
10. Generate metadata for YouTube, including title suggestions, description, and tags
11. Provide instructions for creating a thumbnail

## Video Production

### Creating a Final Video

The `create_final_lofi.sh` script combines music and video into a final video. It accepts the following parameters:

1. `DURATION`: Duration in minutes (default: 180)
2. `MUSIC_DIR`: Directory containing music files (default: "../../library/lo-fi/video_0")
3. `VIDEO_DIR`: Directory containing video files (default: "../../library/lo-fi/video_0")
4. `OUTPUT_FILE`: Path to the output file (default: "../../final/final_${DURATION}min_lofi.mp4")
5. `EXCLUDE_TRACK`: Track to exclude (optional, default: "Drift (1).mp3")

Example:
```bash
cd scripts/video
./create_final_lofi.sh 180 ../../channels/Vintage_Cabin_Retreats/music ../../channels/Vintage_Cabin_Retreats/videos ../../channels/Vintage_Cabin_Retreats/final/final_3hour_vintage_cabin.mp4
```

### Video Customization

You can customize your videos by:
- Using different music tracks for different channels
- Using different video backgrounds for different channels
- Adjusting the duration of the final video
- Excluding specific tracks from the final video

## Publishing to YouTube

### Generating Metadata

The metadata generator script generates metadata for YouTube, including:
- Title suggestions
- Description template
- Tags

You can find this metadata in the channel's metadata directory:
```
channels/Channel_Name/metadata/youtube_metadata_YYYYMMDD.txt
```

### Creating Thumbnails

Create thumbnails for your videos using the following guidelines:
1. Create a 1280x720 image that represents your video
2. Include text that matches your video title
3. Use bold, readable fonts and high contrast
4. Save the thumbnail to the channel's thumbnails directory

### Uploading to YouTube

1. Go to [YouTube Studio](https://studio.youtube.com/)
2. Click "CREATE" > "Upload video"
3. Select your final video file
4. Add the title, description, and tags from the metadata file
5. Upload your thumbnail
6. Set the visibility to Public, Unlisted, or Private
7. Click "PUBLISH"

## Automation Tips

### Content Migration

If you have existing content that you want to migrate to the new structure:

```bash
# List available content in the legacy structure
python scripts/utils/migrate_content.py list

# Copy content to a channel
python scripts/utils/migrate_content.py copy CHANNEL_ID CONTENT_TYPE SOURCE_DIR
```

Example:
```bash
python scripts/utils/migrate_content.py copy 1 music "library/lo-fi/video_0"
```

### Batch Processing

You can create multiple videos for different channels in batch:

```bash
for channel_id in 1 2 3; do
  python scripts/generation/workflow_manager.py $channel_id 180
  # Follow the prompts to create music and video content
done
```

### Reusing Content

You can reuse music and video content across different channels:

```bash
# Copy music from one channel to another
cp -r channels/Channel_Name_1/music/* channels/Channel_Name_2/music/

# Copy videos from one channel to another
cp -r channels/Channel_Name_1/videos/* channels/Channel_Name_2/videos/
```

### Scheduling Uploads

Use YouTube's scheduling feature to upload videos at optimal times:
1. When uploading a video, set the visibility to "Scheduled"
2. Choose a date and time for the video to be published
3. Click "SCHEDULE"

This allows you to batch-create videos and schedule them to be published over time.