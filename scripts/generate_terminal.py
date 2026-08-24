from pathlib import Path
from html import escape

ROOT = Path(__file__).resolve().parents[1]

ASCII_FILE = ROOT / "assets" / "ascii-art.txt"
OUTPUT_FILE = ROOT / "assets" / "terminal.svg"

# =========================================================
# CANVAS / LAYOUT
# =========================================================

WIDTH = 1600
HEIGHT = 760

# Left pane (ASCII)
ART_X = 40
ART_Y = 102
ART_FONT = 7.6
ART_LINE = 10.8
ART_CHAR_W = 4.7

# Right pane (terminal text)
RIGHT_X = 770
RIGHT_Y = 118
RIGHT_LINE = 42
TERM_CHAR_W = 10.9

DIVIDER_X = 736

# =========================================================
# TIMING
# Tweak these if you want faster/slower typing
# =========================================================

BOOT_DELAY = 0.25

# ASCII typing speed
ASCII_CHAR_DELAY = 0.0014
ASCII_LINE_PAUSE = 0.010

# Terminal typing speed
TERM_CHAR_DELAY = 0.014
TERM_LINE_PAUSE = 0.18

# Start right-side shell after this many seconds.
# You can lower this if you want the shell to start earlier.
MIN_SHELL_START = 2.30

# =========================================================
# EDIT YOUR PROFILE INFO HERE
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
# READ ASCII ART
# =========================================================

ascii_lines = ASCII_FILE.read_text(encoding="utf-8").splitlines()

if not ascii_lines:
    ascii_lines = ["(ascii-art.txt is empty)"]

# Replace tabs if they exist
ascii_lines = [line.replace("\t", "    ") for line in ascii_lines]

# =========================================================
# HELPERS
# =========================================================

def svg_char(ch: str) -> str:
    """Render spaces safely in SVG."""
    if ch == " ":
        return "&#160;"
    return escape(ch)


def typed_plain_line(x, y, text, css_class, start_time, char_delay, char_width):
    """
    Render a single line character-by-character.
    Returns: (svg_string, end_time)
    """
    pieces = [f'<g class="{css_class}">']
    t = start_time

    for i, ch in enumerate(text):
        char_x = x + i * char_width
        pieces.append(
            f'''
            <text x="{char_x:.2f}" y="{y:.2f}" visibility="hidden">
                {svg_char(ch)}
                <set attributeName="visibility"
                     to="visible"
                     begin="{t:.3f}s"
                     fill="freeze" />
            </text>
            '''
        )
        t += char_delay

    pieces.append("</g>")
    return "\n".join(pieces), t


def typed_segment_line(x, y, segments, start_time, char_delay, char_width):
    """
    Render a line made of differently styled segments,
    typed character-by-character from left to right.

    segments: [("text", "css_class"), ...]
    Returns: (svg_string, end_time)
    """
    pieces = []
    t = start_time
    cursor_index = 0

    for segment_text, css_class in segments:
        pieces.append(f'<g class="{css_class}">')

        for ch in segment_text:
            char_x = x + cursor_index * char_width
            pieces.append(
                f'''
                <text x="{char_x:.2f}" y="{y:.2f}" visibility="hidden">
                    {svg_char(ch)}
                    <set attributeName="visibility"
                         to="visible"
                         begin="{t:.3f}s"
                         fill="freeze" />
                </text>
                '''
            )
            cursor_index += 1
            t += char_delay

        pieces.append("</g>")

    return "\n".join(pieces), t


def static_text(x, y, text, css_class="label", anchor="start"):
    anchor_attr = f' text-anchor="{anchor}"' if anchor != "start" else ""
    return (
        f'<text x="{x}" y="{y}" class="{css_class}"{anchor_attr}>'
        f'{escape(text)}'
        f'</text>'
    )


# =========================================================
# BUILD SVG
# =========================================================

svg = [f"""
<svg
    xmlns="http://www.w3.org/2000/svg"
    width="{WIDTH}"
    height="{HEIGHT}"
    viewBox="0 0 {WIDTH} {HEIGHT}"
    role="img"
    aria-labelledby="title desc"
>
    <title id="title">Rahym Faisal Khan — Terminal Profile</title>
    <desc id="desc">
        Hacker-themed terminal GitHub profile with ASCII art on the left
        and a typed shell session on the right.
    </desc>

    <defs>
        <pattern id="scanlines" width="4" height="4" patternUnits="userSpaceOnUse">
            <rect width="4" height="2" fill="rgba(255,255,255,0.02)" />
            <rect y="2" width="4" height="2" fill="rgba(0,0,0,0.00)" />
        </pattern>

        <filter id="softGlow" x="-20%" y="-20%" width="140%" height="140%">
            <feGaussianBlur stdDeviation="1.2" result="blur"/>
            <feMerge>
                <feMergeNode in="blur"/>
                <feMergeNode in="SourceGraphic"/>
            </feMerge>
        </filter>
    </defs>

    <style>
        :root {{
            color-scheme: dark;
        }}

        .bg {{
            fill: #000000;
        }}

        .panel {{
            fill: #020402;
            stroke: #1f8f47;
            stroke-width: 2;
        }}

        .topbar {{
            fill: #071107;
        }}

        .pane-left {{
            fill: #000000;
        }}

        .pane-right {{
            fill: #010301;
        }}

        .divider {{
            stroke: #10351b;
            stroke-width: 1;
        }}

        .scan {{
            fill: url(#scanlines);
            opacity: 0.10;
            pointer-events: none;
        }}

        .ascii {{
            fill: #2fd65b;
            font-family:
                "SFMono-Regular",
                Consolas,
                "Liberation Mono",
                Menlo,
                monospace;
            font-size: {ART_FONT}px;
            filter: url(#softGlow);
        }}

        .label {{
            fill: #39d353;
            font:
                700 16px
                "SFMono-Regular",
                Consolas,
                "Liberation Mono",
                Menlo,
                monospace;
        }}

        .prompt {{
            fill: #39d353;
            font:
                700 20px
                "SFMono-Regular",
                Consolas,
                "Liberation Mono",
                Menlo,
                monospace;
            filter: url(#softGlow);
        }}

        .path {{
            fill: #8b949e;
            font:
                700 20px
                "SFMono-Regular",
                Consolas,
                "Liberation Mono",
                Menlo,
                monospace;
        }}

        .command {{
            fill: #f0f6fc;
            font:
                20px
                "SFMono-Regular",
                Consolas,
                "Liberation Mono",
                Menlo,
                monospace;
        }}

        .output {{
            fill: #d2d7de;
            font:
                18px
                "SFMono-Regular",
                Consolas,
                "Liberation Mono",
                Menlo,
                monospace;
        }}

        .accent {{
            fill: #39d353;
            font:
                700 18px
                "SFMono-Regular",
                Consolas,
                "Liberation Mono",
                Menlo,
                monospace;
            filter: url(#softGlow);
        }}

        .cyan {{
            fill: #79c0ff;
            font:
                18px
                "SFMono-Regular",
                Consolas,
                "Liberation Mono",
                Menlo,
                monospace;
        }}

        .muted {{
            fill: #6e7681;
            font:
                18px
                "SFMono-Regular",
                Consolas,
                "Liberation Mono",
                Menlo,
                monospace;
        }}

        .cursor {{
            fill: #39d353;
            font:
                700 20px
                "SFMono-Regular",
                Consolas,
                "Liberation Mono",
                Menlo,
                monospace;
            filter: url(#softGlow);
        }}
    </style>

    <!-- OUTER BACKGROUND -->
    <rect class="bg" width="100%" height="100%" rx="18" />

    <!-- TERMINAL WINDOW -->
    <rect class="panel" x="10" y="10" width="1580" height="740" rx="18" />

    <!-- TITLE BAR -->
    <rect class="topbar" x="11" y="11" width="1578" height="44" rx="16" />
    <rect class="topbar" x="11" y="38" width="1578" height="17" />

    <!-- WINDOW BUTTONS -->
    <circle cx="34" cy="33" r="7" fill="#ff5f56" />
    <circle cx="57" cy="33" r="7" fill="#ffbd2e" />
    <circle cx="80" cy="33" r="7" fill="#27c93f" />

    <!-- WINDOW TITLE -->
    {static_text(WIDTH / 2, 38, "rahym@github: ~/profile", "muted", "middle")}

    <!-- INNER PANES -->
    <rect class="pane-left"  x="24"  y="56" width="696" height="680" rx="10" />
    <rect class="pane-right" x="748" y="56" width="816" height="680" rx="10" />

    <!-- DIVIDER -->
    <line x1="{DIVIDER_X}" y1="55" x2="{DIVIDER_X}" y2="736" class="divider" />

    <!-- PANE LABELS -->
    {static_text(40, 76, "[ ./ascii-art.txt ]", "label")}
    {static_text(770, 76, "[ interactive shell // guest session ]", "label")}
"""]

# =========================================================
# TYPE THE ASCII ART
# =========================================================

ascii_time = BOOT_DELAY

for index, line in enumerate(ascii_lines):
    y = ART_Y + index * ART_LINE
    line_svg, ascii_time = typed_plain_line(
        ART_X,
        y,
        line,
        "ascii",
        ascii_time,
        ASCII_CHAR_DELAY,
        ART_CHAR_W,
    )
    svg.append(line_svg)
    ascii_time += ASCII_LINE_PAUSE

# =========================================================
# TYPE THE RIGHT-SIDE TERMINAL
# =========================================================

t = max(MIN_SHELL_START, ascii_time + 0.18)
y = RIGHT_Y

# 1) whoami
line_svg, t = typed_segment_line(
    RIGHT_X, y,
    [
        ("rahym@github", "prompt"),
        (":", "muted"),
        ("~", "path"),
        ("$ ", "muted"),
        ("whoami", "command"),
    ],
    t,
    TERM_CHAR_DELAY,
    TERM_CHAR_W,
)
svg.append(line_svg)
t += TERM_LINE_PAUSE
y += RIGHT_LINE

line_svg, t = typed_plain_line(
    RIGHT_X, y,
    PROFILE["name"],
    "accent",
    t,
    TERM_CHAR_DELAY,
    TERM_CHAR_W,
)
svg.append(line_svg)
t += TERM_LINE_PAUSE * 0.75
y += 28

line_svg, t = typed_plain_line(
    RIGHT_X, y,
    PROFILE["title"],
    "cyan",
    t,
    TERM_CHAR_DELAY,
    TERM_CHAR_W,
)
svg.append(line_svg)
t += TERM_LINE_PAUSE * 1.2
y += 50

# 2) about
line_svg, t = typed_segment_line(
    RIGHT_X, y,
    [
        ("rahym@github", "prompt"),
        (":", "muted"),
        ("~", "path"),
        ("$ ", "muted"),
        ("cat about.txt", "command"),
    ],
    t,
    TERM_CHAR_DELAY,
    TERM_CHAR_W,
)
svg.append(line_svg)
t += TERM_LINE_PAUSE
y += RIGHT_LINE

line_svg, t = typed_plain_line(
    RIGHT_X, y,
    PROFILE["about"],
    "output",
    t,
    TERM_CHAR_DELAY,
    TERM_CHAR_W,
)
svg.append(line_svg)
t += TERM_LINE_PAUSE * 1.2
y += 52

# 3) stack
line_svg, t = typed_segment_line(
    RIGHT_X, y,
    [
        ("rahym@github", "prompt"),
        (":", "muted"),
        ("~", "path"),
        ("$ ", "muted"),
        ("./stack --list", "command"),
    ],
    t,
    TERM_CHAR_DELAY,
    TERM_CHAR_W,
)
svg.append(line_svg)
t += TERM_LINE_PAUSE
y += RIGHT_LINE

stack_lines = [
    (f"[+] languages  {PROFILE['languages']}", [("[+] languages", "accent"), ("  " + PROFILE["languages"], "output")]),
    (f"[+] web        {PROFILE['web']}", [("[+] web", "accent"), ("        " + PROFILE["web"], "output")]),
    (f"[+] ai/data    {PROFILE['ai_data']}", [("[+] ai/data", "accent"), ("    " + PROFILE["ai_data"], "output")]),
    (f"[+] tools      {PROFILE['tools']}", [("[+] tools", "accent"), ("      " + PROFILE["tools"], "output")]),
]

for _, segments in stack_lines:
    line_svg, t = typed_segment_line(
        RIGHT_X, y,
        segments,
        t,
        TERM_CHAR_DELAY,
        TERM_CHAR_W,
    )
    svg.append(line_svg)
    t += TERM_LINE_PAUSE * 0.65
    y += 32

y += 14
t += 0.08

# 4) contact
line_svg, t = typed_segment_line(
    RIGHT_X, y,
    [
        ("rahym@github", "prompt"),
        (":", "muted"),
        ("~", "path"),
        ("$ ", "muted"),
        ("./contact --show", "command"),
    ],
    t,
    TERM_CHAR_DELAY,
    TERM_CHAR_W,
)
svg.append(line_svg)
t += TERM_LINE_PAUSE
y += RIGHT_LINE

line_svg, t = typed_plain_line(
    RIGHT_X, y,
    f"mail     {PROFILE['email']}",
    "output",
    t,
    TERM_CHAR_DELAY,
    TERM_CHAR_W,
)
svg.append(line_svg)
t += TERM_LINE_PAUSE * 0.70
y += 32

line_svg, t = typed_plain_line(
    RIGHT_X, y,
    f"linkedin {PROFILE['linkedin']}",
    "output",
    t,
    TERM_CHAR_DELAY,
    TERM_CHAR_W,
)
svg.append(line_svg)
t += TERM_LINE_PAUSE
y += 52

# 5) final prompt
line_svg, t = typed_segment_line(
    RIGHT_X, y,
    [
        ("rahym@github", "prompt"),
        (":", "muted"),
        ("~", "path"),
        ("$ ", "muted"),
    ],
    t,
    TERM_CHAR_DELAY,
    TERM_CHAR_W,
)
svg.append(line_svg)

cursor_x = RIGHT_X + len("rahym@github:~$ ") * TERM_CHAR_W

svg.append(
    f"""
    <text x="{cursor_x:.2f}" y="{y:.2f}" class="cursor" visibility="hidden">
        █
        <set attributeName="visibility"
             to="visible"
             begin="{t:.3f}s"
             fill="freeze" />
        <animate attributeName="opacity"
                 values="1;1;0;0;1"
                 keyTimes="0;0.48;0.49;1;1"
                 dur="1s"
                 repeatCount="indefinite"
                 begin="{t:.3f}s" />
    </text>
    """
)

# =========================================================
# SCANLINE OVERLAY
# =========================================================

svg.append(
    """
    <rect class="scan" x="24" y="56" width="1540" height="680" rx="10" />
    """
)

svg.append("</svg>")

# =========================================================
# WRITE FILE
# =========================================================

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
OUTPUT_FILE.write_text("\n".join(svg), encoding="utf-8")

print(f"Generated: {OUTPUT_FILE}")
