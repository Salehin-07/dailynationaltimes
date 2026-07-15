from django import forms
from editorials.models import Post, Tag


class PostForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )
    status = forms.ChoiceField(
        choices=Post._meta.get_field("status").choices,
        widget=forms.Select,
    )

    class Meta:
        model = Post
        fields = [
            "title",
            "category",
            "tags",
            "author_name",
            "excerpt",
            "content",
            "featured_image",
            "is_featured",
            "status",
        ]
        widgets = {
            "content": forms.Textarea(attrs={"rows": 18}),
            "excerpt": forms.Textarea(attrs={"rows": 3}),
        }
