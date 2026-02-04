#!/usr/bin/env python3
"""
THE CHIEFS CODEX - FINAL EDITION Build Script
With new cover, gold filigree dividers, and updated subtitle
"""

import os
import re
from weasyprint import HTML, CSS
from PyPDF2 import PdfReader, PdfWriter

# Paths
BASE_DIR = "/home/ubuntu/ChiefsCodexDefinitive"
MANUSCRIPT = os.path.join(BASE_DIR, "THE_CHIEFS_CODEX_DEFINITIVE.md")
FRONT_COVER = os.path.join(BASE_DIR, "cover_resized.png")
GOLD_DIVIDER = os.path.join(BASE_DIR, "gold_divider_clean.png")
CLOCK_STAR = os.path.join(BASE_DIR, "assets/clock_sunburst_transparent.png")
OUTPUT_PDF = os.path.join(BASE_DIR, "THE_CHIEFS_CODEX_FINAL.pdf")

# Part assignments
PART_ASSIGNMENTS = {
    1: "Part I: The Ascent", 2: "Part I: The Ascent", 3: "Part I: The Ascent",
    4: "Part I: The Ascent", 5: "Part I: The Ascent", 6: "Part I: The Ascent",
    7: "Part II: The Tenure", 8: "Part II: The Tenure", 9: "Part II: The Tenure",
    10: "Part II: The Tenure", 11: "Part II: The Tenure", 12: "Part II: The Tenure",
    13: "Part III: The Departure", 14: "Part III: The Departure", 15: "Part III: The Departure",
    16: "Part III: The Departure", 17: "Part III: The Departure", 18: "Part III: The Departure",
    19: "Part III: The Departure",
}

# Chapter subtitles
CHAPTER_SUBTITLES = {
    1: "Guarding the prince's time by narrowing what reaches him.",
    2: "Doing the ugly work yourself when appearances will not suffice.",
    3: "Hurting the prince in private to keep him from bleeding in public.",
    4: "Revealing divided loyalties without becoming one of them.",
    5: "Deciding who will hate you—and from which direction danger comes.",
    6: "Controlling those whose competence can save or consume the realm.",
    7: "What refusing to dirty yourself truly costs the office.",
    8: "Keeping factions just angry enough to be useful.",
    9: "How and when to make fear audible without wasting it.",
    10: "Using surprise without turning the court into an occupied city.",
    11: "Decisions you must make alone and never explain.",
    12: "Resisting the urge to rule simply because you know how.",
    13: "Becoming smaller before you vanish entirely.",
    14: "Managing illness, decline, and the approach of the inevitable.",
    15: "Making yourself indispensable without becoming visible.",
    16: "Using apparent fragility to draw enemies into the open.",
    17: "Teaching your methods to someone who will outlive you.",
    18: "Learning to live without the gate, and letting the gate live without you.",
    19: "Returning to service when peace has finally found you.",
}

def fix_encoding(text):
    """Fix encoding issues"""
    text = text.replace('\\#', '#').replace('\\*', '*')
    text = text.replace("\\'", "'").replace('\\"', '"')
    replacements = {
        'â€"': '—', 'â€™': "'", 'â€œ': '"', 'â€': '"',
        '\u2019': "'", '\u201c': '"', '\u201d': '"', '\u2014': '—',
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text

def read_manuscript():
    with open(MANUSCRIPT, 'r', encoding='utf-8') as f:
        content = f.read()
    return fix_encoding(content)

def parse_front_matter(content):
    lines = content.split('\n')
    
    # Get new subtitle
    new_subtitle = "On Power, Proximity, and Those Who Guard It"
    
    # Find epigraphs
    epigraphs = []
    for line in lines[:25]:
        line = fix_encoding(line)
        if line.startswith('"') and '—' in line:
            parts = line.split('—', 1)
            if len(parts) == 2:
                quote = parts[0].strip().strip('"')
                attribution = parts[1].strip()
                attribution = re.sub(r'\s*\[Source.*?\]', '', attribution)
                attribution = attribution.replace('**', '').replace('*', '')
                epigraphs.append((quote, attribution))
    
    # Find preface
    preface = ""
    for line in lines[:35]:
        if "Being nineteen chapters" in line:
            preface = fix_encoding(line)
            break
    
    # Find Note on Text
    note_lines = []
    in_note = False
    for i, line in enumerate(lines[:70]):
        if "A Note on the Text" in line:
            in_note = True
            rest = line.replace("**A Note on the Text**", "").replace("A Note on the Text", "").strip()
            if rest:
                note_lines.append(rest)
            continue
        if in_note:
            if "The Editors" in line or "TO THE READER" in line:
                break
            if line.startswith("#"):
                break
            note_lines.append(line)
    
    note_text = ' '.join(note_lines).strip()
    note_text = fix_encoding(note_text)
    note_text = re.sub(r'\s*\[Source.*?\]', '', note_text)
    
    # Find TO THE READER
    to_reader_lines = []
    in_reader = False
    for i, line in enumerate(lines[:120]):
        if "TO THE READER" in line:
            in_reader = True
            continue
        if in_reader:
            if "CONTENTS" in line or line.startswith("**Chapter"):
                break
            if line.strip() == "—":
                continue
            to_reader_lines.append(line)
    
    to_reader_text = '\n\n'.join([p.strip() for p in '\n'.join(to_reader_lines).split('\n\n') if p.strip()])
    to_reader_text = fix_encoding(to_reader_text)
    
    return {
        'title': "THE CHIEFS CODEX",
        'subtitle': new_subtitle,
        'tagline': "The Private Cipher of Bertoldo di Fano",
        'author': "OMAR SALAH",
        'epigraphs': epigraphs,
        'preface': preface,
        'note': note_text,
        'to_reader': to_reader_text
    }

def parse_chapters(content):
    lines = content.split('\n')
    chapters = []
    
    chapter_starts = []
    for i, line in enumerate(lines):
        match = re.match(r'^[#\*]*\s*Chapter\s+(\d+):\s*(.+?)[\*]*$', line.strip(), re.IGNORECASE)
        if match:
            num = int(match.group(1))
            title = match.group(2).strip().rstrip('*')
            chapter_starts.append((i, num, title))
    
    print(f"Found {len(chapter_starts)} chapters")
    
    back_matter_start = len(lines)
    for i, line in enumerate(lines):
        if "## Index of Maxims" in line:
            back_matter_start = i
            break
    
    for idx, (start, num, title) in enumerate(chapter_starts):
        if idx + 1 < len(chapter_starts):
            end = chapter_starts[idx + 1][0]
        else:
            end = back_matter_start
        
        content_lines = lines[start + 1:end]
        chapter_content = '\n'.join(content_lines).strip()
        
        year = None
        year_match = re.search(r'\*\*(\d{4})\*\*', chapter_content[:200])
        if year_match:
            year = year_match.group(1)
            chapter_content = re.sub(r'\*\*\d{4}\*\*\s*\n?', '', chapter_content, count=1)
        
        chapter_content = chapter_content.strip()
        if year:
            chapter_content = re.sub(r'^' + year + r'\s*\n', '', chapter_content)
        
        part = PART_ASSIGNMENTS.get(num, "")
        
        chapters.append({
            'number': num,
            'title': title,
            'part': part,
            'year': year,
            'content': chapter_content
        })
    
    return chapters

def parse_back_matter(content):
    lines = content.split('\n')
    back_matter = {'index_of_maxims': '', 'dramatis_personae': '', 'chronology': ''}
    
    current_section = None
    section_lines = []
    
    for line in lines:
        if "## Index of Maxims" in line:
            if current_section:
                back_matter[current_section] = '\n'.join(section_lines)
            current_section = 'index_of_maxims'
            section_lines = []
        elif "## Dramatis Personae" in line:
            if current_section:
                back_matter[current_section] = '\n'.join(section_lines)
            current_section = 'dramatis_personae'
            section_lines = []
        elif "## Chronology" in line:
            if current_section:
                back_matter[current_section] = '\n'.join(section_lines)
            current_section = 'chronology'
            section_lines = []
        elif line.strip() == "**FINIS**":
            if current_section:
                back_matter[current_section] = '\n'.join(section_lines)
            break
        elif current_section:
            section_lines.append(line)
    
    return back_matter

def markdown_to_html(text, divider_path):
    """Convert markdown to HTML with gold dividers at section breaks"""
    text = fix_encoding(text)
    
    # MAXIM tags
    text = re.sub(r'\[\[MAXIM\]\]\s*(.+?)\s*\[\[/MAXIM\]\]', 
                  r'<blockquote class="maxim">\1</blockquote>', 
                  text, flags=re.DOTALL)
    
    # Bold
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    
    # Italic
    text = re.sub(r'(?<!\*)\*([^*]+?)\*(?!\*)', r'<em>\1</em>', text)
    
    # Section headers with Roman numerals - add gold divider before
    text = re.sub(r'^(I{1,3}V?|VI{0,3}|IX|X{1,3})\.\s+(.*)$', 
                  f'<div class="section-divider"><img src="file://{divider_path}" class="gold-divider"></div><div class="section-header"><strong>\\1. \\2</strong></div>', 
                  text, flags=re.MULTILINE)
    
    # Horizontal rules become gold dividers
    text = re.sub(r'^—+$', f'<div class="section-divider"><img src="file://{divider_path}" class="gold-divider"></div>', text, flags=re.MULTILINE)
    
    # Custom section divider markers
    text = text.replace('---SECTION-DIVIDER---', f'<div class="section-divider"><img src="file://{divider_path}" class="gold-divider"></div>')
    
    # Paragraphs
    paragraphs = text.split('\n\n')
    html_paragraphs = []
    for p in paragraphs:
        p = p.strip()
        if not p:
            continue
        if p.startswith('<'):
            html_paragraphs.append(p)
        else:
            p = p.replace('\n', ' ')
            html_paragraphs.append(f'<p>{p}</p>')
    
    return '\n'.join(html_paragraphs)

def generate_html(front_matter, chapters, back_matter):
    html_parts = []
    
    # HTML header with comprehensive styling
    html_parts.append(f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>The Chiefs Codex - Final Edition</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&family=EB+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500&display=swap');
        
        @page {{
            size: 6in 9in;
            margin: 0.7in 0.75in;
            background: #FDF8F0;
        }}
        
        @page:first {{
            margin: 0;
            background: none;
        }}
        
        body {{
            font-family: 'EB Garamond', Georgia, serif;
            font-size: 11pt;
            line-height: 1.5;
            color: #2D2418;
            background: #FDF8F0;
        }}
        
        .cover-page {{
            page-break-after: always;
            padding: 0;
            margin: -0.7in -0.75in -0.7in -0.75in;
            width: 6in;
            height: 9in;
            position: relative;
            overflow: hidden;
            background: #000;
        }}
        .cover-page img {{
            width: 100%;
            height: 100%;
            object-fit: cover;
            display: block;
            margin: 0;
            padding: 0;
        }}
        
        .blank-page {{
            page-break-after: always;
            height: 100%;
        }}
        
        .title-page {{
            page-break-after: always;
            text-align: center;
            padding-top: 2.5in;
        }}
        .title-page h1 {{
            font-family: 'Cinzel', serif;
            font-size: 28pt;
            font-weight: 700;
            color: #8B1A1A;
            margin-bottom: 0.3in;
            letter-spacing: 3px;
        }}
        .title-page .subtitle {{
            font-family: 'EB Garamond', serif;
            font-size: 14pt;
            font-style: italic;
            color: #5D4E37;
            margin-bottom: 0.2in;
        }}
        .title-page .tagline {{
            font-family: 'EB Garamond', serif;
            font-size: 11pt;
            font-style: italic;
            color: #7A6B5A;
            margin-bottom: 1in;
        }}
        .title-page .author {{
            font-family: 'Cinzel', serif;
            font-size: 14pt;
            font-weight: 600;
            color: #3D2E1F;
            letter-spacing: 2px;
        }}
        
        .copyright-page {{
            page-break-after: always;
            padding-top: 5in;
            font-size: 9pt;
            text-align: center;
            color: #666;
        }}
        
        .epigraph-page {{
            page-break-after: always;
            padding-top: 2in;
            text-align: center;
        }}
        .epigraph {{
            font-style: italic;
            font-size: 12pt;
            margin: 0 1in 0.5in 1in;
            color: #4A3C2A;
        }}
        .epigraph-attribution {{
            font-size: 10pt;
            color: #7A6B5A;
            margin-bottom: 1.5in;
        }}
        
        .preface-page, .note-page {{
            page-break-after: always;
            padding-top: 1.5in;
        }}
        .preface-page h2, .note-page h2 {{
            font-family: 'Cinzel', serif;
            font-size: 14pt;
            text-align: center;
            margin-bottom: 1in;
            color: #3D2E1F;
        }}
        
        .to-reader-page {{
            page-break-before: always;
            page-break-after: always;
            padding-top: 1in;
        }}
        .to-reader-page h2 {{
            font-family: 'Cinzel', serif;
            font-size: 14pt;
            text-align: center;
            margin-bottom: 1.5em;
            color: #3D2E1F;
        }}
        .to-reader-page p {{
            text-align: justify;
            text-indent: 1.5em;
            margin-bottom: 0.8em;
        }}
        
        .toc-page {{
            page-break-before: always;
            page-break-after: always;
            padding-top: 1in;
        }}
        .toc-page h2 {{
            font-family: 'Cinzel', serif;
            font-size: 16pt;
            text-align: center;
            margin-bottom: 1in;
            color: #3D2E1F;
        }}
        .toc-part {{
            font-family: 'Cinzel', serif;
            font-size: 11pt;
            font-weight: 600;
            color: #8B1A1A;
            margin: 1em 0 0.5em 0;
        }}
        .toc-entry {{
            margin: 0.3em 0 0.3em 1em;
        }}
        .toc-subtitle {{
            font-style: italic;
            font-size: 9pt;
            color: #7A6B5A;
            margin-left: 1.5em;
        }}
        
        .part-page {{
            page-break-before: always;
            page-break-after: always;
            text-align: center;
            padding-top: 3in;
        }}
        .part-title {{
            font-family: 'Cinzel', serif;
            font-size: 20pt;
            font-weight: 600;
            color: #8B1A1A;
        }}
        
        .chapter-opener {{
            page-break-before: always;
            page-break-after: always;
            text-align: center;
            padding-top: 2in;
        }}
        .chapter-opener .clock-star {{
            width: 1.5in;
            height: auto;
            margin-bottom: 1em;
        }}
        .chapter-opener .gold-divider {{
            width: 2in;
            height: auto;
            margin-bottom: 1em;
        }}
        .chapter-number {{
            font-family: 'Cinzel', serif;
            font-size: 12pt;
            font-weight: 600;
            color: #8B1A1A;
            letter-spacing: 3px;
            margin-bottom: 0.3em;
        }}
        .chapter-title {{
            font-family: 'Cinzel', serif;
            font-size: 16pt;
            font-weight: 600;
            color: #3D2E1F;
            margin-bottom: 0.5em;
        }}
        .chapter-subtitle {{
            font-style: italic;
            font-size: 10pt;
            color: #5D4E37;
            max-width: 70%;
            margin: 0 auto 1em auto;
            line-height: 1.4;
        }}
        .chapter-year {{
            font-family: 'Cinzel', serif;
            font-size: 11pt;
            color: #8B1A1A;
            margin-top: 0.5em;
        }}
        
        .chapter-body {{
            page-break-before: always;
        }}
        .chapter-body p {{
            text-align: justify;
            text-indent: 1.5em;
            margin-bottom: 0.5em;
        }}
        .chapter-body p:first-of-type {{
            text-indent: 0;
        }}
        
        .section-divider {{
            text-align: center;
            margin: 1.5em 0;
        }}
        .gold-divider {{
            width: 1.5in;
            height: auto;
            opacity: 0.9;
        }}
        
        .section-header {{
            text-align: center;
            margin: 1em 0;
            font-family: 'Cinzel', serif;
            font-size: 11pt;
            color: #5D4E37;
        }}
        
        .maxim {{
            font-style: italic;
            border-left: 3px solid #A6894D;
            padding-left: 1em;
            margin: 1.5em 2em;
            color: #5D4E37;
        }}
        
        .back-matter-page {{
            page-break-before: always;
            padding-top: 1in;
        }}
        .back-matter-page h2 {{
            font-family: 'Cinzel', serif;
            font-size: 14pt;
            text-align: center;
            margin-bottom: 1.5em;
            color: #3D2E1F;
        }}
        
        .finis {{
            page-break-before: always;
            text-align: center;
            padding-top: 4in;
            font-family: 'Cinzel', serif;
            font-size: 14pt;
            color: #8B1A1A;
            letter-spacing: 5px;
        }}
    </style>
</head>
<body>
''')
    
    # Front Cover
    html_parts.append(f'''
<div class="cover-page">
    <img src="file://{FRONT_COVER}" alt="Front Cover">
</div>
''')
    
    # Blank page
    html_parts.append('<div class="blank-page"></div>')
    
    # Title Page
    html_parts.append(f'''
<div class="title-page">
    <h1>{front_matter['title']}</h1>
    <p class="subtitle">{front_matter['subtitle']}</p>
    <p class="tagline">{front_matter['tagline']}</p>
    <p class="author">{front_matter['author']}</p>
</div>
''')
    
    # Copyright Page
    html_parts.append('''
<div class="copyright-page">
    <p>Copyright © 2025 Omar Salah</p>
    <p>All rights reserved.</p>
    <p style="margin-top: 1em;">This is a work of fiction. Names, characters, places, and incidents either are the product of the author's imagination or are used fictitiously.</p>
</div>
''')
    
    # Epigraph Page
    if front_matter['epigraphs']:
        html_parts.append('<div class="epigraph-page">')
        for quote, attr in front_matter['epigraphs'][:2]:
            html_parts.append(f'''
    <div class="epigraph">"{quote}"</div>
    <div class="epigraph-attribution">— {attr}</div>
''')
        html_parts.append('</div>')
    
    # Preface Page
    if front_matter['preface']:
        html_parts.append(f'''
<div class="preface-page">
    <h2>PREFACE</h2>
    <p style="text-align: center; font-style: italic;">{front_matter['preface']}</p>
</div>
''')
    
    # Note on Text
    if front_matter['note']:
        html_parts.append(f'''
<div class="note-page">
    <h2>A NOTE ON THE TEXT</h2>
    <p style="text-align: justify;">{front_matter['note']}</p>
</div>
''')
    
    # TO THE READER
    if front_matter['to_reader']:
        paragraphs = front_matter['to_reader'].split('\n\n')
        html_parts.append('<div class="to-reader-page">')
        html_parts.append('<h2>TO THE READER</h2>')
        for p in paragraphs:
            if p.strip():
                html_parts.append(f'<p>{p.strip()}</p>')
        html_parts.append('</div>')
    
    # Table of Contents
    html_parts.append('''
<div class="toc-page">
    <h2>CONTENTS</h2>
''')
    
    current_part = ""
    for ch in chapters:
        if ch['part'] and ch['part'] != current_part:
            current_part = ch['part']
            html_parts.append(f'    <div class="toc-part">{current_part}</div>')
        subtitle = CHAPTER_SUBTITLES.get(ch['number'], '')
        html_parts.append(f'''    <div class="toc-entry">
        <span>Chapter {ch["number"]}: {ch["title"]}</span>
        <div class="toc-subtitle">{subtitle}</div>
    </div>''')
    
    html_parts.append('</div>')
    
    # Chapters
    current_part = ""
    for ch in chapters:
        if ch['part'] and ch['part'] != current_part:
            current_part = ch['part']
            html_parts.append(f'''
<div class="part-page">
    <h2 class="part-title">{current_part}</h2>
</div>
''')
        
        year_html = f'<div class="chapter-year">{ch["year"]}</div>' if ch['year'] else ''
        content_html = markdown_to_html(ch['content'], GOLD_DIVIDER)
        subtitle = CHAPTER_SUBTITLES.get(ch['number'], '')
        subtitle_html = f'<div class="chapter-subtitle">{subtitle}</div>' if subtitle else ''
        
        # Chapter opener with clock-star ornament
        html_parts.append(f'''
<div class="chapter-opener">
    <img src="file://{CLOCK_STAR}" class="clock-star">
    <div class="chapter-number">CHAPTER {ch['number']}</div>
    <div class="chapter-title">{ch['title']}</div>
    {subtitle_html}
    {year_html}
</div>
''')
        
        # Chapter body
        html_parts.append(f'''
<div class="chapter-body">
    {content_html}
</div>
''')
    
    # Back Matter
    if back_matter['index_of_maxims']:
        html_parts.append('<div class="back-matter-page">')
        html_parts.append('<h2>INDEX OF MAXIMS</h2>')
        maxim_html = markdown_to_html(back_matter['index_of_maxims'], GOLD_DIVIDER)
        html_parts.append(maxim_html)
        html_parts.append('</div>')
    
    if back_matter['dramatis_personae']:
        html_parts.append('<div class="back-matter-page">')
        html_parts.append('<h2>DRAMATIS PERSONAE</h2>')
        dp_html = markdown_to_html(back_matter['dramatis_personae'], GOLD_DIVIDER)
        html_parts.append(dp_html)
        html_parts.append('</div>')
    
    if back_matter['chronology']:
        html_parts.append('<div class="back-matter-page">')
        html_parts.append('<h2>CHRONOLOGY</h2>')
        chron_html = markdown_to_html(back_matter['chronology'], GOLD_DIVIDER)
        html_parts.append(chron_html)
        html_parts.append('</div>')
    
    # FINIS
    html_parts.append('<div class="finis">FINIS</div>')
    
    html_parts.append('</body></html>')
    
    return '\n'.join(html_parts)

def build_pdf():
    print("=" * 60)
    print("THE CHIEFS CODEX - FINAL EDITION")
    print("=" * 60)
    
    print("\n1. Reading manuscript...")
    content = read_manuscript()
    print(f"   Read {len(content)} characters")
    
    print("\n2. Parsing front matter...")
    front_matter = parse_front_matter(content)
    print(f"   Title: {front_matter['title']}")
    print(f"   Subtitle: {front_matter['subtitle']}")
    
    print("\n3. Parsing chapters...")
    chapters = parse_chapters(content)
    print(f"   Found {len(chapters)} chapters")
    
    print("\n4. Parsing back matter...")
    back_matter = parse_back_matter(content)
    
    print("\n5. Generating HTML...")
    html_content = generate_html(front_matter, chapters, back_matter)
    
    html_file = os.path.join(BASE_DIR, "book_final.html")
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"   Saved HTML to {html_file}")
    
    print("\n6. Generating PDF...")
    HTML(string=html_content, base_url=BASE_DIR).write_pdf(OUTPUT_PDF)
    
    reader = PdfReader(OUTPUT_PDF)
    page_count = len(reader.pages)
    
    print(f"\n{'=' * 60}")
    print(f"BUILD COMPLETE!")
    print(f"Output: {OUTPUT_PDF}")
    print(f"Pages: {page_count}")
    print(f"{'=' * 60}")

if __name__ == "__main__":
    build_pdf()
