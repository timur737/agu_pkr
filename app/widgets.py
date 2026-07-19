from django import forms


class CKEditorTextarea(forms.Textarea):
    """Textarea widget enhanced to CKEditor in the Django admin."""

    class Media:
        js = ('app/admin/ckeditor.js',)

    def __init__(self, attrs=None):
        default_attrs = {'class': 'ckeditor-textarea'}
        if attrs:
            classes = attrs.get('class', '')
            attrs = {**attrs, 'class': f"{classes} ckeditor-textarea".strip()}
            default_attrs.update(attrs)
        super().__init__(attrs=default_attrs)
