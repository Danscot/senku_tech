document.addEventListener("DOMContentLoaded", () => {

  const form = document.getElementById("verForm");

  form.addEventListener("submit", async (e) => {

    e.preventDefault();

    const code = document.getElementById("ver").value.trim();

    if (!code) {

      alert("Please fill in all fields");

      return;
    }

    try {

      const response = await fetch("/api/email/ver", {

        method: "POST",

        headers: {

          "Content-Type": "application/json",

          "X-CSRFToken": getCSRFToken(),

        },

        body: JSON.stringify({

          code: code,

        }),
        credentials: "same-origin",

      });

      const data = await response.json();

      if (data.status === "ok") {

        window.location.href = "/account";

      } else {


        window.location.href = "/signup";

        alert(data.message || "Invalid code");

      }
    } catch (error) {
      console.error(error);
      alert("Server error. Please try again.");
    }
  });
});

/* Django CSRF helper */
function getCSRFToken() {
  let cookieValue = null;
  const cookies = document.cookie.split(";");

  for (let cookie of cookies) {
    cookie = cookie.trim();
    if (cookie.startsWith("csrftoken=")) {
      cookieValue = cookie.substring("csrftoken=".length);
      break;
    }
  }
  return cookieValue;
}
