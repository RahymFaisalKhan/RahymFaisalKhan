from pathlib import Path
from html import escape

ROOT = Path(__file__).resolve().parents[1]

ASCII_FILE = ROOT / "assets" / "ascii-art.txt"
OUTPUT_FILE = ROOT / "assets" / "terminal.svg"

WIDTH = 1400
HEIGHT = 620


# =========================================================
# EDIT YOUR PROFILE HERE
# =========================================================

PROFILE = {
    "name": "Rahym Faisal Khan",

    "title": "Software Development | Data Science | AI/ML",

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

    "email": "rahymfaisal123@gmail.com",

    "linkedin": (
        "linkedin.com/in/rahym-faisal-633a6b2b4"
    ),
}


# =========================================================
# ASCII ART
# =========================================================

ascii_lines = ASCII_FILE.read_text(
    encoding="utf-8"
).splitlines()


# =========================================================
# LAYOUT
# =========================================================

ART_X = 34
ART_Y = 82

ART_FONT = 6.8
ART_LINE = 9.7

RIGHT_X = 650
RIGHT_Y = 96
RIGHT_LINE = 34


def normal_text(
    x,
    y,
    text,
    css_class="output",
    delay=None
):
    animation = ""

    if delay is not None:
        animation = (
            f' style="animation-delay:{delay:.2f}s"'
        )

    return (
        f'<text x="{x}" y="{y}" '
        f'class="{css_class} reveal"{animation}>'
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
# SVG HEADER
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

<title id="title">
    Rahym Faisal Khan — Terminal Profile
</title>

<desc id="desc">
    Terminal themed GitHub profile with ASCII art
    and developer information.
</desc>


<style>

    :root {{
        color-scheme: dark;
    }}

    .bg {{
        fill: #030703;
    }}

    .panel {{
        fill: #07110b;
        stroke: #1d5f3a;
        stroke-width: 2;
    }}

    .topbar {{
        fill: #0a1710;
    }}

    .divider {{
        stroke: #173c29;
        stroke-width: 1;
    }}


    /* ===================================
       ASCII
       =================================== */

    .ascii {{
        fill: #3fb950;

        font-family:
            "SFMono-Regular",
            Consolas,
            "Liberation Mono",
            Menlo,
            monospace;

        font-size: {ART_FONT}px;

        white-space: pre;
    }}


    /* ===================================
       TERMINAL TEXT
       =================================== */

    .label {{
        fill: #3fb950;

        font:
            700 14px
            "SFMono-Regular",
            Consolas,
            "Liberation Mono",
            Menlo,
            monospace;
    }}

    .prompt {{
        fill: #3fb950;

        font:
            700 17px
            "SFMono-Regular",
            Consolas,
            "Liberation Mono",
            Menlo,
            monospace;
    }}

    .path {{
        fill: #58a6ff;

        font:
            700 17px
            "SFMono-Regular",
            Consolas,
            "Liberation Mono",
            Menlo,
            monospace;
    }}

    .command {{
        fill: #f0f6fc;

        font:
            17px
            "SFMono-Regular",
            Consolas,
            "Liberation Mono",
            Menlo,
            monospace;
    }}

    .output {{
        fill: #c9d1d9;

        font:
            16px
            "SFMono-Regular",
            Consolas,
            "Liberation Mono",
            Menlo,
            monospace;
    }}

    .accent {{
        fill: #39d353;

        font:
            700 16px
            "SFMono-Regular",
            Consolas,
            "Liberation Mono",
            Menlo,
            monospace;
    }}

    .cyan {{
        fill: #79c0ff;

        font:
            16px
            "SFMono-Regular",
            Consolas,
            "Liberation Mono",
            Menlo,
            monospace;
    }}

    .muted {{
        fill: #6e7681;

        font:
            16px
            "SFMono-Regular",
            Consolas,
            "Liberation Mono",
            Menlo,
            monospace;
    }}


    /* ===================================
       ANIMATION
       =================================== */

    .reveal {{
        opacity: 0;

        animation:
            reveal .18s linear forwards;
    }}

    .cursor {{
        fill: #3fb950;

        animation:
            blink 1s steps(1) infinite;
    }}

    @keyframes reveal {{
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


<!-- BACKGROUND -->

<rect
    class="bg"
    width="100%"
    height="100%"
    rx="18"
/>


<!-- TERMINAL WINDOW -->

<rect
    class="panel"
    x="10"
    y="10"
    width="1380"
    height="600"
    rx="16"
/>


<!-- TITLE BAR -->

<rect
    class="topbar"
    x="11"
    y="11"
    width="1378"
    height="44"
    rx="15"
/>

<rect
    class="topbar"
    x="11"
    y="38"
    width="1378"
    height="17"
/>


<!-- WINDOW BUTTONS -->

<circle
    cx="34"
    cy="33"
    r="7"
    fill="#ff5f56"
/>

<circle
    cx="57"
    cy="33"
    r="7"
    fill="#ffbd2e"
/>

<circle
    cx="80"
    cy="33"
    r="7"
    fill="#27c93f"
/>


<!-- WINDOW TITLE -->

<text
    x="700"
    y="38"
    text-anchor="middle"
    class="muted"
>
    rahym@github: ~/profile
</text>


<!-- DIVIDER -->

<line
    x1="620"
    y1="55"
    x2="620"
    y2="595"
    class="divider"
/>


<!-- PANEL HEADERS -->

<text
    x="34"
    y="74"
    class="label"
>
    [ ./ascii-art.txt ]
</text>

<text
    x="650"
    y="74"
    class="label"
>
    [ interactive shell // guest session ]
</text>

"""]


# =========================================================
# ASCII ART
# =========================================================

for index, line in enumerate(ascii_lines):

    y = ART_Y + index * ART_LINE

    delay = 0.02 + index * 0.012

    svg.append(
        f"""
        <text
            x="{ART_X}"
            y="{y:.1f}"
            class="ascii reveal"
            style="animation-delay:{delay:.3f}s"
        >{escape(line)}</text>
        """
    )


# =========================================================
# TERMINAL CONTENT
# =========================================================

y = RIGHT_Y
delay = 0.70


# --------------------------
# WHOAMI
# --------------------------

svg.append(
    command_line(
        y,
        "whoami",
        delay
    )
)

y += RIGHT_LINE
delay += 0.16


svg.append(
    normal_text(
        RIGHT_X,
        y,
        PROFILE["name"],
        "accent",
        delay
    )
)

y += 24
delay += 0.10


svg.append(
    normal_text(
        RIGHT_X,
        y,
        PROFILE["title"],
        "cyan",
        delay
    )
)

y += 42
delay += 0.14


# --------------------------
# ABOUT
# --------------------------

svg.append(
    command_line(
        y,
        "cat about.txt",
        delay
    )
)

y += RIGHT_LINE
delay += 0.16


svg.append(
    normal_text(
        RIGHT_X,
        y,
        PROFILE["about"],
        "output",
        delay
    )
)

y += 44
delay += 0.14


# --------------------------
# STACK
# --------------------------

svg.append(
    command_line(
        y,
        "./stack --list",
        delay
    )
)

y += RIGHT_LINE
delay += 0.16


stack = [

    (
        "languages",
        PROFILE["languages"]
    ),

    (
        "web      ",
        PROFILE["web"]
    ),

    (
        "ai/data  ",
        PROFILE["ai_data"]
    ),

    (
        "tools    ",
        PROFILE["tools"]
    ),
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

            <tspan class="accent">
                [+] {escape(label)}
            </tspan>

            <tspan class="output">
                  {escape(value)}
            </tspan>

        </text>
        """
    )

    y += 27
    delay += 0.10


# --------------------------
# CONTACT
# --------------------------

y += 9

svg.append(
    command_line(
        y,
        "./contact --show",
        delay
    )
)

y += RIGHT_LINE
delay += 0.16


svg.append(
    normal_text(
        RIGHT_X,
        y,
        f'mail     {PROFILE["email"]}',
        "output",
        delay
    )
)

y += 27
delay += 0.10


svg.append(
    normal_text(
        RIGHT_X,
        y,
        f'linkedin {PROFILE["linkedin"]}',
        "output",
        delay
    )
)

y += 40
delay += 0.10


# =========================================================
# FINAL BLINKING PROMPT
# =========================================================

svg.append(
    f"""
    <text
        x="{RIGHT_X}"
        y="{y}"
        class="reveal"
        style="animation-delay:{delay:.2f}s"
    >

        <tspan class="prompt">
            rahym@github
        </tspan>

        <tspan class="muted">:</tspan>

        <tspan class="path">
            ~
        </tspan>

        <tspan class="muted">
            $
        </tspan>

        <tspan class="cursor">
            █
        </tspan>

    </text>
    """
)


svg.append("</svg>")


# =========================================================
# WRITE FILE
# =========================================================

OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)

OUTPUT_FILE.write_text(
    "\n".join(svg),
    encoding="utf-8"
)

print(
    f"Generated: {OUTPUT_FILE}"
)
