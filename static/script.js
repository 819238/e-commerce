// JavaScript file for handling cart functionality and other interactions

const cart = [];

function addToCart(productId) {
    const product = products.find(p => p.id === productId);
    const existingProduct = cart.find(item => item.id === productId);

    if (existingProduct) {
        existingProduct.quantity += 1;
    } else {
        cart.push({ ...product, quantity: 1 });
    }

    renderCart();
}

function renderCart() {
    const cartItemsContainer = document.getElementById('cart-items');
    cartItemsContainer.innerHTML = '';

    cart.forEach(item => {
        const tr = document.createElement('tr');

        tr.innerHTML = `
            <td>${item.id}</td>
            <td>${item.name}</td>
            <td>Rp ${item.price}</td>
            <td>${item.quantity}</td>
            <td>Rp ${item.price * item.quantity}</td>
        `;

        cartItemsContainer.appendChild(tr);
    });
}

// Example product data to mimic the backend data
const products = [
    { id: 1, name: 'Produk 1', price: 100000 },
    { id: 2, name: 'Produk 2', price: 150000 },
    { id: 3, name: 'Produk 3', price: 200000 }
];
