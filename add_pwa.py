import os

files = ['dabeli/templates/index.html', 'dabeli/templates/menu.html']

head_injection = """
  <!-- PWA Meta Tags -->
  <link rel="manifest" href="/static/manifest.json">
  <meta name="theme-color" content="#ffbe33">
  <link rel="apple-touch-icon" href="/static/images/favicon.png">
"""

sw_injection = """
  <script>
    if ('serviceWorker' in navigator) {
      window.addEventListener('load', () => {
        navigator.serviceWorker.register('/static/sw.js')
          .then(reg => console.log('Service Worker registered!', reg))
          .catch(err => console.error('Service Worker registration failed', err));
      });
    }
  </script>
"""

for file_path in files:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Inject into head
    if '<link rel="manifest"' not in content:
        content = content.replace('</head>', head_injection + '</head>')
    
    # Inject service worker script before body end
    if 'navigator.serviceWorker.register' not in content:
        content = content.replace('</body>', sw_injection + '</body>')

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

print("PWA features added to templates.")
