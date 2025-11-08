// Shared JavaScript functionality for SEVO website

// Initialize shared functionality
document.addEventListener('DOMContentLoaded', function() {
    // Mobile menu toggle
    initMobileMenu();
    
    // Smooth scrolling for anchor links
    initSmoothScroll();
    
    // Year update in footer
    updateYear();
    
    // Scroll effects
    initScrollEffects();
    
    // Floating navbar
    initFloatingNavbar();
});

// Mobile menu functionality
function initMobileMenu() {
    const mobileToggle = document.querySelector('.mobile-menu-toggle');
    const navActions = document.querySelector('.nav-actions');
    
    if (!mobileToggle || !navActions) return;
    
    // Toggle mobile menu
    mobileToggle.addEventListener('click', function() {
        navActions.classList.toggle('mobile-open');
        mobileToggle.classList.toggle('active');
        
        // Prevent body scroll when menu is open
        if (navActions.classList.contains('mobile-open')) {
            document.body.style.overflow = 'hidden';
        } else {
            document.body.style.overflow = '';
        }
    });
    
    // Close mobile menu when clicking outside
    document.addEventListener('click', function(e) {
        if (!navActions.contains(e.target) && !mobileToggle.contains(e.target)) {
            navActions.classList.remove('mobile-open');
            mobileToggle.classList.remove('active');
            document.body.style.overflow = '';
        }
    });
    
    // Close mobile menu when clicking on a link
    const navLinks = navActions.querySelectorAll('a');
    navLinks.forEach(link => {
        link.addEventListener('click', function() {
            navActions.classList.remove('mobile-open');
            mobileToggle.classList.remove('active');
            document.body.style.overflow = '';
        });
    });
}

// Smooth scrolling for anchor links
function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Update year in footer
function updateYear() {
    const yearElement = document.getElementById('year');
    if (yearElement) {
        yearElement.textContent = new Date().getFullYear();
    }
}

// Scroll effects (header shadow, animations, etc.)
function initScrollEffects() {
    const header = document.querySelector('header');
    if (!header) return;
    
    let lastScroll = 0;
    
    window.addEventListener('scroll', function() {
        const currentScroll = window.pageYOffset;
        
        // Add shadow to header on scroll
        if (currentScroll > 10) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
        
        lastScroll = currentScroll;
    });
}

// Floating navbar functionality
function initFloatingNavbar() {
    const header = document.getElementById('main-header');
    if (!header) return;
    
    // Add padding to body to account for fixed header
    const headerHeight = header.offsetHeight;
    document.body.style.paddingTop = headerHeight + 'px';
    
    // Handle scroll events
    let lastScrollY = window.scrollY;
    let ticking = false;
    
    function updateNavbar() {
        const scrollY = window.scrollY;
        
        if (scrollY > 50) {
            header.classList.add('floating');
        } else {
            header.classList.remove('floating');
        }
        
        lastScrollY = scrollY;
        ticking = false;
    }
    
    function requestTick() {
        if (!ticking) {
            window.requestAnimationFrame(updateNavbar);
            ticking = true;
        }
    }
    
    window.addEventListener('scroll', requestTick);
    
    // Update header height on window resize
    window.addEventListener('resize', function() {
        const newHeaderHeight = header.offsetHeight;
        document.body.style.paddingTop = newHeaderHeight + 'px';
    });
}

// Utility functions
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Throttle function for scroll events
function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    }
}

// Animate elements on scroll
function animateOnScroll() {
    const elements = document.querySelectorAll('.animate-on-scroll');
    
    elements.forEach(element => {
        const elementTop = element.getBoundingClientRect().top;
        const elementBottom = element.getBoundingClientRect().bottom;
        
        if (elementTop < window.innerHeight && elementBottom > 0) {
            element.classList.add('animated');
        }
    });
}

// Initialize scroll animations
window.addEventListener('scroll', throttle(animateOnScroll, 100));

// Form validation helper
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

function validateRequired(fields) {
    let isValid = true;
    fields.forEach(field => {
        if (!field.value.trim()) {
            field.classList.add('error');
            isValid = false;
        } else {
            field.classList.remove('error');
        }
    });
    return isValid;
}

// AJAX helper function
function ajaxRequest(url, options = {}) {
    const defaults = {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest'
        }
    };
    
    const config = { ...defaults, ...options };
    
    return fetch(url, config)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .catch(error => {
            console.error('AJAX Error:', error);
            throw error;
        });
}

// Loading states
function showLoading(element) {
    element.classList.add('loading');
    element.disabled = true;
}

function hideLoading(element) {
    element.classList.remove('loading');
    element.disabled = false;
}

// Notification system
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    // Auto remove after 3 seconds
    setTimeout(() => {
        notification.classList.add('fade-out');
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 3000);
}

// Export functions for use in page-specific scripts
window.SEVO = {
    ajaxRequest,
    showNotification,
    showLoading,
    hideLoading,
    validateEmail,
    validateRequired,
    debounce,
    throttle
};
