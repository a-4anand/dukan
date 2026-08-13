import os

files = ['dabeli/templates/index.html', 'dabeli/templates/menu.html']
base_dir = '/Users/aanandkumar/Desktop/dukan'

for file in files:
    path = os.path.join(base_dir, file)
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if "{% include 'pwa_prompt.html' %}" not in content:
            content = content.replace('</body>', "{% include 'pwa_prompt.html' %}\n</body>")

        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Injected PWA prompt into {file}")
