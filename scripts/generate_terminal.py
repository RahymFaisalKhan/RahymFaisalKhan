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

ART_X = 42
ART_Y = 100
ART_FONT = 7.8
ART_LINE = 11.2

RIGHT_X = 770
RIGHT_Y = 118
RIGHT_LINE = 40

DIVIDER_X = 736

# =========================================================
# EDIT YOUR PROFILE INFO HERE
# =========================================================

PROFILE = {
    "name": "Rahym Faisal Khan",
    "title": "Software Development | Data Science | AI/ML",
    "about": (
        "Building software, exploring data, and learning intelligent systems."
    ),
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

# =========================================================
# HELPERS
# =========================================================

def normal_text(x, y, text, css_class="output", delay=None, anchor="start"):
    animation = f' style="animation-delay:{delay:.2f}s"' if delay is not None else ""
    anchor_attr = f' text-anchor="{anchor}"' if anchor != "start" else ""
    return (
        f'<text x="{x}" y="{y}" class="{css_class} reveal"{anchor_attr}{animation}>'
        f'{escape(text)}'
        f'</text>'
    )


def command_line(y, command, delay):
    return f"""
    <text
        x="{RIGHT_X}"
        y="{y}"
        class="reveal"
        style="animation-delay:{delay:.2f}s"
    >
        <tspan class="prompt">rahym@github</tspan>
        <tspan class="muted">:</tspan>
        <tspan class="path">~</tspan>
        <tspan class="muted">$ </tspan>
        <tspan class="command">{escape(command)}</tspan>
    </text>
    """


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
        Terminal themed GitHub profile with ASCII art on the left and
        profile information rendered as a cinematic shell session on the right.
    </desc>

    <defs>
        <pattern id="scanlines" width="4" height="4" patternUnits="userSpaceOnUse">
            <rect width="4" height="2" fill="rgba(255,255,255,0.02)" />
            <rect y="2" width="4" height="2" fill="rgba(0,0,0,0.00)" />
        </pattern>
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
            white-space: pre;
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

        .reveal {{
            opacity: 0;
            animation: reveal 0.12s linear forwards;
        }}

        .cursor {{
            fill: #39d353;
            animation: blink 1s steps(1) infinite;
        }}

        @keyframes reveal {{
            from {{
                opacity: 0;
            }}
            to {{
                opacity: 1;
            }}
        }}

        @keyframes blink {{
            0%, 48% {{
                opacity: 1;
            }}
            49%, 100% {{
                opacity: 0;
            }}
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
    <text x="{WIDTH / 2}" y="38" text-anchor="middle" class="muted">
        rahym@github: ~/profile
    </text>

    <!-- INNER PANES -->
    <rect class="pane-left"  x="24"  y="56" width="696" height="680" rx="10" />
    <rect class="pane-right" x="748" y="56" width="816" height="680" rx="10" />

    <!-- DIVIDER -->
    <line x1="{DIVIDER_X}" y1="55" x2="{DIVIDER_X}" y2="736" class="divider" />

    <!-- PANE LABELS -->
    <text x="40" y="76" class="label">[ ./ascii-art.txt ]</text>
    <text x="770" y="76" class="label">[ interactive shell // guest session ]</text>
"""]

# =========================================================
# ASCII ART REVEAL (line by line, movie style)
# =========================================================

for index, line in enumerate(ascii_lines):
    y = ART_Y + index * ART_LINE
    delay = 0.10 + index * 0.055

    svg.append(
        f"""
        <text
            x="{ART_X}"
            y="{y:.1f}"
            class="ascii reveal"
            xml:space="preserve"
            style="animation-delay:{delay:.3f}s"
        >{escape(line)}</text>
        """
    )

# =========================================================
# RIGHT-SIDE SHELL CONTENT
# Starts after the art has begun to reveal
# =========================================================

y = RIGHT_Y
delay = 2.40

# WHOAMI
svg.append(command_line(y, "whoami", delay))
y += RIGHT_LINE
delay += 0.28

svg.append(normal_text(RIGHT_X, y, PROFILE["name"], "accent", delay))
y += 28
delay += 0.18

svg.append(normal_text(RIGHT_X, y, PROFILE["title"], "cyan", delay))
y += 50
delay += 0.28

# ABOUT
svg.append(command_line(y, "cat about.txt", delay))
y += RIGHT_LINE
delay += 0.28

svg.append(normal_text(RIGHT_X, y, PROFILE["about"], "output", delay))
y += 52
delay += 0.28

# STACK
svg.append(command_line(y, "./stack --list", delay))
y += RIGHT_LINE
delay += 0.28

stack = [
    ("languages", PROFILE["languages"]),
    ("web      ", PROFILE["web"]),
    ("ai/data  ", PROFILE["ai_data"]),
    ("tools    ", PROFILE["tools"]),
]

for label, value in stack:
    svg.append(
        f"""
        <text
            x="{RIGHT_X}"
            y="{y}"
            class="reveal"
            style="animation-delay:{delay:.2f}s"
        >
            <tspan class="accent">[+] {escape(label)}</tspan>
            <tspan class="output">  {escape(value)}</tspan>
        </text>
        """
    )
    y += 32
    delay += 0.18

# CONTACT
y += 14

svg.append(command_line(y, "./contact --show", delay))
y += RIGHT_LINE
delay += 0.28

svg.append(
    normal_text(
        RIGHT_X,
        y,
        f"mail     {PROFILE['email']}",
        "output",
        delay
    )
)
y += 32
delay += 0.18

svg.append(
    normal_text(
        RIGHT_X,
        y,
        f"linkedin {PROFILE['linkedin']}",
        "output",
        delay
    )
)
y += 52
delay += 0.20

# FINAL CURSOR
svg.append(
    f"""
    <text
        x="{RIGHT_X}"
        y="{y}"
        class="reveal"
        style="animation-delay:{delay:.2f}s"
    >
        <tspan class="prompt">rahym@github</tspan>
        <tspan class="muted">:</tspan>
        <tspan class="path">~</tspan>
        <tspan class="muted">$ </tspan>
        <tspan class="cursor">█</tspan>
    </text>
    """
)

# SCANLINE OVERLAY
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
