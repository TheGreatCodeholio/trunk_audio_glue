import os
import argparse
from pydub import AudioSegment
import pytz
from datetime import datetime


def extract_timestamp(filename):
    start = filename.find('-') + 1
    end = filename.find('_', start)
    return int(filename[start:end])


def extract_talkgroup_id(filename):
    end = filename.find('-')
    return filename[:end]


def convert_to_mp3(wav_path, mp3_path):
    audio = AudioSegment.from_wav(wav_path)
    audio.export(mp3_path, format="mp3")


def parse_datetime(date_str, tz_str):
    local = pytz.timezone(tz_str)
    naive = datetime.strptime(date_str, "%m/%d/%Y %I:%M%p")
    local_dt = local.localize(naive, is_dst=None)
    utc_dt = local_dt.astimezone(pytz.utc)
    return int(utc_dt.timestamp())


def main(folder_path, talkgroup_ids, start_time, end_time):
    # Scan the folder and find all WAV files
    files = [f for f in os.listdir(folder_path) if f.endswith('.wav')]

    # Filter files by talkgroup IDs if provided
    if talkgroup_ids:
        files = [f for f in files if extract_talkgroup_id(f) in talkgroup_ids]

    # Filter files by time range if provided
    if start_time is not None and end_time is not None:
        files = [f for f in files if start_time <= extract_timestamp(f) <= end_time]

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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Combine audio files based on talkgroup IDs and timestamps.")
    parser.add_argument("folder_path", type=str, help="Path to the folder containing audio files")
    parser.add_argument("-t", "--talkgroups", type=str, help="Comma-separated list of talkgroup IDs to include",
                        default="")
    parser.add_argument("-d", "--daterange", type=str,
                        help="Start and end time in 'MM/DD/YYYY HH:MMam/pm TZ' format, separated by a comma",
                        default="")

    args = parser.parse_args()

    talkgroup_ids = set(args.talkgroups.split(',')) if args.talkgroups else None

    start_time, end_time = None, None

    if args.daterange:
        try:
            start_str, end_str = args.daterange.split(',')
            start_time = parse_datetime(start_str.strip(), "UTC")  # Adjust the timezone as needed
            end_time = parse_datetime(end_str.strip(), "UTC")  # Adjust the timezone as needed
        except ValueError:
            print("Date range format is incorrect. Please use 'MM/DD/YYYY HH:MMam/pm TZ' format.")
            exit(1)

    main(args.folder_path, talkgroup_ids, start_time, end_time)
