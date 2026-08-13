import re

file_path = 'dabeli/templates/index.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace Hero Image
content = re.sub(
    r'<div class="bg-box">\s*<img src="\.\./static/dimage/WhatsApp%20Image%202024-01-04%20at%2000\.28\.47%20\(3\)\.jpeg" alt="">\s*</div>',
    r'<div class="bg-box">\n      <img src="{% if home_content.hero_image %}{{ home_content.hero_image.url }}{% else %}{{ home_content.hero_image_url }}{% endif %}" alt="Hero Image">\n    </div>',
    content
)

# Replace Hero Title and Subtitle
content = re.sub(
    r'<h1>\s*<span> TASTY</span>\s*</h1>\s*<p>\s*Treat Yourself: Relish Surat\'s tastiest Fast Food at Wallet-Friendly Prices!\s*</p>',
    r'<h1>\n                      <span> {{ home_content.hero_title }}</span>\n                    </h1>\n                    <p>\n                      {{ home_content.hero_subtitle }}\n                    </p>',
    content
)

# Replace About Image
content = re.sub(
    r'<div class="img-box">\s*<img src="\.\./static/images/kid\.png" height="576" width="1024"/></div>',
    r'<div class="img-box">\n            <img src="{% if home_content.about_image %}{{ home_content.about_image.url }}{% else %}{{ home_content.about_image_url }}{% endif %}" alt="About Us"/></div>',
    content
)

# Replace About Title and Text
# The original about text is very long. We can match the heading and the paragraph.
about_pattern = r'<h2>\s*We Are Dinesh Dabeli\s*</h2>\s*</div>\s*<p>.*?</p>'
about_replacement = r'<h2>\n                {{ home_content.about_title }}\n              </h2>\n            </div>\n            <p style="white-space: pre-line;">\n              {{ home_content.about_text }}\n            </p>'
content = re.sub(about_pattern, about_replacement, content, flags=re.DOTALL)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated index.html with Home Page Content tags.")
