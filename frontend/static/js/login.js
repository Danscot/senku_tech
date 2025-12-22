document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("loginForm");

  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const username = document.getElementById("username").value.trim();
    const password = document.getElementById("password").value.trim();

    if (!username || !password) {
      alert("Please fill in all fields");
      return;
    }

    try {
      const response = await fetch("/api/login/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCSRFToken(),
        },
        body: JSON.stringify({
          username: username,
          password: password,
        }),
        credentials: "same-origin", // VERY IMPORTANT
      });

      const data = await response.json();

      if (data.status === "ok") {
        // ✅ Redirect after successful login
        window.location.href = "dashboard/";

      } else {

        alert(data.message || "Invalid username or password");
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
