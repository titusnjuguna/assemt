from django.shortcuts import render,redirect
from .forms import CSVUploadForm
import csv
import tempfile

"""This function save uploaded file temporary on the memory to make it easily accessible"""
def save_uploaded_file(file):
    _, temp_path = tempfile.mkstemp(suffix=".csv")
    file_content = file.read()
    with open(temp_path, 'wb') as temp_file:
        temp_file.write(file_content)
    return temp_path

"""This function take in a list and data of any form, 
however for this case it will take a dictionary and 
check uniqueness of the data, it will return a list"""
def add_unique(lst:list, entry:any)->list:
    # Convert the list of dictionaries to a set of frozensets
    set_of_dicts = {frozenset(d.items()) for d in lst}
        # Check if the new entry is already in the set
    if frozenset(entry.items()) not in set_of_dicts:
        lst.append(entry)

"""This function takes in a csv file and process it to a dictionary"""   
def read_csv(file)->dict:
    records = {}
    with open(file, 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            records[row['unique']] = row
            records[row['date']] = row
            records[row['name']] = row
            records[row['amount']] = row
    return records

""""This function takes in two dictioanry object and 
match missing data to it to return a list """
def find_missing_records(source:dict, target:dict)->list:
    lst = []
    for record in source.values():
        if record['unique'] not in target:
            add_unique(lst,record)
    return lst

"""This function takes in two dictionary objects and returns a list of dictionary object"""
def find_discrepancies(source:dict,target:dict)->list:
    discrepancies = []
    for key, source_value in source.items():
        print(key)
        if key in target:
            target_value = target[key]
            print(target_value)
            if source_value != target_value:
                # add_unique(discrepancies,{
                #     'unique': key,
                #     'field': key,
                #     'source_value': source_value,
                #     'target_value': target_value
                # })
                discrepancies.append({
                    'unique': key,
                    'field': key,
                    'source_value': source_value,
                    'target_value': target_value
                })
    return discrepancies

"""This is the main function that perform all the reconcilition by merging information from different function"""
def reconcile(source_file, target_file, output_path=None, columns_to_compare=None):
    # Read CSV files
    source_records = read_csv(source_file)
    target_records = read_csv(target_file)
    missing_in_target = find_missing_records(source_records, target_records)
    missing_in_source = find_missing_records(target_records, source_records)
    discrepancies = find_discrepancies(source=source_records,target=target_records)
    return {
        'missing_in_target': missing_in_target,
        'missing_in_source': missing_in_source,
        'discrepancies': discrepancies
    }

"""This view renders the homepage for our site"""
def home(request):
    result = request.session.get("result")
    return render(request,'reconciler/index.html',{'result':result})

"""This view renders the result of the reconcilition operation/reporting Page"""
def index(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            source_file = request.FILES["source_file"]
            source_path=save_uploaded_file(source_file)
            target_file = request.FILES["target_file"]
            target_path = save_uploaded_file(target_file)
            result=reconcile (source_path,target_path)
            print(result)
            request.session["result"]=result
            return redirect('home')
    else:
        form = CSVUploadForm()
    return render(request, 'reconciler/uploadcsv.html', {'form': form})
