// Transparency Page Specific JavaScript

// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
  // Initialize transparency page specific functionality
  initMetricAnimations();
  initReportDownloads();
  initImpactAnimations();
});

// Animate metrics numbers
function initMetricAnimations() {
  const metricNumbers = document.querySelectorAll('.metric-card .number');
  if (!metricNumbers.length) return;

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        animateMetricNumber(entry.target);
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.5 });

  metricNumbers.forEach(number => observer.observe(number));
}

function animateMetricNumber(element) {
  const text = element.textContent;
  const match = text.match(/([0-9.,+]+)/);
  if (!match) return;

  const targetText = match[1];
  const prefix = text.substring(0, text.indexOf(targetText));
  const suffix = text.substring(text.indexOf(targetText) + targetText.length);
  
  // Parse the numeric value
  let targetValue;
  if (targetText.includes('.')) {
    targetValue = parseFloat(targetText.replace(/[^0-9.]/g, ''));
  } else {
    targetValue = parseInt(targetText.replace(/[^0-9]/g, ''));
  }
  
  let currentValue = 0;
  const increment = targetValue / 60; // 60 frames for ~1 second animation
  const isDecimal = targetText.includes('.');
  
  const timer = setInterval(() => {
    currentValue += increment;
    if (currentValue >= targetValue) {
      currentValue = targetValue;
      clearInterval(timer);
    }
    
    if (isDecimal) {
      element.textContent = prefix + currentValue.toFixed(1) + suffix;
    } else {
      element.textContent = prefix + Math.floor(currentValue).toLocaleString() + suffix;
    }
  }, 16);
}

// Report download functionality
function initReportDownloads() {
  const reportLinks = document.querySelectorAll('.reports-list a');
  if (!reportLinks.length) return;

  reportLinks.forEach(link => {
    link.addEventListener('click', function(e) {
      e.preventDefault();
      
      const reportName = this.textContent.trim();
      
      // Show loading state
      const originalText = this.textContent;
      this.textContent = 'Downloading...';
      this.style.color = '#999';
      
      // Simulate download
      setTimeout(() => {
        // Reset link state
        this.textContent = originalText;
        this.style.color = '';
        
        // Show success message
        alert(`Downloaded: ${reportName}`);
        console.log(`Downloaded report: ${reportName}`);
        
        // In a real implementation, this would trigger an actual download
        // window.open(this.href, '_blank');
      }, 1500);
    });
  });
}

// Impact list animations
function initImpactAnimations() {
  const impactItems = document.querySelectorAll('.impact-list li');
  if (!impactItems.length) return;

  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry, index) => {
      if (entry.isIntersecting) {
        setTimeout(() => {
          entry.target.style.opacity = '1';
          entry.target.style.transform = 'translateX(0)';
        }, index * 150);
      }
    });
  }, { threshold: 0.2 });

  impactItems.forEach((item, index) => {
    // Set initial state
    item.style.opacity = '0';
    item.style.transform = 'translateX(-30px)';
    item.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    
    observer.observe(item);
  });
}
