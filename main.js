/* ===========================================================
   Oakley Gompels — site interactivity
   - Mobile nav toggle
   - Scroll-reveal (IntersectionObserver)
   - Animated count-up on impact metrics
   - Subtle particle constellation behind the hero
   All motion respects prefers-reduced-motion.
   =========================================================== */
(function () {
    'use strict';

    const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    /* ---------- Mobile navigation ---------- */
    const nav = document.getElementById('nav');
    const toggle = document.getElementById('navToggle');
    const navLinks = document.getElementById('navLinks');

    if (nav && toggle && navLinks) {
        const closeNav = () => {
            nav.classList.remove('nav-open');
            toggle.setAttribute('aria-expanded', 'false');
            toggle.setAttribute('aria-label', 'Open menu');
        };
        toggle.addEventListener('click', () => {
            const open = nav.classList.toggle('nav-open');
            toggle.setAttribute('aria-expanded', String(open));
            toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
        });
        // Close after tapping a link
        navLinks.querySelectorAll('a').forEach(a => a.addEventListener('click', closeNav));
        // Close on Escape
        document.addEventListener('keydown', e => { if (e.key === 'Escape') closeNav(); });
    }

    /* ---------- Scroll reveal ---------- */
    const revealEls = document.querySelectorAll('.reveal');
    if (revealEls.length) {
        if (reduceMotion || !('IntersectionObserver' in window)) {
            revealEls.forEach(el => el.classList.add('is-visible'));
        } else {
            const obs = new IntersectionObserver((entries, o) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        entry.target.classList.add('is-visible');
                        o.unobserve(entry.target);
                    }
                });
            }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
            revealEls.forEach(el => obs.observe(el));
        }
    }

    /* ---------- Count-up metrics ---------- */
    const nums = document.querySelectorAll('.impact-num');
    function runCount(el) {
        const target = parseFloat(el.dataset.target || '0');
        const prefix = el.dataset.prefix || '';
        const suffix = el.dataset.suffix || '';
        if (reduceMotion) { el.textContent = prefix + target + suffix; return; }
        const dur = 1500;
        const start = performance.now();
        const tick = now => {
            const p = Math.min((now - start) / dur, 1);
            const eased = 1 - Math.pow(1 - p, 3);           // easeOutCubic
            const val = Math.round(target * eased);
            el.textContent = prefix + val + suffix;
            if (p < 1) requestAnimationFrame(tick);
        };
        requestAnimationFrame(tick);
    }
    if (nums.length) {
        if (reduceMotion || !('IntersectionObserver' in window)) {
            nums.forEach(runCount);
        } else {
            const numObs = new IntersectionObserver((entries, o) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) { runCount(entry.target); o.unobserve(entry.target); }
                });
            }, { threshold: 0.6 });
            nums.forEach(n => numObs.observe(n));
        }
    }

    /* ---------- Hero particle constellation ---------- */
    const canvas = document.getElementById('heroCanvas');
    if (canvas && !reduceMotion) {
        const ctx = canvas.getContext('2d');
        const hero = canvas.parentElement;
        let w = 0, h = 0, dpr = Math.min(window.devicePixelRatio || 1, 2);
        let particles = [];
        let raf = null;
        const ACCENT = '109,74';       // rgb of #ff6d4a without alpha
        const LIGHT = '167,139,250';   // subtle purple accent

        function size() {
            w = hero.clientWidth;
            h = hero.clientHeight;
            canvas.width = w * dpr;
            canvas.height = h * dpr;
            canvas.style.width = w + 'px';
            canvas.style.height = h + 'px';
            ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
            const count = Math.min(70, Math.round(w * h / 16000));
            particles = Array.from({ length: count }, () => ({
                x: Math.random() * w,
                y: Math.random() * h,
                vx: (Math.random() - 0.5) * 0.28,
                vy: (Math.random() - 0.5) * 0.28,
                r: Math.random() * 1.6 + 0.8,
                c: Math.random() > 0.82 ? LIGHT : '255,' + ACCENT
            }));
        }

        function frame() {
            ctx.clearRect(0, 0, w, h);
            // links
            for (let i = 0; i < particles.length; i++) {
                const a = particles[i];
                a.x += a.vx; a.y += a.vy;
                if (a.x < 0 || a.x > w) a.vx *= -1;
                if (a.y < 0 || a.y > h) a.vy *= -1;
                for (let j = i + 1; j < particles.length; j++) {
                    const b = particles[j];
                    const dx = a.x - b.x, dy = a.y - b.y;
                    const dist = Math.hypot(dx, dy);
                    if (dist < 130) {
                        ctx.strokeStyle = 'rgba(255,' + ACCENT + ',' + (0.10 * (1 - dist / 130)) + ')';
                        ctx.lineWidth = 1;
                        ctx.beginPath();
                        ctx.moveTo(a.x, a.y);
                        ctx.lineTo(b.x, b.y);
                        ctx.stroke();
                    }
                }
            }
            // dots
            particles.forEach(p => {
                ctx.fillStyle = 'rgba(' + p.c + ',0.7)';
                ctx.beginPath();
                ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
                ctx.fill();
            });
            raf = requestAnimationFrame(frame);
        }

        function start() { if (!raf) raf = requestAnimationFrame(frame); }
        function stop() { if (raf) { cancelAnimationFrame(raf); raf = null; } }

        size();
        start();

        let rt;
        window.addEventListener('resize', () => { clearTimeout(rt); rt = setTimeout(size, 200); });
        // Pause when tab hidden or hero scrolled out of view
        document.addEventListener('visibilitychange', () => document.hidden ? stop() : start());
        if ('IntersectionObserver' in window) {
            new IntersectionObserver(entries => {
                entries.forEach(e => e.isIntersecting ? start() : stop());
            }, { threshold: 0 }).observe(hero);
        }
    }

    /* ---------- Footer year (self-updating) ---------- */
    const yearEl = document.querySelector('[data-year]');
    if (yearEl) yearEl.textContent = new Date().getFullYear();

})();
