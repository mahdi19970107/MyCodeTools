import os
import platform
import subprocess
from pathlib import Path

# Define available filters
filters = [
    'crop=1080:1080:700:0',  # Crop1 (ED)
    'crop=1080:1080:0:0',    # Crop2 (AB)
    'eq=brightness=0.15:contrast=1.4:saturation=1.2:gamma=1.1',  # Light Fix
    'hqdn3d=1.5:1.5:6:6',    # Digital Noise Fix
    'unsharp=7:7:1.5:7:7:0.0',  # Strong Sharp & Noise
    'smartblur=1.5:-0.35:-3.5:0.65:0.25:2.0'  # Soft Sharp & Noise
]

filter_names = [
    'Crop1 (ED)',
    'Crop2 (AB)',
    'Light Fix',
    'Digital Noise Fix',
    'Strong Sharp & Noise',
    'Soft Sharp & Noise'
]

def get_input_directory():
    if platform.system() == 'Windows':
        default_dir = os.path.expanduser('~/Downloads')
    else:  # Termux/Android
        default_dir = os.path.expanduser('~/storage/downloads')
    
    current_dir = os.getcwd()
    input_dir = current_dir if current_dir != os.path.expanduser('~') else default_dir
    print(f"Using input directory: {input_dir}")
    return input_dir

def get_filter_and_cpu_selection():
    print("\nAvailable filters:")
    for i, (name, filter_) in enumerate(zip(filter_names, filters), 1):
        print(f"[{i}] {name} : {filter_}")
    
    while True:
        try:
            selection = input("\nEnter filter numbers to apply (e.g. 1,3,4) [default: 1,3,4,5], and add 'gpu' to use GPU (e.g. 1,3,gpu): ")
            use_gpu = False
            if not selection.strip():
                selected = [1, 3, 4, 5]
            else:
                parts = [x.strip().lower() for x in selection.split(',') if x.strip()]
                if 'gpu' in parts:
                    use_gpu = True
                    parts = [p for p in parts if p != 'gpu']
                selected = []
                for p in parts:
                    if p.isdigit():
                        selected.append(int(p))
            valid_selections = [i-1 for i in selected if 0 < i <= len(filters)]
            if not valid_selections:
                print("No valid filters selected. Please try again.")
                continue
            return valid_selections, use_gpu
        except ValueError:
            print("Invalid input. Please enter numbers separated by commas and/or 'gpu'.")

def process_videos(input_dir, selected_filters, filter_numbers):
    output_dir = os.path.join(input_dir, 'output')
    os.makedirs(output_dir, exist_ok=True)

    # Get all MP4 files
    mp4_files = list(Path(input_dir).glob('*.mp4'))
    if not mp4_files:
        print(f"No MP4 files found in {input_dir}")
        return

    # use_gpu is now passed as an argument

    for file_path in mp4_files:
        output_file = os.path.join(
            output_dir,
            f"{file_path.stem}_new({','.join(map(str, filter_numbers))}).mp4"
        )

        # Prepare ffmpeg command
        if platform.system() == 'Windows':
            if process_videos.use_gpu:
                cmd = [
                    'ffmpeg', '-hwaccel', 'dxva2', '-i', str(file_path),
                    '-vf', selected_filters,
                    '-c:v', 'h264_nvenc',
                    '-c:a', 'copy', output_file
                ]
            else:
                cmd = [
                    'ffmpeg', '-i', str(file_path),
                    '-vf', selected_filters,
                    '-c:v', 'libx264', '-crf', '23', '-preset', 'medium',
                    '-c:a', 'copy', output_file
                ]
        else:  # Termux/Android
            if process_videos.use_gpu:
                cmd = [
                    'ffmpeg', '-hwaccel', 'mediacodec', '-i', str(file_path),
                    '-vf', selected_filters,
                    '-c:v', 'h264_mediacodec',
                    '-c:a', 'copy', output_file
                ]
            else:
                cmd = [
                    'ffmpeg', '-i', str(file_path),
                    '-vf', selected_filters,
                    '-c:v', 'libx264', '-crf', '23', '-preset', 'medium',
                    '-c:a', 'copy', output_file
                ]

        try:
            subprocess.run(cmd, check=True)
            print(f"Processed: {file_path} -> {output_file}")
        except subprocess.CalledProcessError:
            print(f"Error processing {file_path}")
            return

def main():
    input_dir = get_input_directory()
    selected_indexes, use_gpu = get_filter_and_cpu_selection()
    # Combine selected filters
    selected_filters = ','.join(filters[i] for i in selected_indexes)
    filter_numbers = [i + 1 for i in selected_indexes]
    process_videos.use_gpu = use_gpu
    process_videos(input_dir, selected_filters, filter_numbers)
    print("\nCompleted!")

if __name__ == '__main__':
    main()