# Silence Remover for Video/Audio Files

A Python script that uses FFmpeg to automatically detect and remove silent portions from video or audio files. The tool trims both audio and video streams, ensuring synchronization, and outputs a clean, seamless file without silent gaps.

## Features

- **Silence Detection**: Detects silent segments based on customizable dB threshold and minimum duration.
- **Precise Trimming**: Removes silence while maintaining audio-video synchronization.
- **Customizable Parameters**: Adjust silence threshold (`-dB`) and minimum silence duration.
- **Efficient Encoding**: Outputs video in H.264 and audio in AAC format for high-quality results.
- **Cross-Platform**: Works on any system with FFmpeg installed.

## Use Cases

- Remove awkward pauses or silence from recorded videos.
- Clean up podcasts or voiceovers by eliminating background noise gaps.
- Optimize video content for social media or presentations.

## Requirements

- Python 3.x
- FFmpeg (must be installed and accessible in the system PATH)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/silence-remover.git
   cd silence-remover
2. Install dependencies:
   ```bash
   pip install -r requirements.txt

## Usage

1. Python Script
   ```bash
   from silence_remover import remove_silence
   remove_silence("input.mp4", "output.mp4", silence_threshold=-30, silence_duration=0.3)

2. Command Line
Run the script directly from the command line:
```bash
python silence_remover.py input.mp4 output.mp4 -t -25 -d 0.5

## Arguments

- **`input.mp4`**: Path to the input video/audio file.
- **`output.mp4`**: Path to save the output file.
- **`-t` or `--threshold`**: Silence threshold in dB (default: `-30`).
- **`-d` or `--duration`**: Minimum silence duration in seconds (default: `0.3`).

---

## How It Works

1. **Silence Detection**:  
   The script uses FFmpeg's `silencedetect` filter to identify silent portions of the audio based on the specified threshold and duration.

2. **Segment Splitting**:  
   The video and audio are split into non-silent segments.

3. **Reconstruction**:  
   The non-silent segments are concatenated back together, ensuring audio-video synchronization.

4. **Output**:  
   The final file is saved without silent gaps, encoded in H.264 (video) and AAC (audio).

---

## Example

```bash
python silence_remover.py input.mp4 output.mp4 -t -25 -d 0.5

