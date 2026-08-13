import re
import os

files = ['dabeli/templates/index.html', 'dabeli/templates/menu.html']
base_dir = '/Users/aanandkumar/Desktop/dukan'

for file in files:
    path = os.path.join(base_dir, file)
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # The bad syntax: <div class="box"> data-aos="fade-up" data-aos-duration="500"
        # with or without leading whitespace
        content = re.sub(
            r'<div class="box">\s*data-aos="fade-up"\s*data-aos-duration="500"\s*(<div>)?',
            r'<div class="box" data-aos="fade-up" data-aos-duration="500">\n              \1',
            content
        )
        # Handle the one without trailing <div> just in case
        content = re.sub(
            r'<div class="box">\s*data-aos="fade-up"\s*data-aos-duration="500"',
            r'<div class="box" data-aos="fade-up" data-aos-duration="500">',
            content
        )

        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed {file}")
