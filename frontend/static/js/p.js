

const endpoint = "https://bot-api.danscot.tech";

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
