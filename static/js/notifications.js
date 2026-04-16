document.addEventListener('DOMContentLoaded', () => {
  const notificationBanner = document.getElementById('statusNotification');
  if (!notificationBanner) {
    return;
  }

  setTimeout(() => {
    notificationBanner.classList.add('d-none');
  }, 5000);
});
