// Shared JavaScript functionality for SEVO website

// Initialize shared functionality
document.addEventListener('DOMContentLoaded', function() {
    // Mobile menu toggle
    initMobileMenu();
    
    // Smooth scrolling for anchor links
    initSmoothScroll();
    
    // Year update in footer
    updateYear();
    
    // Consolidated header behavior (scroll effects + body padding)
    initHeaderBehavior();
});

// Mobile menu functionality with proper event cleanup
function initMobileMenu() {
    const navLinks = document.querySelector('.nav-links');
    const mobileToggle = document.querySelector('.mobile-menu-toggle');
    const navbar = document.querySelector('.floating-navbar');
    
    if (!navLinks || !mobileToggle) return;
    
    // Toggle mobile menu
    const toggleMobileMenu = function() {
        navLinks.classList.toggle('mobile-open');
        mobileToggle.classList.toggle('active');
        document.body.style.overflow = navLinks.classList.contains('mobile-open') ? 'hidden' : '';
    };
    
    // Close mobile menu
    const closeMobileMenu = function() {
        navLinks.classList.remove('mobile-open');
        mobileToggle.classList.remove('active');
        document.body.style.overflow = '';
    };
    
    // Event listeners
    mobileToggle.addEventListener('click', toggleMobileMenu);
    
    // Close mobile menu when clicking on nav links
    navLinks.addEventListener('click', function(e) {
        if (e.target.tagName === 'A') {
            closeMobileMenu();
        }
    });
    
    // Close mobile menu when clicking outside
    const outsideClickHandler = function(e) {
        if (!navLinks.contains(e.target) && !mobileToggle.contains(e.target) && navLinks.classList.contains('mobile-open')) {
            closeMobileMenu();
        }
    };
    
    // Close mobile menu on escape key
    const escapeKeyHandler = function(e) {
        if (e.key === 'Escape' && navLinks.classList.contains('mobile-open')) {
            closeMobileMenu();
        }
    };
    
    document.addEventListener('click', outsideClickHandler);
    document.addEventListener('keydown', escapeKeyHandler);
    
    // Store cleanup function for potential use in SPAs
    window.SEVO = window.SEVO || {};
    window.SEVO.cleanupMobileMenu = function() {
        mobileToggle.removeEventListener('click', toggleMobileMenu);
        document.removeEventListener('click', outsideClickHandler);
        document.removeEventListener('keydown', escapeKeyHandler);
    };
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

// Consolidated header behavior (scroll effects + body padding)
// Enhanced floating transparent navbar with smooth transitions
function initHeaderBehavior() {
    const navbar = document.querySelector('.floating-navbar');
    if (!navbar) return;

    let lastScroll = 0;
    const scrollThreshold = 80; // Increased threshold for better UX
    let ticking = false;

    // Update header height CSS variable
    function updateHeaderHeight() {
        const height = navbar.offsetHeight;
        document.documentElement.style.setProperty('--header-height', `${height}px`);
    }

    // Combined scroll and padding logic with enhanced smooth transitions
    function updateHeader() {
        const currentScroll = window.pageYOffset;

        // Add scrolled class when user scrolls past threshold
        // This triggers the transparent -> solid background transition
        if (currentScroll > scrollThreshold) {
            if (!navbar.classList.contains('scrolled')) {
                navbar.classList.add('scrolled');
            }
        } else {
            if (navbar.classList.contains('scrolled')) {
                navbar.classList.remove('scrolled');
            }
        }

        lastScroll = currentScroll;
        ticking = false;
    }

    // Optimized scroll handler with RequestAnimationFrame for 60fps smooth scrolling
    function onScroll() {
        if (!ticking) {
            requestAnimationFrame(updateHeader);
            ticking = true;
        }
    }

    // Initialize on page load
    updateHeaderHeight();
    updateHeader();

    // Event listeners with proper cleanup and passive flag for better performance
    window.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('resize', debounce(updateHeaderHeight, 250));

    // Store cleanup function for potential use in SPAs
    window.SEVO = window.SEVO || {};
    window.SEVO.cleanupHeader = function() {
        window.removeEventListener('scroll', onScroll);
        window.removeEventListener('resize', debounce(updateHeaderHeight, 250));
    };
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
