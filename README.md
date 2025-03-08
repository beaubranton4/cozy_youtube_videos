# YouTube Channel Music Generator

This script automatically generates background music for YouTube videos based on channel content analysis. It uses natural language processing to analyze video titles and descriptions, then generates appropriate music using the MusicGen AI model.

## Features

- Analyzes YouTube channel content to understand the theme and vibe
- Generates custom background music using AI
- Free to use (uses Facebook's open-source MusicGen model)
- Customizable music duration
- Automatic keyword extraction and analysis

## Prerequisites

- Python 3.8 or higher
- YouTube Data API key (free from Google Cloud Console)

## Setup

1. Clone this repository
2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the project root and add your YouTube API key:
   ```
   YOUTUBE_API_KEY=your_api_key_here
   ```

## Usage

1. Run the script:
   ```bash
   python music_generator.py
   ```
2. Enter the YouTube channel ID when prompted
3. The script will analyze the channel content and generate appropriate background music
4. Generated music will be saved as a WAV file in the current directory

## Notes

- The free YouTube API has daily quotas, so be mindful of the number of requests
- Music generation can take a few minutes depending on your hardware
- Generated music is saved locally and can be used in your videos
- The script uses the small version of MusicGen for faster generation

## Limitations

- Generated music duration is limited to prevent memory issues
- Quality depends on the MusicGen small model capabilities
- YouTube API daily quota limitations apply

## License

This project is open-source and available under the MIT License.
