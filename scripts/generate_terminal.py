from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import math
import re

# =========================================================
# PATHS
# =========================================================

ROOT = Path(__file__).resolve().parents[1]

ASCII_FILE = ROOT / "assets" / "ascii-art.txt"
OUTPUT_FILE = ROOT / "assets" / "terminal.gif"

# =========================================================
# CANVAS
# =========================================================

WIDTH = 1350
HEIGHT = 820

FPS = 18
FRAME_MS = round(1000 / FPS)

# =========================================================
# ANIMATION
# =========================================================

ASCII_START = 0.35
ASCII_CPS = 52.0
ASCII_LINE_STAGGER = 0.045

TERM_COMMAND_CPS = 34.0
TERM_OUTPUT_CPS = 56.0
WELCOME_CPS = 30.0

TERM_LINE_PAUSE = 0.08
TERM_SECTION_PAUSE = 0.20

FINAL_HOLD = 2.5

# =========================================================
# LAYOUT
# =========================================================

ART_X = 34
ART_Y = 100
ART_LINE_H = 11

RIGHT_X = 658
TERM_START_Y = 112

# Vertical spacing between wrapped lines
TERM_LINE_STEP = 31

# Extra vertical gap after sections
TERM_SECTION_GAP = 12

# Main terminal geometry
OUTER_LEFT = 10
OUTER_TOP = 10
OUTER_RIGHT = WIDTH - 10
OUTER_BOTTOM = HEIGHT - 10

TITLE_LEFT = 11
TITLE_TOP = 11
TITLE_RIGHT = WIDTH - 11
TITLE_BOTTOM = 55

LEFT_PANE = (
    24,
    56,
    610,
    HEIGHT - 24,
)

RIGHT_PANE = (
    638,
    56,
    WIDTH - 26,
    HEIGHT - 24,
)

DIVIDER_X = 624
DIVIDER_TOP = 55
DIVIDER_BOTTOM = HEIGHT - 24

LEFT_LABEL_X = 34
RIGHT_LABEL_X = 658
LABEL_Y = 70

# IMPORTANT:
# Everything on the right must fit inside this width.
RIGHT_PADDING = 24

TERM_MAX_WIDTH = (
    RIGHT_PANE[2]
    - RIGHT_X
    - RIGHT_PADDING
)

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
        "Python C++ C Java C# JavaScript "
        "TypeScript Haskell"
    ),

    "web": (
        "React Node.js HTML CSS"
    ),

    "ai_data": (
        "PyTorch NumPy Pandas scikit-learn "
        "LangChain Hugging Face"
    ),

    "tools": (
        "Git GitHub Docker VS Code"
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
# FONTS
# =========================================================

def load_font(size, bold=False):

    if bold:
        candidates = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf",
            "/usr/share/fonts/truetype/liberation2/LiberationMono-Bold.ttf",
            "/System/Library/Fonts/Monaco.ttf",
            "C:/Windows/Fonts/consolab.ttf",
        ]

    else:
        candidates = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
            "/usr/share/fonts/truetype/liberation2/LiberationMono-Regular.ttf",
            "/System/Library/Fonts/Monaco.ttf",
            "C:/Windows/Fonts/consola.ttf",
        ]

    for path in candidates:
        try:
            return ImageFont.truetype(
                path,
                size
            )
        except Exception:
            pass

    return ImageFont.load_default()


# Left ASCII
ASCII_FONT = load_font(10)

# Bigger right-side text
TERM_FONT = load_font(20)
TERM_BOLD = load_font(
    20,
    bold=True
)

LABEL_FONT = load_font(
    16,
    bold=True
)

TITLE_FONT = load_font(15)

# =========================================================
# MEASUREMENT
# =========================================================

MEASURE_IMAGE = Image.new(
    "RGB",
    (10, 10),
    BG
)

MEASURE_DRAW = ImageDraw.Draw(
    MEASURE_IMAGE
)


def get_font(bold):
    return TERM_BOLD if bold else TERM_FONT


def pixel_width(text, bold=False):

    return MEASURE_DRAW.textlength(
        text,
        font=get_font(bold)
    )


# =========================================================
# ASCII ART
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
# TERMINAL BACKGROUND
# =========================================================

def make_base():

    image = Image.new(
        "RGB",
        (WIDTH, HEIGHT),
        BG
    )

    draw = ImageDraw.Draw(
        image
    )

    # -----------------------------------------------------
    # OUTER TERMINAL
    # -----------------------------------------------------

    draw.rounded_rectangle(
        (
            OUTER_LEFT,
            OUTER_TOP,
            OUTER_RIGHT,
            OUTER_BOTTOM
        ),
        radius=18,
        fill=PANEL,
        outline=BORDER,
        width=2
    )

    # -----------------------------------------------------
    # TITLE BAR
    # -----------------------------------------------------

    draw.rounded_rectangle(
        (
            TITLE_LEFT,
            TITLE_TOP,
            TITLE_RIGHT,
            TITLE_BOTTOM
        ),
        radius=16,
        fill=TOP_BAR
    )

    draw.rectangle(
        (
            TITLE_LEFT,
            38,
            TITLE_RIGHT,
            TITLE_BOTTOM
        ),
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
                26,
                x + 7,
                40
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
    # LEFT PANE
    # -----------------------------------------------------

    draw.rounded_rectangle(
        LEFT_PANE,
        radius=10,
        fill="#000000"
    )

    # -----------------------------------------------------
    # RIGHT PANE
    # -----------------------------------------------------

    draw.rounded_rectangle(
        RIGHT_PANE,
        radius=10,
        fill="#010301"
    )

    # -----------------------------------------------------
    # DIVIDER
    # -----------------------------------------------------

    draw.line(
        (
            DIVIDER_X,
            DIVIDER_TOP,
            DIVIDER_X,
            DIVIDER_BOTTOM
        ),
        fill=DIVIDER,
        width=1
    )

    # -----------------------------------------------------
    # LABELS
    # -----------------------------------------------------

    draw.text(
        (
            LEFT_LABEL_X,
            LABEL_Y
        ),
        "[ ./ascii-art.txt ]",
        font=LABEL_FONT,
        fill=GREEN
    )

    draw.text(
        (
            RIGHT_LABEL_X,
            LABEL_Y
        ),
        "[ interactive shell // guest session ]",
        font=LABEL_FONT,
        fill=GREEN
    )

    return image


BASE_IMAGE = make_base()

# =========================================================
# SEGMENT HELPERS
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


def output(
    text,
    color=TEXT,
    bold=False
):

    return [
        (
            text,
            color,
            bold
        )
    ]


def prefixed(
    prefix,
    content,
    prefix_color=GREEN,
    prefix_bold=True,
    content_color=TEXT
):

    return [
        (
            prefix,
            prefix_color,
            prefix_bold
        ),
        (
            "  ",
            TEXT,
            False
        ),
        (
            content,
            content_color,
            False
        ),
    ]


# =========================================================
# REAL PIXEL-BASED WRAPPING
# =========================================================

def merge_piece(
    pieces,
    text,
    color,
    bold
):

    if not text:
        return

    if (
        pieces
        and pieces[-1][1] == color
        and pieces[-1][2] == bold
    ):

        old_text, _, _ = pieces[-1]

        pieces[-1] = (
            old_text + text,
            color,
            bold
        )

    else:

        pieces.append(
            (
                text,
                color,
                bold
            )
        )


def line_pixel_width(segments):

    total = 0

    for text, _, bold in segments:

        total += pixel_width(
            text,
            bold
        )

    return total


def strip_trailing_spaces(segments):

    result = list(segments)

    while result:

        text, color, bold = (
            result[-1]
        )

        stripped = text.rstrip()

        if stripped:

            result[-1] = (
                stripped,
                color,
                bold
            )

            break

        result.pop()

    return result


def split_long_token(
    token,
    color,
    bold,
    max_width
):

    chunks = []

    current = ""

    for char in token:

        proposed = (
            current + char
        )

        if (
            current
            and pixel_width(
                proposed,
                bold
            ) > max_width
        ):

            chunks.append(
                (
                    current,
                    color,
                    bold
                )
            )

            current = char

        else:

            current = proposed

    if current:

        chunks.append(
            (
                current,
                color,
                bold
            )
        )

    return chunks


def wrap_segments(
    segments,
    max_width
):
    """
    Wrap styled text based on the actual rendered
    pixel width.

    Every returned visual line is guaranteed to be
    <= max_width.
    """

    lines = []

    current = []

    # -----------------------------------------------------
    # TOKENIZE ALL SEGMENTS
    # -----------------------------------------------------

    tokens = []

    for text, color, bold in segments:

        parts = re.findall(
            r"\s+|\S+",
            text
        )

        for part in parts:

            tokens.append(
                (
                    part,
                    color,
                    bold
                )
            )

    # -----------------------------------------------------
    # WRAP
    # -----------------------------------------------------

    for token, color, bold in tokens:

        # ---------------------------------------------
        # Ignore whitespace at beginning of new line
        # ---------------------------------------------

        if (
            not current
            and token.isspace()
        ):
            continue

        token_width = pixel_width(
            token,
            bold
        )

        current_width = (
            line_pixel_width(
                current
            )
        )

        # ---------------------------------------------
        # Token fits
        # ---------------------------------------------

        if (
            current_width
            + token_width
            <= max_width
        ):

            merge_piece(
                current,
                token,
                color,
                bold
            )

            continue

        # ---------------------------------------------
        # Whitespace overflows:
        # just start new line
        # ---------------------------------------------

        if token.isspace():

            current = (
                strip_trailing_spaces(
                    current
                )
            )

            if current:

                lines.append(
                    current
                )

            current = []

            continue

        # ---------------------------------------------
        # Current line is full:
        # flush it
        # ---------------------------------------------

        if current:

            current = (
                strip_trailing_spaces(
                    current
                )
            )

            if current:

                lines.append(
                    current
                )

            current = []

        # ---------------------------------------------
        # Single token itself is wider than pane.
        # Split it character-by-character.
        #
        # Useful for long URLs.
        # ---------------------------------------------

        if (
            pixel_width(
                token,
                bold
            )
            > max_width
        ):

            chunks = split_long_token(
                token,
                color,
                bold,
                max_width
            )

            for index, chunk in enumerate(
                chunks
            ):

                if (
                    index
                    < len(chunks) - 1
                ):

                    lines.append(
                        [chunk]
                    )

                else:

                    current = [
                        chunk
                    ]

        else:

            current = [
                (
                    token,
                    color,
                    bold
                )
            ]

    # -----------------------------------------------------
    # FINAL LINE
    # -----------------------------------------------------

    current = (
        strip_trailing_spaces(
            current
        )
    )

    if current:

        lines.append(
            current
        )

    # -----------------------------------------------------
    # SAFETY CHECK
    # -----------------------------------------------------

    for line in lines:

        width = line_pixel_width(
            line
        )

        if width > max_width + 1:

            raise RuntimeError(
                "Wrapped line still exceeds pane: "
                f"{width:.1f}px > "
                f"{max_width:.1f}px"
            )

    return lines


# =========================================================
# BUILD LOGICAL TERMINAL BLOCKS
# =========================================================

blocks = []


def add_block(
    segments,
    cps,
    pause_after=TERM_LINE_PAUSE,
    gap_after=0
):

    blocks.append(
        {
            "segments": segments,
            "cps": cps,
            "pause_after": pause_after,
            "gap_after": gap_after,
        }
    )


# ---------------------------------------------------------
# WELCOME
# ---------------------------------------------------------

add_block(
    output(
        "Welcome to Rahym's GitHub",
        GREEN,
        True
    ),
    WELCOME_CPS,
    0.30,
    TERM_SECTION_GAP
)

# ---------------------------------------------------------
# WHOAMI
# ---------------------------------------------------------

add_block(
    command(
        "whoami"
    ),
    TERM_COMMAND_CPS
)

add_block(
    output(
        PROFILE["name"],
        GREEN,
        True
    ),
    TERM_OUTPUT_CPS,
    0.05
)

add_block(
    output(
        PROFILE["title"],
        BLUE
    ),
    TERM_OUTPUT_CPS,
    TERM_SECTION_PAUSE,
    TERM_SECTION_GAP
)

# ---------------------------------------------------------
# ABOUT
# ---------------------------------------------------------

add_block(
    command(
        "cat about.txt"
    ),
    TERM_COMMAND_CPS
)

add_block(
    output(
        PROFILE["about"]
    ),
    TERM_OUTPUT_CPS,
    TERM_SECTION_PAUSE,
    TERM_SECTION_GAP
)

# ---------------------------------------------------------
# STACK
# ---------------------------------------------------------

add_block(
    command(
        "./stack --list"
    ),
    TERM_COMMAND_CPS
)

add_block(
    prefixed(
        "[+] languages",
        PROFILE["languages"]
    ),
    TERM_OUTPUT_CPS,
    0.05
)

add_block(
    prefixed(
        "[+] web",
        PROFILE["web"]
    ),
    TERM_OUTPUT_CPS,
    0.05
)

add_block(
    prefixed(
        "[+] ai/data",
        PROFILE["ai_data"]
    ),
    TERM_OUTPUT_CPS,
    0.05
)

add_block(
    prefixed(
        "[+] tools",
        PROFILE["tools"]
    ),
    TERM_OUTPUT_CPS,
    TERM_SECTION_PAUSE,
    TERM_SECTION_GAP
)

# ---------------------------------------------------------
# CONTACT
# ---------------------------------------------------------

add_block(
    command(
        "./contact --show"
    ),
    TERM_COMMAND_CPS
)

add_block(
    prefixed(
        "mail",
        PROFILE["email"],
        prefix_color=TEXT,
        prefix_bold=False
    ),
    TERM_OUTPUT_CPS,
    0.05
)

add_block(
    prefixed(
        "linkedin",
        PROFILE["linkedin"],
        prefix_color=TEXT,
        prefix_bold=False
    ),
    TERM_OUTPUT_CPS,
    TERM_SECTION_PAUSE,
    TERM_SECTION_GAP
)

# ---------------------------------------------------------
# FINAL PROMPT
# ---------------------------------------------------------

add_block(
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
    0,
    0
)

# =========================================================
# CONVERT BLOCKS INTO WRAPPED VISUAL LINES
# =========================================================

visual_lines = []

current_y = TERM_START_Y

for block in blocks:

    wrapped = wrap_segments(
        block["segments"],
        TERM_MAX_WIDTH
    )

    for index, segments in enumerate(
        wrapped
    ):

        is_last = (
            index
            == len(wrapped) - 1
        )

        visual_lines.append(
            {
                "y": current_y,
                "segments": segments,
                "cps": block["cps"],
                "pause_after": (
                    block["pause_after"]
                    if is_last
                    else 0.025
                ),
            }
        )

        current_y += (
            TERM_LINE_STEP
        )

    current_y += (
        block["gap_after"]
    )

# =========================================================
# VERTICAL SAFETY CHECK
# =========================================================

if visual_lines:

    last_y = visual_lines[-1]["y"]

    if (
        last_y
        + TERM_LINE_STEP
        > RIGHT_PANE[3] - 8
    ):

        raise RuntimeError(
            "Terminal content is too tall. "
            f"Last line y={last_y}. "
            "Increase HEIGHT or reduce spacing."
        )

# =========================================================
# ASCII TIMING
# =========================================================

ascii_end = max(

    ASCII_START
    + index
    * ASCII_LINE_STAGGER
    + (
        len(line)
        / ASCII_CPS
        if line
        else 0
    )

    for index, line
    in enumerate(ascii_lines)
)

SHELL_START = max(
    2.2,
    ascii_end - 0.8
)

# =========================================================
# TERMINAL TIMELINE
# =========================================================

timeline = []

current_time = SHELL_START

for line in visual_lines:

    total_chars = sum(
        len(text)
        for text, _, _
        in line["segments"]
    )

    end_time = (
        current_time
        + total_chars
        / line["cps"]
    )

    timeline.append(
        {
            "y": line["y"],
            "segments": line["segments"],
            "cps": line["cps"],
            "chars": total_chars,
            "start": current_time,
            "end": end_time,
        }
    )

    current_time = (
        end_time
        + line["pause_after"]
    )

ANIMATION_END = (
    timeline[-1]["end"]
)

TOTAL_TIME = (
    ANIMATION_END
    + FINAL_HOLD
)

# =========================================================
# DRAW STYLED TEXT
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

    for text, color, bold in segments:

        font = get_font(
            bold
        )

        take = min(
            len(text),
            max(
                0,
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

        current_x += (
            draw.textlength(
                partial,
                font=font
            )
        )

        remaining -= take

        if take < len(text):
            break

    return current_x

# =========================================================
# RENDER FRAME
# =========================================================

def render_frame(
    time_seconds
):

    image = BASE_IMAGE.copy()

    draw = ImageDraw.Draw(
        image
    )

    # -----------------------------------------------------
    # ASCII ART
    # -----------------------------------------------------

    for index, line in enumerate(
        ascii_lines
    ):

        line_start = (
            ASCII_START
            + index
            * ASCII_LINE_STAGGER
        )

        if (
            time_seconds
            < line_start
        ):
            continue

        elapsed = (
            time_seconds
            - line_start
        )

        visible = (
            int(
                elapsed
                * ASCII_CPS
            )
            + 1
        )

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

    # -----------------------------------------------------
    # TERMINAL
    # -----------------------------------------------------

    active_cursor = None

    for line in timeline:

        if (
            time_seconds
            < line["start"]
        ):
            continue

        elapsed = (
            time_seconds
            - line["start"]
        )

        visible = (
            int(
                elapsed
                * line["cps"]
            )
            + 1
        )

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

    # -----------------------------------------------------
    # ACTIVE CURSOR
    # -----------------------------------------------------

    if active_cursor:

        cursor_x, cursor_y = (
            active_cursor
        )

        draw.rectangle(
            (
                cursor_x + 1,
                cursor_y + 4,
                cursor_x + 10,
                cursor_y + 24,
            ),
            fill=GREEN
        )

    # -----------------------------------------------------
    # FINAL BLINKING CURSOR
    # -----------------------------------------------------

    elif (
        time_seconds
        >= ANIMATION_END
    ):

        final_line = timeline[-1]

        cursor_x = draw_segments(
            draw,
            RIGHT_X,
            final_line["y"],
            final_line["segments"],
            final_line["chars"]
        )

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
                    final_line["y"] + 4,
                    cursor_x + 10,
                    final_line["y"] + 24,
                ),
                fill=GREEN
            )

    return image

# =========================================================
# PALETTE
# =========================================================

palette_source = (
    render_frame(
        ANIMATION_END
    )
    .quantize(
        colors=64,
        method=Image.Quantize.MEDIANCUT
    )
)

# =========================================================
# GENERATE GIF
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
    f"Terminal max width: "
    f"{TERM_MAX_WIDTH}px"
)
print(
    f"Visual terminal lines: "
    f"{len(visual_lines)}"
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

    frame = frame.quantize(
        palette=palette_source,
        dither=Image.Dither.NONE
    )

    frames.append(
        frame
    )

    if (
        frame_number
        % 50
        == 0
    ):

        print(
            f"{frame_number}"
            f"/{frame_count}"
        )

# =========================================================
# SAVE
# =========================================================

OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)

frames[0].save(
    OUTPUT_FILE,
    save_all=True,
    append_images=frames[1:],
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
