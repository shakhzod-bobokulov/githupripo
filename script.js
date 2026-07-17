const PRODUCTS = [
  { id: 1, name: "Olma", desc: "Yangi, shirin qizil olma 1kg", price: 12000, icon: "🍎", cat: "oziq-ovqat" },
  { id: 2, name: "Non", desc: "Issiq, yangi pishirilgan non", price: 3000, icon: "🍞", cat: "oziq-ovqat" },
  { id: 3, name: "Sut", desc: "Tabiiy sigir suti 1L", price: 9000, icon: "🥛", cat: "oziq-ovqat" },
  { id: 4, name: "Erkaklar futbolkasi", desc: "100% paxta, turli ranglarda", price: 65000, icon: "👕", cat: "kiyim" },
  { id: 5, name: "Ayollar ko'ylagi", desc: "Yozgi yengil ko'ylak", price: 120000, icon: "👗", cat: "kiyim" },
  { id: 6, name: "Krossovka", desc: "Qulay va sport krossovkasi", price: 250000, icon: "👟", cat: "kiyim" },
  { id: 7, name: "Simsiz quloqchin", desc: "Bluetooth 5.0, kuchli tovush", price: 180000, icon: "🎧", cat: "elektronika" },
  { id: 8, name: "Quvvatlovchi batareya", desc: "10000mAh, tez zaryadlash", price: 150000, icon: "🔋", cat: "elektronika" },
  { id: 9, name: "Aqlli soat", desc: "Fitnes va bildirishnomalar", price: 320000, icon: "⌚", cat: "elektronika" },
  { id: 10, name: "Choy dastavkasi", desc: "Keramik, 6 kishilik", price: 95000, icon: "🫖", cat: "uy" },
  { id: 11, name: "Yostiq", desc: "Yumshoq, gipoallergen", price: 45000, icon: "🛏️", cat: "uy" },
  { id: 12, name: "Oshxona pichog'i", desc: "Zanglamaydigan po'lat", price: 38000, icon: "🔪", cat: "uy" },
];

let cart = JSON.parse(localStorage.getItem("cart") || "[]");
let activeCat = "all";

const productGrid = document.getElementById("productGrid");
const cartItemsEl = document.getElementById("cartItems");
const cartCountEl = document.getElementById("cartCount");
const cartTotalEl = document.getElementById("cartTotal");
const cartPanel = document.getElementById("cartPanel");
const cartOverlay = document.getElementById("cartOverlay");

function formatPrice(n) {
  return n.toString().replace(/\B(?=(\d{3})+(?!\d))/g, " ");
}

function renderProducts() {
  const list = activeCat === "all" ? PRODUCTS : PRODUCTS.filter(p => p.cat === activeCat);
  productGrid.innerHTML = list.map(p => `
    <div class="product-card">
      <div class="product-img">${p.icon}</div>
      <div class="product-info">
        <div class="product-name">${p.name}</div>
        <div class="product-desc">${p.desc}</div>
        <div class="product-footer">
          <span class="product-price">${formatPrice(p.price)} so'm</span>
          <button class="add-btn" data-id="${p.id}">Qo'shish</button>
        </div>
      </div>
    </div>
  `).join("");
}

function saveCart() {
  localStorage.setItem("cart", JSON.stringify(cart));
}

function addToCart(id) {
  const existing = cart.find(item => item.id === id);
  if (existing) {
    existing.qty += 1;
  } else {
    cart.push({ id, qty: 1 });
  }
  saveCart();
  renderCart();
}

function changeQty(id, delta) {
  const item = cart.find(i => i.id === id);
  if (!item) return;
  item.qty += delta;
  if (item.qty <= 0) {
    cart = cart.filter(i => i.id !== id);
  }
  saveCart();
  renderCart();
}

function removeFromCart(id) {
  cart = cart.filter(i => i.id !== id);
  saveCart();
  renderCart();
}

function renderCart() {
  const totalCount = cart.reduce((sum, i) => sum + i.qty, 0);
  cartCountEl.textContent = totalCount;

  if (cart.length === 0) {
    cartItemsEl.innerHTML = `<div class="empty-cart">Savatingiz bo'sh</div>`;
    cartTotalEl.textContent = "0";
    return;
  }

  let total = 0;
  cartItemsEl.innerHTML = cart.map(item => {
    const product = PRODUCTS.find(p => p.id === item.id);
    const lineTotal = product.price * item.qty;
    total += lineTotal;
    return `
      <div class="cart-item">
        <div class="cart-item-icon">${product.icon}</div>
        <div class="cart-item-info">
          <div class="cart-item-name">${product.name}</div>
          <div class="cart-item-price">${formatPrice(product.price)} so'm</div>
          <div class="qty-controls">
            <button data-action="dec" data-id="${item.id}">−</button>
            <span>${item.qty}</span>
            <button data-action="inc" data-id="${item.id}">+</button>
          </div>
        </div>
        <button class="remove-btn" data-action="remove" data-id="${item.id}">✕</button>
      </div>
    `;
  }).join("");

  cartTotalEl.textContent = formatPrice(total);
}

// Event delegation
productGrid.addEventListener("click", e => {
  if (e.target.classList.contains("add-btn")) {
    addToCart(Number(e.target.dataset.id));
  }
});

cartItemsEl.addEventListener("click", e => {
  const btn = e.target.closest("button");
  if (!btn) return;
  const id = Number(btn.dataset.id);
  const action = btn.dataset.action;
  if (action === "inc") changeQty(id, 1);
  if (action === "dec") changeQty(id, -1);
  if (action === "remove") removeFromCart(id);
});

document.querySelectorAll(".cat-btn").forEach(btn => {
  btn.addEventListener("click", () => {
    document.querySelector(".cat-btn.active").classList.remove("active");
    btn.classList.add("active");
    activeCat = btn.dataset.cat;
    renderProducts();
  });
});

document.getElementById("cartBtn").addEventListener("click", () => {
  cartPanel.classList.add("open");
  cartOverlay.classList.add("open");
});

function closeCartPanel() {
  cartPanel.classList.remove("open");
  cartOverlay.classList.remove("open");
}

document.getElementById("closeCart").addEventListener("click", closeCartPanel);
cartOverlay.addEventListener("click", closeCartPanel);

document.getElementById("checkoutBtn").addEventListener("click", () => {
  if (cart.length === 0) {
    alert("Savatingiz bo'sh!");
    return;
  }
  alert("Buyurtmangiz qabul qilindi! Tez orada siz bilan bog'lanamiz.");
  cart = [];
  saveCart();
  renderCart();
  closeCartPanel();
});

document.getElementById("burger").addEventListener("click", () => {
  document.getElementById("nav").classList.toggle("open");
});

document.getElementById("contactForm").addEventListener("submit", e => {
  e.preventDefault();
  alert("Xabaringiz yuborildi! Tez orada siz bilan bog'lanamiz.");
  e.target.reset();
});

renderProducts();
renderCart();
