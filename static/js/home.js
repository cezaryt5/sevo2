// Home Page Specific JavaScript

// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
  // Initialize home page specific functionality
  initHomeAnimations();
  initStatsCounters();
});

// Home page animations
function initHomeAnimations() {
  // Animate feature items on scroll
  const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
  };

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.style.opacity = '1';
        entry.target.style.transform = 'translateY(0)';
      }
    });
  }, observerOptions);

  // Observe feature items
  const featureItems = document.querySelectorAll('.feature-item');
  featureItems.forEach(item => {
    item.style.opacity = '0';
    item.style.transform = 'translateY(30px)';
    item.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    observer.observe(item);
  });
}

// Animate statistics numbers
function initStatsCounters() {
  const statsSection = document.querySelector('.statistics');
  if (!statsSection) return;

  const statItems = document.querySelectorAll('.stat-item h3');
  let animated = false;

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting && !animated) {
        animated = true;
        animateCounters(statItems);
      }
    });
  }, { threshold: 0.5 });

  observer.observe(statsSection);
}

function animateCounters(elements) {
  elements.forEach(element => {
    const target = parseInt(element.textContent.replace(/[^0-9]/g, ''));
    const suffix = element.textContent.replace(/[0-9]/g, '');
    let current = 0;
    const increment = target / 50;
    const timer = setInterval(() => {
      current += increment;
      if (current >= target) {
        current = target;
        clearInterval(timer);
      }
      element.textContent = Math.floor(current).toLocaleString() + suffix;
    }, 30);
  });
}
