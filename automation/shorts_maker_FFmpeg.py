"""Frame generation and FFmpeg rendering for YouTube Shorts."""

import os
import shutil
import subprocess
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

# Constants
WIDTH = 1080
HEIGHT = 1920
FPS = 30
BG_COLOR = "black"
TEXT_COLOR = "white"
FONT_SIZE = 72
MARGIN = 80


def _get_font(size: int) -> ImageFont.FreeTypeFont:
    """Return a built-in Pillow font at the given size."""
    try:
        return ImageFont.truetype("DejaVuSans-Bold.ttf", size)
    except OSError:
        try:
            return ImageFont.truetype("DejaVuSans.ttf", size)
        except OSError:
            return ImageFont.load_default()


def _wrap_text(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont, max_width: int) -> list[str]:
    """Wrap text into lines that fit within max_width."""
    words = text.split()
    lines = []
    current_line = []
    for word in words:
        test_line = " ".join(current_line + [word])
        bbox = draw.textbbox((0, 0), test_line, font=font)
        if bbox[2] - bbox[0] <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(" ".join(current_line))
            current_line = [word]
    if current_line:
        lines.append(" ".join(current_line))
    return lines


def generate_frame(text: str, output_path: str) -> None:
    """Generate a single 1080x1920 frame with centered white text on black background."""
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)
    font = _get_font(FONT_SIZE)

    max_text_width = WIDTH - (MARGIN * 2)
    lines = _wrap_text(draw, text, font, max_text_width)

    # Calculate total text height
    line_height = font.getbbox("Ay")[3] - font.getbbox("Ay")[1] + 20
    total_text_height = len(lines) * line_height
    start_y = (HEIGHT - total_text_height) // 2

    for i, line in enumerate(lines):
        bbox = draw.textbbox((0, 0), line, font=font)
        text_width = bbox[2] - bbox[0]
        x = (WIDTH - text_width) // 2
        y = start_y + i * line_height
        draw.text((x, y), line, fill=TEXT_COLOR, font=font)

    img.save(output_path, "PNG")


def render_video(frames_dir: str, output_path: str, durations: list[int]) -> None:
    """Render frames into an MP4 using FFmpeg with per-frame durations."""
    # Build a concat demuxer input file
    concat_file = os.path.join(frames_dir, "concat.txt")
    frame_files = sorted(
        [f for f in os.listdir(frames_dir) if f.startswith("frame_") and f.endswith(".png")]
    )

    with open(concat_file, "w") as cf:
        for i, frame_file in enumerate(frame_files):
            duration = durations[i] if i < len(durations) else 2
            cf.write(f"file '{frame_file}'\n")
            cf.write(f"duration {duration}\n")
        # FFmpeg requires the last file repeated without duration
        if frame_files:
            cf.write(f"file '{frame_files[-1]}'\n")

    cmd = [
        "ffmpeg",
        "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", concat_file,
        "-vsync", "vfr",
        "-pix_fmt", "yuv420p",
        "-vf", f"fps={FPS},scale={WIDTH}:{HEIGHT}:force_original_aspect_ratio=decrease,pad={WIDTH}:{HEIGHT}:(ow-iw)/2:(oh-ih)/2",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "23",
        output_path,
    ]

    subprocess.run(cmd, check=True)


def build_short(cards: list[str], durations: list[int], output_dir: str) -> str:
    """Generate frames, render video, cleanup, and return the output file path."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f"finance_fact_{timestamp}.mp4"
    output_path = os.path.join(output_dir, output_filename)

    frames_dir = os.path.join(output_dir, "frames")
    os.makedirs(frames_dir, exist_ok=True)

    # Generate frames
    for i, card in enumerate(cards):
        frame_path = os.path.join(frames_dir, f"frame_{i:03d}.png")
        generate_frame(card, frame_path)

    # Render video
    render_video(frames_dir, output_path, durations)

    # Cleanup temporary frames
    shutil.rmtree(frames_dir)

    return output_path
