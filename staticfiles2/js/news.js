// News Page Specific JavaScript

// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
  // Initialize news page specific functionality
  initNewsFilters();
  initNewsSearch();
  initPagination();
  initNewsletterForm();
  initNewsAnimations();
});

// News filtering functionality
function initNewsFilters() {
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
      
      // Filter news based on selected tag
      const filterValue = this.textContent.trim().toLowerCase();
      filterNews(filterValue === 'all news' ? '' : filterValue);
    });
  });
}

// News search functionality
function initNewsSearch() {
  const searchInput = document.querySelector('.search-input');
  if (!searchInput) return;
  
  // Debounced search
  const debouncedSearch = debounce(function(e) {
    const searchTerm = e.target.value.toLowerCase();
    filterNews(searchTerm);
  }, 300);
  
  searchInput.addEventListener('input', debouncedSearch);
}

// Filter news based on search term or filter tag
function filterNews(filterTerm) {
  const newsCards = document.querySelectorAll('.news-card');
  let visibleCount = 0;
  
  // Also filter featured article if it exists
  const featuredArticle = document.querySelector('.featured-article');
  if (featuredArticle && filterTerm) {
    const featuredTitle = featuredArticle.querySelector('h2')?.textContent.toLowerCase() || '';
    const featuredContent = featuredArticle.querySelector('p')?.textContent.toLowerCase() || '';
    
    const featuredMatches = featuredTitle.includes(filterTerm) || featuredContent.includes(filterTerm);
    featuredArticle.style.display = featuredMatches ? 'block' : 'none';
  } else if (featuredArticle) {
    featuredArticle.style.display = 'block';
  }
  
  newsCards.forEach(card => {
    const title = card.querySelector('.news-title')?.textContent.toLowerCase() || '';
    const excerpt = card.querySelector('.news-excerpt')?.textContent.toLowerCase() || '';
    const author = card.querySelector('.author-name')?.textContent.toLowerCase() || '';
    const category = card.querySelector('.news-category')?.textContent.toLowerCase() || '';
    
    const matchesSearch = !filterTerm || 
      title.includes(filterTerm) || 
      excerpt.includes(filterTerm) || 
      author.includes(filterTerm) || 
      category.includes(filterTerm);
    
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
        <h3>No news articles found</h3>
        <p>Try adjusting your filters or search terms.</p>
      `;
      noResultsMsg.style.cssText = `
        text-align: center;
        padding: 3rem 1rem;
        grid-column: 1 / -1;
      `;
      
      const container = document.querySelector('.news-grid');
      container.appendChild(noResultsMsg);
    }
  } else if (noResultsMsg) {
    noResultsMsg.remove();
  }
}

// Newsletter form functionality
function initNewsletterForm() {
  const newsletterForm = document.querySelector('.newsletter-form');
  if (!newsletterForm) return;
  
  newsletterForm.addEventListener('submit', function(e) {
    e.preventDefault();
    
    const emailInput = this.querySelector('.newsletter-input');
    const email = emailInput.value.trim();
    
    if (!validateEmail(email)) {
      alert('Please enter a valid email address.');
      return;
    }
    
    // Show loading state
    const submitButton = this.querySelector('.btn-black');
    const originalText = submitButton.textContent;
    submitButton.textContent = 'Subscribing...';
    submitButton.disabled = true;
    
    // Simulate API call
    setTimeout(() => {
      // Reset form
      emailInput.value = '';
      submitButton.textContent = originalText;
      submitButton.disabled = false;
      
      // Show success message
      alert('Thank you for subscribing to our newsletter!');
      console.log('Newsletter subscription for:', email);
    }, 1500);
  });
}

// News animations
function initNewsAnimations() {
  const newsCards = document.querySelectorAll('.news-card');
  const featuredArticle = document.querySelector('.featured-article');
  
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
  
  // Animate featured article first
  if (featuredArticle) {
    featuredArticle.style.opacity = '0';
    featuredArticle.style.transform = 'translateY(20px)';
    featuredArticle.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    observer.observe(featuredArticle);
  }
  
  // Animate news cards
  newsCards.forEach(card => {
    card.style.opacity = '0';
    card.style.transform = 'translateY(20px)';
    card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
    observer.observe(card);
  });
}
