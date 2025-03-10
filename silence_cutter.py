import subprocess
import re

def remove_silence(input_path, output_path, silence_threshold=-30, silence_duration=0.3):
    # Detect silence intervals
    detect_cmd = [
        'ffmpeg',
        '-i', input_path,
        '-af', f'silencedetect=n={silence_threshold}dB:d={silence_duration}',
        '-f', 'null', '-'
    ]
    
    process = subprocess.Popen(detect_cmd, stderr=subprocess.PIPE, text=True)
    _, stderr = process.communicate()

    # Parse silences
    silences = []
    for line in stderr.split('\n'):
        if 'silence_start' in line:
            start = float(re.search(r'silence_start: (\d+\.?\d*)', line).group(1))
        if 'silence_end' in line:
            end = float(re.search(r'silence_end: (\d+\.?\d*)', line).group(1))
            silences.append((start, end))

    # Get total duration
    def get_duration(input_path):
        cmd = [
            'ffprobe',
            '-v', 'error',
            '-show_entries', 'format=duration',
            '-of', 'default=noprint_wrappers=1:nokey=1',
            input_path
        ]
        return float(subprocess.check_output(cmd).decode().strip())
    
    total_duration = get_duration(input_path)

    # Calculate non-silent segments
    segments = []
    prev_end = 0.0
    for silence_start, silence_end in silences:
        if silence_start > prev_end:
            segments.append((prev_end, silence_start))
        prev_end = silence_end
    
    if prev_end < total_duration:
        segments.append((prev_end, total_duration))

    if not segments:
        segments.append((0.0, total_duration))

    # Build filtergraph (FIXED HERE)
    filter_chains = []
    concat_inputs = []
    
    for i, (start, end) in enumerate(segments):
        filter_chains.append(
            f"[0:v]trim=start={start}:end={end},setpts=PTS-STARTPTS[v{i}];"
            f"[0:a]atrim=start={start}:end={end},asetpts=PTS-STARTPTS[a{i}];"
        )
        concat_inputs.append(f"[v{i}][a{i}]")
    
    filter_concat = ''.join(filter_chains) + \
        f"{''.join(concat_inputs)}concat=n={len(segments)}:v=1:a=1[outv][outa]"

    # Execute FFmpeg
    subprocess.run([
        'ffmpeg', '-y',
        '-i', input_path,
        '-filter_complex', filter_concat,
        '-map', '[outv]',
        '-map', '[outa]',
        '-c:v', 'libx264', '-preset', 'fast',
        '-c:a', 'aac', '-b:a', '192k',
        output_path
    ], check=True)