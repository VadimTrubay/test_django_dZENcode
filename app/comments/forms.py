# forms.py
from django import forms
from .models import Comment
from PIL import Image
import tempfile
from captcha.fields import CaptchaField


class CommentForm(forms.ModelForm):
    captcha = CaptchaField()

    class Meta:
        model = Comment
        fields = ["user", "text", "parent"]

    def clean_text(self):
        text = self.cleaned_data.get("text")
        # Проверка на допустимые HTML теги
        allowed_tags = [
            "<a>",
            "</a>",
            "<code>",
            "</code>",
            "<i>",
            "</i>",
            "<strong>",
            "</strong>",
        ]
        for tag in allowed_tags:
            text = text.replace(tag, "")
        return text


class FileUploadForm(forms.Form):
    image = forms.ImageField(required=False)
    text_file = forms.FileField(required=False)

    def clean_image(self):
        image = self.cleaned_data.get("image")
        if image:
            img = Image.open(image)
            img.thumbnail((320, 240), Image.ANTIALIAS)
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
            img.save(temp_file.name, "JPEG")
            return temp_file

    def clean_text_file(self):
        text_file = self.cleaned_data.get("text_file")
        if text_file and text_file.size > 102400:
            raise forms.ValidationError("Размер файла не должен превышать 100 КБ.")
        return text_file
