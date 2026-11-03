(function () {
  const fieldNames = [
    'title', 'description', 'short_information', 'contacts', 'email',
    'date', 'image_ru', 'image_ky', 'image_en', 'file_ru', 'file_ky', 'file_en', 'url', 'value',
  ];
  const visibleFields = {
    text: ['title', 'description', 'file_ru', 'file_ky', 'file_en'],
    photo_text: [
      'title', 'description', 'short_information', 'contacts', 'email',
      'image_ru', 'image_ky', 'image_en', 'file_ru', 'file_ky', 'file_en', 'url',
    ],
    link: ['title', 'description', 'url', 'file_ru', 'file_ky', 'file_en'],
    pdf: ['title', 'description', 'file_ru', 'file_ky', 'file_en'],
    number: ['title', 'description', 'value', 'file_ru', 'file_ky', 'file_en'],
    social: ['title', 'url', 'file_ru', 'file_ky', 'file_en'],
    slider: ['image_ru', 'image_ky', 'image_en', 'file_ru', 'file_ky', 'file_en'],
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
