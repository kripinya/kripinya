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
    nav.style.boxShadow = '0 10px 30px -10px rgba(2, 12, 27, 0.7)';
  } else {
    nav.style.height = '100px';
    nav.style.background = 'transparent';
    nav.style.boxShadow = 'none';
  }

  lastScrollY = window.scrollY;
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
  });
});
