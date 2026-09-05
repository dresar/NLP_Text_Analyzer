from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile, SavedTemplate

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'preferred_analysis_type']
        widgets = {
            'preferred_analysis_type': forms.Select(),
            'bio': forms.Textarea(attrs={'rows': 3}),
        }

class SavedTemplateForm(forms.ModelForm):
    class Meta:
        model = SavedTemplate
        fields = ['name', 'text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 4}),
        }

class TextAnalysisForm(forms.Form):
    ANALYSIS_CHOICES = [
        ('sentiment', 'Sentiment Analysis'),
        ('summary', 'Text Summarization'),
        ('entities', 'Named Entity Recognition'),
        ('classification', 'Text Classification'),
    ]
    
    analysis_type = forms.ChoiceField(
        choices=ANALYSIS_CHOICES,
        widget=forms.RadioSelect(),
        initial='sentiment'
    )
    text = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 6, 'class': 'resize-none'}),
        required=True
    )
    title = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Give your analysis a title (optional)'})
    )
    is_public = forms.BooleanField(
        required=False,
        initial=False,
        label='Make this analysis public'
    )
    tags = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Add tags separated by commas (optional)'})
    )
    
    def clean_text(self):
        text = self.cleaned_data.get('text')
        if len(text.strip()) < 10:
            raise forms.ValidationError("Text must be at least 10 characters long.")
        return text