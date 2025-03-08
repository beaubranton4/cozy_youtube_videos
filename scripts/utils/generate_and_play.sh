#!/bin/bash

# Script to generate and play an extended lofi video
# This will create a 3-hour lofi video and then play it automatically

echo "=== Generating and Playing Extended Lofi Video ==="
echo "This script will:"
echo "1. Generate a 3-hour lofi video with alphabetically ordered audio tracks"
echo "2. Play the video once it's created"
echo ""
echo "Starting video generation..."

# Run the optimized script to create the extended lofi video
./create_extended_lofi_optimized.sh

# Check if the video was created successfully
if [ -f "final/extended_lofi_3hours.mp4" ]; then
    echo ""
    echo "Video generation complete! Starting playback..."
    echo "Press Q to quit playback"
    echo ""
    
    # Play the video
    ffplay "final/extended_lofi_3hours.mp4"
else
    echo ""
    echo "Error: Video file not found. Generation may have failed."
    echo "Check the output above for any error messages."
fi 