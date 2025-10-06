from django import forms
from stripe import Review 
from core.models import ProductReview


class ProductReviewForm(forms.ModelForm):
    review = forms.CharField(widget=forms.Textarea(attrs={'placeholder': "Ecrivez un commentaire"}))

    class Meta:
        model = ProductReview
        fields = ['review', 'rating']