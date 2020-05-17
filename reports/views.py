import csv, io

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.db.models import Q
from .models import AssociateBill
from .forms import OneRecord
from django.contrib import messages

def start(request):
    data = AssociateBill.objects.all()
    datafilter = request.GET.get('datafilter')

    if datafilter != '' and datafilter is not None:
        data = data.filter(Q(bill1__icontains=datafilter) | Q(bill2__icontains=datafilter)).distinct()

    contexto = {
        'data':data
    }
    return render(request, 'index.html', contexto)


def createRecord(request):
    if request.method == 'GET':
        form = OneRecord()
    else:
        form = OneRecord(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')


    return render(request, 'create_record.html',{'form':form})



def editRecord(request, id):
    record = AssociateBill.objects.get(id = id)
    if request.method == 'GET':
        form = OneRecord(instance = record)
    else:
        form = OneRecord(request.POST, instance = record)
        if form.is_valid():
            form.save()
            return redirect('index')

    return render(request, 'create_record.html',{'form':form})


def deleteRecord(request, id):
    record = AssociateBill.objects.get(id = id)
    record.delete()
    return redirect('index')


def export_records_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="records.csv"'

    writer = csv.writer(response)
    writer.writerow(['id', 'bill1', 'bill2'])

    records = AssociateBill.objects.all().values_list('id','bill1','bill2')
    print(records)
    for record in records:
        writer.writerow(record)

    return response

def upload_content(request):
    
     # declaring template
    template = "upload_content.html"
    data = AssociateBill.objects.all()
# prompt is a context variable that can have different values      depending on their context
    prompt = {
        'order': 'Order of the CSV should be bill1, bill2',
        'profiles': data    
              }
    # GET request returns the value of the data with the specified key.
    if request.method == "GET":
        return render(request, template, prompt)
    
    
    csv_file = request.FILES['file']
    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'El formato del archivo no es válido. Subir un CSV.')

    data_set = csv_file.read().decode('UTF-8')
    print(data_set)
    io_string = io.StringIO(data_set)
    next(io_string)
    for column in csv.reader(io_string, delimiter=',', quotechar="|"):
        AssociateBill.objects.create(
            bill1=column[0],
            bill2=column[1]
        )
    context = {}
    return render(request, 'index.html', context)

def delete_all_content(request):
    AssociateBill.objects.delete()
    return redirect('index')
