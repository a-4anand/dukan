import re

files = ['dabeli/templates/menu.html', 'dabeli/templates/index.html']

for file_path in files:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Remove ALL old floating cart blocks (inline-styled ones)
    # Pattern: from <!-- Floating Cart --> to the end of the matching </script> 
    # There might be multiple duplicate blocks
    
    # Remove old floating-cart divs
    content = re.sub(r'<!-- Floating Cart -->.*?<!-- Add to Cart Script -->.*?</script>', '', content, flags=re.DOTALL)
    
    # Also remove any remaining standalone old cart blocks
    content = re.sub(r'<div id="floating-cart" style="[^"]*"[^>]*>.*?</div>\s*', '', content, flags=re.DOTALL)
    content = re.sub(r'<div id="cart-drawer" style="[^"]*"[^>]*>.*?</div>\s*', '', content, flags=re.DOTALL)
    
    # Remove any leftover cart script blocks
    content = re.sub(r'<script>\s*function toggleCartDrawer\(\).*?</script>', '', content, flags=re.DOTALL)
    
    # Insert the include before </body>
    if "{% include 'cart_partial.html' %}" not in content:
        content = content.replace('</body>', "{% include 'cart_partial.html' %}\n</body>")

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Updated {file_path}")
