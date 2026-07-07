const state = {
  lang: localStorage.getItem('menu-lang') || 'tr',
  data: null,
  activeCategoryId: null,
  screen: 'welcome'
};

const I18N = {
  tr: {
    welcome: "Koca Ustanın Yeri'ne hoş geldiniz.",
    viewMenu: 'Menüyü Gör',
    loadingError: 'Menü yüklenemedi. Lütfen sayfayı yenileyin.',
    getDirections: 'Yol tarifi',
    perPiece: 'adet',
    perKg: 'kg',
    back: 'Geri',
    contactInfo: 'İletişim & Bilgi',
    hideContact: 'Gizle'
  },
  en: {
    welcome: 'Welcome to Koca Ustanın Yeri.',
    viewMenu: 'View Menu',
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
