# Trunk Audio Gluer

This script combines multiple audio files into a single MP3 file. It is specifically designed to process `.wav` files in a given directory, sorting them based on timestamps in their filenames and optionally filtering by talkgroup IDs.

## Features

- **Timestamp Sorting**: Orders audio files based on the timestamp embedded in their filenames.
- **Talkgroup Filtering**: Optionally filters files by talkgroup IDs.
- **Format Conversion**: Converts `.wav` files to `.mp3` and combines them into a single MP3 file.

## Requirements

- Python 3
- `pydub` library
- `ffmpeg`

Before running the script, ensure you have Python 3 installed on your system. You can install the required Python library using pip:

```bash
pip install pydub
