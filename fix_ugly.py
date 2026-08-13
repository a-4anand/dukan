import os

file_path = 'dabeli/templates/index.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Find the start of the offer section
offer_start = content.find('<section class="offer_section')
# Find the end of the offer section
# The offer section ends right before the food section
food_start = content.find('<!-- food section -->', offer_start)

if offer_start != -1 and food_start != -1:
    content = content[:offer_start] + content[food_start:]
    print("Offer section removed.")
else:
    print("Could not find offer or food section.")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
