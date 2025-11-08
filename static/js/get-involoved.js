// Get Involved Page Specific JavaScript

// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
  // Initialize get involved page specific functionality
  initFormTabs();
  initDonationFormLogic();
  initVolunteerForm();
  initPartnerForm();
});

// Form tab functionality
function initFormTabs() {
  const tabs = document.querySelectorAll('.tab-button');
  const forms = document.querySelectorAll('.form-section');
  
  // Function to show correct form based on tab
  function showForm(formId) {
    forms.forEach(form => {
      form.classList.remove('active');
    });
    tabs.forEach(tab => {
      tab.classList.remove('active');
    });

    const targetForm = document.getElementById('form-' + formId);
    if (targetForm) {
      targetForm.classList.add('active');
    }
    
    const targetTab = document.querySelector(`.tab-button[data-form="${formId}"]`);
    if (targetTab) {
      targetTab.classList.add('active');
    }
  }

  // Add click listeners to tabs
  tabs.forEach(tab => {
    tab.addEventListener('click', function() {
      showForm(this.dataset.form);
    });
  });
  
  // Set initial state
  showForm('donate');
}

// Donation form logic
function initDonationFormLogic() {
  // --- Bank Info Object ---
  const bankInfo = {
    "Bank of Khartoum": {
      name: "SEVO Organization",
      number: "1234-5678-9012-3456"
    },
    "Faisal Islamic Bank": {
      name: "SEVO Organization",
      number: "9876-5432-1098-7654"
    },
    "Omdurman National Bank": {
      name: "SEVO Organization",
      number: "1111-2222-3333-4444"
    },
    "Al Baraka Bank": {
      name: "SEVO Organization",
      number: "5555-6666-7777-8888"
    },
    "Bank of Sudan": {
      name: "SEVO Organization",
      number: "9999-0000-1111-2222"
    }
  };
  
  const donationTypeRadios = document.querySelectorAll('input[name="donation_type"]');
  const internationalFields = document.getElementById('international-fields');
  const localFields = document.getElementById('local-fields');
  const bankRadios = document.querySelectorAll('input[name="bank"]');
  const bankDetailsBox = document.getElementById('bank-details-box');
  const fileInput = document.getElementById('payment_proof');
  const fileLabel = document.getElementById('file-label');
  const fileName = document.getElementById('file-name');
  const otherAmountRadio = document.getElementById('amount_other');
  const otherAmountWrapper = document.getElementById('other-amount-wrapper');
  const otherAmountInput = document.getElementById('other_amount_input');

  // Listen for change on Donation Type
  donationTypeRadios.forEach(radio => {
    radio.addEventListener('change', function() {
      if (this.value === 'international') {
        internationalFields.style.display = 'block';
        localFields.style.display = 'none';
      } else {
        internationalFields.style.display = 'none';
        localFields.style.display = 'block';
      }
    });
  });

  // Listen for change on Bank selection
  bankRadios.forEach(radio => {
    radio.addEventListener('change', function() {
      const selectedBank = this.value;
      const details = bankInfo[selectedBank];
      if (details) {
        bankDetailsBox.innerHTML = `
          <h3>${selectedBank}</h3>
          <p><strong>Account Name:</strong> ${details.name}</p>
          <p><strong>Account Number:</strong> ${details.number}</p>
        `;
        bankDetailsBox.style.display = 'block';
      }
    });
  });

  // Listen for change on File Input
  if (fileInput) {
    fileInput.addEventListener('change', function() {
      if (this.files.length > 0) {
        fileLabel.style.display = 'none';
        fileName.textContent = this.files[0].name;
      } else {
        fileLabel.style.display = 'block';
        fileName.textContent = '';
      }
    });
  }
  
  // Show/hide "Other Amount" input
  if (otherAmountRadio && otherAmountWrapper) {
    const amountRadios = document.querySelectorAll('input[name="amount"]');
    
    amountRadios.forEach(radio => {
      radio.addEventListener('change', function() {
        if (otherAmountRadio.checked) {
          otherAmountWrapper.style.display = 'block';
          if (otherAmountInput) otherAmountInput.focus();
        } else {
          otherAmountWrapper.style.display = 'none';
        }
      });
    });
  }

  // Trigger radio change for default view
  const checkedDonationType = document.querySelector('input[name="donation_type"]:checked');
  if (checkedDonationType) {
    checkedDonationType.dispatchEvent(new Event('change'));
  }
}

// Volunteer form functionality
function initVolunteerForm() {
  const volunteerForm = document.getElementById('form-volunteer');
  if (!volunteerForm) return;
  
  volunteerForm.addEventListener('submit', function(e) {
    e.preventDefault();
    
    const name = document.getElementById('volt_name')?.value.trim();
    const email = document.getElementById('volt_email')?.value.trim();
    const phone = document.getElementById('volt_phone')?.value.trim();
    const message = document.getElementById('volt_message')?.value.trim();
    
    // Basic validation
    if (!name || !email || !message) {
      alert('Please fill in all required fields.');
      return;
    }
    
    if (!validateEmail(email)) {
      alert('Please enter a valid email address.');
      return;
    }
    
    // Show loading state
    const submitButton = this.querySelector('.btn');
    const originalText = submitButton.textContent;
    submitButton.textContent = 'Submitting...';
    submitButton.disabled = true;
    
    // Simulate API call
    setTimeout(() => {
      // Reset form
      this.reset();
      submitButton.textContent = originalText;
      submitButton.disabled = false;
      
      // Show success message
      alert('Thank you for signing up to volunteer! We will contact you soon.');
      console.log('Volunteer signup:', { name, email, phone, message });
    }, 1500);
  });
}

// Partner form functionality
function initPartnerForm() {
  const partnerForm = document.getElementById('form-partner');
  if (!partnerForm) return;
  
  partnerForm.addEventListener('submit', function(e) {
    e.preventDefault();
    
    const orgName = document.getElementById('part_org_name')?.value.trim();
    const contactName = document.getElementById('part_contact_name')?.value.trim();
    const email = document.getElementById('part_email')?.value.trim();
    const message = document.getElementById('part_message')?.value.trim();
    
    // Basic validation
    if (!orgName || !contactName || !email || !message) {
      alert('Please fill in all required fields.');
      return;
    }
    
    if (!validateEmail(email)) {
      alert('Please enter a valid email address.');
      return;
    }
    
    // Show loading state
    const submitButton = this.querySelector('.btn');
    const originalText = submitButton.textContent;
    submitButton.textContent = 'Submitting...';
    submitButton.disabled = true;
    
    // Simulate API call
    setTimeout(() => {
      // Reset form
      this.reset();
      submitButton.textContent = originalText;
      submitButton.disabled = false;
      
      // Show success message
      alert('Thank you for your partnership inquiry! We will contact you soon.');
      console.log('Partner inquiry:', { orgName, contactName, email, message });
    }, 1500);
  });
}
