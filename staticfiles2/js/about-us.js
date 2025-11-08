// About Us Page Specific JavaScript

// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
  // Initialize about page specific functionality
  initTimelineAnimations();
  initChartAnimations();
});

// Timeline animations
function initTimelineAnimations() {
  const timelineItems = document.querySelectorAll('.timeline-item');
  if (!timelineItems.length) return;

  const observerOptions = {
    threshold: 0.2,
    rootMargin: '0px 0px -50px 0px'
  };

  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry, index) => {
      if (entry.isIntersecting) {
        setTimeout(() => {
          entry.target.style.opacity = '1';
          entry.target.style.transform = 'translateX(0)';
        }, index * 100); // Stagger animation
      }
    });
  }, observerOptions);

  timelineItems.forEach((item, index) => {
    // Set initial state
    item.style.opacity = '0';
    item.style.transform = item.classList.contains('timeline-item:nth-child(even)') 
      ? 'translateX(30px)' 
      : 'translateX(-30px)';
    item.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    
    observer.observe(item);
  });
}

// Chart animations
function initChartAnimations() {
  const chartCards = document.querySelectorAll('.chart-card');
  if (!chartCards.length) return;

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        animateChart(entry.target);
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.5 });

  chartCards.forEach(card => observer.observe(card));
}

function animateChart(chartCard) {
  const pieChart = chartCard.querySelector('.pie-chart');
  const barChart = chartCard.querySelector('.bar-chart');
  
  if (pieChart) {
    // Animate pie chart rotation
    pieChart.style.transform = 'rotate(-90deg)';
    pieChart.style.transition = 'transform 1s ease';
    setTimeout(() => {
      pieChart.style.transform = 'rotate(0deg)';
    }, 100);
  }
  
  if (barChart) {
    // Animate bar charts
    const bars = barChart.querySelectorAll('.bar');
    bars.forEach((bar, index) => {
      const finalHeight = bar.style.height;
      bar.style.height = '0';
      setTimeout(() => {
        bar.style.height = finalHeight;
        bar.style.transition = 'height 0.8s ease';
      }, index * 150);
    });
  }
}
