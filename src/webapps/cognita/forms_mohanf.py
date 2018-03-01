from django import forms
from cognita.models import Course, Lecture, Reading, Video, Part, Module, Tag
from ckeditor_uploader.widgets import CKEditorUploadingWidget



class CourseForm(forms.ModelForm):
    Category_CHOICES = (
        ('CS', 'Computer Science'),
        ('MATH', 'Mathematics'),
        ('ART', 'Art'),
        ('BUS', 'Business'),
        ('SCI', 'Natural Science'),
        ('SSCI', 'Social Science'),
        ('LIT', 'Literature'),
        ('UCL', 'Unclassified'),
    )

    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 8}), required=True)
    creator_info = forms.CharField(label='Write your self introduction below', widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 8}), required=True)
    category = forms.ChoiceField(choices=Category_CHOICES, widget=forms.Select(), initial='UCL')

    class Meta:
        model = Course
        fields = ['title', 'description', 'creator_info', 'category', 'course_image']
        widget = {'course_image': forms.ImageField()}

    # def clean_course_image(self):
    #     image = self.cleaned_data.get('course_image')
    #     image_name = image.name
    #     #print image_name
    #     if not all(ord(c) < 128 for c in image_name):
    #         #print 'aaaaa'
    #         raise forms.ValidationError('invalid file name')
    #     return image


class LectureForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 8}), required=True)

    class Meta:
        model = Lecture
        fields = ['title', 'description']


class ReadingForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 8}), required=True)
    expected_hour = forms.FloatField(required=True, min_value=0.1, max_value=24)

    class Meta:
        model = Reading
        fields = ['title', 'description', 'expected_hour', 'file']

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if not file:
            raise forms.ValidationError('Please upload a PDF file')

        if file:
            filename = file.name
            if not filename.endswith('.pdf'):
                raise forms.ValidationError('Please upload a PDF file.')
        return file


class VideoForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 8}), required=True)
    link = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), help_text='Please enter a valid Youtube link', required=True)
    expected_hour = forms.FloatField(required=True, min_value=0.1, max_value=24)

    class Meta:
        model = Video
        fields = ['title', 'description', 'expected_hour', 'link']

    def clean_link(self):
        link = self.cleaned_data.get('link')
        link = link.replace("watch?v=", "embed/")
        return link


class DeletePartForm(forms.Form):
    part_id = forms.CharField(required=True)

    def clean_part_id(self):
        part_id = self.cleaned_data.get('part_id')
        if not Part.objects.filter(id=part_id).count():
            raise forms.ValidationError('Invalid Delete Item')
        return part_id


class DeleteModuleForm(forms.Form):
    module_id = forms.CharField(required=True)

    def clean_module_id(self):
        module_id = self.cleaned_data.get('module_id')
        if not Module.objects.filter(id=module_id).count():
            raise forms.ValidationError('Invalid Delete Module')
        return module_id


class PublishForm(forms.Form):
    course_id = forms.CharField(required=True)

    def clean_course_id(self):
        course_id = self.cleaned_data.get('course_id')
        if not Course.objects.filter(id=course_id).count():
            raise forms.ValidationError('Invalid Course Id')
        return course_id


class SearchOptionForm(forms.Form):
    CHOICES = [('P', 'Popularity'),
               ('C', 'Created Time')]

    Category_CHOICES = (
        ('CS', 'Computer Science'),
        ('MATH', 'Mathematics'),
        ('ART', 'Art'),
        ('BUS', 'Business'),
        ('SCI', 'Natural Science'),
        ('SSCI', 'Social Science'),
        ('LIT', 'Literature'),
        ('UCL', 'Unclassified'),
    )

    sort_by = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect())
    filter_with = forms.MultipleChoiceField(choices=Category_CHOICES, required=False, widget=forms.CheckboxSelectMultiple)
    srch_term = forms.CharField(widget=forms.HiddenInput(attrs={'id':'last_search'}), label="")


class UpperReadingForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 8}), required=True)
    expected_hour = forms.FloatField(required=True, min_value=0.1, max_value=24)

    class Meta:
        model = Reading
        fields = ['title', 'description', 'expected_hour']


class MaterialForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 8}), required=True)
    material = forms.CharField(widget=CKEditorUploadingWidget(config_name='material_editor', attrs={'id': 'material_input'}), required=False)
    expected_hour = forms.FloatField(required=True, min_value=0.1, max_value=24)

    class Meta:
        model = Reading
        fields = ['title', 'description', 'expected_hour', 'material']

    # def clean_expected_hour(self):
    #     expected_hour = self.cleaned_data.get('expected_hour')
    #     if expected_hour <= 0:
    #         print expected_hour
    #         raise forms.ValidationError('Enter a positive number')
    #     return expected_hour


class LowerReadingForm(forms.ModelForm):
    material = forms.CharField(widget=CKEditorUploadingWidget(config_name='material_editor', attrs={'id': 'material_input'}), required=False)

    class Meta:
        model = Reading
        fields = ['material']


class TagForm(forms.ModelForm):
    tag_content = forms.CharField(required=True)

    class Meta:
        model = Tag
        fields = ['tag_content']

    def clean_tag_content(self):
        tag_content = self.cleaned_data.get('tag_content')
        tag_content = tag_content.lower()
        return tag_content


class DeleteTagForm(forms.Form):
    tag_id = forms.CharField(required=True)

    def clean_tag_id(self):
        tag_id = self.cleaned_data.get('tag_id')
        if not Tag.objects.filter(id=tag_id).count():
            raise forms.ValidationError('invalid tag')
        return tag_id