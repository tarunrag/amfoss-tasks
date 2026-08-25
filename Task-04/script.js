// --- State Management ---
let coinsData = [];
let wishlist = JSON.parse(localStorage.getItem('cryptoWishlist')) || [];
let currentTab = 'market'; // 'market' or 'wishlist'
let currentChartCoinId = null;
let chartInstance = null;

// --- DOM Elements ---
const cryptoGrid = document.getElementById('cryptoGrid');
const searchInput = document.getElementById('searchInput');
const themeToggle = document.getElementById('themeToggle');
const marketTab = document.getElementById('marketTab');
const wishlistTab = document.getElementById('wishlistTab');
const wishlistCount = document.getElementById('wishlistCount');
const loader = document.getElementById('loader');

// Modal Elements
const chartModal = document.getElementById('chartModal');
const closeBtn = document.querySelector('.close-btn');
const modalCoinTitle = document.getElementById('modalCoinTitle');
const timeBtns = document.querySelectorAll('.time-btn');

// --- Initialization ---
init();

function init() {
    updateWishlistCount();
    checkTheme();
    fetchMarketData();

    // Event Listeners
    searchInput.addEventListener('input', handleSearch);
    themeToggle.addEventListener('click', toggleTheme);
    marketTab.addEventListener('click', () => switchTab('market'));
    wishlistTab.addEventListener('click', () => switchTab('wishlist'));
    closeBtn.addEventListener('click', closeModal);
    window.addEventListener('click', (e) => {
        if (e.target === chartModal) closeModal();
    });

    timeBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            timeBtns.forEach(b => b.classList.remove('active'));
            e.target.classList.add('active');
            fetchChartData(currentChartCoinId, e.target.dataset.days);
        });
    });
}

// --- API Calls ---
async function fetchMarketData() {
    try {
        loader.style.display = 'block';
        // Fetch top 50 coins in USD
        const response = await fetch('https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=50&page=1&sparkline=false');
        coinsData = await response.json();
        loader.style.display = 'none';
        renderCoins(coinsData);
    } catch (error) {
        console.error("Error fetching data:", error);
        loader.innerText = "Failed to load data. API rate limit may be reached.";
    }
}

async function fetchChartData(coinId, days) {
    try {
        const response = await fetch(`https://api.coingecko.com/api/v3/coins/${coinId}/market_chart?vs_currency=usd&days=${days}`);
        const data = await response.json();
        renderChart(data.prices);
    } catch (error) {
        console.error("Error fetching chart data:", error);
    }
}

// --- UI Rendering ---
function renderCoins(coins) {
    cryptoGrid.innerHTML = '';
    
    coins.forEach(coin => {
        const isWishlisted = wishlist.includes(coin.id);
        const priceChange = coin.price_change_percentage_24h;
        const changeClass = priceChange >= 0 ? 'positive' : 'negative';
        const changeSign = priceChange >= 0 ? '+' : '';

        const card = document.createElement('div');
        card.className = 'card';
        card.innerHTML = `
            <button class="wishlist-btn ${isWishlisted ? 'active' : ''}" data-id="${coin.id}">
                <i class="fa-solid fa-star"></i>
            </button>
            <div class="card-header" onclick="openModal('${coin.id}', '${coin.name}')">
                <img src="${coin.image}" alt="${coin.name}">
                <h3>${coin.name} <span>(${coin.symbol.toUpperCase()})</span></h3>
            </div>
            <div class="card-price" onclick="openModal('${coin.id}', '${coin.name}')">
                $${coin.current_price.toLocaleString()}
            </div>
            <div class="card-change ${changeClass}">
                ${changeSign}${priceChange.toFixed(2)}% (24h)
            </div>
        `;
        cryptoGrid.appendChild(card);
    });

    // Attach Wishlist Listeners
    document.querySelectorAll('.wishlist-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.stopPropagation();
            toggleWishlist(btn.dataset.id, btn);
        });
    });
}

// --- Functionality ---
function handleSearch(e) {
    const searchTerm = e.target.value.toLowerCase();
    let filteredCoins = coinsData.filter(coin => 
        coin.name.toLowerCase().includes(searchTerm) || 
        coin.symbol.toLowerCase().includes(searchTerm)
    );
    
    if (currentTab === 'wishlist') {
        filteredCoins = filteredCoins.filter(coin => wishlist.includes(coin.id));
    }
    
    renderCoins(filteredCoins);
}

function switchTab(tab) {
    currentTab = tab;
    marketTab.classList.remove('active');
    wishlistTab.classList.remove('active');
    
    if (tab === 'market') {
        marketTab.classList.add('active');
        renderCoins(coinsData);
    } else {
        wishlistTab.classList.add('active');
        const wishlistCoins = coinsData.filter(coin => wishlist.includes(coin.id));
        renderCoins(wishlistCoins);
    }
    searchInput.value = ''; // Reset search on tab switch
}

function toggleWishlist(coinId, btnElement) {
    if (wishlist.includes(coinId)) {
        wishlist = wishlist.filter(id => id !== coinId);
        btnElement.classList.remove('active');
        // If we are currently on the wishlist tab, remove the card from view immediately
        if (currentTab === 'wishlist') switchTab('wishlist'); 
    } else {
        wishlist.push(coinId);
        btnElement.classList.add('active');
    }
    localStorage.setItem('cryptoWishlist', JSON.stringify(wishlist));
    updateWishlistCount();
}

function updateWishlistCount() {
    wishlistCount.innerText = `(${wishlist.length})`;
}

// --- Chart Modal Logic ---
function openModal(coinId, coinName) {
    currentChartCoinId = coinId;
    modalCoinTitle.innerText = `${coinName} Price Chart`;
    chartModal.style.display = 'flex';
    
    // Reset time buttons to 24H default
    timeBtns.forEach(b => b.classList.remove('active'));
    timeBtns[0].classList.add('active');
    
    fetchChartData(coinId, 1);
}

function closeModal() {
    chartModal.style.display = 'none';
    currentChartCoinId = null;
}

function renderChart(prices) {
    const ctx = document.getElementById('coinChart').getContext('2d');
    
    // Destroy previous chart instance if it exists to prevent overlapping
    if (chartInstance) {
        chartInstance.destroy();
    }

    const labels = prices.map(price => {
        const date = new Date(price[0]);
        // Format time based on amount of data
        return prices.length > 200 ? date.toLocaleDateString() : date.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
    });
    const dataPoints = prices.map(price => price[1]);

    const isDarkMode = document.body.getAttribute('data-theme') === 'dark';
    const gridColor = isDarkMode ? '#333' : '#e0e0e0';
    const textColor = isDarkMode ? '#e0e0e0' : '#333';

    chartInstance = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Price (USD)',
                data: dataPoints,
                borderColor: '#2962ff',
                backgroundColor: 'rgba(41, 98, 255, 0.1)',
                borderWidth: 2,
                fill: true,
                pointRadius: 0,
                pointHoverRadius: 5
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: { ticks: { color: textColor, maxTicksLimit: 8 }, grid: { color: gridColor } },
                y: { ticks: { color: textColor }, grid: { color: gridColor } }
            },
            plugins: {
                legend: { display: false }
            }
        }
    });
}

// --- Theme Management ---
function checkTheme() {
    const savedTheme = localStorage.getItem('cryptoTheme');
    const icon = themeToggle.querySelector('i');
    
    if (savedTheme === 'dark') {
        document.body.setAttribute('data-theme', 'dark');
        icon.classList.replace('fa-moon', 'fa-sun');
    }
}

function toggleTheme() {
    const isDark = document.body.getAttribute('data-theme') === 'dark';
    const icon = themeToggle.querySelector('i');

    if (isDark) {
        document.body.removeAttribute('data-theme');
        localStorage.setItem('cryptoTheme', 'light');
        icon.classList.replace('fa-sun', 'fa-moon');
    } else {
        document.body.setAttribute('data-theme', 'dark');
        localStorage.setItem('cryptoTheme', 'dark');
        icon.classList.replace('fa-moon', 'fa-sun');
    }
    
    // Redraw chart if open to update axis colors
    if (chartModal.style.display === 'flex') {
        const activeTimeBtn = document.querySelector('.time-btn.active');
        fetchChartData(currentChartCoinId, activeTimeBtn.dataset.days);
    }
}