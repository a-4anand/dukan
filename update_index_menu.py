import os

file_path = 'dabeli/templates/index.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# I will find the start of filters_menu and end of the food_section in index.html
start = content.find('<ul class="filters_menu">')
end = content.find('</section>', start)

svg_content = """<svg version="1.1" id="Capa_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" viewBox="0 0 456.029 456.029" style="enable-background:new 0 0 456.029 456.029;" xml:space="preserve">
                        <g><g><path d="M345.6,338.862c-29.184,0-53.248,23.552-53.248,53.248c0,29.184,23.552,53.248,53.248,53.248 c29.184,0,53.248-23.552,53.248-53.248C398.336,362.926,374.784,338.862,345.6,338.862z" /></g></g>
                        <g><g><path d="M439.296,84.91c-1.024,0-2.56-0.512-4.096-0.512H112.64l-5.12-34.304C104.448,27.566,84.992,10.67,61.952,10.67H20.48 C9.216,10.67,0,19.886,0,31.15c0,11.264,9.216,20.48,20.48,20.48h41.472c2.56,0,4.608,2.048,5.12,4.608l31.744,216.064 c4.096,27.136,27.648,47.616,55.296,47.616h212.992c26.624,0,49.664-18.944,55.296-45.056l33.28-166.4 C457.728,97.71,450.56,86.958,439.296,84.91z" /></g></g>
                        <g><g><path d="M215.04,389.55c-1.024-28.16-24.576-50.688-52.736-50.688c-29.696,1.536-52.224,26.112-51.2,55.296 c1.024,28.16,24.064,50.688,52.224,50.688h1.024C193.536,443.31,216.576,418.734,215.04,389.55z" /></g></g>
                      </svg>"""

replacement = """<ul class="filters_menu">
        <li class="active" data-filter="*">All</li>
        {% for category in categories %}
        <li data-filter=".{{ category.css_class }}">{{ category.name }}</li>
        {% endfor %}
      </ul>

      <div class="filters-content">
        <div class="row grid">
          {% for item in items %}
          <div class="col-sm-6 col-lg-4 all {{ item.category.css_class }}" data-aos="fade-up" data-aos-duration="500">
            <div class="box">
              <div>
                <div class="img-box">
                  <img src="{% if item.image %}{{ item.image.url }}{% else %}{{ item.image_url }}{% endif %}" alt="{{ item.name }}">
                </div>
                <div class="detail-box">
                  <h5>
                    {{ item.name }}
                  </h5>
                  <p>
                    {{ item.description }}
                  </p>
                  <div class="options">
                    <h6>
                      ₹{{ item.price }}
                    </h6>
                    <a href="#" onclick="addToCart(event, '{{ item.id }}')">
                      """ + svg_content + """
                    </a>
                  </div>
                </div>
              </div>
            </div>
          </div>
          {% endfor %}
        </div>
      </div>
"""
if start != -1 and end != -1:
    content = content[:start] + replacement + "\n    " + content[end:]
    
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("index.html menu section updated successfully.")
