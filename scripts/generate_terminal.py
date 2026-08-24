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
# =========================================================

WIDTH = 1600
HEIGHT = 740

FPS = 18
FRAME_MS = round(1000 / FPS)


# =========================================================
# ANIMATION SPEED
# =========================================================

#
# ASCII art:
#
# Each line begins shortly after the line above it,
# and every line reveals from left -> right.
#
# This gives a cascading "terminal printing" effect
# without taking 60+ seconds to draw the whole image.
#

ASCII_START = 0.35

# Characters typed per second on each ASCII line
ASCII_CPS = 52.0

# Delay before the next ASCII line begins typing
ASCII_LINE_STAGGER = 0.045


#
# Right-side terminal
#

# Commands type slightly slower
TERM_COMMAND_CPS = 34.0

# Output types slightly faster
TERM_OUTPUT_CPS = 58.0

# Welcome message speed
WELCOME_CPS = 30.0


# Small pauses between lines
TERM_LINE_PAUSE = 0.12

# Larger pauses between sections
TERM_SECTION_PAUSE = 0.22


# How long finished terminal remains visible
# before GIF restarts.
FINAL_HOLD = 2.5


# =========================================================
# LAYOUT
# =========================================================

ART_X = 40
ART_Y = 100
ART_LINE_H = 11

RIGHT_X = 770


# =========================================================
# PROFILE
# =========================================================

PROFILE = {
    "name": "Rahym Faisal Khan",

    "title": (
        "Software Development | Data Science | AI/ML"
    ),

    "about": (
        "Building software, exploring data, "
        "and learning intelligent systems."
    ),

    "languages": (
        "Python  C++  C  Java  C#  "
        "JavaScript  TypeScript  Haskell"
    ),

    "web": (
        "React  Node.js  HTML  CSS"
    ),

    "ai_data": (
        "PyTorch  NumPy  Pandas  scikit-learn  "
        "LangChain  Hugging Face"
    ),

    "tools": (
        "Git  GitHub  Docker  VS Code"
    ),

    "email": (
        "rahymfaisal123@gmail.com"
    ),

    "linkedin": (
        "linkedin.com/in/rahym-faisal-633a6b2b4"
    ),
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


ASCII_FONT = load_font(9)

TERM_FONT = load_font(16)
TERM_BOLD = load_font(16, bold=True)

LABEL_FONT = load_font(15, bold=True)
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
    ascii_lines = [
        "(ascii-art.txt is empty)"
    ]


# =========================================================
# CREATE STATIC TERMINAL BACKGROUND
# =========================================================

def make_base():

    image = Image.new(
        "RGB",
        (WIDTH, HEIGHT),
        BG
    )

    draw = ImageDraw.Draw(image)

    # -----------------------------------------------------
    # OUTER TERMINAL
    # -----------------------------------------------------

    draw.rounded_rectangle(
        (10, 10, 1590, 730),
        radius=18,
        fill=PANEL,
        outline=BORDER,
        width=2
    )

    # -----------------------------------------------------
    # TITLE BAR
    # -----------------------------------------------------

    draw.rounded_rectangle(
        (11, 11, 1589, 55),
        radius=16,
        fill=TOP_BAR
    )

    # Flatten bottom part of rounded title bar
    draw.rectangle(
        (11, 38, 1589, 55),
        fill=TOP_BAR
    )

    # -----------------------------------------------------
    # WINDOW BUTTONS
    # -----------------------------------------------------

    buttons = [
        (34, RED),
        (57, YELLOW),
        (80, WINDOW_GREEN),
    ]

    for x, color in buttons:

        draw.ellipse(
            (
                x - 7,
                33 - 7,
                x + 7,
                33 + 7,
            ),
            fill=color
        )

    # -----------------------------------------------------
    # WINDOW TITLE
    # -----------------------------------------------------

    title = "rahym@github: ~/profile"

    title_width = draw.textlength(
        title,
        font=TITLE_FONT
    )

    draw.text(
        (
            (WIDTH - title_width) / 2,
            23
        ),
        title,
        font=TITLE_FONT,
        fill=MUTED
    )

    # -----------------------------------------------------
    # LEFT BLACK PANE
    # -----------------------------------------------------

    draw.rounded_rectangle(
        (24, 56, 720, 716),
        radius=10,
        fill="#000000"
    )

    # -----------------------------------------------------
    # RIGHT BLACK PANE
    # -----------------------------------------------------

    draw.rounded_rectangle(
        (748, 56, 1564, 716),
        radius=10,
        fill="#010301"
    )

    # -----------------------------------------------------
    # DIVIDER
    # -----------------------------------------------------

    draw.line(
        (736, 55, 736, 716),
        fill=DIVIDER,
        width=1
    )

    # -----------------------------------------------------
    # LABELS
    # -----------------------------------------------------

    draw.text(
        (40, 70),
        "[ ./ascii-art.txt ]",
        font=LABEL_FONT,
        fill=GREEN
    )

    draw.text(
        (770, 70),
        "[ interactive shell // guest session ]",
        font=LABEL_FONT,
        fill=GREEN
    )

    return image


BASE_IMAGE = make_base()


# =========================================================
# TERMINAL LINE HELPERS
# =========================================================

def command(text):

    return [
        (
            "rahym@github",
            GREEN,
            True
        ),

        (
            ":",
            MUTED,
            False
        ),

        (
            "~",
            BLUE,
            True
        ),

        (
            "$ ",
            MUTED,
            False
        ),

        (
            text,
            WHITE,
            False
        ),
    ]


def output(text, color=TEXT, bold=False):

    return [
        (
            text,
            color,
            bold
        )
    ]


def char_count(segments):

    return sum(
        len(text)
        for text, _, _ in segments
    )


# =========================================================
# RIGHT SIDE CONTENT
# =========================================================

#
# Format:
#
# (
#     y position,
#     text segments,
#     characters per second,
#     pause afterwards
# )
#

terminal_specs = [

    # -----------------------------------------------------
    # WELCOME
    # -----------------------------------------------------

    (
        108,

        [
            (
                "Welcome to Rahym's GitHub",
                GREEN,
                True
            )
        ],

        WELCOME_CPS,

        0.35
    ),

    # -----------------------------------------------------
    # WHOAMI
    # -----------------------------------------------------

    (
        150,
        command("whoami"),
        TERM_COMMAND_CPS,
        TERM_LINE_PAUSE
    ),

    (
        183,
        output(
            PROFILE["name"],
            GREEN,
            True
        ),
        TERM_OUTPUT_CPS,
        0.08
    ),

    (
        211,
        output(
            PROFILE["title"],
            BLUE
        ),
        TERM_OUTPUT_CPS,
        TERM_SECTION_PAUSE
    ),

    # -----------------------------------------------------
    # ABOUT
    # -----------------------------------------------------

    (
        255,
        command(
            "cat about.txt"
        ),
        TERM_COMMAND_CPS,
        TERM_LINE_PAUSE
    ),

    (
        288,
        output(
            PROFILE["about"]
        ),
        TERM_OUTPUT_CPS,
        TERM_SECTION_PAUSE
    ),

    # -----------------------------------------------------
    # STACK
    # -----------------------------------------------------

    (
        334,
        command(
            "./stack --list"
        ),
        TERM_COMMAND_CPS,
        TERM_LINE_PAUSE
    ),

    (
        369,

        [
            (
                "[+] languages",
                GREEN,
                True
            ),

            (
                "  " + PROFILE["languages"],
                TEXT,
                False
            ),
        ],

        TERM_OUTPUT_CPS,

        0.08
    ),

    (
        399,

        [
            (
                "[+] web",
                GREEN,
                True
            ),

            (
                "        " + PROFILE["web"],
                TEXT,
                False
            ),
        ],

        TERM_OUTPUT_CPS,

        0.08
    ),

    (
        429,

        [
            (
                "[+] ai/data",
                GREEN,
                True
            ),

            (
                "    " + PROFILE["ai_data"],
                TEXT,
                False
            ),
        ],

        TERM_OUTPUT_CPS,

        0.08
    ),

    (
        459,

        [
            (
                "[+] tools",
                GREEN,
                True
            ),

            (
                "      " + PROFILE["tools"],
                TEXT,
                False
            ),
        ],

        TERM_OUTPUT_CPS,

        TERM_SECTION_PAUSE
    ),

    # -----------------------------------------------------
    # CONTACT
    # -----------------------------------------------------

    (
        510,

        command(
            "./contact --show"
        ),

        TERM_COMMAND_CPS,

        TERM_LINE_PAUSE
    ),

    (
        543,

        output(
            "mail     "
            + PROFILE["email"]
        ),

        TERM_OUTPUT_CPS,

        0.08
    ),

    (
        573,

        output(
            "linkedin "
            + PROFILE["linkedin"]
        ),

        TERM_OUTPUT_CPS,

        TERM_SECTION_PAUSE
    ),

    # -----------------------------------------------------
    # FINAL PROMPT
    # -----------------------------------------------------

    (
        625,

        [
            (
                "rahym@github",
                GREEN,
                True
            ),

            (
                ":",
                MUTED,
                False
            ),

            (
                "~",
                BLUE,
                True
            ),

            (
                "$ ",
                MUTED,
                False
            ),
        ],

        TERM_COMMAND_CPS,

        0.0
    ),
]


# =========================================================
# CALCULATE ASCII TIMING
# =========================================================

ascii_end = max(

    ASCII_START
    + index * ASCII_LINE_STAGGER
    + (
        len(line)
        / ASCII_CPS
        if line
        else 0
    )

    for index, line
    in enumerate(ascii_lines)
)


# Start welcome slightly BEFORE ASCII fully completes.
#
# This creates a nice overlap:
#
# ASCII still finishing
#         +
# "Welcome to Rahym's GitHub" starts typing
#

SHELL_START = max(
    2.2,
    ascii_end - 0.8
)


# =========================================================
# CALCULATE TERMINAL TIMELINE
# =========================================================

terminal_lines = []

current_time = SHELL_START


for (
    y,
    segments,
    cps,
    pause
) in terminal_specs:

    total_chars = char_count(
        segments
    )

    end_time = (
        current_time
        + total_chars / cps
    )

    terminal_lines.append({

        "y": y,

        "segments": segments,

        "cps": cps,

        "start": current_time,

        "end": end_time,

        "chars": total_chars,
    })

    current_time = (
        end_time
        + pause
    )


ANIMATION_END = (
    terminal_lines[-1]["end"]
)

TOTAL_TIME = (
    ANIMATION_END
    + FINAL_HOLD
)


# =========================================================
# DRAW A PARTIALLY-TYPED TERMINAL LINE
# =========================================================

def draw_segments(
    draw,
    x,
    y,
    segments,
    visible_chars
):

    current_x = x
    remaining = visible_chars

    for (
        text,
        color,
        bold
    ) in segments:

        font = (
            TERM_BOLD
            if bold
            else TERM_FONT
        )

        take = max(
            0,
            min(
                len(text),
                remaining
            )
        )

        partial = text[:take]

        if partial:

            draw.text(
                (
                    current_x,
                    y
                ),
                partial,
                font=font,
                fill=color
            )

        # -------------------------------------------------
        # Segment only partially typed
        # -------------------------------------------------

        if take < len(text):

            current_x += draw.textlength(
                partial,
                font=font
            )

            remaining = 0
            break

        # -------------------------------------------------
        # Entire segment visible
        # -------------------------------------------------

        current_x += draw.textlength(
            text,
            font=font
        )

        remaining -= len(text)

    return current_x


# =========================================================
# RENDER ONE FRAME
# =========================================================

def render_frame(time_seconds):

    image = BASE_IMAGE.copy()

    draw = ImageDraw.Draw(
        image
    )

    # =====================================================
    # ASCII ART
    # =====================================================

    for index, line in enumerate(
        ascii_lines
    ):

        line_start = (
            ASCII_START
            + index
            * ASCII_LINE_STAGGER
        )

        if time_seconds < line_start:
            continue

        elapsed = (
            time_seconds
            - line_start
        )

        visible = int(
            elapsed
            * ASCII_CPS
        ) + 1

        visible = min(
            len(line),
            max(
                0,
                visible
            )
        )

        if visible:

            draw.text(
                (
                    ART_X,
                    ART_Y
                    + index
                    * ART_LINE_H
                ),
                line[:visible],
                font=ASCII_FONT,
                fill=ASCII_GREEN
            )

    # =====================================================
    # TERMINAL TEXT
    # =====================================================

    active_cursor = None

    for line in terminal_lines:

        if (
            time_seconds
            < line["start"]
        ):
            continue

        elapsed = (
            time_seconds
            - line["start"]
        )

        visible = int(
            elapsed
            * line["cps"]
        ) + 1

        visible = min(
            line["chars"],
            max(
                0,
                visible
            )
        )

        end_x = draw_segments(
            draw,
            RIGHT_X,
            line["y"],
            line["segments"],
            visible
        )

        # Cursor follows currently typing line
        if (
            line["start"]
            <= time_seconds
            < line["end"]
            and visible
            < line["chars"]
        ):

            active_cursor = (
                end_x,
                line["y"]
            )

    # =====================================================
    # ACTIVE TYPING CURSOR
    # =====================================================

    if active_cursor:

        cursor_x, cursor_y = (
            active_cursor
        )

        draw.rectangle(
            (
                cursor_x + 1,
                cursor_y + 3,
                cursor_x + 8,
                cursor_y + 20,
            ),
            fill=GREEN
        )

    # =====================================================
    # FINAL BLINKING CURSOR
    # =====================================================

    elif (
        time_seconds
        >= ANIMATION_END
    ):

        final_line = (
            terminal_lines[-1]
        )

        cursor_x = draw_segments(
            draw,
            RIGHT_X,
            final_line["y"],
            final_line["segments"],
            final_line["chars"]
        )

        #
        # Blink twice every second.
        #

        cursor_visible = (
            int(
                (
                    time_seconds
                    - ANIMATION_END
                )
                * 2
            )
            % 2
            == 0
        )

        if cursor_visible:

            draw.rectangle(
                (
                    cursor_x + 1,
                    final_line["y"] + 3,
                    cursor_x + 8,
                    final_line["y"] + 20,
                ),
                fill=GREEN
            )

    return image


# =========================================================
# BUILD GIF PALETTE
# =========================================================

#
# Using a shared palette keeps the GIF dramatically smaller
# and prevents colors from flickering between frames.
#

palette_source = render_frame(
    ANIMATION_END
).quantize(
    colors=64,
    method=Image.Quantize.MEDIANCUT
)


# =========================================================
# GENERATE FRAMES
# =========================================================

frame_count = (
    math.ceil(
        TOTAL_TIME
        * FPS
    )
    + 1
)


frames = []


print()
print(
    "Generating animated terminal..."
)
print(
    f"Frames: {frame_count}"
)
print(
    f"Duration: {TOTAL_TIME:.1f}s"
)
print()


for frame_number in range(
    frame_count
):

    current_time = (
        frame_number
        / FPS
    )

    frame = render_frame(
        current_time
    )

    # Convert to shared GIF palette
    frame = frame.quantize(
        palette=palette_source,
        dither=Image.Dither.NONE
    )

    frames.append(
        frame
    )

    if (
        frame_number % 50
        == 0
    ):

        print(
            f"{frame_number}"
            f"/{frame_count}"
        )


# =========================================================
# SAVE GIF
# =========================================================

OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)


frames[0].save(

    OUTPUT_FILE,

    save_all=True,

    append_images=(
        frames[1:]
    ),

    duration=FRAME_MS,

    loop=0,

    optimize=True,

    disposal=1
)


size_mb = (
    OUTPUT_FILE.stat().st_size
    / 1024
    / 1024
)


print()
print(
    f"Generated: {OUTPUT_FILE}"
)
print(
    f"Size: {size_mb:.2f} MB"
)
print()
