#!/usr/bin/env python3
"""
Converte analisi-unificata.md in HTML multi-pagina con:
- Navigazione sidebar
- Progress bar globale (pagine visitate)
- Mermaid.js per diagrammi
- Testo identico all'originale
"""

import re
import html as html_mod

def parse_markdown(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    return text

def convert_inline(text):
    """Convert inline markdown: **bold**, *italic*, `code`"""
    # Bold
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    # Italic (but not ** which is bold)
    text = re.sub(r'(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)', r'<em>\1</em>', text)
    # Inline code
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
    # HTML entities
    text = text.replace('→', '&rarr;')
    text = text.replace('←', '&larr;')
    text = text.replace('↑', '&uarr;')
    text = text.replace('↓', '&darr;')
    text = text.replace('✅', '&#x2705;')
    text = text.replace('❌', '&#x274C;')
    text = text.replace('⚠️', '&#x26A0;&#xFE0F;')
    text = text.replace('🔴', '&#x1F534;')
    text = text.replace('🟠', '&#x1F7E0;')
    text = text.replace('🟡', '&#x1F7E1;')
    text = text.replace('🟢', '&#x1F7E2;')
    text = text.replace('🔵', '&#x1F535;')
    text = text.replace('🟣', '&#x1F7E3;')
    text = text.replace('⚪', '&#x26AA;')
    text = text.replace('📝', '&#x1F4DD;')
    text = text.replace('🔧', '&#x1F527;')
    text = text.replace('🔍', '&#x1F50D;')
    text = text.replace('🔒', '&#x1F512;')
    text = text.replace('🚀', '&#x1F680;')
    text = text.replace('🏗️', '&#x1F3D7;&#xFE0F;')
    text = text.replace('📦', '&#x1F4E6;')
    text = text.replace('🧪', '&#x1F9EA;')
    text = text.replace('📋', '&#x1F4CB;')
    text = text.replace('⚙️', '&#x2699;&#xFE0F;')
    text = text.replace('💰', '&#x1F4B0;')
    text = text.replace('🔌', '&#x1F50C;')
    text = text.replace('🔨', '&#x1F528;')
    text = text.replace('💡', '&#x1F4A1;')
    text = text.replace('👤', '&#x1F464;')
    text = text.replace('🎯', '&#x1F3AF;')
    text = text.replace('📊', '&#x1F4CA;')
    text = text.replace('📈', '&#x1F4C8;')
    text = text.replace('📉', '&#x1F4C9;')
    text = text.replace('🔇', '&#x1F507;')
    text = text.replace('🔊', '&#x1F50A;')
    text = text.replace('🖥️', '&#x1F5A5;&#xFE0F;')
    text = text.replace('💻', '&#x1F4BB;')
    text = text.replace('📱', '&#x1F4F1;')
    text = text.replace('🌐', '&#x1F310;')
    text = text.replace('🔄', '&#x1F504;')
    text = text.replace('🛡️', '&#x1F6E1;&#xFE0F;')
    text = text.replace('🔐', '&#x1F510;')
    return text

def convert_table_line(line):
    """Convert a markdown table line to HTML table row."""
    cells = [c.strip() for c in line.split('|')[1:-1]]
    return cells

def is_table_separator(line):
    """Check if line is a table separator (|---|)."""
    return bool(re.match(r'^\|[\s:-]+\|', line.strip()))

def process_blocks(lines):
    """Process markdown lines into HTML blocks per section."""
    sections = {}  # title -> list of HTML lines
    current_section = "Introduzione"
    current_content = []
    in_code_block = False
    code_block_lang = ""
    code_lines = []
    in_table = False
    table_headers = []
    table_rows = []
    pending_paragraph = []  # Buffer for multi-line paragraphs
    
    def flush_paragraph():
        nonlocal pending_paragraph
        if pending_paragraph:
            text = ' '.join(pending_paragraph)
            # Collapse multiple spaces
            text = re.sub(r'\s+', ' ', text).strip()
            if text:
                current_content.append(f'<p>{convert_inline(text)}</p>')
            pending_paragraph = []
    
    def flush_code():
        nonlocal code_lines
        flush_paragraph()
        if code_lines:
            lang = code_block_lang
            if lang == 'mermaid':
                content = "".join(code_lines)
                content = content.replace('&lt;', '<').replace('&gt;', '>')
                import re; content = re.sub(r',\s*optional\b', '', content)
                current_content.append(f'<div class="mermaid-wrapper"><div class="mermaid">\n{content}\n</div></div>')
            else:
                code_text = html_mod.escape("".join(code_lines))
                lang_attr = f' class="language-{lang}"' if lang else ''
                label = f'<span class="code-label">{lang}</span>' if lang else ''
                current_content.append(f'<pre>{label}<code{lang_attr}>{code_text}</code></pre>')
            code_lines = []

    def flush_table():
        nonlocal table_headers, table_rows
        flush_paragraph()
        if table_headers or table_rows:
            html = '<div class="table-wrapper"><table>\n'
            if table_headers:
                html += '<thead><tr>' + ''.join(f'<th>{convert_inline(h)}</th>' for h in table_headers) + '</tr></thead>\n'
            if table_rows:
                html += '<tbody>\n'
                for row in table_rows:
                    html += '<tr>' + ''.join(f'<td>{convert_inline(c)}</td>' for c in row) + '</tr>\n'
                html += '</tbody>\n'
            html += '</table></div>'
            current_content.append(html)
            table_headers = []
            table_rows = []
    
    for line in lines:
        stripped = line.rstrip('\n')
        
        # Code block handling
        if stripped.startswith('```'):
            if in_code_block:
                in_code_block = False
                flush_code()
                code_block_lang = ""
            else:
                in_code_block = True
                code_block_lang = stripped[3:].strip()
                code_lines = []
            continue
        
        if in_code_block:
            code_lines.append(stripped + '\n')
            continue
        
        # Flush table if not in one
        if in_table and not stripped.startswith('|'):
            in_table = False
            flush_table()
        
        # Handle horizontal rule
        if stripped.strip() == '---':
            flush_paragraph()
            current_content.append('<hr>')
            continue
        
        # Skip H1 lines (main title) — already handled by build_html
        if stripped.startswith('# ') and not stripped.startswith('## '):
            continue
        
        # Handle headers (section breaks)
        if stripped.startswith('## '):
            flush_paragraph()
            # Flush previous section
            title = stripped[3:].strip()
            if current_section not in sections:
                sections[current_section] = current_content[:]
            else:
                sections[current_section] = current_content[:] if current_content else current_content
            current_section = title
            current_content = []
            continue
        
        if stripped.startswith('### '):
            flush_paragraph()
            current_content.append(f'<h3>{convert_inline(stripped[4:].strip())}</h3>')
            continue
        
        if stripped.startswith('#### '):
            flush_paragraph()
            current_content.append(f'<h4>{convert_inline(stripped[5:].strip())}</h4>')
            continue
        
        # Table handling
        if stripped.startswith('|') and stripped.endswith('|'):
            flush_paragraph()
            cells = convert_table_line(stripped)
            if not cells:
                continue
            if is_table_separator(stripped):
                if not in_table:
                    in_table = True
                continue
            if not in_table:
                in_table = True
                table_headers = cells
            else:
                table_rows.append(cells)
            continue
        
        # Blockquote
        if stripped.startswith('> '):
            flush_paragraph()
            content = convert_inline(stripped[2:].strip())
            current_content.append(f'<blockquote>{content}</blockquote>')
            continue
        
        # List items
        if re.match(r'^(\s*[-*+]\s)', stripped):
            flush_paragraph()
            content = convert_inline(re.sub(r'^(\s*)[-*+]\s', r'\1', stripped))
            indent = len(stripped) - len(stripped.lstrip())
            current_content.append(f'<li data-indent="{indent}">{content}</li>')
            continue
        
        if re.match(r'^\s*\d+[.)]\s', stripped):
            flush_paragraph()
            content = convert_inline(re.sub(r'^\s*\d+[.)]\s', '', stripped))
            current_content.append(f'<li class="ordered">{content}</li>')
            continue
        
        # Empty line — flush pending paragraph
        if stripped.strip() == '':
            flush_paragraph()
            continue
        
        # Multi-line paragraph support: accumulate lines
        pending_paragraph.append(stripped)
    
    # Flush last section
    flush_paragraph()
    if current_section not in sections:
        sections[current_section] = current_content[:]
    else:
        sections[current_section] = current_content[:] if current_content else current_content
    
    return sections

def group_lists(blocks):
    """Group consecutive <li> into <ul>/<ol>."""
    result = []
    i = 0
    while i < len(blocks):
        block = blocks[i]
        if block.startswith('<li'):
            list_items = []
            ordered = False
            while i < len(blocks) and (blocks[i].startswith('<li') or blocks[i].startswith('<li')):
                if blocks[i].startswith('<li class="ordered"'):
                    ordered = True
                list_items.append(blocks[i])
                i += 1
            tag = 'ol' if ordered else 'ul'
            result.append(f'<{tag}>\n' + '\n'.join(list_items) + f'\n</{tag}>')
        else:
            result.append(block)
            i += 1
    return result

def build_html(sections):
    """Build the complete HTML document."""
    section_titles = list(sections.keys())
    total_sections = len(section_titles)
    
    # Build page content for each section
    pages_html = []
    for idx, title in enumerate(section_titles):
        blocks = sections[title]
        blocks = group_lists(blocks)
        content = '\n    '.join(blocks)
        is_intro = (idx == 0)
        pages_html.append(f'''    <div class="page" id="page-{idx}" data-title="{html_mod.escape(title)}">
      <div class="page-number">Sezione {idx+1} di {total_sections}</div>
      {"<h1>Analisi Unificata dell&apos;Architettura Sistec HMI</h1>" if is_intro else f"<h2>{html_mod.escape(title)}</h2>"}
      {content}
    </div>''')
    
    # Build sidebar navigation
    nav_items = []
    for idx, title in enumerate(section_titles):
        short = title[:60] + ('...' if len(title) > 60 else '')
        nav_items.append(
            f'      <li><a href="#" onclick="goToPage({idx})" data-page="{idx}" class="nav-link" title="{html_mod.escape(title)}">{html_mod.escape(short)}</a></li>'
        )
    
    nav_html = '\n'.join(nav_items)
    
    # Ensure mermaid is also embedded as a fallback CDN
    html = f'''<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Analisi Unificata — Sistec HMI</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.11.0/highlight.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.11.0/languages/csharp.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.11.0/languages/json.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.11.0/languages/xml.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.11.0/languages/yaml.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.11.0/languages/sql.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.11.0/languages/javascript.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.11.0/languages/markdown.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.11.0/languages/ini.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js"></script>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.11.0/styles/atom-one-dark.min.css">
<style>
  *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
    background: #f5f5f5;
    color: #1a1a1a;
    display: flex;
    min-height: 100vh;
  }}
  
  /* Progress Bar */
  #progress-container {{
    position: fixed;
    top: 0; left: 0; right: 0;
    height: 6px;
    background: #e0e0e0;
    z-index: 1000;
  }}
  #progress-bar {{
    height: 100%;
    width: 0%;
    background: linear-gradient(90deg, #1565c0, #42a5f5);
    transition: width 0.5s ease;
  }}
  #progress-text {{
    position: fixed;
    top: 8px;
    right: 16px;
    font-size: 12px;
    color: #666;
    z-index: 1001;
  }}
  
  /* Sidebar */
  #sidebar {{
    width: 260px;
    min-width: 260px;
    background: #1e293b;
    color: #e2e8f0;
    overflow-y: auto;
    height: 100vh;
    position: sticky;
    top: 0;
    padding-top: 16px;
  }}
  #sidebar h3 {{
    padding: 12px 16px 8px;
    font-size: 13px;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    color: #94a3b8;
    font-weight: 600;
  }}
  #sidebar ul {{
    list-style: none;
    padding: 0;
  }}
  #sidebar li a {{
    display: block;
    padding: 6px 16px 6px 16px;
    color: #cbd5e1;
    text-decoration: none;
    font-size: 13px;
    line-height: 1.4;
    border-left: 3px solid transparent;
    transition: all 0.15s;
    cursor: pointer;
  }}
  #sidebar li a:hover {{
    background: #334155;
    color: #fff;
    border-left-color: #60a5fa;
  }}
  #sidebar li a.active {{
    background: #334155;
    color: #fff;
    border-left-color: #3b82f6;
    font-weight: 600;
  }}
  #sidebar li a.read {{
    color: #93c5fd;
  }}
  
  /* Main */
  #main {{
    flex: 1;
    padding: 0;
    overflow-y: auto;
    height: 100vh;
    background: #fff;
  }}
  .page {{
    display: none;
    padding: 48px 48px 64px;
    max-width: 900px;
    margin: 0 auto;
    line-height: 1.7;
  }}
  .page.active {{ display: block; }}
  .page-number {{
    font-size: 12px;
    color: #94a3b8;
    margin-bottom: 8px;
    text-transform: uppercase;
    letter-spacing: 1px;
  }}
  
  h1 {{
    font-size: 28px;
    font-weight: 700;
    margin-bottom: 24px;
    color: #0f172a;
    line-height: 1.3;
  }}
  h2 {{
    font-size: 22px;
    font-weight: 700;
    margin-bottom: 20px;
    margin-top: 0;
    color: #0f172a;
    padding-bottom: 8px;
    border-bottom: 2px solid #e2e8f0;
  }}
  h3 {{
    font-size: 18px;
    font-weight: 600;
    margin-top: 28px;
    margin-bottom: 12px;
    color: #1e293b;
  }}
  h4 {{
    font-size: 15px;
    font-weight: 600;
    margin-top: 20px;
    margin-bottom: 8px;
    color: #334155;
  }}
  p {{ margin-bottom: 12px; }}
  
  a {{ color: #2563eb; }}
  a:hover {{ color: #1d4ed8; }}
  
  blockquote {{
    border-left: 4px solid #3b82f6;
    background: #f0f7ff;
    padding: 12px 16px;
    margin: 12px 0;
    border-radius: 0 6px 6px 0;
    color: #1e3a5f;
  }}
  
  code {{
    background: #f1f5f9;
    padding: 2px 6px;
    border-radius: 4px;
    font-family: 'Cascadia Code', 'Fira Code', 'Consolas', monospace;
    font-size: 13px;
  }}
  pre {{
    background: #0f172a;
    color: #e2e8f0;
    padding: 16px;
    border-radius: 8px;
    overflow-x: auto;
    margin: 12px 0;
    position: relative;
  }}
  pre code {{
    background: transparent;
    padding: 0;
    color: inherit;
    font-size: 13px;
    line-height: 1.5;
    font-family: 'Cascadia Code', 'Fira Code', 'Consolas', monospace;
  }}
  pre code.hljs {{
    padding: 0;
    background: transparent;
  }}
  .code-label {{
    position: absolute;
    top: 0;
    right: 0;
    background: #334155;
    color: #94a3b8;
    font-size: 11px;
    padding: 2px 8px;
    border-radius: 0 8px 0 6px;
    text-transform: uppercase;
    letter-spacing: 1px;
  }}
  
  /* Tables */
  .table-wrapper {{
    overflow-x: auto;
    margin: 16px 0;
  }}
  table {{
    border-collapse: collapse;
    width: 100%;
    font-size: 14px;
  }}
  th {{
    background: #f1f5f9;
    font-weight: 600;
    text-align: left;
    padding: 8px 12px;
    border: 1px solid #e2e8f0;
  }}
  td {{
    padding: 6px 12px;
    border: 1px solid #e2e8f0;
    vertical-align: top;
  }}
  tr:nth-child(even) td {{
    background: #fafafa;
  }}
  
  /* Lists */
  ul, ol {{ margin: 8px 0 8px 24px; }}
  li {{ margin-bottom: 4px; }}
  
  hr {{
    border: none;
    border-top: 1px solid #e2e8f0;
    margin: 32px 0;
  }}
  
  /* Mermaid */
  .mermaid {{
    margin: 20px 0;
    text-align: center;
    background: #fafafa;
    padding: 16px;
    border-radius: 8px;
    border: 1px solid #e2e8f0;
    overflow-x: auto;
  }}
  
  /* Navigation buttons */
  #nav-buttons {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 32px;
    padding-top: 16px;
    border-top: 1px solid #e2e8f0;
  }}
  #nav-buttons button {{
    padding: 10px 24px;
    border: none;
    border-radius: 8px;
    font-size: 14px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.15s;
  }}
  #btn-prev {{
    background: #e2e8f0;
    color: #334155;
  }}
  #btn-prev:hover {{ background: #cbd5e1; }}
  #btn-next {{
    background: #2563eb;
    color: #fff;
  }}
  #btn-next:hover {{ background: #1d4ed8; }}
  #btn-prev:disabled, #btn-next:disabled {{
    opacity: 0.4;
    cursor: not-allowed;
  }}
  #page-indicator {{
    font-size: 13px;
    color: #64748b;
  }}
  
  /* Mermaid maximize / zoom */
  .mermaid-wrapper {{
    position: relative;
    display: inline-block;
    width: 100%;
  }}
  .mermaid-btn-max {{
    position: absolute;
    top: 8px;
    right: 8px;
    width: 32px;
    height: 32px;
    border: none;
    border-radius: 6px;
    background: rgba(15,23,42,0.6);
    color: #fff;
    font-size: 16px;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    opacity: 0;
    transition: opacity 0.2s;
    z-index: 2;
  }}
  .mermaid-wrapper:hover .mermaid-btn-max {{
    opacity: 1;
  }}
  .mermaid-btn-max:hover {{
    background: rgba(15,23,42,0.85);
  }}
  
  #mermaid-modal {{
    display: none;
    position: fixed;
    inset: 0;
    z-index: 9999;
    background: rgba(0,0,0,0.75);
    justify-content: center;
    align-items: center;
  }}
  #mermaid-modal.open {{
    display: flex;
  }}
  #mermaid-modal-content {{
    position: relative;
    background: #fff;
    border-radius: 12px;
    padding: 24px;
    max-width: 94vw;
    max-height: 94vh;
    overflow: hidden;
    box-shadow: 0 20px 60px rgba(0,0,0,0.5);
  }}
  #mermaid-modal-close {{
    position: absolute;
    top: 8px;
    right: 8px;
    width: 36px;
    height: 36px;
    border: none;
    border-radius: 50%;
    background: #e2e8f0;
    color: #334155;
    font-size: 20px;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 10;
  }}
  #mermaid-modal-close:hover {{
    background: #cbd5e1;
  }}
  #mermaid-modal-svg {{
    cursor: grab;
    transform-origin: 0 0;
  }}
  #mermaid-modal-svg.dragging {{
    cursor: grabbing;
  }}
  #mermaid-modal-zoom-info {{
    position: absolute;
    bottom: 12px;
    left: 50%;
    transform: translateX(-50%);
    background: rgba(0,0,0,0.6);
    color: #fff;
    font-size: 12px;
    padding: 4px 12px;
    border-radius: 12px;
    pointer-events: none;
  }}
  
  /* Responsive */
  @media (max-width: 768px) {{
    #sidebar {{ display: none; }}
    .page {{ padding: 24px 16px 32px; }}
  }}
</style>
</head>
<body>

<div id="progress-container">
  <div id="progress-bar"></div>
</div>
<div id="progress-text">0% letto</div>

<div id="sidebar">
  <h3>Sezioni</h3>
  <ul>
{nav_html}
  </ul>
</div>

<div id="main">
{chr(10).join(pages_html)}
  
  <div id="nav-buttons" style="max-width:900px;margin:0 auto;padding:16px 48px 48px;">
    <button id="btn-prev" onclick="prevPage()">&larr; Precedente</button>
    <span id="page-indicator">1 / {total_sections}</span>
    <button id="btn-next" onclick="nextPage()">Successivo &rarr;</button>
  </div>
</div>

<div id="mermaid-modal" onclick="closeMermaidModal()">
  <div id="mermaid-modal-content" onclick="event.stopPropagation()">
    <button id="mermaid-modal-close" onclick="closeMermaidModal()">&times;</button>
    <div id="mermaid-modal-svg"></div>
    <div id="mermaid-modal-zoom-info">100%</div>
  </div>
</div>

<script>
  mermaid.initialize({{
    startOnLoad: false,
    theme: 'default',
    securityLevel: 'loose',
    fontFamily: 'Segoe UI, sans-serif'
  }});

  let currentPage = 0;
  const totalPages = {total_sections};
  const pages = document.querySelectorAll('.page');
  const navLinks = document.querySelectorAll('.nav-link');
  const btnPrev = document.getElementById('btn-prev');
  const btnNext = document.getElementById('btn-next');
  const pageIndicator = document.getElementById('page-indicator');
  const progressBar = document.getElementById('progress-bar');
  const progressText = document.getElementById('progress-text');
  
  // Track which pages have been visited
  let visited = new Array(totalPages).fill(false);
  // Track which pages have had mermaid rendered
  let renderedMermaid = new Array(totalPages).fill(false);
  
  function updateProgress() {{
    const read = visited.filter(v => v).length;
    const pct = Math.round((read / totalPages) * 100);
    progressBar.style.width = pct + '%';
    progressText.textContent = pct + '% letto (' + read + '/' + totalPages + ' sezioni)';
  }}
  
  async function renderMermaid(pageEl) {{
    const mermaidNodes = pageEl.querySelectorAll('.mermaid');
    if (mermaidNodes.length === 0) return;
    try {{
      await mermaid.run({{ nodes: Array.from(mermaidNodes) }});
    }} catch(e) {{
      console.warn('Mermaid render error:', e);
    }}
  }}
  
  // Mermaid modal: pan & zoom
  let mmScale = 1, mmTx = 0, mmTy = 0;
  let mmDrag = false, mmStartX = 0, mmStartY = 0;

  function openMermaidModal(svgEl) {{
    const container = document.getElementById('mermaid-modal-svg');
    container.innerHTML = '';
    const clone = svgEl.cloneNode(true);
    clone.style.width = '';
    clone.style.height = '';
    clone.style.maxWidth = '80vw';
    clone.style.maxHeight = '80vh';
    container.appendChild(clone);
    mmScale = 1; mmTx = 0; mmTy = 0;
    applyMermaidTransform();
    document.getElementById('mermaid-modal').classList.add('open');
    document.body.style.overflow = 'hidden';
  }}

  function closeMermaidModal() {{
    document.getElementById('mermaid-modal').classList.remove('open');
    document.body.style.overflow = '';
  }}

  function applyMermaidTransform() {{
    const svg = document.querySelector('#mermaid-modal-svg > svg');
    if (!svg) return;
    svg.style.transform = 'translate(' + mmTx + 'px,' + mmTy + 'px) scale(' + mmScale + ')';
    document.getElementById('mermaid-modal-zoom-info').textContent = Math.round(mmScale * 100) + '%';
  }}

  // Modal mouse events for pan + zoom
  const modalSvg = document.getElementById('mermaid-modal-svg');
  modalSvg.addEventListener('mousedown', function(e) {{
    mmDrag = true; mmStartX = e.clientX - mmTx; mmStartY = e.clientY - mmTy;
    modalSvg.classList.add('dragging');
  }});
  document.addEventListener('mousemove', function(e) {{
    if (!mmDrag) return;
    mmTx = e.clientX - mmStartX; mmTy = e.clientY - mmStartY;
    applyMermaidTransform();
  }});
  document.addEventListener('mouseup', function() {{
    mmDrag = false; modalSvg.classList.remove('dragging');
  }});
  document.getElementById('mermaid-modal-content').addEventListener('wheel', function(e) {{
    e.preventDefault();
    const delta = e.deltaY > 0 ? 0.9 : 1.1;
    const newScale = Math.min(5, Math.max(0.2, mmScale * delta));
    // zoom toward mouse position
    const rect = this.getBoundingClientRect();
    const mx = e.clientX - rect.left;
    const my = e.clientY - rect.top;
    const ratio = newScale / mmScale;
    mmTx = mx - ratio * (mx - mmTx);
    mmTy = my - ratio * (my - mmTy);
    mmScale = newScale;
    applyMermaidTransform();
  }}, {{ passive: false }});

  // Add maximize buttons to mermaid wrappers after render
  function setupMermaidButtons() {{
    document.querySelectorAll('.mermaid-wrapper').forEach(function(w) {{
      if (w.querySelector('.mermaid-btn-max')) return;
      const btn = document.createElement('button');
      btn.className = 'mermaid-btn-max';
      btn.innerHTML = '&#x26F6;';
      btn.title = 'Ingrandisci diagramma';
      btn.addEventListener('click', function(e) {{
        e.stopPropagation();
        const svg = w.querySelector('svg');
        if (svg) openMermaidModal(svg);
      }});
      w.appendChild(btn);
    }});
  }}
  
  // Patch renderMermaid to add buttons after render
  async function renderMermaid(pageEl) {{
    const mermaidNodes = pageEl.querySelectorAll('.mermaid');
    if (mermaidNodes.length === 0) return;
    try {{
      await mermaid.run({{ nodes: Array.from(mermaidNodes) }});
      setupMermaidButtons();
    }} catch(e) {{
      console.warn('Mermaid render error:', e);
    }}
  }}

  function goToPage(idx) {{
    if (idx < 0 || idx >= totalPages) return;
    
    // Mark current as visited
    visited[currentPage] = true;
    navLinks[currentPage].classList.add('read');
    
    // Hide all pages
    pages.forEach(p => p.classList.remove('active'));
    navLinks.forEach(l => l.classList.remove('active'));
    
    // Show target page
    currentPage = idx;
    const pageEl = pages[idx];
    pageEl.classList.add('active');
    navLinks[idx].classList.add('active');
    
    // Mark target as visited
    visited[idx] = true;
    navLinks[idx].classList.add('read');
    
    // Update buttons
    btnPrev.disabled = (idx === 0);
    btnNext.disabled = (idx === totalPages - 1);
    pageIndicator.textContent = (idx + 1) + ' / ' + totalPages;
    
    // Update progress
    updateProgress();
    
    // Scroll to top
    document.getElementById('main').scrollTop = 0;
    
    // Render mermaid on this page (only once per page visit)
    if (!renderedMermaid[idx]) {{
      renderedMermaid[idx] = true;
      renderMermaid(pageEl);
    }}
    
    // Highlight code blocks on this page
    pageEl.querySelectorAll('pre code[class*="language-"]').forEach((block) => {{
      hljs.highlightElement(block);
    }});
  }}
  
  function nextPage() {{
    if (currentPage < totalPages - 1) goToPage(currentPage + 1);
  }}
  
  function prevPage() {{
    if (currentPage > 0) goToPage(currentPage - 1);
  }}
  
  // Keyboard shortcuts
  document.addEventListener('keydown', function(e) {{
    if (e.key === 'ArrowRight' || e.key === ' ') {{
      e.preventDefault();
      nextPage();
    }} else if (e.key === 'ArrowLeft') {{
      e.preventDefault();
      prevPage();
    }} else if (e.key === 'Home') {{
      e.preventDefault();
      goToPage(0);
    }} else if (e.key === 'End') {{
      e.preventDefault();
      goToPage(totalPages - 1);
    }}
  }});
  
  // Initialize
  goToPage(0);
</script>
</body>
</html>'''
    
    return html

def main():
    md_path = 'analisi-unificata.md'
    html_path = 'analisi-unificata.html'
    
    print("Lettura %s..." % md_path)
    text = parse_markdown(md_path)
    lines = text.split('\n')
    
    print("%d righe lette. Elaborazione sezioni..." % len(lines))
    sections = process_blocks(lines)
    
    print("%d sezioni trovate:" % len(sections))
    for i, (title, blocks) in enumerate(sections.items()):
        print("   %d. %s (%d blocchi)" % (i+1, title, len(blocks)))
    
    print("\nGenerazione HTML...")
    html = build_html(sections)
    
    print("Scrittura %s..." % html_path)
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    file_size = len(html.encode('utf-8'))
    print("Fatto! %s (%d KB)" % (html_path, file_size/1024))

if __name__ == '__main__':
    main()
