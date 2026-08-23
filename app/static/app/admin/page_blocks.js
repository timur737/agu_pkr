(function () {
  const fieldNames = ['title', 'description', 'date', 'photo', 'file', 'url', 'value'];
  const visibleFields = {
    text: ['title', 'description', 'file'],
    photo_text: ['title', 'description', 'photo', 'file'],
    link: ['title', 'description', 'url', 'file'],
    pdf: ['title', 'description', 'file'],
    number: ['title', 'description', 'value', 'file'],
    social: ['title', 'url', 'file'],
    slider: ['photo', 'file'],
  };

  function fieldRow(container, name) {
    return container.querySelector(`.field-${name}`);
  }

  function updateBlock(container) {
    const type = container.querySelector('select[name$="-block_type"]');
    if (!type) return;

    const shown = visibleFields[type.value] || fieldNames;
    fieldNames.forEach((name) => {
      const row = fieldRow(container, name);
      if (row) row.hidden = !shown.includes(name);
    });
    container.dataset.blockType = type.value;
  }

  function initialize(root) {
    root.querySelectorAll('.inline-related, .module.aligned').forEach((container) => {
      const select = container.querySelector('select[name$="-block_type"]');
      if (!select || select.dataset.structureInitialized) return;
      select.dataset.structureInitialized = 'true';
      select.addEventListener('change', () => updateBlock(container));
      updateBlock(container);
    });
  }

  document.addEventListener('DOMContentLoaded', () => initialize(document));
  document.addEventListener('formset:added', (event) => initialize(event.target));
})();
