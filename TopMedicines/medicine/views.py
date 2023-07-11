from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
import pandas as pd
import numpy as np

# Create your views here.
def index(request):
    return render(request, 'index.html')


def view_medicine(request):
    context = {}
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        url = fs.url(name)

        number = int(request.POST['number'])

        df = pd.read_excel(uploaded_file)
        unique_df = df.groupby(['Medicine','Cost'], as_index=False)['Quantity'].sum()
        sorted_df = unique_df.sort_values(by=['Quantity'], ascending=False)
        sorted_df = sorted_df.head(number)
        sorted_df['Total_Cost'] = sorted_df['Cost']*sorted_df['Quantity']
        sorted_df['S_No'] = np.arange(1, len(sorted_df)+1)

        sorted_df = sorted_df.iloc[:, [4,0,2,1,3]]

        data_dict = sorted_df.to_dict(orient='records')
        context['data'] = data_dict

        sorted_df.to_excel('media/file.xlsx', index=False)

    return render(request, 'index.html', context)
    
