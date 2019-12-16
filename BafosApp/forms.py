from django import forms
from .models import BlogPost,Category,PostManager
from django.forms import ModelForm
from .models import ArticleFile
from django.core.validators import *


class ArticleFileForm(ModelForm):
    class Meta:
        model = ArticleFile
        fields = ['file']


class CsvFileField(forms.FileField):
    def validate(self, value):
        # First run the parent class' validation routine
        super().validate(value)
        # Run our own file extension check
        file_extension = os.path.splitext(value.name)[1]
        if file_extension != '.csv':
            raise ValidationError(
                 ('Invalid file extension'),
                 code='invalid'
            )