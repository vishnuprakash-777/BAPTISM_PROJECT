from django import forms
from .models import Baptism,ParishDetails,BaptismAdvanced,FieldTable,Option

class BaptismForm(forms.ModelForm):
    class Meta:
        model = Baptism
        fields = [
            'place_of_baptism',
            'date_of_baptism',
            'time_of_baptism',
            'child_name_first',
            'child_name_second',
            'dob',
            'mother_name',
            'father_name',
            'godfather_name',
            'godmother_name',
            'contact_no',
            'email',
            'remark'
        ]
        widgets = {
            'date_of_baptism': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'time_of_baptism': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'dob': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }
        
    def clean_contact_no(self):
        contact_no = self.cleaned_data.get('contact_no')
        if not contact_no.isdigit():
            raise forms.ValidationError("Contact number must contain only digits.")
        if len(contact_no) != 10:
            raise forms.ValidationError("Contact number must be exactly 10 digits.")
        return contact_no


class ParishDetailsForm(forms.ModelForm):
    class Meta:
        model = ParishDetails
        fields = [
            'deanery', 'name_of_parish', 'place_of_parish', 
            'address', 'email', 'contact_no', 'status'
        ]
        widgets = {
            'address': forms.Textarea(attrs={'rows': 4}),
        }

    def clean_contact_no(self):
        contact_no = self.cleaned_data.get('contact_no')
        if not contact_no.isdigit():
            raise forms.ValidationError("Contact number must contain only digits.")
        if len(contact_no) != 10:
            raise forms.ValidationError("Contact number must be exactly 10 digits.")
        return contact_no


class BaptismAdvancedForm(forms.ModelForm):
    class Meta:
        model = BaptismAdvanced
        fields = [
            'basic_baptism_id',
            'q_id',
            'priest_id',
            'question',
            'question_type',
            'compulsary',
            'status',
            'field_id',
            'data_varchar',
        ]
        widgets = {
            'question': forms.Textarea(attrs={'rows': 4}),
        }

class FieldTableForm(forms.ModelForm):
    class Meta:
        model = FieldTable
        fields = ['order_no', 'type', 'data', 'choice', 'q_id', 'status']
        widgets = {
            'type': forms.Select(attrs={'class': 'form-control'}),
            'data': forms.Textarea(attrs={'class': 'form-control'}),
            'choice': forms.Select(attrs={'class': 'form-control'}),
            'order_no': forms.NumberInput(attrs={'class': 'form-control'}),
            'q_id': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }



from .models import Answer,Question

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['q_id', 'basic_baptism_id', 'option_id','advanced_baptism_id', 'text_answer','status']  # Exclude answer_id since it's auto-generated




class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['q_id','order_id', 'question_text','section' ,'answer_type', 'expand_question', 'compulsary', 'status']
        widgets = {
            'section': forms.Select(attrs={'class': 'form-control'}),
            'answer_type': forms.Select(attrs={'class': 'form-control'}),
            'compulsary': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }



class OptionForm(forms.ModelForm):
    class Meta:
        model = Option
        fields = ['q_id', 'value', 'status', 'type']
        widgets = {
            'value': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter option value'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'q_id': 'Question ID',
            'value': 'Option Value',
            'status': 'Status',
            'type': 'Option Type',
        }


from django import forms
from .models import Deanery

class DeaneryForm(forms.ModelForm):
    class Meta:
        model = Deanery
        fields = ['deanery_name','dean_name','address','status']  # Exclude 'deanery_id' and 'created_time' (auto-generated)



from django import forms
from django.contrib.auth.hashers import make_password
from .models import LoginDetails

class SecretaryLoginForm(forms.Form):
    user_name = forms.CharField(max_length=255, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), required=True)

class SecretaryRegistrationForm(forms.ModelForm):
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}), required=True
    )

    class Meta:
        model = LoginDetails
        fields = ['user_name', 'password', 'contact_no', 'email']
        widgets = {
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'user_name': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_no': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")
        
        return cleaned_data  # Ensure valid data is returned

    def save(self, commit=True):
        user = super().save(commit=False)
        user.password = make_password(self.cleaned_data["password"])  # Encrypt password
        user.role = "Secretary"  # Set default role
        if commit:
            user.save()
        return user
    
    def clean_contact_no(self):
        contact_no = self.cleaned_data.get('contact_no')
        if not contact_no.isdigit():
            raise forms.ValidationError("Contact number must contain only digits.")
        if len(contact_no) != 10:
            raise forms.ValidationError("Contact number must be exactly 10 digits.")
        return contact_no
    

class UserLoginForm(forms.Form):
    user_name = forms.CharField(max_length=255, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), required=True)
    
class UserRegistrationForm(forms.ModelForm):
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}), required=True
    )

    class Meta:
        model = LoginDetails
        fields = ['user_name', 'password', 'contact_no', 'email']
        widgets = {
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'user_name': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_no': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")
        
        return cleaned_data  # Ensure valid data is returned

    def save(self, commit=True):
        user = super().save(commit=False)
        user.password = make_password(self.cleaned_data["password"])  # Encrypt password
        user.role = "User"  # Default role for users
        if commit:
            user.save()
        return user
    
    def clean_contact_no(self):
        contact_no = self.cleaned_data.get('contact_no')
        if not contact_no.isdigit():
            raise forms.ValidationError("Contact number must contain only digits.")
        if len(contact_no) != 10:
            raise forms.ValidationError("Contact number must be exactly 10 digits.")
        return contact_no


class PriestLoginForm(forms.Form):
    user_name = forms.CharField(max_length=255, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), required=True)

class PriestRegistrationForm(forms.ModelForm):
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}), required=True
    )

    class Meta:
        model = LoginDetails
        fields = ['user_name', 'password', 'contact_no', 'email', 'parish']
        widgets = {
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'user_name': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_no': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'parish': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")

        return cleaned_data  # Ensure valid data is returned

    def save(self, commit=True):
        priest = super().save(commit=False)
        priest.password = make_password(self.cleaned_data["password"])  # Encrypt password
        priest.role = "Priest"  # Assign "Priest" role
        if commit:
            priest.save()
        return priest
    
    def clean_contact_no(self):
        contact_no = self.cleaned_data.get('contact_no')
        if not contact_no.isdigit():
            raise forms.ValidationError("Contact number must contain only digits.")
        if len(contact_no) != 10:
            raise forms.ValidationError("Contact number must be exactly 10 digits.")
        return contact_no