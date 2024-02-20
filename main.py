import ffmpeg
import argparse
import os


def get_video_duration(input_file):
    probe = ffmpeg.probe(input_file)
    duration = float(probe["format"]["duration"])
    return duration


def get_video_file_size_mb(input_file):
    probe = ffmpeg.probe(input_file)
    file_size = int(probe["format"]["size"])
    return file_size / 1e6


def convert_to_hh_mm_ss(seconds):
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


def move_to_videos_directory(filename, destination="~/Movies"):
    os.system(f"mkdir {destination}/{filename[:-4]}")
    os.system(f"mv {filename[:-4]}*{filename[-4:]} {destination}/{filename[:-4]}/")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", help="The filename of the input file.")
    parser.add_argument("output_file", help="The filename of the output file.")
    parser.add_argument(
        "--target_file_size", type=int, default=2000, help="Target file size in mb."
    )

    args = parser.parse_args()

    input_file = args.input_file
    output_file = args.output_file
    target_file_size = args.target_file_size

    file_size = get_video_file_size_mb(input_file)
    file_duration = get_video_duration(input_file)

    step = file_duration * (target_file_size / file_size)
    start = 0
    end = start + step if start + step < file_duration else file_duration
    output_no = 1

    while True:
        output_name = output_file[:-4] + f"_{output_no}" + output_file[-4:]
        ffmpeg.input(input_file, ss=start, to=end).output(output_name).run()

        start = end
        if start == file_duration:
            break
        end = end + step if end + step < file_duration else file_duration
        output_no += 1

    move_to_videos_directory(output_file)
