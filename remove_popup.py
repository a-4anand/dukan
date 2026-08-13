import re

file_path = 'dabeli/templates/index.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Remove inline CSS block
css_pattern = r'<style>\s*/\* ✅ Unique Dablie Styles - Mobile Friendly \*/.*?</style>'
content = re.sub(css_pattern, '', content, flags=re.DOTALL)

# Remove HTML block
html_pattern = r'<div id="dablie-popup-container" class="dablie-popup-container">.*?</div>\s*</div>\s*</div>'
content = re.sub(html_pattern, '', content, flags=re.DOTALL)

# Remove JS block (from script down to close script)
# Wait, let's just find the exact block and string replace.
js_block = """  <script>
    function showDabliePopup() {
      const popup = document.getElementById("dablie-popup-container");
      popup.style.display = "flex";
    }

    function closeDabliePopup() {
    const popup = document.getElementById("dablie-popup-container");
      popup.style.display = "none";
    }
    
    // Automatically show the pop-up 2 seconds after the page loads
    window.onload = function() {
      setTimeout(showDabliePopup, 2000);
    };
  </script>"""

if js_block in content:
    content = content.replace(js_block, '')
else:
    # Use regex if exact match fails
    js_pattern = r'<script>\s*function showDabliePopup.*?</script>'
    content = re.sub(js_pattern, '', content, flags=re.DOTALL)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Popup removed.")
