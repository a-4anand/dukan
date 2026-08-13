import os
import re

files = ['dabeli/templates/index.html', 'dabeli/templates/menu.html']

aos_css = '  <link href="https://unpkg.com/aos@2.3.1/dist/aos.css" rel="stylesheet">\n'
aos_js = '  <script src="https://unpkg.com/aos@2.3.1/dist/aos.js"></script>\n  <script>AOS.init();</script>\n'

for file_path in files:
    if not os.path.exists(file_path):
        continue
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Add CSS
    if 'aos.css' not in content:
        content = content.replace('</head>', aos_css + '</head>')
    
    # Add JS
    if 'aos.js' not in content:
        content = content.replace('</body>', aos_js + '</body>')

    # Add data-aos to boxes
    content = re.sub(r'(<div class="box">)', r'\1 data-aos="fade-up" data-aos-duration="500"', content)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

print("AOS added to templates.")
