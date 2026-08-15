from pathlib import Path

root = Path(r'c:\Users\User\Desktop\edu')
sections = ['admin', 'staff', 'student']

section_home = {
    'admin': 'British Poly · Home.html',
    'staff': 'page1.html',
    'student': 'page1.html',
}

style = '''
<style>
  .page-nav {
    display: flex;
    flex-wrap: wrap;
    gap: 8px 12px;
    padding: 12px 18px;
    background: #0a1e3c;
    border-bottom: 1px solid rgba(255,255,255,0.08);
    font-family: Arial, sans-serif;
    font-size: 12px;
    margin: 0;
    position: sticky;
    top: 0;
    z-index: 50;
  }
  .page-nav strong {
    color: #ffffff;
    margin-right: 6px;
    font-weight: 700;
    letter-spacing: 0.06em;
    text-transform: uppercase;
  }
  .page-nav a {
    color: #dfeaff;
    text-decoration: none;
    padding: 6px 10px;
    border-radius: 999px;
    background: rgba(255,255,255,0.07);
    transition: background 0.2s ease;
  }
  .page-nav a:hover {
    background: rgba(255,255,255,0.14);
    color: #ffffff;
  }
</style>
'''

for section in sections:
    section_path = root / section
    if not section_path.exists():
        continue
    files = sorted(section_path.glob('*.html'))
    for file in files:
        text = file.read_text(encoding='utf-8', errors='ignore')
        if 'page-nav' in text:
            continue

        links = []
        for other in files:
            if other.name == file.name:
                continue
            label = other.stem.replace('.', ' ').replace('_', ' ')
            links.append(f'<a href="{other.name}">{label}</a>')

        if section in section_home and (section_path / section_home[section]).exists():
            home_name = section_home[section]
            label = section.title() + ' Home'
            links.insert(0, f'<a href="{home_name}">{label}</a>')

        nav = '<div class="page-nav"><strong>Pages</strong>' + ''.join(links) + '</div>'

        if '<body>' in text:
            text = text.replace('<body>', '<body>\n' + style + nav, 1)
        else:
            text = '<body>\n' + style + nav + '\n' + text, 1

        file.write_text(text, encoding='utf-8')

print('Linked all HTML pages with a page navigation bar.')
