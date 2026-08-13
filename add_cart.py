import os

file_path = 'dabeli/templates/index.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

cart_html = """
<!-- Floating Cart -->
<div id="floating-cart" style="position: fixed; bottom: 20px; right: 20px; background: #ffbe33; color: white; width: 60px; height: 60px; border-radius: 50%; display: flex; justify-content: center; align-items: center; cursor: pointer; box-shadow: 0 4px 8px rgba(0,0,0,0.2); z-index: 1000;" onclick="toggleCartDrawer()">
    <i class="fa fa-shopping-cart" style="font-size: 24px;"></i>
    <span id="cart-count" style="position: absolute; top: -5px; right: -5px; background: red; color: white; border-radius: 50%; padding: 2px 6px; font-size: 12px;">0</span>
</div>

<!-- Cart Drawer -->
<div id="cart-drawer" style="position: fixed; top: 0; right: -350px; width: 350px; height: 100vh; background: white; box-shadow: -2px 0 5px rgba(0,0,0,0.5); z-index: 1001; transition: right 0.3s; padding: 20px; overflow-y: auto;">
    <button onclick="toggleCartDrawer()" style="float: right; background: none; border: none; font-size: 20px; cursor: pointer;">&times;</button>
    <h3 style="color: #222831;">Your Order</h3>
    <hr>
    <div id="cart-items" style="color: #222831;"></div>
    <hr>
    <button onclick="checkoutWhatsApp()" style="width: 100%; padding: 10px; background: #25D366; color: white; border: none; border-radius: 5px; font-weight: bold; cursor: pointer; margin-top: 20px;">
        <i class="fa fa-whatsapp"></i> Order on WhatsApp
    </button>
</div>

<!-- Add to Cart Script -->
<script>
    function toggleCartDrawer() {
        const drawer = document.getElementById('cart-drawer');
        if (drawer.style.right === '0px') {
            drawer.style.right = '-350px';
        } else {
            drawer.style.right = '0px';
            loadCartData();
        }
    }

    function loadCartData() {
        fetch('/get_cart/')
        .then(res => res.json())
        .then(data => {
            const container = document.getElementById('cart-items');
            container.innerHTML = '';
            if(data.items.length === 0) {
                container.innerHTML = '<p>Your cart is empty.</p>';
            } else {
                data.items.forEach(item => {
                    container.innerHTML += `<div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                        <span>${item.name} (x${item.qty})</span>
                    </div>`;
                });
            }
            document.getElementById('cart-count').innerText = data.total_items;
        });
    }

    // Load initial count
    window.onload = function() {
        fetch('/get_cart/')
        .then(res => res.json())
        .then(data => {
            document.getElementById('cart-count').innerText = data.total_items;
        });
    }

    function addToCart(event, itemId) {
        event.preventDefault();
        fetch('/add_to_cart/' + itemId + '/')
        .then(res => res.json())
        .then(data => {
            if(data.status === 'success') {
                document.getElementById('cart-count').innerText = data.cart_count;
                // Add a simple toast
                let toast = document.createElement('div');
                toast.innerText = "Added to Cart!";
                toast.style.cssText = "position: fixed; bottom: 20px; left: 50%; transform: translateX(-50%); background: #222831; color: white; padding: 10px 20px; border-radius: 5px; z-index: 9999;";
                document.body.appendChild(toast);
                setTimeout(() => toast.remove(), 2000);
            }
        });
    }

    function checkoutWhatsApp() {
        fetch('/get_cart/')
        .then(res => res.json())
        .then(data => {
            if(data.items.length === 0) {
                alert("Cart is empty!");
                return;
            }
            let msg = "Hello Dinesh Dabeli! I want to order:\\n\\n";
            data.items.forEach(item => {
                msg += `- ${item.name} (x${item.qty})\\n`;
            });
            msg += "\\nPlease confirm my order.";
            let encodedMsg = encodeURIComponent(msg);
            // Assuming the business number is 919876543210
            window.open("https://wa.me/919876543210?text=" + encodedMsg, "_blank");
        });
    }
</script>
"""

# Modify the swiggy links to add to cart links in the generated section
# The loop in menu.html looks like this:
# <a href="{{ item.order_link }}"> ... </a>
# We will change it to:
# <a href="#" onclick="addToCart(event, '{{ item.id }}')"> ... </a>

content = content.replace('<a href="{{ item.order_link }}">', '<a href="#" onclick="addToCart(event, \'{{ item.id }}\')">')

# Append cart html before </body>
content = content.replace('</body>', cart_html + '\n</body>')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Cart added to menu.html")
