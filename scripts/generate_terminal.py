from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import math

# =========================================================
# PATHS
# =========================================================

ROOT = Path(__file__).resolve().parents[1]

ASCII_FILE = ROOT / "assets" / "ascii-art.txt"
OUTPUT_FILE = ROOT / "assets" / "terminal.gif"

# =========================================================
# CANVAS
# Smaller width so GitHub scales it up more in the README
# =========================================================

WIDTH = 1350
HEIGHT = 740

FPS = 18
FRAME_MS = round(1000 / FPS)

# =========================================================
# ANIMATION SPEED
# =========================================================

ASCII_START = 0.35
ASCII_CPS = 52.0
ASCII_LINE_STAGGER = 0.045

TERM_COMMAND_CPS = 34.0
TERM_OUTPUT_CPS = 58.0
WELCOME_CPS = 30.0

TERM_LINE_PAUSE = 0.08
TERM_SECTION_PAUSE = 0.18

FINAL_HOLD = 2.5

# =========================================================
# LAYOUT
# =========================================================

ART_X = 34
ART_Y = 98
ART_LINE_H = 11

RIGHT_X = 658
TERM_START_Y = 108
TERM_LINE_STEP = 29
TERM_BLOCK_GAP = 36

# Outer terminal geometry
OUTER_LEFT = 10
OUTER_TOP = 10
OUTER_RIGHT = 1340
OUTER_BOTTOM = 730

TITLE_LEFT = 11
TITLE_TOP = 11
TITLE_RIGHT = 1339
TITLE_BOTTOM = 55

LEFT_PANE = (24, 56, 610, 716)
RIGHT_PANE = (638, 56, 1324, 716)

DIVIDER_X = 624
DIVIDER_TOP = 55
DIVIDER_BOTTOM = 716

LEFT_LABEL_X = 34
RIGHT_LABEL_X = 658
LABEL_Y = 70

TERM_WRAP_WIDTH = RIGHT_PANE[2] - RIGHT_X - 18

# =========================================================
# PROFILE
# =========================================================

PROFILE = {
    "name": "Rahym Faisal Khan",
    "title": "Software Development | Data Science | AI/ML",
    "about": "Building software, exploring data, and learning intelligent systems.",
    "languages": "Python  C++  C  Java  C#  JavaScript  TypeScript  Haskell",
    "web": "React  Node.js  HTML  CSS",
    "ai_data": "PyTorch  NumPy  Pandas  scikit-learn  LangChain  Hugging Face",
    "tools": "Git  GitHub  Docker  VS Code",
    "email": "rahymfaisal123@gmail.com",
    "linkedin": "linkedin.com/in/rahym-faisal-633a6b2b4",
}

# =========================================================
# COLORS
# =========================================================

BG = "#000000"

PANEL = "#020402"
TOP_BAR = "#071107"

BORDER = "#1f8f47"
DIVIDER = "#10351b"

GREEN = "#39d353"
ASCII_GREEN = "#2fd65b"

WHITE = "#f0f6fc"
TEXT = "#d2d7de"
BLUE = "#79c0ff"
MUTED = "#6e7681"

RED = "#ff5f56"
YELLOW = "#ffbd2e"
WINDOW_GREEN = "#27c93f"

# =========================================================
# LOAD FONTS
# =========================================================

def load_font(size, bold=False):
    candidates = []

    if bold:
        candidates += [
            "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf",
            "/usr/share/fonts/truetype/liberation2/LiberationMono-Bold.ttf",
            "/System/Library/Fonts/Monaco.ttf",
            "C:/Windows/Fonts/consolab.ttf",
        ]
    else:
        candidates += [
            "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
            "/usr/share/fonts/truetype/liberation2/LiberationMono-Regular.ttf",
            "/System/Library/Fonts/Monaco.ttf",
            "C:/Windows/Fonts/consola.ttf",
        ]

    for path in candidates:
        try:
            return ImageFont.truetype(path, size)
        except Exception:
            pass

    return ImageFont.load_default()


ASCII_FONT = load_font(10)

TERM_FONT = load_font(19)
TERM_BOLD = load_font(19, bold=True)

LABEL_FONT = load_font(16, bold=True)
TITLE_FONT = load_font(15)

# =========================================================
# LOAD ASCII ART
# =========================================================

ascii_lines = ASCII_FILE.read_text(
    encoding="utf-8"
).replace(
    "\t",
    "    "
).splitlines()

if not ascii_lines:
    ascii_lines = ["(ascii-art.txt is empty)"]

# =========================================================
# STATIC TERMINAL BACKGROUND
# =========================================================

def make_base():
    image = Image.new("RGB", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(image)

    # OUTER TERMINAL
    draw.rounded_rectangle(
        (OUTER_LEFT, OUTER_TOP, OUTER_RIGHT, OUTER_BOTTOM),
        radius=18,
        fill=PANEL,
        outline=BORDER,
        width=2
    )

    # TITLE BAR
    draw.rounded_rectangle(
        (TITLE_LEFT, TITLE_TOP, TITLE_RIGHT, TITLE_BOTTOM),
        radius=16,
        fill=TOP_BAR
    )

    draw.rectangle(
        (TITLE_LEFT, 38, TITLE_RIGHT, TITLE_BOTTOM),
        fill=TOP_BAR
    )

    # WINDOW BUTTONS
    buttons = [
        (34, RED),
        (57, YELLOW),
        (80, WINDOW_GREEN),
    ]

    for x, color in buttons:
        draw.ellipse(
            (x - 7, 33 - 7, x + 7, 33 + 7),
            fill=color
        )

    # WINDOW TITLE
    title = "rahym@github: ~/profile"
    title_width = draw.textlength(title, font=TITLE_FONT)

    draw.text(
        ((WIDTH - title_width) / 2, 23),
        title,
        font=TITLE_FONT,
        fill=MUTED
    )

    # LEFT PANE
    draw.rounded_rectangle(
        LEFT_PANE,
        radius=10,
        fill="#000000"
    )

    # RIGHT PANE
    draw.rounded_rectangle(
        RIGHT_PANE,
        radius=10,
        fill="#010301"
    )

    # DIVIDER
    draw.line(
        (DIVIDER_X, DIVIDER_TOP, DIVIDER_X, DIVIDER_BOTTOM),
        fill=DIVIDER,
        width=1
    )

    # LABELS
    draw.text(
        (LEFT_LABEL_X, LABEL_Y),
        "[ ./ascii-art.txt ]",
        font=LABEL_FONT,
        fill=GREEN
    )

    draw.text(
        (RIGHT_LABEL_X, LABEL_Y),
        "[ interactive shell // guest session ]",
        font=LABEL_FONT,
        fill=GREEN
    )

    return image


BASE_IMAGE = make_base()

# =========================================================
# TEXT / WRAP HELPERS
# =========================================================

MEASURE_IMAGE = Image.new("RGB", (10, 10), BG)
MEASURE_DRAW = ImageDraw.Draw(MEASURE_IMAGE)

def text_width(text, font):
    return MEASURE_DRAW.textlength(text, font=font)


def wrap_words(text, font, max_width):
    words = text.split()
    if not words:
        return [""]

    lines = []
    current = words[0]

    for word in words[1:]:
        candidate = current + " " + word
        if text_width(candidate, font) <= max_width:
            current = candidate
        else:
            lines.append(current)
            current = word

    lines.append(current)
    return lines


def wrap_words_indented(text, font, first_width, later_width):
    words = text.split()
    if not words:
        return [""]

    lines = []
    current = words[0]
    current_limit = first_width

    for word in words[1:]:
        candidate = current + " " + word
        if text_width(candidate, font) <= current_limit:
            current = candidate
        else:
            lines.append(current)
            current = word
            current_limit = later_width

    lines.append(current)
    return lines


def command_segments(text):
    return [
        ("rahym@github", GREEN, True),
        (":", MUTED, False),
        ("~", BLUE, True),
        ("$ ", MUTED, False),
        (text, WHITE, False),
    ]


def simple_segments(text, color=TEXT, bold=False):
    return [(text, color, bold)]


def prefixed_wrapped_segments(prefix, content, prefix_color=GREEN, prefix_bold=True,
                              content_color=TEXT, content_bold=False, gap="  "):
    prefix_width = text_width(prefix, TERM_BOLD if prefix_bold else TERM_FONT)
    gap_width = text_width(gap, TERM_FONT)

    first_width = max(60, TERM_WRAP_WIDTH - prefix_width - gap_width)
    continuation_indent = " " * (len(prefix) + len(gap))
    later_width = max(60, TERM_WRAP_WIDTH - text_width(continuation_indent, TERM_FONT))

    wrapped = wrap_words_indented(content, TERM_FONT, first_width, later_width)

    lines = []

    if wrapped:
        first_line = [
            (prefix, prefix_color, prefix_bold),
            (gap + wrapped[0], content_color, content_bold),
        ]
        lines.append(first_line)

        for continuation in wrapped[1:]:
            lines.append([
                (continuation_indent + continuation, content_color, content_bold)
            ])

    return lines


# =========================================================
# BUILD VISUAL TERMINAL LINES
# Each item is one visual line on the right pane
# =========================================================

visual_lines = []

def add_line(segments, cps, pause_after, step_after):
    visual_lines.append({
        "segments": segments,
        "cps": cps,
        "pause_after": pause_after,
        "step_after": step_after,
    })


def add_wrapped_plain_block(text, color=TEXT, bold=False, cps=TERM_OUTPUT_CPS,
                            block_pause=TERM_SECTION_PAUSE):
    lines = wrap_words(text, TERM_BOLD if bold else TERM_FONT, TERM_WRAP_WIDTH)
    for i, line in enumerate(lines):
        add_line(
            simple_segments(line, color, bold),
            cps,
            0.03 if i < len(lines) - 1 else block_pause,
            TERM_LINE_STEP if i < len(lines) - 1 else TERM_BLOCK_GAP
        )


def add_prefixed_block(prefix, content, prefix_color=GREEN, prefix_bold=True,
                       content_color=TEXT, content_bold=False, cps=TERM_OUTPUT_CPS,
                       block_pause=0.08, gap="  "):
    lines = prefixed_wrapped_segments(
        prefix=prefix,
        content=content,
        prefix_color=prefix_color,
        prefix_bold=prefix_bold,
        content_color=content_color,
        content_bold=content_bold,
        gap=gap
    )

    for i, line_segments in enumerate(lines):
        add_line(
            line_segments,
            cps,
            0.03 if i < len(lines) - 1 else block_pause,
            TERM_LINE_STEP if i < len(lines) - 1 else TERM_LINE_STEP
        )


# Welcome
add_line(
    [("Welcome to Rahym's GitHub", GREEN, True)],
    WELCOME_CPS,
    0.35,
    TERM_BLOCK_GAP
)

# whoami
add_line(command_segments("whoami"), TERM_COMMAND_CPS, TERM_LINE_PAUSE, TERM_LINE_STEP)
add_wrapped_plain_block(PROFILE["name"], color=GREEN, bold=True, cps=TERM_OUTPUT_CPS, block_pause=0.06)
add_wrapped_plain_block(PROFILE["title"], color=BLUE, bold=False, cps=TERM_OUTPUT_CPS, block_pause=TERM_SECTION_PAUSE)

# about
add_line(command_segments("cat about.txt"), TERM_COMMAND_CPS, TERM_LINE_PAUSE, TERM_LINE_STEP)
add_wrapped_plain_block(PROFILE["about"], color=TEXT, bold=False, cps=TERM_OUTPUT_CPS, block_pause=TERM_SECTION_PAUSE)

# stack
add_line(command_segments("./stack --list"), TERM_COMMAND_CPS, TERM_LINE_PAUSE, TERM_LINE_STEP)
add_prefixed_block("[+] languages", PROFILE["languages"], gap="  ", block_pause=0.08)
add_prefixed_block("[+] web", PROFILE["web"], gap="        ", block_pause=0.08)
add_prefixed_block("[+] ai/data", PROFILE["ai_data"], gap="    ", block_pause=0.08)
add_prefixed_block("[+] tools", PROFILE["tools"], gap="      ", block_pause=TERM_SECTION_PAUSE)

# contact
add_line(command_segments("./contact --show"), TERM_COMMAND_CPS, TERM_LINE_PAUSE, TERM_LINE_STEP)
add_prefixed_block("mail", PROFILE["email"], prefix_color=TEXT, prefix_bold=False,
                   content_color=TEXT, content_bold=False, gap="     ", block_pause=0.08)
add_prefixed_block("linkedin", PROFILE["linkedin"], prefix_color=TEXT, prefix_bold=False,
                   content_color=TEXT, content_bold=False, gap=" ", block_pause=TERM_SECTION_PAUSE)

# final prompt
add_line(
    [
        ("rahym@github", GREEN, True),
        (":", MUTED, False),
        ("~", BLUE, True),
        ("$ ", MUTED, False),
    ],
    TERM_COMMAND_CPS,
    0.0,
    TERM_LINE_STEP
)

# =========================================================
# PLACE TERMINAL LINES VERTICALLY
# =========================================================

current_y = TERM_START_Y
for line in visual_lines:
    line["y"] = current_y
    current_y += line["step_after"]

# =========================================================
# TIMING
# =========================================================

ascii_end = max(
    ASCII_START + index * ASCII_LINE_STAGGER + (len(line) / ASCII_CPS if line else 0)
    for index, line in enumerate(ascii_lines)
)

SHELL_START = max(2.2, ascii_end - 0.8)

timeline_lines = []
current_time = SHELL_START

for line in visual_lines:
    total_chars = sum(len(text) for text, _, _ in line["segments"])
    end_time = current_time + total_chars / line["cps"]

    timeline_lines.append({
        "y": line["y"],
        "segments": line["segments"],
        "cps": line["cps"],
        "start": current_time,
        "end": end_time,
        "chars": total_chars,
    })

    current_time = end_time + line["pause_after"]

ANIMATION_END = timeline_lines[-1]["end"]
TOTAL_TIME = ANIMATION_END + FINAL_HOLD

# =========================================================
# DRAW PARTIALLY-TYPED LINE
# =========================================================

def draw_segments(draw, x, y, segments, visible_chars):
    current_x = x
    remaining = visible_chars

    for text, color, bold in segments:
        font = TERM_BOLD if bold else TERM_FONT

        take = max(0, min(len(text), remaining))
        partial = text[:take]

        if partial:
            draw.text(
                (current_x, y),
                partial,
                font=font,
                fill=color
            )

        if take < len(text):
            current_x += draw.textlength(partial, font=font)
            break

        current_x += draw.textlength(text, font=font)
        remaining -= len(text)

    return current_x

# =========================================================
# RENDER ONE FRAME
# =========================================================

def render_frame(time_seconds):
    image = BASE_IMAGE.copy()
    draw = ImageDraw.Draw(image)

    # ASCII ART
    for index, line in enumerate(ascii_lines):
        line_start = ASCII_START + index * ASCII_LINE_STAGGER

        if time_seconds < line_start:
            continue

        elapsed = time_seconds - line_start
        visible = int(elapsed * ASCII_CPS) + 1
        visible = min(len(line), max(0, visible))

        if visible:
            draw.text(
                (ART_X, ART_Y + index * ART_LINE_H),
                line[:visible],
                font=ASCII_FONT,
                fill=ASCII_GREEN
            )

    # TERMINAL TEXT
    active_cursor = None

    for line in timeline_lines:
        if time_seconds < line["start"]:
            continue

        elapsed = time_seconds - line["start"]
        visible = int(elapsed * line["cps"]) + 1
        visible = min(line["chars"], max(0, visible))

        end_x = draw_segments(
            draw,
            RIGHT_X,
            line["y"],
            line["segments"],
            visible
        )

        if line["start"] <= time_seconds < line["end"] and visible < line["chars"]:
            active_cursor = (end_x, line["y"])

    # ACTIVE TYPING CURSOR
    if active_cursor:
        cursor_x, cursor_y = active_cursor
        draw.rectangle(
            (cursor_x + 1, cursor_y + 4, cursor_x + 9, cursor_y + 23),
            fill=GREEN
        )

    # FINAL BLINKING CURSOR
    elif time_seconds >= ANIMATION_END:
        final_line = timeline_lines[-1]

        cursor_x = draw_segments(
            draw,
            RIGHT_X,
            final_line["y"],
            final_line["segments"],
            final_line["chars"]
        )

        cursor_visible = int((time_seconds - ANIMATION_END) * 2) % 2 == 0

        if cursor_visible:
            draw.rectangle(
                (cursor_x + 1, final_line["y"] + 4, cursor_x + 9, final_line["y"] + 23),
                fill=GREEN
            )

    return image

# =========================================================
# BUILD GIF PALETTE
# =========================================================

palette_source = render_frame(ANIMATION_END).quantize(
    colors=64,
    method=Image.Quantize.MEDIANCUT
)

# =========================================================
# GENERATE FRAMES
# =========================================================

frame_count = math.ceil(TOTAL_TIME * FPS) + 1
frames = []

print()
print("Generating animated terminal...")
print(f"Frames: {frame_count}")
print(f"Duration: {TOTAL_TIME:.1f}s")
print()

for frame_number in range(frame_count):
    current_time = frame_number / FPS
    frame = render_frame(current_time)

    frame = frame.quantize(
        palette=palette_source,
        dither=Image.Dither.NONE
    )

    frames.append(frame)

    if frame_number % 50 == 0:
        print(f"{frame_number}/{frame_count}")

# =========================================================
# SAVE GIF
# =========================================================

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

frames[0].save(
    OUTPUT_FILE,
    save_all=True,
    append_images=frames[1:],
    duration=FRAME_MS,
    loop=0,
    optimize=True,
    disposal=1
)

size_mb = OUTPUT_FILE.stat().st_size / 1024 / 1024

print()
print(f"Generated: {OUTPUT_FILE}")
print(f"Size: {size_mb:.2f} MB")
print()
