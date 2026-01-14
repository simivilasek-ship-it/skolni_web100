import os, re, sys
root = os.path.abspath(os.path.dirname(__file__)+'..')
missing = []
html_files = []
for dirpath, dirs, files in os.walk(root):
    for f in files:
        if f.lower().endswith('.html'):
            html_files.append(os.path.join(dirpath, f))

link_re = re.compile(r'(?:href|src)\s*=\s*"([^"]+)"')
skip_prefixes = ('http://','https://','//','mailto:','tel:','javascript:','#')
for html in sorted(html_files):
    with open(html, 'r', encoding='utf-8') as fh:
        text = fh.read()
    for m in link_re.findall(text):
        link = m.strip()
        if not link or link.startswith(skip_prefixes):
            continue
        # handle anchor-only
        if link.startswith('#'):
            continue
        # treat absolute-root as repo root
        if link.startswith('/'):
            resolved = os.path.join(root, link.lstrip('/'))
        else:
            base = os.path.dirname(html)
            resolved = os.path.normpath(os.path.join(base, link))
        # if it's a directory path, check index.html
        if os.path.isdir(resolved):
            check_path = os.path.join(resolved, 'index.html')
        else:
            check_path = resolved
        if not os.path.exists(check_path):
            missing.append((html, link, check_path))

if not missing:
    print('No missing local links found.')
    sys.exit(0)

print('Missing links:')
for html, link, path in missing:
    rel_html = os.path.relpath(html, root)
    rel_path = os.path.relpath(path, root)
    print(f'- {rel_html} -> "{link}" (expected: {rel_path})')

print('\nTotal missing: ', len(missing))
sys.exit(1)
