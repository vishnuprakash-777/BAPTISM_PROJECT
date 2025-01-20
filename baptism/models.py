from django.db import models
from django.utils.timezone import now
 # Final save to commit changes

from django.db import models
from django.utils.timezone import now

from django.core.mail import send_mail
from django.db.models.signals import post_delete
from django.dispatch import receiver

class Deanery(models.Model):
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    ]
    deanery_id = models.AutoField(primary_key=True)
    deanery_name = models.CharField(max_length=255, null=False)
    dean_name = models.CharField(max_length=255, null=False)
    address = models.CharField(max_length=255, null=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.deanery_name

class ParishDetails(models.Model):
    parish_id = models.AutoField(primary_key=True)
    deanery = models.ForeignKey(Deanery, on_delete=models.CASCADE,null=True, 
    blank=True)  # Foreign key to Deanery
    name_of_parish = models.CharField(max_length=255)
    place_of_parish = models.CharField(max_length=255)
    address = models.TextField()
    email = models.EmailField()
    contact_no = models.CharField(max_length=15)
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Active')
    created_time = models.DateTimeField(default=now)

    def __str__(self):
        return self.name_of_parish

    @property
    def deanery_name(self):
        return self.deanery.deanery_name if self.deanery else None

class Baptism(models.Model):
    basic_baptism_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(default=1)  # Default value
    place_of_baptism = models.ForeignKey(ParishDetails, on_delete=models.SET_NULL, null=True, blank=True)  # Foreign key to ParishDetails
    date_of_baptism = models.DateField()
    time_of_baptism = models.TimeField()
    child_name_first = models.CharField(max_length=255)
    child_name_second = models.CharField(max_length=255)
    dob = models.DateField()
    mother_name = models.CharField(max_length=255)
    father_name = models.CharField(max_length=255)
    godfather_name = models.CharField(max_length=255)
    godmother_name = models.CharField(max_length=255)
    remark = models.CharField(max_length=255, default='Nil')
    contact_no = models.CharField(max_length=15)
    email = models.EmailField()
    advanced_baptism_id = models.IntegerField(editable=False, null=True)  # Non-editable and nullable
    priest_id = models.IntegerField(default=1)
    created_time = models.DateTimeField(default=now)
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')

    def save(self, *args, **kwargs):
        # Automatically increment user_id if not set
        if not self.user_id:
            last_user_id = Baptism.objects.aggregate(models.Max('user_id'))['user_id__max']
            self.user_id = (last_user_id or 0) + 1

        # Only set advanced_baptism_id after creating the record to generate basic_baptism_id
        if not self.pk:  # This block runs only when creating a new record
            super().save(*args, **kwargs)  # First save to generate basic_baptism_id
            self.advanced_baptism_id = self.basic_baptism_id  # Set advanced_baptism_id to basic_baptism_id
        else:
            self.advanced_baptism_id = self.basic_baptism_id  # Update advanced_baptism_id if not a new record

        super().save(*args, **kwargs)  # Final save to commit changes

    @property
    def place_of_baptism_name(self):
        if self.place_of_baptism:
            return self.place_of_baptism.name_of_parish
        return None
    

   
    
class LoginDetails(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=50)
    last_login = models.DateTimeField(default=now)
    contact_no = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Active')
    parish_id = models.IntegerField(default=1)

    def __str__(self):
        return self.user_name
    


from django.db import models
from django.utils.timezone import now

class BaptismAdvanced(models.Model):
    advanced_baptism_id = models.AutoField(primary_key=True)
    basic_baptism_id = models.IntegerField()
    q_id = models.IntegerField()
    priest_id = models.IntegerField()
    question = models.TextField()
    QUESTION_CHOICES = [
        ('MULTIPLE', 'MULTIPLE'),
        ('MULTIPLE-SELECT','MULTIPLE-SELECT'),
        ('TEXT-AREA','TEXT-AREA')
    ]
    question_type = models.CharField(max_length=255,choices=QUESTION_CHOICES,default='MULTIPLE')
    compulsary = models.BooleanField()  # True for compulsary, False otherwise
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Active')
    created_time = models.DateTimeField(default=now)
    field_id = models.IntegerField()
    data_varchar = models.CharField(max_length=255)

    def __str__(self):
        return f"Advanced Baptism {self.advanced_baptism_id}"


class FieldTable(models.Model):
    field_id = models.AutoField(primary_key=True)
    order_no = models.IntegerField()
    TYPE_CHOICES = [
        ('READING', 'READING'),
        ('SONG','SONG'),
        ('PRAYER','PRAYER'),
        ('REMARKS','REMARKS'),
        ('AUTHORIZATION','AUTHORIZATION'),
        ('FINANCIAL','FINANCIAL'),
        ('SPECIAL SAINTS','SPECIAL SAINTS'),
    ]
    type = models.CharField(max_length=20,choices=TYPE_CHOICES,default='READING')
    data = models.TextField()
    QUESTION_CHOICES = [
        ('MULTIPLE', 'MULTIPLE'),
        ('MULTIPLE-SELECT','MULTIPLE-SELECT'),
        ('TEXT-AREA','TEXT-AREA'),
    ]
    choice = models.CharField(max_length=20,choices=QUESTION_CHOICES,default='MULTIPLE')
    q_id = models.IntegerField()
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Active')
    created_time = models.DateTimeField(default=now)

    def __str__(self):
        return f"Field {self.field_id}: {self.type} (Order {self.order_no})"

class Answer(models.Model):
    answer_id = models.AutoField(primary_key=True)
    q_id = models.IntegerField(null=False)
    basic_baptism_id = models.IntegerField(null=False)
    option_id = models.CharField(max_length=255,null=True, blank=True)  
    text_answer = models.CharField(max_length=255, null=True, blank=True)  # Optional field for text answers
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Active')
    created_time = models.DateTimeField(default=now)
    advanced_baptism_id = models.IntegerField(null=False)



class Question(models.Model):
    ANSWER_TYPE_CHOICES = [
        ('radio', 'Radio'),
        ('text', 'Text'),
        ('checkbox','Checkbox')
    ]
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]
    COMPULSORY_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]
    CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]
    SECTION_CHOICES = [
        ('READING DETAILS', 'READING DETAILS'),
        ('THE PRAYER OF THE ASSEMBLY','THE PRAYER OF THE ASSEMBLY'),
        ('SPECIAL SAINTS TO COMMEMORATE','SPECIAL SAINTS TO COMMEMORATE'),
        ('SONG SELECTION','SONG SELECTION'),
        ('REMARKS','REMARKS'),
        ('AUTHORIZATION','AUTHORIZATION'),
        ('FINANCIAL PARTICIPATION','FINANCIAL PARTICIPATION'),
    ]


    q_id = models.AutoField(primary_key=True)
    order_id = models.IntegerField(unique=True)
    question_text = models.CharField(max_length=255)
    section = models.CharField(max_length=50,choices=SECTION_CHOICES)
    answer_type = models.CharField(max_length=10, choices=ANSWER_TYPE_CHOICES)
    expand_question = models.CharField(max_length=3, choices=CHOICES)
    compulsary = models.CharField(max_length=3, choices=COMPULSORY_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    created_time = models.DateTimeField(default=now)

    def __str__(self):
        return f" (QID: {self.q_id})"


from django.db import models
 # Assuming Question model is in a file named `question`

class Option(models.Model):
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    ]

    TYPE_CHOICES = [
        ('Radio', 'Radio'),
        ('Text', 'Text'),
        ('Checkbox','Checkbox')

    ]
    
    option_id = models.AutoField(primary_key=True)
    q_id = models.ForeignKey(Question, on_delete=models.CASCADE, to_field='q_id', related_name='options')
    value = models.CharField(max_length=255)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Active')
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='Radio')
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Option {self.option_id}: {self.value}"
    
    
class Certificate(models.Model):
    certificate_id = models.AutoField(primary_key=True)
    certificate_code = models.CharField(max_length=6, unique=True)
    child_name = models.CharField(max_length=255)
    certificate_date = models.DateField()
    parish_name = models.CharField(max_length=255)
    qr_code_url = models.URLField(max_length=200, null=True, blank=True)  # Store the URL of the QR code image
    qr_code = models.ImageField(upload_to='qr_codes/', null=True, blank=True)

    def __str__(self):
        return f"{self.certificate_code} - {self.child_name}"

    



