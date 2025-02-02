from django.urls import path
from .views import (
    baptism_form_view, 
    upload_parish_details, 
    success_page, 
    upload_baptism_advanced, 
    upload_field_table,
    field_table_list, 
    field_table_add, 
    field_table_edit, 
    field_table_delete,
    baptism_advanced_list, 
    baptism_advanced_add, 
    baptism_advanced_edit, 
    baptism_advanced_delete,
    parish_details_list,
    parish_details_add,
    parish_details_edit,
    parish_details_delete,
    baptism_list,
    baptism_add,
    baptism_edit,
    baptism_delete,
    upload_answer_details,
    answer_list,
    answer_add,
    answer_edit,
    answer_delete,
    upload_question,
    upload_option,
    option_list,
    option_add,
    option_delete,
    option_edit,
    question_list,
    question_add,
    question_edit,
    question_delete,
    section_questions,
    home_page,
    upload_deanery,
    deanery_add,
    deanery_edit,
    deanery_list,
    deanery_delete,
    baptism_list_and_edit,
    approved_baptisms,
    generate_certificate,
    baptism_dashboard,
    certificate_add,
    certificate_delete,
    certificate_edit,
    certificate_list,
    verify_certificate,
    certificate_details,
    example,
    approved_baptisms2,
    pending_baptisms,
    rejected_baptisms,
    secretary_login,
    secretary_register,
    logout_user
    


)

urlpatterns = [
    # Existing URLs
    path('add/', baptism_form_view, name='add_baptism'),
    path('', home_page, name='home_page'), 
    path('upload-parish/', upload_parish_details, name='upload_parish'),
    path('parish-success/', success_page, name='parish_success'),
    path('upload-baptism-advanced/', upload_baptism_advanced, name='upload_baptism_advanced'),
    path('upload-field/', upload_field_table, name='upload_field'),
    path('upload-answer/',upload_answer_details , name='upload_answer_details'),
    path('upload-question/', upload_question, name='upload_question'),
    path('upload-option/', upload_option, name='upload_option'),
    path('upload-deanery/',upload_deanery,name='upload_deaneryp'),
    path('field-table-success/', success_page, name='field_table_success'), 

    # FieldTable URLs
    path('field_table_list/', field_table_list, name='field_table_list'),
    path('fields/', field_table_list, name='field_list'), 
    path('fields/add/', field_table_add, name='field_add'), 
    path('fields/edit/<int:pk>/', field_table_edit, name='field_table_edit'),
    path('fields/delete/<int:field_id>/', field_table_delete, name='field_delete'),

    # BaptismAdvanced URLs
    path('baptism-advanced/', baptism_advanced_list, name='baptism_advanced_list'),  # Listing page
    path('baptism-advanced/add/', baptism_advanced_add, name='baptism_advanced_add'),  # Add page
    path('baptism-advanced/edit/<int:pk>/', baptism_advanced_edit, name='baptism_advanced_edit'),  # Edit page
    path('baptism-advanced/delete/<int:advanced_baptism_id>/', baptism_advanced_delete, name='baptism_advanced_delete'),  # Delete page


    path('parishes/', parish_details_list, name='parish_details_list'),
    path('parishes/add/', parish_details_add, name='parish_details_add'),
    path('parishes/edit/<int:pk>/', parish_details_edit, name='parish_details_edit'),
    path('parishes/delete/<int:parish_id>/', parish_details_delete, name='parish_details_delete'),

    path('baptisms/', baptism_list, name='baptism_list'),  # List baptisms
    path('baptisms/add/', baptism_add, name='baptism_add'),  # Add new baptism
    path('baptisms/edit/<int:pk>/', baptism_edit, name='baptism_edit'),  # Edit existing baptism
    path('baptisms/delete/<int:baptism_id>/', baptism_delete, name='baptism_delete'),  # Delete     

    path('answers/', answer_list, name='answer_list'),
    path('answers/add/', answer_add, name='answer_add'),
    path('answers/edit/<int:pk>/', answer_edit, name='answer_edit'),
    path('answers/delete/<int:answer_id>/', answer_delete, name='answer_delete'),

    path('deaneries/', deanery_list, name='deanery_list'),
    path('deaneries/add/', deanery_add, name='deanery_add'),
    path('deaneries/edit/<int:pk>/', deanery_edit, name='deanery_edit'),
    path('deaneries/delete/<int:deanery_id>/', deanery_delete, name='deanery_delete'),

    path('options/', option_list, name='option_list'),
    path('options/add/', option_add, name='option_add'),
    path('options/edit/<int:pk>/', option_edit, name='option_edit'),
    path('options/delete/<int:option_id>/', option_delete, name='option_delete'),

    path('questions/', question_list, name='question_list'),
    path('questions/add/',question_add, name='question_add'),
    path('questions/edit/<int:pk>/',question_edit, name='question_edit'),
    path('questions/delete/<int:question_id>/',question_delete, name='question_delete'),

    path('certificates/', certificate_list, name='certificate_list'),
    #path('certificates/add/', certificate_add, name='certificate_add'),
    #path('certificates/edit/<int:pk>/', certificate_edit, name='certificate_edit'),
    #path('certificates/delete/<int:certificate_id>/', certificate_delete, name='certificate_delete'),

    path('section/', home_page, name='home_page'),
    path('section/<str:section_name>/', section_questions, name='section_questions'),

    path('dashboard/manage-baptism/', baptism_list_and_edit, name='baptism_list_and_edit'),



    path('dashboard/', baptism_dashboard, name='baptism_dashboard'),
    path('dashboard/approved-baptisms/', approved_baptisms, name='approved_baptisms'),
    path('generate-certificate/<int:id>/', generate_certificate, name='generate_certificate'),
    path('verify/', verify_certificate, name='verify_certificate'),
    path('verify/<str:certificate_code>/', certificate_details, name='certificate_details'),
    path('example/',example,name='example'),

    path('dashboard/approved/', approved_baptisms2, name='approved_baptisms2'),
    path('dashboard/rejected/', rejected_baptisms, name='rejected_baptisms'),
    path('dashboard/pending/', pending_baptisms, name='pending_baptisms'),

    path("login/", secretary_login, name="secretary_login"),
    path("register/", secretary_register, name="secretary_register"),
    path("logout/", logout_user, name="logout"),


]





