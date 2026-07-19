(function () {
  const CKEDITOR_URL = 'https://cdn.ckeditor.com/ckeditor5/41.4.2/classic/ckeditor.js';
  const SELECTOR = 'textarea.ckeditor-textarea';

  function initializeEditors() {
    if (!window.ClassicEditor) {
      return;
    }

    document.querySelectorAll(SELECTOR).forEach((textarea) => {
      if (textarea.dataset.ckeditorInitialized === 'true') {
        return;
      }

      textarea.dataset.ckeditorInitialized = 'true';
      window.ClassicEditor.create(textarea).catch((error) => {
        console.error('CKEditor initialization failed:', error);
      });
    });
  }

  function loadCKEditor() {
    if (window.ClassicEditor) {
      initializeEditors();
      return;
    }

    if (document.querySelector('script[data-ckeditor-cdn="true"]')) {
      return;
    }

    const script = document.createElement('script');
    script.src = CKEDITOR_URL;
    script.async = true;
    script.dataset.ckeditorCdn = 'true';
    script.onload = initializeEditors;
    document.head.appendChild(script);
  }

  document.addEventListener('DOMContentLoaded', loadCKEditor);
  document.addEventListener('formset:added', initializeEditors);
})();
