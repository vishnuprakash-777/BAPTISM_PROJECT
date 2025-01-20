
from django.contrib import admin
from .models import Baptism,ParishDetails,LoginDetails,BaptismAdvanced,FieldTable,Answer,Question,Option
@admin.register(Baptism)
class BaptismAdmin(admin.ModelAdmin):
    list_display = (
        'basic_baptism_id', 'child_name_first', 'child_name_second',
        'place_of_baptism', 'date_of_baptism', 'status'
    )
    search_fields = ('child_name_first', 'child_name_second', 'place_of_baptism')
    list_filter = ('status', 'date_of_baptism')

@admin.register(ParishDetails)
class ParishDetailsAdmin(admin.ModelAdmin):
    list_display = ('parish_id', 'name_of_parish', 'place_of_parish', 'status', 'created_time')
    list_filter = ('status',)
    search_fields = ('name_of_parish', 'place_of_parish')




@admin.register(LoginDetails)
class LoginDetailsAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'email', 'contact_no', 'role', 'status', 'last_login', 'parish_id')
    search_fields = ('user_name', 'email', 'contact_no')
    list_filter = ('role', 'status', 'parish_id')
    ordering = ('-last_login',)

    fieldsets = (
        (None, {
            'fields': ('user_name', 'password', 'email', 'contact_no', 'role', 'status', 'parish_id')
        }),
        ('Timestamps', {
            'fields': ('last_login',)
        }),
    )
    readonly_fields = ('last_login',)  # Make last_login read-only in the admin panel

    def save_model(self, request, obj, form, change):
        """
        Override save_model to hash the password before saving in the admin panel.
        """
        if 'password' in form.changed_data:
            from django.contrib.auth.hashers import make_password
            obj.password = make_password(obj.password)
        super().save_model(request, obj, form, change)




@admin.register(BaptismAdvanced)
class BaptismAdvancedAdmin(admin.ModelAdmin):
    list_display = ('advanced_baptism_id', 'basic_baptism_id', 'question', 'question_type', 'compulsary', 'status', 'created_time')
    search_fields = ('question', 'question_type')
    list_filter = ('status', 'compulsary')
    ordering = ('-created_time',)



@admin.register(FieldTable)
class FieldTableAdmin(admin.ModelAdmin):
    list_display = ('field_id', 'order_no', 'type', 'q_id', 'status', 'created_time')
    list_filter = ('status', 'created_time')
    search_fields = ('type', 'data', 'choice')

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('answer_id', 'q_id', 'basic_baptism_id','advanced_baptism_id', 'option_id', 'text_answer')  # Displayed columns in the admin panel
    search_fields = ('answer_id', 'q_id', 'basic_baptism_id','advanced_baptism_id' ,'option_id', 'text_answer')  # Search functionality
    list_filter = ('q_id', 'basic_baptism_id','advanced_baptism_id')  # Filters in the sidebar
    ordering = ('answer_id',)  # Default ordering of the records


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('q_id', 'order_id', 'question_text', 'answer_type', 'expand_question', 'status', 'created_time')
    list_filter = ('q_id', 'answer_type', 'created_time')
    search_fields = ('question_text', 'expand_question', 'q_id')
    ordering = ('order_id',)
    



@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ('option_id', 'q_id', 'value', 'status', 'type', 'created_time')
    list_filter = ('status', 'type', 'created_time')
    search_fields = ('value',)


from django.contrib import admin
from .models import Deanery

@admin.register(Deanery)
class DeaneryAdmin(admin.ModelAdmin):
    list_display = ('deanery_id', 'deanery_name', 'status', 'created_time')
    search_fields = ('deanery_name', 'status')
    list_filter = ('status',)


from .models import Certificate

@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    # Fields to display in the admin list view
    list_display = ('certificate_id', 'certificate_code', 'child_name', 'certificate_date', 'parish_name','qr_code_url','qr_code')
    # Fields to make searchable
    search_fields = ('certificate_code', 'child_name', 'parish_name')
    # Fields to filter by
    list_filter = ('certificate_date', 'parish_name')
    # Fields to display as readonly
    readonly_fields = ('certificate_id',)

    # Optionally customize how the admin form orders fields
    fieldsets = (
        (None, {
            'fields': ('certificate_code', 'child_name', 'certificate_date', 'parish_name','qr_code_url','qr_code')
        }),
    )