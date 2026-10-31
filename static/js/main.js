/**
 * main.js – Sweet Cravings Client-Side JavaScript
 * ─────────────────────────────────────────────────
 * Handles:
 *   • Cart quantity controls
 *   • Search & filter live feedback
 *   • Image gallery / lightbox helper
 *   • Flash message auto-dismiss
 *   • Cake size/flavour selection price display
 */

/* ── Auto-dismiss flash alerts after 4 seconds ─────────────────── */
document.addEventListener('DOMContentLoaded', function () {

  const alerts = document.querySelectorAll('.alert-auto-dismiss');
  alerts.forEach(function (alert) {
    setTimeout(function () {
      const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
      if (bsAlert) bsAlert.close();
    }, 4000);
  });

  /* ── Cart quantity stepper ─────────────────────────────────────── */
  // Increase quantity
  document.querySelectorAll('.qty-increase').forEach(function (btn) {
    btn.addEventListener('click', function () {
      const input = this.closest('.qty-group').querySelector('.qty-input');
      input.value = parseInt(input.value) + 1;
    });
  });

  // Decrease quantity (min = 1)
  document.querySelectorAll('.qty-decrease').forEach(function (btn) {
    btn.addEventListener('click', function () {
      const input = this.closest('.qty-group').querySelector('.qty-input');
      const current = parseInt(input.value);
      if (current > 1) input.value = current - 1;
    });
  });

  /* ── Cake detail page: update price display when size changes ───── */
  const sizeSelect    = document.getElementById('size-select');
  const priceDisplay  = document.getElementById('price-display');
  const basePriceElem = document.getElementById('base-price');

  if (sizeSelect && priceDisplay && basePriceElem) {
    const basePrice = parseFloat(basePriceElem.dataset.price);

    // Price multipliers per size (adjust as needed)
    const sizeMultiplier = {
      '0.5kg': 0.6,
      '1kg':   1.0,
      '1.5kg': 1.4,
      '2kg':   1.8,
      '3kg':   2.5,
      '4kg':   3.2,
      '5kg':   4.0
    };

    sizeSelect.addEventListener('change', function () {
      const multiplier = sizeMultiplier[this.value] || 1.0;
      const newPrice   = (basePrice * multiplier).toFixed(2);
      priceDisplay.textContent = '₹' + newPrice;
    });
  }

  /* ── Search box – highlight empty search ───────────────────────── */
  const searchForm  = document.getElementById('search-form');
  const searchInput = document.getElementById('search-input');

  if (searchForm && searchInput) {
    searchForm.addEventListener('submit', function (e) {
      if (searchInput.value.trim() === '') {
        // Allow empty to reset – don't block
      }
    });
  }

  /* ── Animate stat numbers (counting up) on home page ───────────── */
  const statNumbers = document.querySelectorAll('.stat-number[data-target]');
  if (statNumbers.length > 0) {
    const observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          const target  = parseInt(entry.target.dataset.target);
          const suffix  = entry.target.dataset.suffix || '';
          animateCount(entry.target, 0, target, 1500, suffix);
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.5 });

    statNumbers.forEach(function (el) { observer.observe(el); });
  }

  function animateCount(el, start, end, duration, suffix) {
    const range     = end - start;
    const startTime = performance.now();

    function step(now) {
      const elapsed  = now - startTime;
      const progress = Math.min(elapsed / duration, 1);
      const value    = Math.floor(start + range * easeOut(progress));
      el.textContent = value.toLocaleString() + suffix;
      if (progress < 1) requestAnimationFrame(step);
    }

    requestAnimationFrame(step);
  }

  function easeOut(t) { return 1 - Math.pow(1 - t, 3); }

  /* ── Admin: confirm before deleting a cake ─────────────────────── */
  document.querySelectorAll('.confirm-delete').forEach(function (form) {
    form.addEventListener('submit', function (e) {
      if (!confirm('Are you sure you want to delete this cake? This cannot be undone.')) {
        e.preventDefault();
      }
    });
  });

  /* ── Image preview before upload (admin add/edit cake) ─────────── */
  const imgInput   = document.getElementById('cake-image-input');
  const imgPreview = document.getElementById('img-preview');

  if (imgInput && imgPreview) {
    imgInput.addEventListener('change', function () {
      const file = this.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = function (e) {
          imgPreview.src = e.target.result;
          imgPreview.style.display = 'block';
        };
        reader.readAsDataURL(file);
      }
    });
  }

  /* ── Smooth scroll for anchor links ────────────────────────────── */
  document.querySelectorAll('a[href^="#"]').forEach(function (a) {
    a.addEventListener('click', function (e) {
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });

  /* ── Mobile navbar collapse on link click ───────────────────────── */
  const navbarCollapse = document.querySelector('.navbar-collapse');
  document.querySelectorAll('.nav-link').forEach(function (link) {
    link.addEventListener('click', function () {
      if (navbarCollapse && navbarCollapse.classList.contains('show')) {
        const toggler = document.querySelector('.navbar-toggler');
        if (toggler) toggler.click();
      }
    });
  });

});
