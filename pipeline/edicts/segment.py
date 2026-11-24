"""Split one patch post's Markdown into change items.

The notes use three main layouts over the years:

* 2017-18: a heading per class ("## Alchemist:") with bullets under it.
* 2018-20: quoted labels ("> Balance Changes: Observer") or bold lines
  acting as sub-headings, sometimes with bullets inside quotes.
* 2021-23: themed headings ("Summary", "Detail") with bullets, or short
  Steam posts made of plain lines.

Each top-level bullet (with its nested bullets) becomes one item. Paragraphs
outside lists become items too; a paragraph of several short lines is split
into one item per line, since several Steam posts list changes that way.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

from markdown_it import MarkdownIt
from markdown_it.token import Token

_md = MarkdownIt("commonmark", {"html": False}).enable("strikethrough").enable("table")

LABEL_LEVEL = 7          # pseudo-headings sit below real h1-h6
MAX_LABEL_CHARS = 90

_FOLLOW_UP = re.compile(r"^Follow-up #?\d+ by (.+?) \((\d{4}-\d{2}-\d{2})\)$")
_SIGN_OFF = re.compile(
    r"discord\.gg|throneofli\.es/discord|^[-–—]+\s*\w+|^see you|^join us|^enjoy|^cheers"
    r"|^thanks|^thank you|^have fun|^gl ?hf|full patch notes|patch notes (here|@)"
    r"|^see (our|the) |^discuss|^more info|support@|^follow (us|our)|twitter|facebook"
    r"|^greetings|^hello|^hey (all|everyone|guys)", re.I)
_IMAGE_ONLY = re.compile(r"^(\s*!\[[^\]]*\]\([^)]*\)\s*)+$")
_LINK_ONLY = re.compile(r"^\s*(<?https?://\S+>?|\[[^\]]*\]\([^)]*\))\s*$")
_BOLD_ONLY = re.compile(r"^(\*\*|__)[^*_]{1,90}?\1\s*:?\s*$")   # bullets used as sub-headings
_LINKED_IMAGE = re.compile(r"^\s*\[!\[[^\]]*\]\([^)]*\)\]\([^)]*\)\s*$")


@dataclass
class Item:
    section: list[str]
    markdown: str
    origin: str                 # list | paragraph | line | intro (text before any structure)
    follow_up: dict | None = None   # set for replies the author posted later in the thread
    order: int = 0
    plain: str = field(default="")

    @property
    def is_reply_text(self) -> bool:
        """Prose in a later reply: usually discussion, not a change."""
        return (self.follow_up is not None and not self.follow_up.get("rerelease")
                and self.origin not in ("list", "bullet-line"))


def plain_text(markdown: str) -> str:
    """Markdown to searchable plain text."""
    s = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", markdown)
    s = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", s)
    s = re.sub(r"<(https?://[^>]+)>", r"\1", s)
    s = re.sub(r"(^|\n)\s*(>\s*)*([-*+]|\d+\.)\s+", r"\1", s)
    s = re.sub(r"(^|\n)\s*>\s?", r"\1", s)
    s = re.sub(r"[*_~`#]+", "", s)
    s = re.sub(r"\s+", " ", s)
    s = re.sub(r"^[•·▪‣]\s*", "", s.strip())    # bullet glyphs typed as text
    return s.strip()


def is_lead_in(text: str) -> bool:
    """A short line introducing what follows rather than a change itself."""
    t = text.strip()
    return (len(t) <= 60 and t.endswith((":", "："))) or bool(re.fullmatch(r"\[[^\]]{1,40}\]", t))


def _heading_text(markdown: str) -> str:
    return plain_text(markdown).strip().rstrip(":").strip()


def _is_bold_label(inline: Token) -> str | None:
    """A paragraph that is only bold text, e.g. **Login Screen got a revamp:**"""
    if _BOLD_ONLY.match(inline.content.strip()):
        # also catches "** QoL:**", which isn't valid bold to a Markdown parser
        text = _heading_text(inline.content)
        if text:
            return text
    kids =[k for k in (inline.children or []) if not (k.type == "text" and not k.content.strip())]
    if len(kids) >= 3 and kids[0].type in ("strong_open", "em_open") \
            and kids[-1].type in ("strong_close", "em_close") \
            and all(k.type not in ("softbreak", "hardbreak", "image") for k in kids):
        text = _heading_text(inline.content)
        if 0 < len(text) <= MAX_LABEL_CHARS:
            return text
    if len(kids) == 4 and kids[0].type in ("strong_open", "em_open") \
            and kids[2].type in ("strong_close", "em_close") and kids[3].type == "text" \
            and kids[3].content.strip() in (":", "："):
        return _heading_text(inline.content)
    return None


def segment(markdown: str) -> list[Item]:
    lines = markdown.split("\n")
    tokens = _md.parse(markdown)
    items: list[Item] = []
    stack: list[tuple[int, str]] = []
    follow_up: dict | None = None

    def section() -> list[str]:
        return [t for _, t in stack]

    # A bold-only bullet is taken as a sub-heading. If nothing is emitted under
    # it before the next heading, it was an item after all (e.g. "- **Grim
    # Reaper**" followed only by a picture), and is emitted as one.
    pending: list = []          # [markdown, section, follow_up] or empty

    def flush_pending() -> None:
        if pending:
            md, sec, fu = pending
            pending.clear()
            text = plain_text(md)
            items.append(Item(sec, md, "bold-list", fu, len(items), text))

    def push(level: int, text: str, bold_md: str | None = None) -> None:
        flush_pending()
        while stack and stack[-1][0] >= level:
            stack.pop()
        if bold_md is not None:
            pending[:] = [bold_md, [t for _, t in stack], follow_up]
        stack.append((level, text))

    def source(tok: Token) -> str:
        a, b = tok.map
        return "\n".join(lines[a:b])

    def emit(md: str, origin: str) -> None:
        md = md.strip()
        if not md:
            return
        text = plain_text(md)
        if not text or _IMAGE_ONLY.match(md) or _LINK_ONLY.match(md) or _LINKED_IMAGE.match(md):
            return
        if is_lead_in(text) and "\n" not in md:
            # "Detail:", "Some abilities changes in Quick mode:", "[Possible Role]".
            # Unlike a bold bullet, a lead-in with nothing after it is dropped.
            push(LABEL_LEVEL, text.strip("[]:： "))
            return
        if origin != "list" and _SIGN_OFF.search(text) and len(text) < 160:
            return
        if origin in ("line", "paragraph") and re.match(r"\s*[•·▪‣]", md):
            origin = "bullet-line"      # "• Fixed …" typed as text, still a list entry
        pending.clear()
        items.append(Item(section(), md, origin, follow_up, len(items), text))

    i = 0
    depth_list = 0      # >0 while inside a top-level list item
    quote_depth = 0
    seen_structure = False   # any heading, label or list yet? text before is "intro"
    while i < len(tokens):
        tok = tokens[i]
        t = tok.type
        if t == "heading_open":
            text = _heading_text(tokens[i + 1].content)
            m = _FOLLOW_UP.match(text)
            if m:
                flush_pending()
                stack.clear()
                follow_up = {"author": m.group(1), "date": m.group(2)}
            elif text:
                push(int(tok.tag[1]), text)
            seen_structure = True
            i += 3
            continue
        if t == "blockquote_open":
            # A quote holding one short paragraph is a label, e.g.
            # "> Balance Changes: Observer". Anything else is walked normally.
            close = _matching_close(tokens, i)
            inner = tokens[i + 1:close]
            paras = [k for k in inner if k.type == "paragraph_open"]
            others = [k for k in inner if k.type.endswith("_open") and k.type != "paragraph_open"]
            if depth_list == 0 and len(paras) == 1 and not others:
                text = _heading_text(inner[1].content)
                if 0 < len(text) <= MAX_LABEL_CHARS and "\n" not in inner[1].content.strip():
                    push(LABEL_LEVEL, text)
                    seen_structure = True
                    i = close + 1
                    continue
            quote_depth += 1
            i += 1
            continue
        if t == "blockquote_close":
            quote_depth -= 1
            i += 1
            continue
        if t in ("bullet_list_open", "ordered_list_open") and depth_list == 0:
            depth_list = 1
            i += 1
            continue
        if t == "list_item_open" and depth_list == 1:
            close = _matching_close(tokens, i)
            inner = tokens[i + 1:close]
            label = None
            if len([k for k in inner if k.type == "paragraph_open"]) == 1 and \
                    not any(k.type.endswith("list_open") for k in inner):
                # Steam lists lost their nesting; a bold-only bullet was a sub-heading
                label = _is_bold_label(inner[1])
            if label:
                push(LABEL_LEVEL, label, bold_md=_strip_marker(source(tok)))
            else:
                emit(_strip_marker(source(tok)), "list")
            seen_structure = True
            i = close + 1
            continue
        if t in ("bullet_list_close", "ordered_list_close") and depth_list == 1:
            depth_list = 0
            i += 1
            continue
        if t == "paragraph_open" and depth_list == 0:
            inline = tokens[i + 1]
            label = _is_bold_label(inline)
            if label:
                push(LABEL_LEVEL, label)
                seen_structure = True
            else:
                body = _strip_quote(source(tok))
                parts = [p for p in body.split("\n") if p.strip()]
                if len(parts) >= 2 and _BOLD_ONLY.match(parts[0].strip()):
                    # "**PATCH NOTES:**" directly followed by plain lines
                    push(LABEL_LEVEL, _heading_text(parts[0]))
                    seen_structure = True
                    parts = parts[1:]
                if len(parts) >= 2 and all(len(p) < 220 for p in parts):
                    for p in parts:
                        emit(p, "line" if seen_structure else "intro")
                else:
                    emit(body, "paragraph" if seen_structure else "intro")
            i += 3
            continue
        if t == "table_open":
            close = _matching_close(tokens, i)
            emit(source(tok), "paragraph")
            i = close + 1
            continue
        i += 1
    flush_pending()
    return items


def _matching_close(tokens: list[Token], start: int) -> int:
    level = tokens[start].level
    close_type = tokens[start].type.replace("_open", "_close")
    for j in range(start + 1, len(tokens)):
        if tokens[j].type == close_type and tokens[j].level == level:
            return j
    return len(tokens) - 1


def _strip_quote(md: str) -> str:
    return "\n".join(re.sub(r"^\s*(>\s?)+", "", ln) for ln in md.split("\n"))


def _strip_marker(md: str) -> str:
    """Remove the bullet of a list item and dedent its continuation lines."""
    md = _strip_quote(md)
    lines = md.split("\n")
    m = re.match(r"^(\s*)([-*+]|\d+[.)])\s+", lines[0])
    if not m:
        return md
    indent = len(m.group(0))
    out = [lines[0][indent:]]
    for ln in lines[1:]:
        out.append(ln[indent:] if ln[:indent].strip() == "" else ln.lstrip())
    return "\n".join(out)


def count_top_level_bullets(markdown: str) -> int:
    """Count top-level bullets straight from the parse tree, for the QA report.

    This doesn't share segment()'s walking, labelling or filtering, so a gap
    between the two numbers points at items segment() lost or invented.
    Image-only, link-only and bold-only bullets are left out, as segment()
    drops or relabels them on purpose.
    """
    lines = markdown.split("\n")
    n = 0
    open_items = 0
    for tok in _md.parse(markdown):
        if tok.type == "list_item_open":
            if open_items == 0:
                span = [ln for ln in lines[tok.map[0]:tok.map[1]] if ln.strip()]
                rest = re.sub(r"^\s*(>\s*)*([-*+]|\d+[.)])\s*", "", span[0]).strip()
                one_line = len(span) == 1
                if not (one_line and (_IMAGE_ONLY.match(rest) or _LINK_ONLY.match(rest)
                                      or _LINKED_IMAGE.match(rest) or _BOLD_ONLY.match(rest)
                                      or is_lead_in(plain_text(rest)))):
                    n += 1
            open_items += 1
        elif tok.type == "list_item_close":
            open_items -= 1
    return n
