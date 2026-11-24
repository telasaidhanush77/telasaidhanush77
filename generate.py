"""Profile README SVGs v4 — sci-fi HUD (globe, glitch, iridescent frame). usage: gen3.py OUT_DIR PHOTO.jpg FONT_DIR
CSS-only animation; fonts + photo embedded; nothing external (GitHub renders via <img>)."""
import base64, math, pathlib, sys

OUT, PHOTO_P, FONTS = map(pathlib.Path, sys.argv[1:4])
(OUT / "projects").mkdir(parents=True, exist_ok=True)

BG, PANEL, PANEL2 = "#04060d", "#0a1122", "#0f1930"
BLUE, CYAN, RED, AMBER = "#247bff", "#3fd8ff", "#ff354f", "#ffb547"
INK, MUTED, LINE = "#eaf2ff", "#8796b4", "#1b2a4c"
b64 = lambda p: base64.b64encode(p.read_bytes()).decode()
PHOTO = "data:image/jpeg;base64," + b64(PHOTO_P)
FACES = {"or700": ("OR", 700), "or500": ("OR", 500), "rj600": ("RJ", 600), "jb400": ("JB", 400)}

def fontcss():
    return "".join(f"@font-face{{font-family:{f};font-weight:{w};src:url(data:font/woff2;base64,{b64(FONTS / (k + '.woff2'))}) format('woff2')}}"
                   for k, (f, w) in FACES.items())

BASE = (".d{font-family:OR,'Segoe UI',sans-serif;font-weight:700}.d5{font-family:OR,'Segoe UI',sans-serif;font-weight:500}"
        ".t{font-family:RJ,'Segoe UI',sans-serif;font-weight:600}.mono{font-family:JB,Consolas,monospace}"
        "@keyframes spin{to{transform:rotate(360deg)}}@keyframes spinr{to{transform:rotate(-360deg)}}"
        "@keyframes blink{50%{opacity:0}}.blink{animation:blink 1.1s steps(1) infinite}"
        "@keyframes flick{0%,100%{opacity:1}92%{opacity:1}93%{opacity:.35}94%{opacity:1}96%{opacity:.6}97%{opacity:1}}.flick{animation:flick 6s infinite}"
        "@keyframes dash{to{stroke-dashoffset:-400}}.trace{stroke-dasharray:36 364;animation:dash 3.2s linear infinite}"
        "@keyframes rise{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:none}}"
        # v4: iridescent frame, scan bar, wireframe globe, photo glitch, equalizer
        f"@keyframes ir1{{0%,100%{{stop-color:{CYAN}}}33%{{stop-color:#9b5cff}}66%{{stop-color:{RED}}}}}"
        f"@keyframes ir2{{0%,100%{{stop-color:#9b5cff}}33%{{stop-color:{RED}}}66%{{stop-color:{CYAN}}}}}"
        f"@keyframes ir3{{0%,100%{{stop-color:{RED}}}33%{{stop-color:{CYAN}}}66%{{stop-color:#9b5cff}}}}"
        ".ir1{animation:ir1 8s linear infinite}.ir2{animation:ir2 8s linear infinite}.ir3{animation:ir3 8s linear infinite}"
        "@keyframes sbar{from{transform:translateY(-120px)}to{transform:translateY(var(--sh))}}.sbar{animation:sbar 7s linear infinite}"
        "@keyframes lon{0%{transform:scaleX(1)}50%{transform:scaleX(-1)}100%{transform:scaleX(1)}}.lon{animation:lon 14s ease-in-out infinite}"
        "@keyframes gs{0%,86%,100%{transform:none;opacity:0}87%{transform:translateX(-9px);opacity:1}89%{transform:translateX(7px);opacity:1}91%{transform:translateX(-3px);opacity:1}92%{opacity:0}}"
        ".gs1{animation:gs 5s steps(1) infinite}.gs2{animation:gs 5s steps(1) infinite;animation-delay:-.3s}"
        "@keyframes eq{0%,100%{transform:scaleY(.25)}50%{transform:scaleY(1)}}.eq{animation:eq 1.2s ease-in-out infinite}"
        "@keyframes tick{to{transform:translateX(var(--tw))}}.tick{animation:tick 6s ease-in-out infinite alternate}"
        "@keyframes ind{from{transform:translateX(-70px)}to{transform:translateX(230px)}}.ind{animation:ind 2.2s cubic-bezier(.6,0,.4,1) infinite}"
        "@media (prefers-reduced-motion:reduce){*{animation:none!important}}")

def chamfer(x, y, w, h, c=16, **kw):
    pts = f"{x+c},{y} {x+w},{y} {x+w},{y+h-c} {x+w-c},{y+h} {x},{y+h} {x},{y+c}"
    attrs = " ".join(f'{k.replace("_", "-")}="{v}"' for k, v in kw.items())
    return f'<polygon points="{pts}" {attrs}/>'

def brackets(x, y, w, h, col, s=14):
    p = (f"M{x},{y+s}V{y}H{x+s} M{x+w-s},{y}H{x+w}V{y+s} M{x+w},{y+h-s}V{y+h}H{x+w-s} M{x+s},{y+h}H{x}V{y+h-s}")
    return f'<path d="{p}" fill="none" stroke="{col}" stroke-width="2"/>'

def frame(w, h, body, css="", title=None, tag=None, rule=True):
    head = ""
    if title:
        head = (f'<text class="mono" x="32" y="40" font-size="12" letter-spacing="3" fill="{CYAN}">{tag}</text>'
                f'<text class="d" x="32" y="70" font-size="24" letter-spacing="2" fill="{INK}">{title}</text>'
                f'<line x1="32" y1="84" x2="{w-32}" y2="84" stroke="{LINE}"/><line class="sweep" x1="32" y1="84" x2="152" y2="84" stroke="{CYAN}" stroke-width="2"/>')
        css += f"@keyframes sweep{{0%{{transform:translateX(0)}}100%{{transform:translateX({w-184}px)}}}}.sweep{{animation:sweep 5s ease-in-out infinite alternate}}"
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img">
<defs>
<linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{CYAN}"/><stop offset=".5" stop-color="{BLUE}"/><stop offset="1" stop-color="{RED}"/></linearGradient>
<linearGradient id="gi" x1="0" y1="0" x2="1" y2="1"><stop class="ir1" offset="0" stop-color="{CYAN}"/><stop class="ir2" offset=".5" stop-color="#9b5cff"/><stop class="ir3" offset="1" stop-color="{RED}"/></linearGradient>
<linearGradient id="gn" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#ffffff"/><stop offset=".6" stop-color="#bfeeff"/><stop offset="1" stop-color="{CYAN}"/></linearGradient>
<linearGradient id="sb" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{CYAN}" stop-opacity="0"/><stop offset=".92" stop-color="{CYAN}" stop-opacity=".07"/><stop offset="1" stop-color="{CYAN}" stop-opacity=".35"/></linearGradient>
<filter id="grain" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency=".85" numOctaves="2" stitchTiles="stitch"/><feColorMatrix values="0 0 0 0 .7  0 0 0 0 .85  0 0 0 0 1  0 0 0 .07 0"/></filter>
<linearGradient id="gh" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{CYAN}"/><stop offset="1" stop-color="{BLUE}"/></linearGradient>
<radialGradient id="gb"><stop offset="0" stop-color="{BLUE}" stop-opacity=".28"/><stop offset="1" stop-color="{BLUE}" stop-opacity="0"/></radialGradient>
<radialGradient id="gr"><stop offset="0" stop-color="{RED}" stop-opacity=".18"/><stop offset="1" stop-color="{RED}" stop-opacity="0"/></radialGradient>
<pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse"><path d="M32 0H0V32" fill="none" stroke="#0e1834" stroke-width="1"/></pattern>
<pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="1.4" fill="#000" opacity=".35"/></pattern>
<filter id="glow" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="3.5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<filter id="blur" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="16"/></filter>
<clipPath id="fr">{chamfer(0, 0, w, h, 26)}</clipPath>
</defs>
<style>{fontcss()}{BASE}{css}</style>
<g clip-path="url(#fr)"><rect width="{w}" height="{h}" fill="{BG}"/><rect width="{w}" height="{h}" fill="url(#grid)"/>
<circle cx="{w*.15:.0f}" cy="0" r="{h*.95:.0f}" fill="url(#gb)"/><circle cx="{w*.9:.0f}" cy="{h}" r="{h*.95:.0f}" fill="url(#gr)"/>
<rect width="{w}" height="{h}" filter="url(#grain)"/>
<rect class="sbar" width="{w}" height="120" fill="url(#sb)" style="--sh:{h}px"/></g>
{chamfer(1, 1, w-2, h-2, 25, fill="none", stroke="url(#gi)", stroke_width=2, stroke_opacity=.9)}
{brackets(10, 10, w-20, h-20, CYAN)}
{ruler(w, h) if rule else ""}
{head}{body}</svg>'''

def ruler(w, h):
    """HUD tick ruler along the bottom edge with a sliding marker."""
    x0, x1, y = 44, w - 44, h - 15
    ticks = "".join(f"M{x},{y}v{-6 if (x - x0) % 80 == 0 else -3}" for x in range(x0, x1 + 1, 16))
    return (f'<path d="{ticks}" stroke="{CYAN}" stroke-opacity=".35" stroke-width="1"/>'
            f'<path class="tick" d="M{x0},{y-10}l5,6 5,-6z" fill="{CYAN}" style="--tw:{x1 - x0 - 10}px"/>')

def globe(cx, cy, R, col=CYAN, op=.3):
    """Wireframe globe: static latitudes + meridians whose scaleX oscillates to fake rotation."""
    lat = "".join(f'<ellipse cx="{cx}" cy="{cy + R*f:.1f}" rx="{R*math.sqrt(1 - f*f):.1f}" ry="{R*math.sqrt(1 - f*f)*.16:.1f}"/>' for f in (-.7, -.35, 0, .35, .7))
    lon = "".join(f'<ellipse class="lon" cx="{cx}" cy="{cy}" rx="{R}" ry="{R}" style="transform-origin:{cx}px {cy}px;animation-delay:-{i*14/12:.2f}s"/>' for i in range(6))
    return (f'<g fill="none" stroke="{col}" stroke-opacity="{op}" stroke-width="1"><circle cx="{cx}" cy="{cy}" r="{R}" stroke-opacity="{op*1.6:.2f}"/>'
            f'{lat}{lon}</g>')

def eq(x, y, n, w, h, col, gap=3):
    """Decorative equalizer bars, bottom-anchored."""
    return "".join(f'<rect class="eq" x="{x + i*(w+gap)}" y="{y - h}" width="{w}" height="{h}" fill="{col}" opacity=".75" '
                   f'style="transform-origin:{x + i*(w+gap)}px {y}px;animation-delay:-{(i*0.37) % 1.2:.2f}s;animation-duration:{0.9 + (i*7 % 5)*0.15:.2f}s"/>' for i in range(n))

def icon(paths, x, y, size, col):
    return (f'<g transform="translate({x} {y}) scale({size/24:.3f})" fill="none" stroke="{col}" stroke-width="2" '
            f'stroke-linecap="round" stroke-linejoin="round">{paths}</g>')

I = {
    "code": '<polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/>',
    "bulb": '<path d="M15 14c.2-1 .7-1.7 1.5-2.5 1-.9 1.5-2.2 1.5-3.5A6 6 0 0 0 6 8c0 1 .2 2.2 1.5 3.5.7.7 1.3 1.5 1.5 2.5"/><path d="M9 18h6"/><path d="M10 22h4"/>',
    "book": '<path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/>',
    "github": '<path d="M15 22v-4a4.8 4.8 0 0 0-1-3.5c3 0 6-2 6-5.5.08-1.25-.27-2.48-1-3.5.28-1.15.28-2.35 0-3.5 0 0-1 0-3 1.5-2.64-.5-5.36-.5-8 0C6 2 5 2 5 2c-.3 1.15-.3 2.35 0 3.5A5.4 5.4 0 0 0 4 9c0 3.5 3 5.5 6 5.5-.39.49-.68 1.05-.85 1.65-.17.6-.22 1.23-.15 1.85v4"/><path d="M9 18c-4.51 2-5-2-7-2"/>',
    "linkedin": '<path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z"/><rect x="2" y="9" width="4" height="12"/><circle cx="4" cy="4" r="2"/>',
    "globe": '<circle cx="12" cy="12" r="10"/><path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20"/><path d="M2 12h20"/>',
    "mail": '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/>',
    "arrow": '<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>',
}

def hexpts(cx, cy, r, flat=False):
    a0 = 0 if flat else 30
    return " ".join(f"{cx + r*math.cos(math.radians(a0 + 60*i)):.1f},{cy + r*math.sin(math.radians(a0 + 60*i)):.1f}" for i in range(6))

def hologram(cx, cy, r, cid, gr=40):
    """Photo in a hexagon with scanlines, a moving scan beam and orbit rings."""
    s1, s2 = cy - r * .35, cy + r * .2
    return f'''<g>
{globe(cx, cy, r + gr)}
<polygon points="{hexpts(cx, cy, r+8)}" fill="url(#g)" opacity=".45" filter="url(#blur)"/>
<g class="ring" style="transform-origin:{cx}px {cy}px"><ellipse cx="{cx}" cy="{cy}" rx="{r+46}" ry="{(r+46)*.3:.0f}" fill="none" stroke="{CYAN}" stroke-opacity=".55" stroke-width="1.5" stroke-dasharray="2 7" transform="rotate(-18 {cx} {cy})"/></g>
<g class="ringr" style="transform-origin:{cx}px {cy}px"><ellipse cx="{cx}" cy="{cy}" rx="{r+30}" ry="{(r+30)*.36:.0f}" fill="none" stroke="{RED}" stroke-opacity=".5" stroke-width="1.5" stroke-dasharray="14 10" transform="rotate(24 {cx} {cy})"/></g>
<clipPath id="{cid}"><polygon points="{hexpts(cx, cy, r)}"/></clipPath>
<g clip-path="url(#{cid})">
<image id="{cid}i" href="{PHOTO}" x="{cx-r}" y="{cy-r}" width="{2*r}" height="{2*r}"/>
<clipPath id="{cid}a"><rect x="{cx-r}" y="{s1:.0f}" width="{2*r}" height="{r*.12:.0f}"/></clipPath>
<clipPath id="{cid}b"><rect x="{cx-r}" y="{s2:.0f}" width="{2*r}" height="{r*.07:.0f}"/></clipPath>
<g class="gs1" clip-path="url(#{cid}a)"><use href="#{cid}i"/><rect x="{cx-r}" y="{s1:.0f}" width="{2*r}" height="{r*.12:.0f}" fill="{RED}" opacity=".35"/></g>
<g class="gs2" clip-path="url(#{cid}b)"><use href="#{cid}i"/><rect x="{cx-r}" y="{s2:.0f}" width="{2*r}" height="{r*.07:.0f}" fill="{CYAN}" opacity=".45"/></g>
<rect x="{cx-r}" y="{cy-r}" width="{2*r}" height="{2*r}" fill="{BLUE}" opacity=".12"/>
<rect x="{cx-r}" y="{cy-r}" width="{2*r}" height="{2*r}" fill="url(#scan)"/>
<rect class="beam" x="{cx-r}" y="{cy-r-30}" width="{2*r}" height="26" fill="url(#beam)" style="--h:{2*r+60}px"/>
</g>
<polygon points="{hexpts(cx, cy, r)}" fill="none" stroke="url(#g)" stroke-width="3"/>
<polygon class="flick" points="{hexpts(cx, cy, r+12)}" fill="none" stroke="{CYAN}" stroke-opacity=".35" stroke-dasharray="40 18"/>
</g>'''

HOLO_CSS = (".ring{animation:spin 26s linear infinite}.ringr{animation:spinr 18s linear infinite}"
            "@keyframes beam{0%{transform:translateY(0)}100%{transform:translateY(var(--h))}}.beam{animation:beam 3.4s cubic-bezier(.5,0,.5,1) infinite}")
BEAM_DEF = f'<defs><linearGradient id="beam" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{CYAN}" stop-opacity="0"/><stop offset=".8" stop-color="{CYAN}" stop-opacity=".45"/><stop offset="1" stop-color="#fff" stop-opacity=".8"/></linearGradient></defs>'

def readout(x, y, k, v, col=CYAN):
    return f'<text class="mono" x="{x}" y="{y}" font-size="11" letter-spacing="1.5" fill="{MUTED}">{k} <tspan fill="{col}">{v}</tspan></text>'

# ───────────── 1. hero ─────────────
def intro():
    W, H = 880, 420
    # perspective floor: converging verticals + scrolling horizontals, masked to fade at the horizon
    vx, hy = 300, 300
    verts = "".join(f'<line x1="{vx + (i - 8) * 6}" y1="{hy}" x2="{vx + (i - 8) * 120}" y2="{H}"/>' for i in range(17))
    hors = "".join(f'<line x1="0" y1="{hy + 6 + i*18}" x2="{W}" y2="{hy + 6 + i*18}"/>' for i in range(8))
    floor = f'''<defs><linearGradient id="fade" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="#fff" stop-opacity=".9"/></linearGradient>
<mask id="fm"><rect x="0" y="{hy}" width="{W}" height="{H-hy}" fill="url(#fade)"/></mask></defs>
<g mask="url(#fm)" stroke="{BLUE}" stroke-opacity=".55" stroke-width="1">{verts}<g class="floor">{hors}</g></g>'''
    name = "TELA SAI DHANUSH"
    letters = "".join(f'<tspan class="l" style="animation-delay:{.25 + i*.045:.2f}s">{c if c != " " else "&#160;"}</tspan>' for i, c in enumerate(name))
    roles = ["BACKEND ENGINEER", "PYTHON + TYPESCRIPT DEV", "LLM TOOLING BUILDER", "ODOO DEVELOPER"]
    role_t = "".join(f'<g class="r" style="opacity:{1 if i == 0 else 0};animation-delay:{i*2.5}s"><text class="d5" x="70" y="200" font-size="19" letter-spacing="3" fill="{CYAN if i % 2 == 0 else RED}" filter="url(#glow)">{r}<tspan class="blink" fill="{INK}">_</tspan></text></g>' for i, r in enumerate(roles))
    body = f'''{BEAM_DEF}{floor}
<text class="mono" x="40" y="48" font-size="11" letter-spacing="3" fill="{CYAN}">// IDENT.SYS — PROFILE LOADED</text>
{readout(560, 48, "UPLINK", "STABLE")}{readout(690, 48, "BUILD", "2026.11")}
<text class="mono" x="40" y="96" font-size="15" fill="{MUTED}"><tspan fill="{CYAN}">&gt;_</tspan> whoami</text>
<g class="flick">
<text class="d gl1" x="38" y="150" font-size="44" letter-spacing="2" fill="{RED}" opacity="0">{name}</text>
<text class="d gl2" x="38" y="150" font-size="44" letter-spacing="2" fill="{CYAN}" opacity="0">{name}</text>
<text class="d" x="38" y="150" font-size="44" letter-spacing="2" fill="url(#gn)" filter="url(#glow)">{letters}</text></g>
<text class="mono" x="40" y="200" font-size="18" fill="{MUTED}">&gt;</text>{role_t}
<text class="t" x="40" y="246" font-size="22" fill="{INK}">I build backends and LLM tools that show their work.</text>
{chamfer(40, 266, 300, 34, 10, fill=PANEL2, stroke=CYAN, stroke_opacity=.6)}
<circle class="ping" cx="60" cy="283" r="5" fill="{CYAN}" style="transform-origin:60px 283px"/><circle cx="60" cy="283" r="5" fill="{CYAN}"/>
<text class="mono" x="76" y="288" font-size="12" letter-spacing="1.5" fill="{INK}">OPEN TO BACKEND / LLM ROLES</text>
{readout(358, 288, "LOC", "HYDERABAD, IN")}{readout(358, 312, "NODE", "TECHSOPHY")}
{hologram(730, 196, 104, "hp")}
{readout(640, 366, "ID", "TSD-077")}{readout(744, 366, "STATUS", "ONLINE", "#3dffa8")}'''
    css = (HOLO_CSS + ".l{animation:rise .4s cubic-bezier(.2,.8,.2,1) backwards}"
           "@keyframes role{0%{opacity:0}3%{opacity:1}22%{opacity:1}25%{opacity:0}100%{opacity:0}}.r{animation:role 10s linear infinite}"
           "@keyframes ping{0%{transform:scale(1);opacity:.9}100%{transform:scale(3.4);opacity:0}}.ping{animation:ping 1.8s ease-out infinite}"
           "@keyframes floor{to{transform:translateY(18px)}}.floor{animation:floor 1.1s linear infinite}"
           "@keyframes g1{0%,90%,100%{opacity:0;transform:none}91%{opacity:.8;transform:translate(-4px,1px)}93%{opacity:.8;transform:translate(3px,-1px)}95%{opacity:0}}"
           "@keyframes g2{0%,90%,100%{opacity:0;transform:none}91%{opacity:.8;transform:translate(4px,-1px)}93%{opacity:.8;transform:translate(-3px,1px)}95%{opacity:0}}"
           ".gl1{animation:g1 6s steps(1) infinite}.gl2{animation:g2 6s steps(1) infinite}")
    return frame(W, H, body, css)

# ───────────── 2. status modules ─────────────
def right_now():
    W, H = 880, 306
    mods = [("MODULE 01", "BUILDING", ["Hospital billing &amp;", "reporting at Techsophy"], CYAN, "code"),
            ("MODULE 02", "LEARNING", ["LLM evaluation &amp;", "agent guardrails"], RED, "bulb"),
            ("MODULE 03", "READING", ["Postgres query plans", "&amp; Odoo internals"], AMBER, "book")]
    out = ""
    for i, (m, lab, lines, col, ic) in enumerate(mods):
        x, y = 32 + i * 278, 104
        cx, cy = x + 48, y + 52
        out += f'''<g class="c" style="animation-delay:{.15 + i*.2:.2f}s">
{chamfer(x, y, 260, 172, 14, fill=PANEL, stroke=LINE)}
{brackets(x+4, y+4, 252, 164, col, 10)}
<clipPath id="m{i}"><rect x="{x+20}" y="{y+152}" width="220" height="3"/></clipPath><rect x="{x+20}" y="{y+152}" width="220" height="3" fill="{LINE}"/><g clip-path="url(#m{i})"><rect class="ind" x="{x+20}" y="{y+152}" width="70" height="3" fill="{col}" filter="url(#glow)" style="animation-delay:-{i*.7:.1f}s"/></g>
<circle cx="{cx}" cy="{cy}" r="26" fill="none" stroke="{LINE}" stroke-width="4"/>
<circle class="spin" cx="{cx}" cy="{cy}" r="26" fill="none" stroke="{col}" stroke-width="4" stroke-dasharray="40 124" stroke-linecap="round" style="transform-origin:{cx}px {cy}px;animation-delay:-{i}s"/>
<circle cx="{cx}" cy="{cy}" r="34" fill="none" stroke="{col}" stroke-opacity=".3" stroke-dasharray="2 5"/>
{icon(I[ic], cx-11, cy-11, 22, col)}
<text class="mono" x="{x+92}" y="{y+42}" font-size="11" letter-spacing="2" fill="{MUTED}">{m}</text>
<text class="d" x="{x+92}" y="{y+66}" font-size="16" letter-spacing="2" fill="{col}" filter="url(#glow)">{lab}</text>
<text class="t" x="{x+20}" y="{y+116}" font-size="19" fill="{INK}">{lines[0]}</text>
<text class="t" x="{x+20}" y="{y+139}" font-size="19" fill="{INK}">{lines[1]}</text></g>'''
    css = ".c{animation:rise .6s cubic-bezier(.2,.8,.2,1) backwards}.spin{animation:spin 2.4s linear infinite}"
    return frame(W, H, out, css, "SYSTEM STATUS", "// ACTIVE PROCESSES — UPDATED NOV 2026")

# ───────────── 3. arsenal (honeycomb) ─────────────
def toolkit():
    W, H = 880, 400
    groups = [("LANG", CYAN, ["Python", "TypeScript", "Java", "SQL"]), ("BACKEND", BLUE, ["FastAPI", "Node.js", "Fastify", "Spring Boot"]),
              ("DATA", AMBER, ["PostgreSQL", "pgvector", "DuckDB", "Prisma"]), ("AI / LLM", RED, ["Groq", "Ollama", "RAG", "MCP"]),
              ("FRONTEND", "#3dffa8", ["React", "Next.js", "Streamlit", "Expo"])]
    tiles = [(k, col) for _, col, ks in groups for k in ks]
    r, rows = 46, [7, 6, 7]
    dx, dy = r * math.sqrt(3) + 6, r * 1.5 + 5
    out, n = [], 0
    for ri, cnt in enumerate(rows):
        for ci in range(cnt):
            k, col = tiles[n]
            cx = 252 + ci * dx + (dx / 2 if cnt == 6 else 0)
            cy = 166 + ri * dy
            d = f"{(ci * .18 + ri * .12):.2f}s"
            out.append(f'<g><polygon points="{hexpts(cx, cy, r)}" fill="{PANEL}" stroke="{col}" stroke-opacity=".35" stroke-width="1.5"/>'
                       f'<polygon class="lit" points="{hexpts(cx, cy, r)}" fill="{col}" fill-opacity=".14" stroke="{col}" stroke-width="2" filter="url(#glow)" style="animation-delay:{d}"/>'
                       f'<circle cx="{cx:.1f}" cy="{cy - 22:.1f}" r="2.5" fill="{col}"/>'
                       f'<text class="t" x="{cx:.1f}" y="{cy + 6:.1f}" text-anchor="middle" font-size="{15 if len(k) < 10 else 13}" fill="{INK}">{k}</text></g>')
            n += 1
    legend = "".join(f'{chamfer(32, 112 + i*52, 150, 40, 10, fill=PANEL, stroke=col, stroke_opacity=.5)}'
                     f'<rect x="44" y="{126 + i*52}" width="12" height="12" fill="{col}" transform="rotate(45 50 {132 + i*52})"/>'
                     f'<text class="mono" x="68" y="{137 + i*52}" font-size="12" letter-spacing="2" fill="{INK}">{lab}</text>' for i, (lab, col, _) in enumerate(groups))
    css = "@keyframes lit{0%,100%{opacity:0}8%{opacity:1}22%{opacity:0}}.lit{opacity:0;animation:lit 4s ease-in-out infinite}"
    return frame(W, H, legend + "".join(out), css, "ARSENAL", "// LOADOUT — 20 MODULES INSTALLED")

# ───────────── 4. mission log ─────────────
PROJECTS = [
    ("debate-desk", "01", "DEBATE DESK", "PYTHON · GROQ · SEC EDGAR · STREAMLIT", CYAN,
     ["Two AI agents argue for and against a company using only its latest", "10-K. Every claim must quote the filing; the judge reads the case", "twice with the sides swapped to cancel position bias."],
     "$0.0041", "PER DEBATE", "100% QUOTES VERIFIED"),
    ("lead-radar", "02", "LEAD RADAR", "PYTHON · POSTGRESQL · FASTAPI", RED,
     ["A GTM pipeline: messy B2B leads are deduplicated, enriched, scored,", "routed and synced to a CRM idempotently, with a reproducible", "benchmark behind every number."],
     "0.968", "DEDUPE F1", "14 LEADS / SEC"),
    ("claimlens", "03", "CLAIMLENS", "FASTAPI · PGVECTOR · NEXT.JS", AMBER,
     ["Know what your health insurance will pay before you're admitted:", "every policy rule quoted with its page number, IRDAI rules applied", "on top, worked out line by line."],
     "LIVE", "DEMO ONLINE", "RENDER DEPLOY"),
]

def project(slug, num, title, stack, col, lines, big, k1, k2):
    W, H = 880, 230
    desc = "".join(f'<text class="t" x="40" y="{140 + i*24}" font-size="18" fill="{MUTED}">{t}</text>' for i, t in enumerate(lines))
    body = f'''<text class="mono" x="40" y="44" font-size="11" letter-spacing="3" fill="{col}">MISSION {num} // STATUS: <tspan fill="#3dffa8">SHIPPED</tspan></text>
<text class="d" x="40" y="86" font-size="30" letter-spacing="2" fill="{INK}">{title}</text>
<text class="mono" x="40" y="112" font-size="12" letter-spacing="1.5" fill="{col}">{stack}</text>
{desc}
{chamfer(640, 36, 208, 158, 14, fill=PANEL, stroke=col, stroke_opacity=.45)}
<text class="mono" x="744" y="64" text-anchor="middle" font-size="10" letter-spacing="2" fill="{MUTED}">{k1}</text>
<text class="d" x="744" y="112" text-anchor="middle" font-size="38" fill="{col}" filter="url(#glow)">{big}</text>
<text class="mono" x="744" y="140" text-anchor="middle" font-size="10" letter-spacing="2" fill="{MUTED}">{k2}</text>
<g class="go"><text class="d5" x="728" y="178" text-anchor="middle" font-size="12" letter-spacing="2" fill="{INK}">OPEN REPO</text>{icon(I["arrow"], 784, 166, 16, col)}</g>
<path d="M40 208 H300 l10 -10 H600" fill="none" stroke="{LINE}" stroke-width="2"/>
<path class="trace" d="M40 208 H300 l10 -10 H600" fill="none" stroke="{col}" stroke-width="2" filter="url(#glow)"/>
<path class="trace t2" d="M40 208 H300 l10 -10 H600" fill="none" stroke="#fff" stroke-width="2" stroke-opacity=".8"/>
<circle cx="600" cy="198" r="4" fill="{col}"/>{eq(652, 214, 24, 5, 12, col)}'''
    css = "@keyframes go{50%{transform:translateX(5px)}}.go{animation:go 2s ease-in-out infinite}.t2{stroke-dasharray:8 392;animation-duration:2.1s;animation-delay:-1s}"
    return frame(W, H, body, css, rule=False)

# ───────────── 5. holo ID card ─────────────
def card():
    W, H = 420, 600
    stats = [("6", "REPOS"), ("4", "LANGS"), ("3", "INTERNSHIPS")]
    st = "".join(f'<text class="d" x="{110 + i*100}" y="408" text-anchor="middle" font-size="24" fill="{INK}">{v}</text>'
                 f'<text class="mono" x="{110 + i*100}" y="428" text-anchor="middle" font-size="10" letter-spacing="1.5" fill="{MUTED}">{k}</text>' for i, (v, k) in enumerate(stats))
    facts = ["2nd place, HITAM XPLORE", "B.Tech CSE (AI &amp; ML), 2026", "A Debate Desk run costs $0.0041"]
    ft = "".join(f'<rect x="56" y="{476 + i*30}" width="8" height="8" fill="{[CYAN, RED, AMBER][i]}" transform="rotate(45 60 {480 + i*30})"/>'
                 f'<text class="t" x="76" y="{486 + i*30}" font-size="17" fill="{INK}">{f}</text>' for i, f in enumerate(facts))
    body = f'''{BEAM_DEF}<defs><linearGradient id="holo" x1="0" y1="0" x2="1" y2="1">
<stop class="h1" offset="0" stop-color="{CYAN}"/><stop offset=".5" stop-color="#9b5cff"/><stop class="h3" offset="1" stop-color="{RED}"/></linearGradient>
<clipPath id="cc">{chamfer(30, 30, 360, 540, 22)}</clipPath></defs>
{chamfer(30, 30, 360, 540, 22, fill=PANEL, stroke="url(#holo)", stroke_width=3)}
<text class="mono" x="52" y="64" font-size="11" letter-spacing="2" fill="{MUTED}">HOLO-ID · CLASS: DEV</text>
<text class="mono" x="368" y="64" text-anchor="end" font-size="11" letter-spacing="2" fill="{RED}">★ RARE</text>
{hologram(210, 196, 92, "hc", 26)}
<text class="d" x="210" y="340" text-anchor="middle" font-size="21" letter-spacing="2" fill="{INK}">TELA SAI DHANUSH</text>
<text class="mono" x="210" y="364" text-anchor="middle" font-size="12" letter-spacing="2" fill="{CYAN}">BACKEND · LLM TOOLING · ODOO</text>
{chamfer(52, 380, 316, 60, 10, fill=PANEL2, stroke=LINE)}{st}
<text class="mono" x="52" y="462" font-size="11" letter-spacing="2" fill="{MUTED}">// FUN FACTS</text>{ft}
<rect class="shine" x="-240" y="0" width="120" height="{H}" fill="#fff" opacity=".08" clip-path="url(#cc)"/>'''
    css = (HOLO_CSS + "@keyframes shine{0%{transform:skewX(-20deg) translateX(0)}45%,100%{transform:skewX(-20deg) translateX(880px)}}.shine{animation:shine 5s ease-in-out infinite}"
           f"@keyframes h{{0%,100%{{stop-color:{CYAN}}}50%{{stop-color:{RED}}}}}@keyframes hr{{0%,100%{{stop-color:{RED}}}50%{{stop-color:{CYAN}}}}}"
           ".h1{animation:h 6s ease-in-out infinite}.h3{animation:hr 6s ease-in-out infinite}")
    return frame(W, H, body, css)

# ───────────── 6. open channel (radar) ─────────────
def say_hi():
    W, H = 880, 340
    cx, cy, R = 170, 186, 118
    rings = "".join(f'<circle cx="{cx}" cy="{cy}" r="{R*f:.0f}" fill="none" stroke="{CYAN}" stroke-opacity=".25"/>' for f in (1, .72, .44))
    links = [("github", "GITHUB", "github.com/telasaidhanush77", CYAN), ("linkedin", "LINKEDIN", "linkedin.com/in/saidhanush-st", RED),
             ("globe", "PORTFOLIO", "sai-dhanush-dev.netlify.app", AMBER), ("mail", "EMAIL", "telasaidhanush77@gmail.com", "#3dffa8")]
    rows = ""
    for i, (ic, lab, url, col) in enumerate(links):
        y = 108 + i * 52
        rows += f'''<g class="c" style="animation-delay:{.2 + i*.15:.2f}s">{chamfer(340, y, 508, 42, 10, fill=PANEL, stroke=LINE)}
{icon(I[ic], 356, y+12, 18, col)}<text class="mono" x="386" y="{y+26}" font-size="11" letter-spacing="2" fill="{col}">{lab}</text>
<text class="t" x="490" y="{y+27}" font-size="18" fill="{INK}">{url}</text>
<text class="mono" x="836" y="{y+26}" text-anchor="end" font-size="11" fill="{MUTED}">[ OK ]</text></g>'''
    sweep = (f'<defs><linearGradient id="sw" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{CYAN}" stop-opacity="0"/><stop offset="1" stop-color="{CYAN}" stop-opacity=".5"/></linearGradient>'
             f'<clipPath id="pc3"><circle cx="{cx}" cy="{cy}" r="44"/></clipPath></defs>'
             f'<g class="radar" style="transform-origin:{cx}px {cy}px"><path d="M{cx} {cy} L{cx+R} {cy} A{R} {R} 0 0 0 {cx + R*math.cos(math.radians(-50)):.1f} {cy + R*math.sin(math.radians(-50)):.1f} Z" fill="url(#sw)"/>'
             f'<line x1="{cx}" y1="{cy}" x2="{cx+R}" y2="{cy}" stroke="{CYAN}" stroke-width="2" filter="url(#glow)"/></g>')
    blips = "".join(f'<circle class="blip" cx="{cx + R*f*math.cos(math.radians(a)):.0f}" cy="{cy + R*f*math.sin(math.radians(a)):.0f}" r="4" fill="{col}" style="animation-delay:{d}s"/>'
                    for f, a, col, d in [(.8, -30, RED, 0), (.6, 120, AMBER, 1.2), (.9, 210, "#3dffa8", 2.1)])
    body = f'''<text class="mono" x="340" y="48" font-size="11" letter-spacing="3" fill="{CYAN}">// OPEN CHANNEL — TRANSMIT ANYTIME</text>
<text class="d" x="340" y="84" font-size="26" letter-spacing="2" fill="{INK}">SAY HI <tspan fill="{CYAN}" class="blink">_</tspan></text>
{rings}<line x1="{cx-R}" y1="{cy}" x2="{cx+R}" y2="{cy}" stroke="{CYAN}" stroke-opacity=".15"/><line x1="{cx}" y1="{cy-R}" x2="{cx}" y2="{cy+R}" stroke="{CYAN}" stroke-opacity=".15"/>
{sweep}{blips}{''.join(f'<circle class="pr" cx="{cx}" cy="{cy}" r="46" fill="none" stroke="{CYAN}" stroke-width="1.5" style="transform-origin:{cx}px {cy}px;animation-delay:{d}s"/>' for d in (0, 1.3))}
<text class="mono" x="760" y="80" text-anchor="end" font-size="10" letter-spacing="2" fill="{MUTED}">TX</text>{eq(768, 84, 10, 5, 22, CYAN)}
<image href="{PHOTO}" x="{cx-44}" y="{cy-44}" width="88" height="88" clip-path="url(#pc3)"/>
<circle cx="{cx}" cy="{cy}" r="44" fill="none" stroke="url(#g)" stroke-width="3"/>
<text class="mono" x="{cx}" y="{cy+R+22}" text-anchor="middle" font-size="11" letter-spacing="2" fill="{MUTED}">SIGNAL: <tspan fill="#3dffa8">STRONG</tspan></text>
{rows}'''
    css = (".radar{animation:spin 4s linear infinite}@keyframes blip{0%,100%{opacity:.15}10%{opacity:1}40%{opacity:.15}}.blip{animation:blip 4s linear infinite}"
           ".c{animation:rise .5s cubic-bezier(.2,.8,.2,1) backwards}"
           "@keyframes pr{0%{transform:scale(1);opacity:.7}100%{transform:scale(2.6);opacity:0}}.pr{animation:pr 2.6s ease-out infinite}")
    return frame(W, H, body, css)

files = {"intro": intro(), "right-now": right_now(), "toolkit": toolkit(), "card": card(), "say-hi": say_hi()}
files.update({f"projects/{p[0]}": project(*p) for p in PROJECTS})
for nm, s in files.items():
    (OUT / f"{nm}.svg").write_text(s, encoding="utf-8")
print({k: len(v) // 1024 for k, v in files.items()})
