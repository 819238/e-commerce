document.addEventListener('DOMContentLoaded', function() {
    let cart = JSON.parse(localStorage.getItem('cart')) || {};

    function updateCartUI() {
        const cartCountElement = document.querySelector('.cart-count');
        const totalQuantity = Object.values(cart).reduce((sum, item) => sum + item.quantity, 0);
        if (cartCountElement) {
            cartCountElement.textContent = totalQuantity;
        }
    }

    function updateCartModal() {
        const cartItemsModal = document.getElementById('cart-items-modal');
        if (cartItemsModal) {
            cartItemsModal.innerHTML = '';
            let total = 0;

            for (const id in cart) {
                const item = cart[id];
                const itemTotal = item.price * item.quantity;
                total += itemTotal;

                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${item.id}</td>
                    <td>${item.name}</td>
                    <td>Rp ${item.price.toFixed(2)}</td>
                    <td>${item.quantity}</td>
                    <td>Rp ${itemTotal.toFixed(2)}</td>
                `;
                cartItemsModal.appendChild(row);
            }

            const totalRow = document.createElement('tr');
            totalRow.innerHTML = `
                <td colspan="4"><strong>Total</strong></td>
                <td><strong>Rp ${total.toFixed(2)}</strong></td>
            `;
            cartItemsModal.appendChild(totalRow);
        }
    }

    function addToCart(id, name, price) {
        if (cart[id]) {
            cart[id].quantity += 1;
        } else {
            cart[id] = { id, name, price: parseFloat(price), quantity: 1 };
        }
        localStorage.setItem('cart', JSON.stringify(cart));
        updateCartUI();
    }

    document.addEventListener('click', function(event) {
        if (event.target.classList.contains('add-to-cart')) {
            const { id, name, price } = event.target.dataset;
            addToCart(id, name, price);
        } else if (event.target.classList.contains('cart')) {
            const cartModal = document.getElementById('cart-modal');
            if (cartModal) {
                cartModal.style.display = 'block';
                updateCartModal();
            }
        } else if (event.target.classList.contains('close-button')) {
            const cartModal = document.getElementById('cart-modal');
            if (cartModal) {
                cartModal.style.display = 'none';
            }
        } else if (event.target.id === 'clear-cart') {
            localStorage.removeItem('cart');
            cart = {};
            updateCartUI();
            updateCartModal();
        }
    });

    updateCartUI();
});