import os
import argparse
from pydub import AudioSegment


def extract_timestamp(filename):
    # Extracts the timestamp from the filename
    start = filename.find('-') + 1
    end = filename.find('_', start)
    return filename[start:end]


def extract_talkgroup_id(filename):
    # Extracts the talkgroup ID from the filename
    end = filename.find('-')
    return filename[:end]


def convert_to_mp3(wav_path, mp3_path):
    # Converts WAV to MP3
    audio = AudioSegment.from_wav(wav_path)
    audio.export(mp3_path, format="mp3")


def main(folder_path, talkgroup_ids):
    # Scan the folder and find all WAV files
    files = [f for f in os.listdir(folder_path) if f.endswith('.wav')]

    # Filter files by talkgroup IDs if provided
    if talkgroup_ids:
        files = [f for f in files if extract_talkgroup_id(f) in talkgroup_ids]

    # Sort files based on the extracted timestamp
    files.sort(key=extract_timestamp)

    # Initialize an empty audio segment
    combined = AudioSegment.empty()

    for file in files:
        wav_path = os.path.join(folder_path, file)
        mp3_path = wav_path.replace('.wav', '.mp3')

        # Convert to MP3 if it's not already an MP3 file
        if not os.path.exists(mp3_path):
            convert_to_mp3(wav_path, mp3_path)

        # Append to the combined audio
        combined += AudioSegment.from_mp3(mp3_path)

    # Export the combined audio
    combined.export("combined_output.mp3", format="mp3")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Combine audio files based on talkgroup IDs and timestamps.")
    parser.add_argument("folder_path", type=str, help="Path to the folder containing audio files")
    parser.add_argument("-t", "--talkgroups", type=str, help="Comma-separated list of talkgroup IDs to include",
                        default="")

    args = parser.parse_args()

    talkgroup_ids = set(args.talkgroups.split(',')) if args.talkgroups else None

    main(args.folder_path, talkgroup_ids)
