console.log('Hey');

if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker
      .register('/sw.js')
      /* eslint-disable */
      .then(() => {
        console.log('sw.js is loaded');
      })
      .catch(() => {});
    /* eslint-enable */
  });
}
