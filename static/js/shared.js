// Shared JavaScript functionality for SEVO website

(function() {
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

    // Mobile menu functionality with proper event cleanup
    function initMobileMenu() {
        const navLinks = document.querySelector('.nav-links');
        const mobileToggle = document.querySelector('.mobile-menu-toggle');
        
        if (!navLinks || !mobileToggle) return;
        
        const toggleMobileMenu = function() {
            navLinks.classList.toggle('mobile-open');
            mobileToggle.classList.toggle('active');
            document.body.style.overflow = navLinks.classList.contains('mobile-open') ? 'hidden' : '';
        };
        
        const closeMobileMenu = function() {
            navLinks.classList.remove('mobile-open');
            mobileToggle.classList.remove('active');
            document.body.style.overflow = '';
        };
        
        mobileToggle.addEventListener('click', toggleMobileMenu);
        
        navLinks.addEventListener('click', function(e) {
            if (e.target.tagName === 'A') {
                closeMobileMenu();
            }
        });
        
        const outsideClickHandler = function(e) {
            if (!navLinks.contains(e.target) && !mobileToggle.contains(e.target) && navLinks.classList.contains('mobile-open')) {
                closeMobileMenu();
            }
        };
        
        const escapeKeyHandler = function(e) {
            if (e.key === 'Escape' && navLinks.classList.contains('mobile-open')) {
                closeMobileMenu();
            }
        };
        
        document.addEventListener('click', outsideClickHandler);
        document.addEventListener('keydown', escapeKeyHandler);
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
    function initHeaderBehavior() {
        const navbar = document.querySelector('.floating-navbar');
        if (!navbar) return;

        let lastScroll = 0;
        const scrollThreshold = 80;
        let ticking = false;

        function updateHeaderHeight() {
            const height = navbar.offsetHeight;
            document.documentElement.style.setProperty('--header-height', `${height}px`);
        }

        function updateHeader() {
            const currentScroll = window.pageYOffset;

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

        function onScroll() {
            if (!ticking) {
                requestAnimationFrame(updateHeader);
                ticking = true;
            }
        }

        updateHeaderHeight();
        updateHeader();

        window.addEventListener('scroll', onScroll, { passive: true });
        window.addEventListener('resize', debounce(updateHeaderHeight, 250));
    }

    // Initialize all shared functionality on DOMContentLoaded
    document.addEventListener('DOMContentLoaded', function() {
        initMobileMenu();
        initSmoothScroll();
        updateYear();
        initHeaderBehavior();
    });

})();
