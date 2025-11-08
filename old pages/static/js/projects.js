// Projects Page Specific JavaScript

// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
  // Initialize projects page specific functionality
  initProjectFilters();
  initProjectSearch();
  initPagination();
  initProjectAnimations();
});

// Project filtering functionality
function initProjectFilters() {
  const filterTags = document.querySelectorAll('.filter-tag');
  if (!filterTags.length) return;
  
  filterTags.forEach(tag => {
    tag.addEventListener('click', function() {
      // Toggle active state
      filterTags.forEach(t => {
        t.classList.remove('active');
        t.setAttribute('aria-pressed', 'false');
      });
      
      this.classList.add('active');
      this.setAttribute('aria-pressed', 'true');
      
      // Filter projects based on selected tag
      const filterValue = this.textContent.trim().toLowerCase();
      filterProjects(filterValue === 'all projects' ? '' : filterValue);
    });
  });
}

// Project search functionality
function initProjectSearch() {
  const searchInput = document.querySelector('.search-input');
  if (!searchInput) return;
  
  // Debounced search
  const debouncedSearch = debounce(function(e) {
    const searchTerm = e.target.value.toLowerCase();
    filterProjects(searchTerm);
  }, 300);
  
  searchInput.addEventListener('input', debouncedSearch);
}

// Filter projects based on search term or filter tag
function filterProjects(filterTerm) {
  const projectCards = document.querySelectorAll('.project-card');
  let visibleCount = 0;
  
  projectCards.forEach(card => {
    const title = card.querySelector('.project-title')?.textContent.toLowerCase() || '';
    const description = card.querySelector('.project-description')?.textContent.toLowerCase() || '';
    const tags = Array.from(card.querySelectorAll('.project-tag')).map(tag => tag.textContent.toLowerCase());
    
    const matchesSearch = !filterTerm || 
      title.includes(filterTerm) || 
      description.includes(filterTerm) || 
      tags.some(tag => tag.includes(filterTerm));
    
    if (matchesSearch) {
      card.style.display = 'block';
      visibleCount++;
    } else {
      card.style.display = 'none';
    }
  });
  
  // Show no results message if needed
  updateNoResultsMessage(visibleCount);
  
  // Show loading state briefly
  if (filterTerm) {
    showLoading();
    setTimeout(hideLoading, 500);
  }
}

// Update no results message
function updateNoResultsMessage(count) {
  let noResultsMsg = document.getElementById('no-results');
  
  if (count === 0) {
    if (!noResultsMsg) {
      noResultsMsg = document.createElement('div');
      noResultsMsg.id = 'no-results';
      noResultsMsg.className = 'no-results';
      noResultsMsg.innerHTML = `
        <h3>No projects found</h3>
        <p>Try adjusting your filters or search terms.</p>
      `;
      noResultsMsg.style.cssText = `
        text-align: center;
        padding: 3rem 1rem;
        grid-column: 1 / -1;
      `;
      
      const container = document.querySelector('.projects-grid');
      container.appendChild(noResultsMsg);
    }
  } else if (noResultsMsg) {
    noResultsMsg.remove();
  }
}

// Pagination functionality
function initPagination() {
  const pageButtons = document.querySelectorAll('.page-btn');
  if (!pageButtons.length) return;
  
  pageButtons.forEach(button => {
    button.addEventListener('click', function() {
      if (this.disabled) return;
      
      // Remove active state from all buttons
      pageButtons.forEach(btn => {
        btn.classList.remove('active');
        btn.removeAttribute('aria-current');
      });
      
      // Add active state to clicked button
      this.classList.add('active');
      this.setAttribute('aria-current', 'page');
      
      // Show loading state
      showLoading();
      
      // Simulate page loading
      setTimeout(() => {
        hideLoading();
        // In a real implementation, this would load new projects
        console.log('Loading projects for page:', this.textContent);
        
        // Scroll to top of projects grid
        document.querySelector('.projects-grid').scrollIntoView({ 
          behavior: 'smooth', 
          block: 'start' 
        });
      }, 800);
    });
  });
}

// Project animations
function initProjectAnimations() {
  const projectCards = document.querySelectorAll('.project-card');
  if (!projectCards.length) return;
  
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry, index) => {
      if (entry.isIntersecting) {
        setTimeout(() => {
          entry.target.style.opacity = '1';
          entry.target.style.transform = 'translateY(0)';
        }, index * 100);
      }
    });
  }, { threshold: 0.1 });
  
  projectCards.forEach(card => {
    card.style.opacity = '0';
    card.style.transform = 'translateY(20px)';
    card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
    observer.observe(card);
  });
}
