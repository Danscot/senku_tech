/***********************
 * MOBILE NAV
 ***********************/
const burger = document.getElementById('burger');
const mobileNav = document.getElementById('mobileNav');
const mobileClose = document.getElementById('mobileClose');

burger.addEventListener('click', () => {
  burger.classList.toggle('open');
  mobileNav.classList.toggle('active');
});

mobileClose.addEventListener('click', () => {
  burger.classList.remove('open');
  mobileNav.classList.remove('active');
});

/***********************
 * USER STATE
 ***********************/
const userData = JSON.parse(
  document.getElementById('user-data').textContent
);

let state = {
  current: 'bot',
  session: null,
  containers: 0,
  uptimeHours: 0,
  coin: userData.coin
};

const mainArea = document.getElementById('mainArea');
const sidebarLinks = document.querySelectorAll('.sidebar-link');
const bottomBtns = document.querySelectorAll('.bottom-nav button');
const modal = document.getElementById('modal');
const modalBody = document.getElementById('modalBody');

const sidebarBotDot = document.getElementById('sidebarBotDot');
const sidebarBotText = document.getElementById('sidebarBotText');
const panelContainers = document.getElementById('panelContainers');
const panelUptime = document.getElementById('panelUptime');
const coinBalance = document.getElementById('coinBalance');

/***********************
 * MODAL HELPERS
 ***********************/
function openModal(html) {
  modalBody.innerHTML = html;
  modal.style.display = 'flex';
}

function closeModal() {
  modal.style.display = 'none';
}

/***********************
 * NAV HELPERS
 ***********************/
function setActiveNav(section) {
  sidebarLinks.forEach(el =>
    el.classList.toggle('active', el.dataset.section === section)
  );
  bottomBtns.forEach(el =>
    el.classList.toggle('active', el.dataset.section === section)
  );
  state.current = section;
}

function updateSidebarWidgets() {
  if (state.session) {
    sidebarBotDot.style.background = '#4caf50';
    sidebarBotText.textContent = 'Active • ' + state.session.number;
  } else {
    sidebarBotDot.style.background = '#e53935';
    sidebarBotText.textContent = 'No session';
  }

  panelContainers.textContent = state.containers;
  panelUptime.textContent = state.uptimeHours + 'h';
  coinBalance.textContent = Number(state.coin).toFixed(2);
}

/***********************
 * RENDER ROUTER
 ***********************/
function renderSection(section) {
  if (section === 'bot') renderBotForm();
  if (section === 'panel') renderPanel();
  if (section === 'coin') renderCoin();
  updateSidebarWidgets();
}

sidebarLinks.forEach(el =>
  el.addEventListener('click', () => {
    setActiveNav(el.dataset.section);
    renderSection(el.dataset.section);
  })
);

bottomBtns.forEach(el =>
  el.addEventListener('click', () => {
    setActiveNav(el.dataset.section);
    renderSection(el.dataset.section);
  })
);

/***********************
 * BOT PAGE
 ***********************/
function renderBotForm() {
  mainArea.innerHTML = `
    <h2>Bot Management</h2>
    <p>Pair your WhatsApp bot (costs coins)</p>

    <div class="row">
      <input id="phone" class="small-input" type="text" placeholder="23767070" />
      <button id="pairBtn" class="btn">Pair Bot</button>
    </div>
  `;

  document.getElementById('pairBtn').addEventListener('click', onPairClick);
}

/***********************
 * PANEL
 ***********************/
function renderPanel() {
  mainArea.innerHTML = `
    <h2>Panel</h2>
    <p class="muted">Coming soon</p>
  `;
}

/***********************
 * COIN PAGE
 ***********************/
function renderCoin() {
  mainArea.innerHTML = `
    <h2>Coins</h2>
    <p class="muted">Watch ads to earn coins</p>

    <div class="card">
      <button class="btn" id="claimCoin">
        Watch Ad & Get 1 Coin
      </button>
    </div>

    <div class="card">
      <div class="muted">Balance</div>
      <div id="c" style="font-size:1.4rem;font-weight:900">
        ${Number(state.coin).toFixed(2)} ⭐
      </div>
    </div>
  `;

  document.getElementById('claimCoin').addEventListener('click', rewardWithPopup);
}

/***********************
 * BOT PAIRING (FIXED)
 ***********************/
async function onPairClick() {
  const phone = document.getElementById('phone').value.trim();
  if (phone.length < 5) return alert("Invalid number");

  // Open ad (required by Adsterra)
  if (!openAdsterraPopup()) return;

  openModal(`<div class="spinner"></div><p>Processing pairing...</p>`);

  try {
    const res = await fetch("/pair", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCSRFToken(),
      },
      credentials: "same-origin",
      body: JSON.stringify({ number: phone }),
    });

    const data = await res.json();

    if (!res.ok) throw new Error(data.message || "Pairing failed");

    state.session = { number: data.number };
    state.coin = data.coins;
    updateSidebarWidgets();

    openModal(`
      <h3>Pairing Code</h3>
      <div style="font-size:1.6rem;font-weight:900">${data.code}</div>
      <button class="btn" onclick="closeModal()">Close</button>
    `);

  } catch (err) {
    openModal(`
      <h3>Error</h3>
      <p>${err.message}</p>
      <button class="btn" onclick="closeModal()">Close</button>
    `);
  }
}

/***********************
 * COIN REWARD (IMPROVED UX)
 ***********************/
let rewardCooldown = false;

async function rewardWithPopup() {
  if (rewardCooldown) return;
  rewardCooldown = true;

  if (!openAdsterraPopup()) {
    rewardCooldown = false;
    return;
  }

  openModal(`<div class="spinner"></div><p>Verifying ad...</p>`);

  try {
    const res = await fetch("/api/coins/add/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCSRFToken(),
      },
      credentials: "same-origin",
      body: JSON.stringify({ amount: 1 }),
    });

    const data = await res.json();

    if (data.status === "limit") {
      // User reached the daily limit
      const nextTime = new Date(data.reset_at); // Expect backend sends ISO date
      const now = new Date();
      const diffMs = nextTime - now;

      const hours = Math.floor(diffMs / 1000 / 60 / 60);
      const minutes = Math.floor((diffMs / 1000 / 60) % 60);

      openModal(`
        <h3>⚠️ Daily Limit Reached</h3>
        <p>You have collected the maximum coins for today.</p>
        <p>Next collect available in <strong>${hours}h ${minutes}m</strong>.</p>
        <button class="btn" onclick="closeModal()">OK</button>
      `);

    } else if (data.status === "ok") {
      // Successful coin addition
      state.coin = data.coins;
      document.getElementById("c").textContent =
        Number(state.coin).toFixed(2) + " ⭐";
      coinBalance.textContent = Number(state.coin).toFixed(2);

      openModal(`
        <h3>✅ Coin Added</h3>
        <p>You earned <strong>+1 coin</strong></p>
        <button class="btn" onclick="closeModal()">Nice</button>
      `);
    }

  } catch (err) {
    openModal(`<p>Failed to credit coin</p>`);
    console.error(err);
  }

  setTimeout(() => rewardCooldown = false, 4000);
}

/***********************
 * ADSTERra POPUP
 ***********************/
function openAdsterraPopup() {
  const adUrl =
    "https://www.effectivegatecpm.com/jttieru3se?key=13e5c20050d5773e0f1284e77814f6cc";

  const win = window.open(adUrl, "_blank");
  if (!win) {
    alert("Please allow popups to continue.");
    return false;
  }
  return true;
}

/***********************
 * CSRF
 ***********************/
function getCSRFToken() {
  return document.cookie
    .split("; ")
    .find(row => row.startsWith("csrftoken="))
    ?.split("=")[1];
}

/***********************
 * INIT
 ***********************/
(function init() {
  setActiveNav('bot');
  renderSection('bot');
  updateSidebarWidgets();

  modal.addEventListener('click', e => {
    if (e.target === modal) closeModal();
  });
})();
