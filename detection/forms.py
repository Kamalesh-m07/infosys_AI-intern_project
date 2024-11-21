from django import forms

class MediaUploadForm(forms.Form):
    image = forms.ImageField(label="Select an Image", required=False)
    video = forms.FileField(label="Select a Video", required=False)

    def clean(self):
        cleaned_data = super().clean()
        image = cleaned_data.get("image")
        video = cleaned_data.get("video")

        # Ensure that at least one file (image or video) is uploaded
        if not image and not video:
            raise forms.ValidationError("Please upload either an image or a video.")
        return cleaned_data


class ContactForm(forms.Form):
    username = forms.CharField(max_length=100, label="Your Name", required=True)
    email = forms.EmailField(label="Your Email", required=True)
    issue = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Describe the issue or inquiry here.'}),
        max_length=500,
        label="Your Message",
        required=True
    )
