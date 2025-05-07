from django.shortcuts import render
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import UploadedFile
from fileparser.validators import validate_file_extension, validate_file_size
from .utils import read_uploaded_file
from .models import person_collection
from backend.models import EducationalBackground

def home(request):
    return render(request, 'index.html')


def upload_resume(request):
    if request.method == 'POST' and request.FILES.get('file'):
        try:
            file = request.FILES['file']
            ext = file.name.split('.')[-1].lower()
            
            validate_file_extension(file)
            validate_file_size(file)
            
            resume_data = read_uploaded_file(file, ext)
            # print('file name: ', file)
            print("file content: ", resume_data)
            if 'education' in resume_data:
                education_text = resume_data['education']['text']
                education_tables = resume_data['education']['tables']
                
                for table_name, table_data in education_tables.items():
                    print(len(table_data))
                    for row in table_data[1:]:
                        if len(row) >= 3:
                            EducationalBackground.objects.create(
                                # expert = 1,
                                institution_name=row[0],
                                year_of_grad=row[1],
                                education_level=row[2]
                            )
            
            return JsonResponse({
                'success': True,
                'resume_data': resume_data,
                'filename': file.name
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)
    
    return JsonResponse({
        'success': False,
        'error': 'Invalid request'
    }, status=400)



    
from django.http import HttpResponse

def index(request):
    return HttpResponse("<h1> App is  running")

def add_person(request):
    records = {
        "first_name": "jhon",
        "last_name":"abebe",
    }
    
    person_collection.insert_one(records)
    
    return HttpResponse("new person is add")

def get_all_person(request):
    person= person_collection.find()
    return (person)