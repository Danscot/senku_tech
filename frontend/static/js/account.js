// Burger menu
const burger = document.getElementById('burger');
const mobileNav = document.getElementById('mobileNav');
const mobileClose = document.getElementById('mobileClose');

burger?.addEventListener('click', () => {
  burger.classList.toggle('open');
  mobileNav.classList.toggle('active');
});

mobileClose?.addEventListener('click', () => {
  burger.classList.remove('open');
  mobileNav.classList.remove('active');
});

// Bot expiration status
const botExp = "{{ bot_exp|default:'' }}";
if (botExp === "" || botExp === "None") {
  const dot = document.getElementById('dot');
  if (dot) dot.style.background = 'red';
}
