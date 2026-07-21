const state = {
  lang: localStorage.getItem('menu-lang') || 'tr',
  data: null,
  activeCategoryId: null,
  screen: 'welcome'
};

const I18N = {
  tr: {
    welcome: "Deniz esintili lezzetler, taze balık ve zengin meze çeşitleriyle sizi soframıza bekliyoruz.",
    tagline: 'Balık · Meze · Izgara',
    viewMenu: 'Menüyü Keşfet',
    welcomeFoot: 'Yalova · Ceylan Kent',
    loadingError: 'Menü yüklenemedi. Lütfen sayfayı yenileyin.',
    getDirections: 'Yol tarifi',
    perPiece: 'adet',
    perKg: 'kg',
    back: 'Geri',
    contactInfo: 'İletişim & Bilgi',
    hideContact: 'Gizle'
  },
  en: {
    welcome: 'Fresh fish, rich meze varieties and sea-breeze flavors await you at our table.',
    tagline: 'Fish · Meze · Grill',
    viewMenu: 'Explore Menu',
    welcomeFoot: 'Yalova · Ceylan Kent',
    loadingError: 'Menu could not be loaded. Please refresh the page.',
    getDirections: 'Directions',
    perPiece: 'pc',
    perKg: 'kg',
    back: 'Back',
    contactInfo: 'Contact & Info',
    hideContact: 'Hide'
  }
};

function t(key) {
  return I18N[state.lang]?.[key] ?? I18N.tr[key] ?? key;
}

function getCategoryName(cat) {
  return state.lang === 'en' ? cat.nameEn : cat.name;
}

function getItemName(item) {
  return state.lang === 'en' ? item.nameEn : item.name;
}

function getSubcategoryName(sub) {
  return state.lang === 'en' ? sub.nameEn : sub.name;
}

function getAddress(contact) {
  if (!contact.address) return '';
  return state.lang === 'en' ? contact.address.en : contact.address.tr;
}
