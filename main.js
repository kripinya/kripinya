// Mouse Glow Effect
const mouseGlow = document.getElementById('mouse-glow');
document.addEventListener('mousemove', (e) => {
  mouseGlow.style.transform = `translate(${e.clientX - 300}px, ${e.clientY - 300}px)`;
});

// Scroll Reveal Logic
const revealElements = document.querySelectorAll('.reveal');
const revealObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('active');
    }
  });
}, {
  threshold: 0.15,
  rootMargin: '0px 0px -50px 0px'
});

revealElements.forEach(el => revealObserver.observe(el));

// Sticky Nav with Minimal Shift
const nav = document.querySelector('.nav');
let lastScrollY = window.scrollY;

window.addEventListener('scroll', () => {
  if (window.scrollY > 100) {
    nav.style.height = '70px';
    nav.style.background = 'rgba(10, 25, 47, 0.85)';
    nav.style.backdropFilter = 'blur(10px)';
    nav.style.boxShadow = '0 10px 30px -10px rgba(2, 12, 27, 0.7)';
  } else {
    nav.style.height = '100px';
    nav.style.background = 'transparent';
    nav.style.backdropFilter = 'none';
    nav.style.boxShadow = 'none';
  }

  lastScrollY = window.scrollY;
});

// Scroll Progress Bar
const scrollProgress = document.getElementById('scroll-progress');

window.addEventListener('scroll', () => {
  const scrollTop = window.scrollY;
  const docHeight = document.documentElement.scrollHeight - window.innerHeight;
  const scrollPercent = (scrollTop / docHeight) * 100;
  scrollProgress.style.width = scrollPercent + '%';
});

// Real Typewriter Effect with Cursor
function typeEffect(element, speed, callback) {
  const text = element.innerText;
  element.innerText = '';
  element.style.opacity = '1';

  let i = 0;
  const cursor = document.createElement('span');
  cursor.innerText = '_';
  cursor.classList.add('typing-cursor');
  element.appendChild(cursor);

  const timer = setInterval(() => {
    if (i < text.length) {
      cursor.before(text.charAt(i));
      i++;
    } else {
      clearInterval(timer);
      cursor.remove();
      if (callback) callback();
    }
  }, speed);
}

const h1 = document.querySelector('.typewriter');
const h2 = document.querySelector('.typewriter-sub');

if (h1 && h2) {
  h1.style.opacity = '0';
  h2.style.opacity = '0';

  setTimeout(() => {
    typeEffect(h1, 70, () => {
      setTimeout(() => typeEffect(h2, 40), 500);
    });
  }, 800);
}

// Tagline Rotation (after initial typewriter completes)
const taglines = [
  'i build scalable cloud systems.',
  'cloud engineer | ml researcher.',
  'building intelligent infrastructure.'
];

let currentTagline = 0;

function rotateTagline() {
  const taglineEl = document.getElementById('rotating-tagline');
  if (!taglineEl) return;

  // Fade out
  taglineEl.style.transition = 'opacity 0.5s ease';
  taglineEl.style.opacity = '0';

  setTimeout(() => {
    currentTagline = (currentTagline + 1) % taglines.length;
    taglineEl.innerText = taglines[currentTagline];
    taglineEl.style.opacity = '1';
  }, 500);
}

// Start rotation after initial typewriter finishes (~5 seconds)
setTimeout(() => {
  setInterval(rotateTagline, 4000);
}, 6000);


// Project Expansion Toggle (Click whole box)
document.querySelectorAll('.project-item').forEach(item => {
  item.addEventListener('click', (e) => {
    // Don't toggle if clicking an actual link inside the box
    if (e.target.closest('a')) return;

    item.classList.toggle('active');
  });
});


// Smooth Scroll for Navigation Links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function (e) {
    e.preventDefault();
    const targetId = this.getAttribute('href');
    if (targetId === '#') return;

    const targetElement = document.querySelector(targetId);
    if (targetElement) {
      const navHeight = 70;
      const targetPosition = targetElement.getBoundingClientRect().top + window.pageYOffset - navHeight;

      window.scrollTo({
        top: targetPosition,
        behavior: 'smooth'
      });
    }

    // Close mobile menu on link click
    const navLinks = document.getElementById('nav-links');
    const hamburger = document.getElementById('nav-hamburger');
    if (navLinks && navLinks.classList.contains('open')) {
      navLinks.classList.remove('open');
      hamburger.classList.remove('active');
    }
  });
});


// Mobile Hamburger Menu Toggle
const hamburger = document.getElementById('nav-hamburger');
const navLinks = document.getElementById('nav-links');

if (hamburger && navLinks) {
  hamburger.addEventListener('click', () => {
    hamburger.classList.toggle('active');
    navLinks.classList.toggle('open');
  });

  // Close menu when clicking outside
  document.addEventListener('click', (e) => {
    if (!e.target.closest('.nav-content') && navLinks.classList.contains('open')) {
      navLinks.classList.remove('open');
      hamburger.classList.remove('active');
    }
  });
}


// Active Nav Link Highlighting on Scroll
const sections = document.querySelectorAll('section[id]');
const navAnchors = document.querySelectorAll('.nav-links a[href^="#"]');

function highlightActiveNav() {
  const scrollY = window.scrollY + 120;

  sections.forEach(section => {
    const sectionTop = section.offsetTop;
    const sectionHeight = section.offsetHeight;
    const sectionId = section.getAttribute('id');

    if (scrollY >= sectionTop && scrollY < sectionTop + sectionHeight) {
      navAnchors.forEach(a => {
        a.classList.remove('active');
        if (a.getAttribute('href') === '#' + sectionId) {
          a.classList.add('active');
        }
      });
    }
  });
}

window.addEventListener('scroll', highlightActiveNav);
