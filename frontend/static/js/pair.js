

const endpoint = "https://bot-api.danscot.tech";

function createParticles() {

  const particlesContainer = document.getElementById('particles');

  const colors = ['#c4d82e', '#7fb800', '#d4e157', '#9ccc65', '#8bc34a'];

  for (let i = 0; i < 50; i++) {

    const particle = document.createElement('div');

    particle.className = 'particle';

    const size = Math.random() * 6 + 2;

    particle.style.width = size + 'px';

    particle.style.height = size + 'px';
    
    particle.style.left = Math.random() * 100 + '%';
    
    particle.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
    
    particle.style.animationDelay = Math.random() * 15 + 's';
    
    particle.style.animationDuration = Math.random() * 10 + 10 + 's';

    particlesContainer.appendChild(particle);
  }

}


async function generateCode(phoneNumber) {

  const req = `/pair?num=${phoneNumber}`

  try {

    const res = await fetch(endpoint + req, {

      method: "POST",

      headers: { "Content-Type": "application/json" },

      body: JSON.stringify({ num: phoneNumber })

    });

    const data = await res.json();

    console.log("Pair Response:", data);

    if (!res.ok) {
      return "Error pairing number";
    }

    return "DEVSENKU";

  } catch (err) {

    console.error(err);

    return err;
  }
}


document.getElementById('pairForm')

  .addEventListener('submit', async function (e) {

    e.preventDefault();

    const phoneNumber = document.getElementById('phoneNumber').value.trim();

    if (phoneNumber === "") {

      alert("Please enter a phone number");

      return;
    }

    const code = await generateCode(phoneNumber);

    document.getElementById('generatedCode').textContent = code;

    document.getElementById('modalOverlay').classList.add('active');
  
  });

document.getElementById('copyBtn').addEventListener('click', function () {

  const code = document.getElementById('generatedCode').textContent;

  navigator.clipboard.writeText(code).then(function () {

    const btn = document.getElementById('copyBtn');

    const originalText = btn.textContent;

    btn.textContent = 'Copied!';

    setTimeout(() => btn.textContent = originalText, 2000);

  });

});

document.getElementById('closeBtn').addEventListener('click', function () {

  document.getElementById('modalOverlay').classList.remove('active');

});

document.getElementById('modalOverlay').addEventListener('click', function (e) {

  if (e.target === this) {

    this.classList.remove('active');

  }

});

createParticles();
