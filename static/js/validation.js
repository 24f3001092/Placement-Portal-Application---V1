document.addEventListener('DOMContentLoaded', () => {
  const forms = document.querySelectorAll('form[data-validate="true"]');

  forms.forEach((form) => {
    form.addEventListener('submit', (event) => {
      const requiredFields = form.querySelectorAll('[required]');
      let valid = true;

      requiredFields.forEach((field) => {
        if (!field.value.trim()) {
          valid = false;
          field.classList.add('is-invalid');
        } else {
          field.classList.remove('is-invalid');
        }
      });

      if (!valid) {
        event.preventDefault();
      }
    });
  });
});
