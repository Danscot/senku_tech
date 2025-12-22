document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("signupForm");

  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const username = document.getElementById("username").value.trim();
    const password = document.getElementById("password").value.trim();
    const password2 = document.getElementById("password2").value.trim();
    const email = document.getElementById("email").value.trim();

    if (password != password2) {
      alert("password Not Matching");
      return;
    }

    try {
      const response = await fetch("/api/signin/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCSRFToken(),
        },
        body: JSON.stringify({
          username: username,
          password: password,
          email: email
        }),
        credentials: "same-origin", // VERY IMPORTANT
      });

      const data = await response.json();

      if (data.status === "created") {
        // ✅ Redirect after successful login
        window.location.href = "dashboard";

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
