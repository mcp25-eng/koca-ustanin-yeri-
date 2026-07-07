const CATEGORY_FALLBACKS = {
  mezeler: 'assets/foods/haydari.jpg',
  'ara-sicaklar': 'assets/foods/kalamar-tava.jpg',
  salatalar: 'assets/foods/coban-salata.jpg',
  'izgara-baliklar': 'assets/foods/levrek-izgara.jpg',
  'tava-baliklar': 'assets/foods/hamsi-tava.jpg',
  'izgara-et': 'assets/foods/karisik-izgara.jpg',
  'tatli-meyve': 'assets/foods/dondurmali-irmik.jpg',
  mesrubatlar: 'assets/foods/mevsim-meyveleri.jpg',
  raki: 'assets/category/raki.jpg',
  saraplar: 'assets/category/wine.jpg'
};

const COMPACT_CATEGORIES = ['mesrubatlar', 'raki', 'saraplar'];
const IMAGE_CACHE_VERSION = 'menu-v35';

const SOCIAL_ICONS = {
  instagram: `<svg viewBox="0 0 24 24"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zM12 0C8.741 0 8.333.014 7.053.072 2.695.272.273 2.69.073 7.052.014 8.333 0 8.741 0 12c0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98C8.333 23.986 8.741 24 12 24c3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98C15.668.014 15.259 0 12 0zm0 5.838a6.162 6.162 0 100 12.324 6.162 6.162 0 000-12.324zM12 16a4 4 0 110-8 4 4 0 010 8zm6.406-11.845a1.44 1.44 0 100 2.881 1.44 1.44 0 000-2.881z"/></svg>`,
  facebook: `<svg viewBox="0 0 24 24"><path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/></svg>`,
  tiktok: `<svg viewBox="0 0 24 24"><path d="M19.59 6.69a4.83 4.83 0 01-3.77-4.25V2h-3.45v13.67a2.89 2.89 0 01-2.88 2.5 2.89 2.89 0 01-2.89-2.89 2.89 2.89 0 012.89-2.89c.28 0 .54.04.79.1v-3.5a6.37 6.37 0 00-.79-.05A6.34 6.34 0 003.15 15.2a6.34 6.34 0 0010.86 4.48v-7.1a8.16 8.16 0 005.58 2.17V10.3a4.84 4.84 0 01-3.77-1.12V6.69h3.77z"/></svg>`,
  googleMaps: `<svg viewBox="0 0 24 24"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5a2.5 2.5 0 010-5 2.5 2.5 0 010 5z"/></svg>`,
  whatsapp: `<svg viewBox="0 0 24 24"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.435 9.884-9.881 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/></svg>`,
  phone: `<svg viewBox="0 0 24 24"><path d="M6.62 10.79a15.05 15.05 0 006.59 6.59l2.2-2.2a1 1 0 011.01-.24c1.12.37 2.33.57 3.58.57a1 1 0 011 1V20a1 1 0 01-1 1C10.07 21 3 13.93 3 5a1 1 0 011-1h3.5a1 1 0 011 1c0 1.25.2 2.46.57 3.58a1 1 0 01-.25 1.01l-2.2 2.2z"/></svg>`
};

function escapeHtml(str) {
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

function getItemImage(item, categoryId) {
  const path = item.image || CATEGORY_FALLBACKS[categoryId] || CATEGORY_FALLBACKS.mezeler;
  return `${path}?v=${IMAGE_CACHE_VERSION}`;
}

function getCategoryImage(categoryId) {
  return `${CATEGORY_FALLBACKS[categoryId] || CATEGORY_FALLBACKS.mezeler}?v=${IMAGE_CACHE_VERSION}`;
}

function formatPrice(item, settings) {
  if (!settings.showPrices || item.price == null) return '';
  let unit = '';
  if (item.unit === 'adet') unit = ` / ${t('perPiece')}`;
  if (item.unit === 'kg') unit = ` / ${t('perKg')}`;
  return `${item.price} ${settings.currency}${unit}`;
}

function showScreen(name) {
  state.screen = name;
  const welcome = document.getElementById('welcome-screen');
  const menu = document.getElementById('menu-screen');
  if (name === 'menu') {
    welcome.classList.add('hidden');
    menu.classList.remove('hidden');
    menu.setAttribute('aria-hidden', 'false');
  } else {
    menu.classList.add('hidden');
    menu.setAttribute('aria-hidden', 'true');
    welcome.classList.remove('hidden');
  }
}

function updateLangToggle() {
  const isTr = state.lang === 'tr';
  const flag = isTr ? '🇹🇷' : '🇬🇧';
  const label = isTr ? 'TR' : 'EN';
  document.getElementById('lang-flag').textContent = flag;
  document.getElementById('lang-label').textContent = label;
  document.getElementById('lang-flag-menu').textContent = flag;
  document.getElementById('lang-label-menu').textContent = label;
  document.documentElement.lang = state.lang;
}

function renderWelcome() {
  const data = state.data;
  if (!data) return;
  document.getElementById('restaurant-name-welcome').textContent = data.restaurant.name;
  document.getElementById('welcome-tagline').textContent = t('tagline');
  document.getElementById('welcome-text').textContent = t('welcome');
  document.getElementById('view-menu-label').textContent = t('viewMenu');
  document.getElementById('welcome-foot').textContent = t('welcomeFoot');
  document.getElementById('logo-welcome').src = data.restaurant.logo;
}

function renderSocialLinks(social, whatsapp, mapsUrl) {
  const container = document.getElementById('social-links');
  container.innerHTML = '';
  const links = [
    { key: 'instagram', url: social.instagram },
    { key: 'facebook', url: social.facebook },
    { key: 'tiktok', url: social.tiktok },
    { key: 'googleMaps', url: mapsUrl || social.googleMaps }
  ];
  if (whatsapp) {
    links.unshift({
      key: 'whatsapp',
      url: `https://wa.me/90${whatsapp.replace(/\D/g, '').replace(/^0/, '')}`
    });
  }
  links.filter(l => l.url).forEach(link => {
    const a = document.createElement('a');
    a.href = link.url;
    a.className = 'social-btn';
    a.target = '_blank';
    a.rel = 'noopener noreferrer';
    a.innerHTML = SOCIAL_ICONS[link.key];
    container.appendChild(a);
  });
}

function renderContact(contact) {
  const container = document.getElementById('contact-info');
  container.innerHTML = '';
  contact.phones.forEach(phone => {
    const a = document.createElement('a');
    a.href = `tel:+90${phone.number.replace(/\D/g, '').replace(/^0/, '')}`;
    a.className = 'contact-link';
    a.innerHTML = `${SOCIAL_ICONS.phone}<span>${phone.name}: ${phone.number}</span>`;
    container.appendChild(a);
  });
}

function renderFooter(contact, settings) {
  const address = getAddress(contact);
  const maps = document.getElementById('footer-maps');
  if (address && contact.googleMaps) {
    maps.href = contact.googleMaps;
    maps.innerHTML = `${SOCIAL_ICONS.googleMaps}<span>${escapeHtml(address)}</span>`;
    maps.style.display = '';
  } else {
    maps.style.display = 'none';
  }
  document.getElementById('footer-note').textContent =
    state.lang === 'en' ? (settings.footerNoteEn || settings.footerNote) : settings.footerNote;

  const review = document.getElementById('footer-review');
  const reviewText = state.lang === 'en'
    ? (settings.reviewNoteEn || settings.reviewNote)
    : settings.reviewNote;
  if (review && reviewText) {
    document.getElementById('footer-review-text').textContent = reviewText;
    review.href = contact.googleReview || contact.googleMaps || '#';
    review.style.display = '';
  } else if (review) {
    review.style.display = 'none';
  }

  updateFooterToggleLabel();
}

function updateFooterToggleLabel() {
  const label = document.getElementById('footer-toggle-label');
  const footer = document.getElementById('bottombar');
  if (!label || !footer) return;
  label.textContent = footer.classList.contains('bottombar--open') ? t('hideContact') : t('contactInfo');
}

function initFooterToggle() {
  const footer = document.getElementById('bottombar');
  const toggle = document.getElementById('footer-toggle');
  const panel = document.getElementById('footer-panel');
  const menuScreen = document.getElementById('menu-screen');
  if (!footer || !toggle || !panel) return;

  toggle.addEventListener('click', () => {
    const open = footer.classList.toggle('bottombar--open');
    toggle.setAttribute('aria-expanded', String(open));
    panel.hidden = !open;
    menuScreen.classList.toggle('footer-open', open);
    updateFooterToggleLabel();
  });

  updateFooterToggleLabel();
}

function renderCategoryStrip(categories) {
  const strip = document.getElementById('category-strip');
  if (!state.activeCategoryId && categories.length) {
    state.activeCategoryId = categories[0].id;
  }
  strip.innerHTML = categories.map(cat => `
    <button type="button" class="category-pill${cat.id === state.activeCategoryId ? ' active' : ''}"
            data-id="${cat.id}" role="tab" aria-selected="${cat.id === state.activeCategoryId}">
      <img class="category-pill__img" src="${getCategoryImage(cat.id)}" alt="" loading="lazy">
      <span class="category-pill__label">${escapeHtml(getCategoryName(cat))}</span>
    </button>
  `).join('');

  strip.querySelectorAll('.category-pill').forEach(btn => {
    btn.addEventListener('click', () => {
      state.activeCategoryId = btn.dataset.id;
      renderCategoryStrip(categories);
      renderActiveCategory();
      btn.scrollIntoView({ behavior: 'smooth', inline: 'center', block: 'nearest' });
    });
  });
}

function renderMenuItem(item, settings, categoryId) {
  const price = formatPrice(item, settings);
  const primary = escapeHtml(getItemName(item));
  const secondary = state.lang === 'en' ? escapeHtml(item.name) : escapeHtml(item.nameEn);
  const showImage = settings.showItemImages && !COMPACT_CATEGORIES.includes(categoryId);

  if (!showImage) {
    return `
      <div class="compact-item">
        <div>
          <div class="compact-item__name">${primary}</div>
          ${secondary ? `<div class="compact-item__name-en">${secondary}</div>` : ''}
        </div>
        ${price ? `<div class="compact-item__price">${price}</div>` : ''}
      </div>
    `;
  }

  const img = getItemImage(item, categoryId);
  const fallback = CATEGORY_FALLBACKS[categoryId] || CATEGORY_FALLBACKS.mezeler;
  return `
    <article class="product-card">
      <div class="product-card__img-wrap">
        <img class="product-card__img" src="${img}" alt="${primary}" loading="lazy"
             onerror="this.onerror=null;this.src='${fallback}?v=${IMAGE_CACHE_VERSION}'">
      </div>
      <div class="product-card__body">
        <h3 class="product-card__name">${primary}</h3>
        ${secondary ? `<p class="product-card__name-en">${secondary}</p>` : ''}
        ${price ? `<p class="product-card__price">${price}</p>` : ''}
      </div>
    </article>
  `;
}

function renderActiveCategory() {
  const data = state.data;
  const cat = data.categories.find(c => c.id === state.activeCategoryId);
  const container = document.getElementById('menu-content');
  if (!cat) {
    container.innerHTML = '';
    return;
  }

  const subtitle = state.lang === 'en' ? cat.name : cat.nameEn;
  let itemsHtml = '';

  if (cat.subcategories) {
    itemsHtml = cat.subcategories.map(sub => `
      <h3 class="subcategory-label">${escapeHtml(getSubcategoryName(sub))}</h3>
      <div class="compact-list">
        ${sub.items.map(item => renderMenuItem(item, data.settings, cat.id)).join('')}
      </div>
    `).join('');
  } else if (COMPACT_CATEGORIES.includes(cat.id)) {
    itemsHtml = `<div class="compact-list">${cat.items.map(item => renderMenuItem(item, data.settings, cat.id)).join('')}</div>`;
  } else {
    itemsHtml = `<div class="product-list">${cat.items.map(item => renderMenuItem(item, data.settings, cat.id)).join('')}</div>`;
  }

  container.innerHTML = `
    <div class="menu-panel">
      <h2 class="menu-panel__title">${escapeHtml(getCategoryName(cat))}</h2>
      <p class="menu-panel__subtitle">${escapeHtml(subtitle)}</p>
      ${itemsHtml}
    </div>
  `;
}

function renderMenuScreen() {
  const data = state.data;
  document.getElementById('restaurant-name-menu').textContent = data.restaurant.name;
  document.getElementById('logo-menu').src = data.restaurant.logo;
  renderCategoryStrip(data.categories);
  renderActiveCategory();
  renderContact(data.contact);
  renderSocialLinks(data.social, data.contact.whatsapp, data.contact.googleMaps);
  renderFooter(data.contact, data.settings);
}

function renderAll() {
  if (!state.data) return;
  renderWelcome();
  if (state.screen === 'menu') renderMenuScreen();
  updateLangToggle();
}

function toggleLang() {
  state.lang = state.lang === 'tr' ? 'en' : 'tr';
  localStorage.setItem('menu-lang', state.lang);
  renderAll();
}

function openMenu() {
  showScreen('menu');
  renderMenuScreen();
  window.scrollTo(0, 0);
}

function closeMenu() {
  showScreen('welcome');
}

async function init() {
  document.getElementById('year').textContent = new Date().getFullYear();
  document.getElementById('view-menu-btn').addEventListener('click', openMenu);
  document.getElementById('back-btn').addEventListener('click', closeMenu);
  document.getElementById('lang-toggle').addEventListener('click', toggleLang);
  document.getElementById('lang-toggle-menu').addEventListener('click', toggleLang);
  initFooterToggle();

  try {
    const res = await fetch('data/menu.json');
    state.data = await res.json();
    renderAll();
  } catch (err) {
    document.getElementById('welcome-text').textContent = t('loadingError');
    console.error(err);
  }
}

init();
