// ===== Mobile Menu Toggle =====
const menuToggle = document.getElementById("menu-toggle");
const navLinks = document.querySelector(".nav-links");

menuToggle.addEventListener("click", () => {
  navLinks.classList.toggle("show");
});

// ===== Smooth Scroll =====
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function (e) {
    const target = document.querySelector(this.getAttribute('href'));
    if (target) {
      e.preventDefault();
      target.scrollIntoView({ behavior: 'smooth' });
      navLinks.classList.remove("show");
    }
  });
});

// ===== Scroll Navbar Effect =====
window.addEventListener("scroll", () => {
  const nav = document.querySelector(".navbar");
  if (window.scrollY > 60) {
    nav.style.background = "rgba(255,255,255,0.15)";
    nav.style.backdropFilter = "blur(12px)";
    nav.style.borderBottom = "1px solid rgba(255,255,255,0.3)";
  } else {
    nav.style.background = "rgba(255,255,255,0.1)";
    nav.style.borderBottom = "1px solid rgba(255,255,255,0.2)";
  }
});
