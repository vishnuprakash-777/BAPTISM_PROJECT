from django.shortcuts import render, redirect
from .forms import BaptismForm,ParishDetailsForm,BaptismAdvancedForm,FieldTableForm,AnswerForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from datetime import datetime
from django.core.paginator import Paginator
from django.shortcuts import render
from .models import FieldTable

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Baptism, ParishDetails
from .forms import BaptismForm

def baptism_form_view(request):
    parishes = ParishDetails.objects.all()
    user_id = request.session.get("user_id")  # Retrieve user_id from session

    if request.method == "POST":
        form = BaptismForm(request.POST)
        if form.is_valid():
            baptism = form.save(commit=False)
            baptism.user_id = user_id  # Assign logged-in user_id
            baptism.save()
            messages.success(request, "Baptism details submitted successfully!")
            return redirect('field_table_success')  # Ensure this URL exists
        else:
            messages.error(request, "Please correct the errors below.")
            print(form.errors)  # Debugging

    else:
        form = BaptismForm()

    return render(request, 'baptism/baptism_form.html', {'form': form, 'parishes': parishes, 'user_id': user_id})



from django.shortcuts import redirect

def upload_parish_details(request):
    if request.method == 'POST':
        form = ParishDetailsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('field_table_success')  # Redirect to the success page
    else:
        form = ParishDetailsForm()
    return render(request, 'baptism/upload_parish_details.html', {'form': form})


def success_page(request):
    return render(request, 'baptism/success.html')








def upload_baptism_advanced(request):
    if request.method == 'POST':
        form = BaptismAdvancedForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('field_table_success')  # Redirect to the desired page
    else:
        form = BaptismAdvancedForm()
    return render(request, 'baptism/upload_baptism_advanced.html', {'form': form})



def upload_field_table(request):
    if request.method == 'POST':
        form = FieldTableForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('field_table_success')  # Update this with your success page URL name
    else:
        form = FieldTableForm()
    
    return render(request, 'baptism/upload_field_table.html', {'form': form})

from django.shortcuts import render, get_object_or_404, redirect
from .models import FieldTable,BaptismAdvanced

def field_table_list(request):
    query = request.GET.get('q', '')
    fields = FieldTable.objects.all()

    if query:
        fields = fields.filter(field_id__icontains=query) | fields.filter(q_id__icontains=query)

    paginator = Paginator(fields, 10)  # Show 10 fields per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'field_table_list.html', {'page_obj': page_obj, 'query': query})

from django.http import HttpResponse

def field_table_add(request):
    if request.method == 'POST':
        form = FieldTableForm(request.POST)
        if form.is_valid():
            form.save()  # This will save the new record in the database
            return redirect('field_table_list')  # Redirect to list page after saving
    else:
        form = FieldTableForm()
    return render(request, 'field_table_add.html', {'form': form})

def field_table_edit(request, pk):
    field_table = get_object_or_404(FieldTable, pk=pk)  # Retrieve the existing record
    if request.method == 'POST':
        form = FieldTableForm(request.POST, instance=field_table)  # Bind form to the existing record
        if form.is_valid():
            form.save()  # This will update the existing record in the database
            return redirect('field_table_list')  # Redirect to list page after saving
    else:
        form = FieldTableForm(instance=field_table)  # Prepopulate the form with the existing record's data
    return render(request, 'field_table_edit.html', {'form': form})

def field_table_delete(request, field_id):
    field = get_object_or_404(FieldTable, pk=field_id)
    field.delete()
    return redirect('field_list')

  # Ensure you import your model



from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from .models import BaptismAdvanced
from .forms import BaptismAdvancedForm

# List View
def baptism_advanced_list(request):
    query = request.GET.get('q', '')
    baptisms = BaptismAdvanced.objects.all()

    if query:
        baptisms = baptisms.filter(q_id__icontains=query) | baptisms.filter(field_id__icontains=query)

    paginator = Paginator(baptisms, 10)  # Show 10 records per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'baptism_advanced_list.html', {'page_obj': page_obj, 'query': query})

# Add View
def baptism_advanced_add(request):
    if request.method == 'POST':
        form = BaptismAdvancedForm(request.POST)
        if form.is_valid():
            form.save()  # Save the new record in the database
            return redirect('baptism_advanced_list')  # Redirect to list page
    else:
        form = BaptismAdvancedForm()
    return render(request, 'baptism_advanced_add.html', {'form': form})

# Edit View
def baptism_advanced_edit(request, pk):
    baptism = get_object_or_404(BaptismAdvanced, pk=pk)  # Retrieve the existing record
    if request.method == 'POST':
        form = BaptismAdvancedForm(request.POST, instance=baptism)  # Bind form to the existing record
        if form.is_valid():
            form.save()  # Update the existing record in the database
            return redirect('baptism_advanced_list')  # Redirect to list page
    else:
        form = BaptismAdvancedForm(instance=baptism)  # Prepopulate form with the existing data
    return render(request, 'baptism_advanced_edit.html', {'form': form})

# Delete View
def baptism_advanced_delete(request, advanced_baptism_id):
    baptism = get_object_or_404(BaptismAdvanced, pk=advanced_baptism_id)
    baptism.delete()  # Delete the record from the database
    return redirect('baptism_advanced_list')


from .models import ParishDetails


# List view with search and pagination
def parish_details_list(request):
    query = request.GET.get('q', '')
    parishes = ParishDetails.objects.all()

    if query:
        parishes = parishes.filter(name_of_parish__icontains=query) | parishes.filter(place_of_parish__icontains=query)

    paginator = Paginator(parishes, 10)  # Show 10 parishes per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'parish_details_list.html', {'page_obj': page_obj, 'query': query})

# Add new parish view
def parish_details_add(request):
    deaneries = Deanery.objects.all()  # Fetch all deanery options
    if request.method == 'POST':
        form = ParishDetailsForm(request.POST)
        if form.is_valid():
            form.save()  # Save the new parish record
            return redirect('parish_details_list')  # Redirect to list page after saving
    else:
        form = ParishDetailsForm()
    return render(request, 'parish_details_add.html', {'form': form,'deaneries': deaneries},)

# Edit existing parish view
def parish_details_edit(request, pk):
    deaneries = Deanery.objects.all() 
    parish = get_object_or_404(ParishDetails, pk=pk)  # Retrieve the existing parish record
    if request.method == 'POST':
        form = ParishDetailsForm(request.POST, instance=parish)  # Bind form to existing record
        if form.is_valid():
            form.save()  # Update the parish record
            return redirect('parish_details_list')  # Redirect to list page after saving
    else:
        form = ParishDetailsForm(instance=parish)  # Prepopulate form with existing parish data
    return render(request, 'parish_details_edit.html', {'form': form,'deaneries': deaneries,'parish': parish})

# Delete parish view
def parish_details_delete(request, parish_id):
    parish = get_object_or_404(ParishDetails, pk=parish_id)
    parish.delete()  # Delete the parish record
    return redirect('parish_details_list')  # Redirect to the list page after deletion


from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.core.paginator import Paginator
from .models import Baptism
from .forms import BaptismForm  # Assuming you have a form for Baptism model

# View for listing Baptism records with search functionality
def baptism_list(request):
    query = request.GET.get('q', '')
    baptisms = Baptism.objects.all()

    if query:
       baptisms = baptisms.filter(basic_baptism_id__icontains=query) | baptisms.filter(child_name_first__icontains=query) | baptisms.filter(child_name_second__icontains=query)

    paginator = Paginator(baptisms, 10)  # Show 10 baptisms per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'baptism_list.html', {'page_obj': page_obj, 'query': query})

# View for adding a new Baptism record
def baptism_add(request):
    if request.method == 'POST':
        form = BaptismForm(request.POST)
        if form.is_valid():
            form.save()  # Save the new baptism record to the database
            return redirect('baptism_list')  # Redirect to baptism list page after saving
    else:
        form = BaptismForm()
    return render(request, 'baptism_add.html', {'form': form})

# View for editing an existing Baptism record
def baptism_edit(request, pk):
    baptism = get_object_or_404(Baptism, pk=pk)  # Retrieve the existing baptism record
    if request.method == 'POST':
        form = BaptismForm(request.POST, instance=baptism)  # Bind form to the existing baptism record
        if form.is_valid():
            form.save()  # Update the baptism record in the database
            return redirect('baptism_list')  # Redirect to baptism list page after saving
    else:
        form = BaptismForm(instance=baptism)  # Prepopulate the form with the baptism record data
    return render(request, 'baptism_edit.html', {'form': form})

# View for deleting a Baptism record
def baptism_delete(request, baptism_id):
    baptism = get_object_or_404(Baptism, pk=baptism_id)
    baptism.delete()
    return redirect('baptism_list')  # Redirect to the baptism list page after deletion




def upload_answer_details(request):
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('field_table_success')  # Redirect to a success page
    else:
        form = AnswerForm()
    return render(request, 'baptism/upload_answer_details.html', {'form': form})


from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from .models import Answer
from .forms import AnswerForm

# List all answers with pagination and search
def answer_list(request):
    query = request.GET.get('q', '')
    answers = Answer.objects.all()

    if query:
        answers = answers.filter(q_id__icontains=query) | answers.filter(option_id__icontains=query)

    paginator = Paginator(answers, 10)  # Show 10 answers per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'answer_list.html', {'page_obj': page_obj, 'query': query})

# Add a new answer
def answer_add(request):
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            form.save()  # Save the new answer record
            return redirect('answer_list')  # Redirect to the list page after saving
    else:
        form = AnswerForm()
    return render(request, 'answer_add.html', {'form': form})

# Edit an existing answer
def answer_edit(request, pk):
    answer = get_object_or_404(Answer, pk=pk)  # Retrieve the existing answer record
    if request.method == 'POST':
        form = AnswerForm(request.POST, instance=answer)  # Bind form to the existing record
        if form.is_valid():
            form.save()  # Update the answer record
            return redirect('answer_list')  # Redirect to the list page after saving
    else:
        form = AnswerForm(instance=answer)  # Prepopulate form with existing answer data
    return render(request, 'answer_edit.html', {'form': form,'answer': answer})

# Delete an answer
def answer_delete(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    answer.delete()  # Delete the answer record
    return redirect('answer_list')  # Redirect to the list page after deletion


from .forms import QuestionForm

def upload_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('field_table_success')  # Redirect to a list page or success page
    else:
        form = QuestionForm()
    return render(request, 'baptism/upload_question.html', {'form': form})

from django.shortcuts import render, redirect
from .forms import OptionForm

def upload_option(request):
    if request.method == 'POST':
        form = OptionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('field_table_success')  # Redirect to the option list page
    else:
        form = OptionForm()
    return render(request, 'baptism/upload_option.html', {'form': form})

from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from .models import Option,Question
from .forms import OptionForm,QuestionForm

# List all options with pagination and search
def option_list(request):
    query = request.GET.get('q', '')
    options = Option.objects.all()

    if query:
        options = options.filter(q_id__icontains=query) | options.filter(option_id__icontains=query)

    paginator = Paginator(options, 10)  # Show 10 options per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'option_list.html', {'page_obj': page_obj, 'query': query})

# Add a new option
def option_add(request):
    if request.method == 'POST':
        form = OptionForm(request.POST)
        if form.is_valid():
            form.save()  # Save the new option record
            return redirect('option_list')  # Redirect to the list page after saving
    else:
        form = OptionForm()
    questions = Question.objects.all()  # Get all questions
    return render(request, 'option_add.html', {'form': form, 'questions': questions})

# Edit an existing option
def option_edit(request, pk):
    option = get_object_or_404(Option, pk=pk)  # Retrieve the existing option record
    if request.method == 'POST':
        form = OptionForm(request.POST, instance=option)  # Bind form to the existing record
        if form.is_valid():
            form.save()  # Update the option record
            return redirect('option_list')  # Redirect to the list page after saving
    else:
        form = OptionForm(instance=option)  # Prepopulate form with existing option data
    questions = Question.objects.all()  # Get all questions
    return render(request, 'option_edit.html', {'form': form, 'questions': questions,'option': option})






# Delete an option
def option_delete(request, option_id):
    option = get_object_or_404(Option, pk=option_id)
    option.delete()  # Delete the option record
    return redirect('option_list')  # Redirect to the list page after deletion


# List of questions
def question_list(request):
    query = request.GET.get('q', '')
    questions = Question.objects.all()

    if query:
        questions = questions.filter(q_id__icontains=query) 

    paginator = Paginator(questions, 10)  # Show 10 questions per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'question_list.html', {'page_obj': page_obj, 'query': query})

# Add a new question
def question_add(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()  # Save the new question record
            return redirect('question_list')  # Redirect to the list page after saving
    else:
        form = QuestionForm()
    return render(request, 'question_add.html', {'form': form})

# Edit an existing question
def question_edit(request, pk):
    question = get_object_or_404(Question, pk=pk)  # Retrieve the existing question record
    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)  # Bind form to the existing record
        if form.is_valid():
            form.save()  # Update the question record
            return redirect('question_list')  # Redirect to the list page after saving
    else:
        form = QuestionForm(instance=question)  # Prepopulate form with existing question data
    return render(request, 'question_edit.html', {'form': form,'question': question})

# Delete a question
def question_delete(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    question.delete()  # Delete the question record
    return redirect('question_list')  # Redirect to the list page after deletion




from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import transaction
from .models import Question, Answer,Option

SECTIONS = [
    "READING DETAILS", "THE PRAYER OF THE ASSEMBLY", "SONG SELECTION", "SPECIAL SAINTS TO COMMEMORATE", "REMARKS",
    "AUTHORIZATION", "FINANCIAL PARTICIPATION"
]

SECTION_DESCRIPTIONS = {
    "READING DETAILS": "Please choose one of the reading details, Psalm or Gospel (page 25-41).",
    "THE PRAYER OF THE ASSEMBLY": "The prayer of the assembly includes selecting one from each category.",
    "SONG SELECTION": "Please select songs for the baptism celebration.",
    "SPECIAL SAINTS TO COMMEMORATE": "We add here the names of the patron saints of the child, family, and church, and finish.",
    "REMARKS": "If you have any doubts or questions, please feel free to contact Father Jomy by email or in the space below. To contact jomykollithanath@gmail.com",
    "AUTHORIZATION": "I would like to baptize my child.",
    "FINANCIAL PARTICIPATION": "You are probably wondering what you should give to the parish to compensate it for its expenses and to show your solidarity. Your parish usually suggests an indicative amount, but the amount can be adjusted according to your means. To do this, you must contact the parish secretariat. This sum is intended to cover the costs of preparation and celebration."
}

from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import transaction
from .models import Question, Answer
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import transaction
from .models import Question, Answer, Option

from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import transaction
from .models import Question, Answer

SECTIONS = [
    "READING DETAILS", "THE PRAYER OF THE ASSEMBLY", "SONG SELECTION", "SPECIAL SAINTS TO COMMEMORATE", "REMARKS",
    "AUTHORIZATION", "FINANCIAL PARTICIPATION"
]

SECTION_DESCRIPTIONS = {
    "READING DETAILS": "Please choose one of the reading details, Psalm or Gospel (page 25-41).",
    "THE PRAYER OF THE ASSEMBLY": "The prayer of the assembly includes selecting one from each category.",
    "SONG SELECTION": "Please select songs for the baptism celebration.",
    "SPECIAL SAINTS TO COMMEMORATE": "We add here the names of the patron saints of the child, family, and church, and finish.",
    "REMARKS": "If you have any doubts or questions, please feel free to contact Father Jomy by email or in the space below. To contact jomykollithanath@gmail.com",
    "AUTHORIZATION": "I would like to baptize my child.",
    "FINANCIAL PARTICIPATION": "You are probably wondering what you should give to the parish to compensate it for its expenses and to show your solidarity. Your parish usually suggests an indicative amount, but the amount can be adjusted according to your means. To do this, you must contact the parish secretariat. This sum is intended to cover the costs of preparation and celebration."
}

def section_questions(request, section_name):
    section_name = section_name.upper()
    if section_name not in SECTIONS:
        messages.error(request, "Invalid section. Redirecting to the first section.")
        return redirect('section_questions', section_name=SECTIONS[0].lower())

    questions = Question.objects.filter(section=section_name, status="active")
    current_index = SECTIONS.index(section_name)
    prev_section = SECTIONS[current_index - 1].lower() if current_index > 0 else None
    next_section = SECTIONS[current_index + 1].lower() if current_index < len(SECTIONS) - 1 else None
    section_description = SECTION_DESCRIPTIONS.get(section_name, "")

    if request.method == "POST":
        try:
            with transaction.atomic():
                for question in questions:
                    answer_data = request.POST.getlist(f"answer_{question.q_id}")

                    # Validate compulsory questions
                    if question.compulsary == "yes" and not answer_data:
                        messages.error(request, f"Question {question.order_id} is compulsory and must be answered.")
                        break
                else:
                    # Save answers
                    for question in questions:
                        answer_data = request.POST.getlist(f"answer_{question.q_id}")
                        answer = Answer(
                            q_id=question.q_id,
                            basic_baptism_id=1,  # Replace with the actual ID
                            advanced_baptism_id=1,  # Example: user ID
                            status="active"
                        )

                        if question.answer_type == "text":
                            answer.text_answer = answer_data[0] if answer_data else None
                        elif question.answer_type == "radio":
                            answer.option_id = answer_data[0] if answer_data else None
                        elif question.answer_type == "checkbox":
                            answer.option_id = ",".join(answer_data) if answer_data else None

                        answer.save()

                    # Redirect based on section
                    if next_section:
                        return redirect('section_questions', section_name=next_section)
                    else:
                        messages.success(request, "You have completed the questionnaire!")
                        return redirect('field_table_success')

        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")

    context = {
        "section_name": section_name.capitalize(),
        "section_description": section_description,
        "questions": questions,
        "prev_section": prev_section,
        "next_section": next_section,
        "is_last_section": next_section is None,
    }
    return render(request, "section_questions.html", context)










from django.shortcuts import render, redirect
from .models import Baptism  # Import the Baptism model

def home_page(request):
    user_id = request.session.get("user_id")  # Retrieve user_id from session

    if not user_id:
        return redirect("user_login")  # Redirect to login if user is not logged in

    # Fetch all baptism records associated with the logged-in user
    baptisms = Baptism.objects.filter(user_id=user_id).order_by('-created_time')

    return render(request, "baptism/home.html", {"user_id": user_id, "baptisms": baptisms})



from django.shortcuts import render, redirect
from .forms import DeaneryForm

def upload_deanery(request):
    if request.method == 'POST':
        form = DeaneryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('field_table_success')  # Redirect to a success page after submission
    else:
        form = DeaneryForm()
    
    return render(request, 'baptism/upload_deanery.html', {'form': form})

from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from .models import Deanery
from .forms import DeaneryForm

# List all deaneries
def deanery_list(request):
    query = request.GET.get('q', '')
    deaneries = Deanery.objects.all()

    if query:
        deaneries = deaneries.filter(deanery_name__icontains=query) | deaneries.filter(deanery_id__icontains=query)

    paginator = Paginator(deaneries, 10)  # Show 10 deaneries per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'deanery_list.html', {'page_obj': page_obj, 'query': query})

# Add a new deanery
def deanery_add(request):
    if request.method == 'POST':
        form = DeaneryForm(request.POST)
        if form.is_valid():
            form.save()  # Save the new deanery record
            return redirect('deanery_list')  # Redirect to the list page after saving
    else:
        form = DeaneryForm()
    return render(request, 'deanery_add.html', {'form': form})

# Edit an existing deanery
def deanery_edit(request, pk):
    deanery = get_object_or_404(Deanery, pk=pk)  # Retrieve the existing deanery record
    if request.method == 'POST':
        form = DeaneryForm(request.POST, instance=deanery)  # Bind form to the existing record
        if form.is_valid():
            form.save()  # Update the deanery record
            return redirect('deanery_list')  # Redirect to the list page after saving
    else:
        form = DeaneryForm(instance=deanery)  # Prepopulate form with existing deanery data
    return render(request, 'deanery_edit.html', {'form': form,'deanery': deanery})

# Delete a deanery
def deanery_delete(request, deanery_id):
    deanery = get_object_or_404(Deanery, pk=deanery_id)
    deanery.delete()  # Delete the deanery record
    return redirect('deanery_list')  # Redirect to the list page after deletion


from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.http import HttpResponseBadRequest
from .models import Certificate

# List all certificates with search and pagination
def certificate_list(request):
    query = request.GET.get('q', '')
    certificates = Certificate.objects.all()

    if query:
        certificates = certificates.filter(
            certificate_code__icontains=query
        ) | certificates.filter(
            child_name__icontains=query
        ) | certificates.filter(
            parish_name__icontains=query
        )

    paginator = Paginator(certificates, 10)  # Show 10 certificates per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'certificate_list.html', {'page_obj': page_obj, 'query': query})

# Add a new certificate
def certificate_add(request):
    if request.method == 'POST':
        certificate_code = request.POST.get('certificate_code')
        child_name = request.POST.get('child_name')
        certificate_date = request.POST.get('certificate_date')
        parish_name = request.POST.get('parish_name')

        if all([certificate_code, child_name, certificate_date, parish_name]):
            Certificate.objects.create(
                certificate_code=certificate_code,
                child_name=child_name,
                certificate_date=certificate_date,
                parish_name=parish_name
            )
            return redirect('certificate_list')
        else:
            return HttpResponseBadRequest('All fields are required.')
    return render(request, 'certificate_add.html')

# Edit an existing certificate
def certificate_edit(request, pk):
    certificate = get_object_or_404(Certificate, pk=pk)
    if request.method == 'POST':
        certificate.certificate_code = request.POST.get('certificate_code', certificate.certificate_code)
        certificate.child_name = request.POST.get('child_name', certificate.child_name)
        certificate.certificate_date = request.POST.get('certificate_date', certificate.certificate_date)
        certificate.parish_name = request.POST.get('parish_name', certificate.parish_name)

        certificate.save()
        return redirect('certificate_list')
    return render(request, 'certificate_edit.html', {'certificate': certificate})

# Delete a certificate
def certificate_delete(request, certificate_id):
    certificate = get_object_or_404(Certificate, pk=certificate_id)
    certificate.delete()
    return redirect('certificate_list')




# views.py

from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render
from .models import Baptism

def baptism_list_and_edit(request):
    if request.method == 'POST':
        baptism_id = request.POST.get('baptism_id')
        new_status = request.POST.get('status')
        if baptism_id and new_status:
            baptism = Baptism.objects.get(pk=baptism_id)
            baptism.status = new_status
            baptism.save()

            parish = baptism.place_of_baptism
            if parish:
                parish_name = parish.name_of_parish
                parish_email = parish.email
                parish_contact_no = parish.contact_no
            else:
                parish_name = 'the parish'
                parish_email = 'N/A'
                parish_contact_no = 'N/A'

            if new_status == 'Approved':
                subject = "Baptism Request Approved"
                subject = "Baptism Request Approved"
                message = (
                    f"Your baptism request has been approved.\n\n"
                    f"Details:\n"
                    f"Time: {baptism.time_of_baptism}\n"
                    f"Date: {baptism.date_of_baptism}\n"
                    f"Child Name: {baptism.child_name_first} {baptism.child_name_second}\n\n"
                    f"Parish Details:\n"
                    f"Parish Name: {parish_name}\n"
                    f"Email: {parish_email}\n"
                    f"Contact Number: {parish_contact_no}\n\n"
                    f"Thank you."
                )
                send_mail(subject, message, settings.EMAIL_HOST_USER, [baptism.email])


            elif new_status == 'Rejected':
                subject = "Baptism Request Rejected"
                message = (
                    f"Your baptism request has been rejected.\n\n"
                    f"Parish Details:\n"
                    f"Parish Name: {parish_name}\n"
                    f"Email: {parish_email}\n"
                    f"Contact Number: {parish_contact_no}\n\n"
                    f"For further queries, please contact the officials of {parish_name}."
                )
                send_mail(subject, message, settings.EMAIL_HOST_USER, [baptism.email])

    baptisms = Baptism.objects.all()
    return render(request, 'baptism/baptism_list_and_edit.html', {'baptisms': baptisms})


'''def approved_baptisms(request):
    baptisms_list = Baptism.objects.filter(status='Approved').order_by('-date_of_baptism')  # Sorting by date
    paginator = Paginator(baptisms_list, 10)  # Show 10 baptisms per page
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj
    }
    
    return render(request, 'approved_baptisms.html', context)'''


'''from django.http import HttpResponse
from .models import Baptism
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors

def generate_certificate(request, id):
    baptism = Baptism.objects.get(pk=id)
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="baptism_certificate_{id}.pdf"'

    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter
    
    # Title: Certificate of Baptism
    p.setFont("Helvetica-Bold", 28)
    p.setFillColor(colors.darkblue)
    p.drawCentredString(width / 2, height - 100, "Certificate of Baptism")
    
    # Decorative line
    p.setLineWidth(2)
    p.line(100, height - 120, width - 100, height - 120)
    
    # Body text
    p.setFont("Helvetica", 14)
    p.setFillColor(colors.black)
    p.drawString(100, height - 180, "This certifies that")
    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, height - 210, f"{baptism.child_name_first} {baptism.child_name_second}")
    p.setFont("Helvetica", 14)
    p.drawString(100, height - 250, "was baptized in the name of the Father and of the Son and of the Holy Spirit on")
    p.drawString(100, height - 290, f"the {baptism.date_of_baptism.strftime('%d')} day of {baptism.date_of_baptism.strftime('%B')} {baptism.date_of_baptism.year}")
    p.drawString(100, height - 330, f"at {baptism.place_of_baptism_name if baptism.place_of_baptism_name else 'the Parish Church'}")
    
    # Signature line and text
    p.drawString(100, height - 390, "Pastor")
    p.line(150, height - 395, 250, height - 395)

    p.showPage()
    p.save()

    return response
'''
'''from django.template.loader import render_to_string
from django.http import HttpResponse
from weasyprint import HTML
from .models import Baptism

from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.http import HttpResponse
from weasyprint import HTML
from io import BytesIO

def generate_certificate(request, id):
    # Fetch the baptism record
    baptism = Baptism.objects.get(pk=id)

    # Render the HTML template for the PDF
    html_string = render_to_string('baptism_certificate.html', {
        'child_name': f"{baptism.child_name_first} {baptism.child_name_second}",
        'baptism_date': baptism.date_of_baptism.strftime('%d'),
        'baptism_month': baptism.date_of_baptism.strftime('%B'),
        'baptism_year': baptism.date_of_baptism.year,
        'baptism_place': baptism.place_of_baptism_name if baptism.place_of_baptism_name else 'the Parish Church',
    })

    # Generate the PDF in memory
    pdf_buffer = BytesIO()
    HTML(string=html_string).write_pdf(pdf_buffer)
    pdf_buffer.seek(0)  # Reset buffer position to the beginning

    # Prepare the email
    subject = "Your Baptism Certificate"
    message = "Dear Parent/Guardian,\n\nPlease find attached the baptism certificate for your child."
    email = EmailMessage(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [baptism.email],
    )
    email.attach(f'baptism_certificate_{id}.pdf', pdf_buffer.getvalue(), 'application/pdf')

    # Send the email
    email.send()

    # Close the PDF buffer
    pdf_buffer.close()

    # Return the PDF for download as well
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="baptism_certificate_{id}.pdf"'
    HTML(string=html_string).write_pdf(response)

    return response

'''

import random
import string
from django.http import HttpResponse
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from weasyprint import HTML
from io import BytesIO
from .models import Baptism, Certificate
from django.conf import settings
import qrcode
from io import BytesIO
from django.core.files.base import ContentFile

def generate_certificate(request, id):
    # Fetch the baptism record
    baptism = Baptism.objects.get(pk=id)
    
    # Generate a unique 6-character alphanumeric code for the certificate
    def generate_unique_code():
        while True:
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            if not Certificate.objects.filter(certificate_code=code).exists():
                return code
    
    # Save certificate details to the database
    certificate_code = generate_unique_code()
    certificate = Certificate.objects.create(
        certificate_code=certificate_code,
        child_name=f"{baptism.child_name_first} {baptism.child_name_second}",
        certificate_date=baptism.date_of_baptism,
        parish_name=baptism.place_of_baptism_name if baptism.place_of_baptism_name else "the Parish Church",
    )
    
    #certificate_url = request.build_absolute_uri(f'baptism/verify/{certificate.certificate_code}/')
    certificate_url = f"http://127.0.0.1:8000/baptism/verify/{certificate.certificate_code}/"  # Add the trailing slash
    # Generate the QR code
    qr_code = qrcode.make(certificate_url)

    # Save the QR code as an image
    qr_code_buffer = BytesIO()
    qr_code.save(qr_code_buffer, format="PNG")
    qr_code_buffer.seek(0)

    # Convert the QR code image to a ContentFile and save it to the certificate
    certificate.qr_code.save(f'certificate_{id}_qr.png', ContentFile(qr_code_buffer.read()), save=True)

    certificate.qr_code_url = request.build_absolute_uri(certificate.qr_code.url)

    certificate.save()
    

    # Render the HTML template for the PDF
    html_string = render_to_string('baptism_certificate.html', {
        'child_name': certificate.child_name,
        'baptism_date': certificate.certificate_date.strftime('%d'),
        'baptism_month': certificate.certificate_date.strftime('%B'),
        'baptism_year': certificate.certificate_date.year,
        'baptism_place': certificate.parish_name,
        'certificate_code': certificate.certificate_code,
        'certificate_qr_code': certificate.qr_code_url,
        'certificate_qr_code_image':certificate.qr_code,
    })

    # Generate the PDF in memory
    pdf_buffer = BytesIO()
    HTML(string=html_string).write_pdf(pdf_buffer)
    pdf_buffer.seek(0)  # Reset buffer position to the beginning

    # Prepare the email
    subject = "Your Baptism Certificate"
    message = "Dear Parent/Guardian,\n\nPlease find attached the baptism certificate for your child."
    email = EmailMessage(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [baptism.email],
    )
    email.attach(f'{certificate.certificate_code}.pdf', pdf_buffer.getvalue(), 'application/pdf')

    # Send the email
    email.send()

    # Close the PDF buffer
    pdf_buffer.close()

    # Return the PDF for download as well
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{certificate.certificate_code}.pdf"'
    HTML(string=html_string).write_pdf(response)

    return response


from django.shortcuts import render
from .models import Certificate

def verify_certificate(request):
    certificate_details = None
    error_message = None

    if request.method == 'POST':
        certificate_code = request.POST.get('certificate_code', '').strip()

        # Check if a certificate exists with the provided code
        try:
            certificate_details = Certificate.objects.get(certificate_code=certificate_code)
        except Certificate.DoesNotExist:
            error_message = "Make sure you enter the correct code."

    return render(request, 'verify_certificate.html', {
        'certificate_details': certificate_details,
        'error_message': error_message,
    })



from django.shortcuts import render
from django.db.models import Count
from .models import Baptism

def baptism_dashboard(request):
    # Aggregate counts for each status
    counts = Baptism.objects.values('status').annotate(count=Count('status'))
    data = {
        'Pending': 0,
        'Approved': 0,
        'Rejected': 0,
    }
    for count in counts:
        data[count['status']] = count['count']

    context = {
        'pending_count': data['Pending'],
        'approved_count': data['Approved'],
        'rejected_count': data['Rejected'],
    }
    return render(request, 'baptism_dashboard.html', context)


from django.shortcuts import render, get_object_or_404
from .models import Certificate

def certificate_details(request, certificate_code):
    # Fetch the certificate by its code
    certificate = get_object_or_404(Certificate, certificate_code=certificate_code)
    
    return render(request, 'certificate_details.html', {'certificate': certificate})


def example(request):
    return render(request,'exmaple.html')


from django.core.paginator import Paginator
from django.shortcuts import render
from django.utils.timezone import now
import datetime
from .models import Baptism

def approved_baptisms(request):
    return filter_baptisms_by_month(request, 'Approved', 'approved_baptisms.html')

def approved_baptisms2(request):
    return filter_baptisms_by_month(request, 'Approved', 'approved_baptisms2.html')

def rejected_baptisms(request):
    return filter_baptisms_by_month(request, 'Rejected', 'rejected_baptisms.html')

def pending_baptisms(request):
    return filter_baptisms_by_month(request, 'Pending', 'pending_baptisms.html')

def filter_baptisms_by_month(request, status, template_name):
    # Get current month and year
    current_year = now().year
    current_month = now().month

    # Get user-selected month & year (default to current month/year)
    selected_month = int(request.GET.get('month', current_month))
    selected_year = int(request.GET.get('year', current_year))

    # Filter baptisms by status and date
    baptisms = Baptism.objects.filter(
        status=status,
        date_of_baptism__year=selected_year,
        date_of_baptism__month=selected_month
    ).order_by('-date_of_baptism')

    # Pagination setup (10 records per page)
    paginator = Paginator(baptisms, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Pass months and years list to template
    months = [
        (1, "January"), (2, "February"), (3, "March"), (4, "April"),
        (5, "May"), (6, "June"), (7, "July"), (8, "August"),
        (9, "September"), (10, "October"), (11, "November"), (12, "December")
    ]
    
    # Generate a list of last 5 years dynamically
    years = [current_year + i for i in range(5)]

    return render(request, template_name, {
        'page_obj': page_obj,
        'selected_month': selected_month,
        'selected_year': selected_year,
        'months': months,
        'years': years,
        'status': status
    })

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from .forms import SecretaryLoginForm, SecretaryRegistrationForm, UserLoginForm, UserRegistrationForm,PriestLoginForm,PriestRegistrationForm
from .models import LoginDetails

# Common login function
def authenticate_user(request, role, login_form_class, template_name, dashboard_redirect):
    if request.method == "POST":
        form = login_form_class(request.POST)
        if form.is_valid():
            user_name = form.cleaned_data["user_name"]
            password = form.cleaned_data["password"]

            try:
                user = LoginDetails.objects.get(user_name=user_name, role=role)
                if check_password(password, user.password):  
                    request.session["user_id"] = user.user_id  
                    messages.success(request, "Login successful!")
                    return redirect(dashboard_redirect)  
            except LoginDetails.DoesNotExist:
                pass  # Avoid exposing username existence

            messages.error(request, "Incorrect username or password.")  

    else:
        form = login_form_class()

    return render(request, template_name, {"form": form})


# Secretary Login
def secretary_login(request):
    return authenticate_user(request, role="Secretary", login_form_class=SecretaryLoginForm, template_name="secretary_login.html", dashboard_redirect="baptism_dashboard")


# Common registration function
def register_user(request, role, registration_form_class, login_redirect, template_name):
    if request.method == "POST":
        form = registration_form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = role  # Assign role
            user.save()
            messages.success(request, "Registration successful! Please log in.")
            return redirect(login_redirect)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = registration_form_class()

    return render(request, template_name, {"form": form})


# Secretary Registration
def secretary_register(request):
    return register_user(request, role="Secretary", registration_form_class=SecretaryRegistrationForm, login_redirect="secretary_login", template_name="secretary_register.html")


# User Login
def user_login(request):
    return authenticate_user(request, role="User", login_form_class=UserLoginForm, template_name="user_login.html", dashboard_redirect="home_page")


# User Registration
def user_register(request):
    return register_user(request, role="User", registration_form_class=UserRegistrationForm, login_redirect="user_login", template_name="user_register.html")


# Logout for both users and secretaries
def logout_user(request):
    request.session.flush()  
    messages.success(request, "Logged out successfully.")
    return redirect("secretary_login")  # Redirect to secretary login or user login as needed

def logout_user2(request):
    request.session.flush()  
    messages.success(request, "Logged out successfully.")
    return redirect("user_login")  # Redirect to secretary login or user login as needed


# Common login function for priests
def priest_login(request):
    return authenticate_user(request, role="Priest", login_form_class=PriestLoginForm, template_name="priest_login.html", dashboard_redirect="priest_dashboard")

# Common registration function for priests
def priest_register(request):
    return register_user(request, role="Priest", registration_form_class=PriestRegistrationForm, login_redirect="priest_login", template_name="priest_register.html")

# Priest logout
def logout_priest(request):
    request.session.flush()
    messages.success(request, "Logged out successfully.")
    return redirect("priest_login")  # Redirect to priest login page

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Baptism, LoginDetails  # Import necessary models

@login_required
def priest_dashboard(request):
    """Display only baptisms from the priest's registered church"""
    priest = LoginDetails.objects.get(user_id=request.user.id) # Get logged-in priest's details
    
    if priest.role == 'Priest' and priest.parish:
        baptisms = Baptism.objects.filter(place_of_baptism=priest.parish)  # Get baptisms for the priest's parish
    else:
        baptisms = []  # If the priest has no parish, show no data

    return render(request, 'priest_dashboard.html', {'baptisms': baptisms})
