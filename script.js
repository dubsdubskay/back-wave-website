// Mobile nav toggle
const navToggle = document.querySelector(".nav-toggle");
const mainNav = document.querySelector(".main-nav");

if (navToggle && mainNav) {
  navToggle.addEventListener("click", () => {
    mainNav.classList.toggle("open");
  });

  // Close menu when clicking a link (mobile)
  mainNav.addEventListener("click", (e) => {
    if (e.target.tagName === "A") {
      mainNav.classList.remove("open");
    }
  });
}

// Hero capability toggle buttons -> highlight corresponding pillar card
const heroToggles = document.querySelectorAll(".hero-toggle");
const pillarCards = document.querySelectorAll(".pillar-card");
const pillarsSection = document.getElementById("pillars");

if (heroToggles.length && pillarCards.length && pillarsSection) {
  heroToggles.forEach((btn) => {
    btn.addEventListener("click", (event) => {
      event.preventDefault(); // Prevent default #pillars jump

      const targetId = btn.getAttribute("data-target");

      // Update button styles (primary vs ghost)
      heroToggles.forEach((b) => {
        if (b === btn) {
          b.classList.add("btn-primary");
          b.classList.remove("btn-ghost");
        } else {
          b.classList.remove("btn-primary");
          b.classList.add("btn-ghost");
        }
      });

      // Highlight matching pillar card
      pillarCards.forEach((card) => {
        const pillarId = card.getAttribute("data-pillar");
        card.classList.toggle("active", pillarId === targetId);
      });

      // Smooth scroll so cards come into view but toggles remain visible
      const rect = pillarsSection.getBoundingClientRect();
      const offset =160; // Adjust this value as needed px of hero to keep in view
      const targetY = window.scrollY + rect.top - offset;

      window.scrollTo({
        top: targetY,
        behavior: 'smooth'
      });

    });
  });
}

// Past Performance tabs
const tabButtons = document.querySelectorAll(".tab-button");
const tabPanels = document.querySelectorAll(".tab-panel");

if (tabButtons.length && tabPanels.length) {
  tabButtons.forEach((button) => {
    button.addEventListener("click", () => {
      const targetPanel = button.getAttribute("data-tab-target");

      // Update active button
      tabButtons.forEach((btn) => {
        btn.classList.toggle("active", btn === button);
      });

      // Update active panel
      tabPanels.forEach((panel) => {
        const panelId = panel.getAttribute("data-tab-panel");
        panel.classList.toggle("active", panelId === targetPanel);
      });
    });
  });
}

// Past Performance carousels (lazy-susan style)
const carousels = document.querySelectorAll(".project-carousel");

carousels.forEach((carousel) => {
  const track = carousel.querySelector(".carousel-track");
  const prev = carousel.querySelector(".carousel-arrow.prev");
  const next = carousel.querySelector(".carousel-arrow.next");

  if (!track || !prev || !next) return;

  const getScrollAmount = () => track.clientWidth * 0.9;

  prev.addEventListener("click", () => {
    track.scrollBy({
      left: -getScrollAmount(),
      behavior: "smooth",
    });
  });

  next.addEventListener("click", () => {
    track.scrollBy({
      left: getScrollAmount(),
      behavior: "smooth",
    });
  });
});


// Footer year
const yearSpan = document.getElementById("year");
if (yearSpan) {
  yearSpan.textContent = new Date().getFullYear();
}
