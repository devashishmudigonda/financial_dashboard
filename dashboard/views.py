# from django.shortcuts import render
# from .models import FinancialData

# def index(request):
#     data = FinancialData.objects.all()
#     return render(request, 'index.html', {'data': data})




#ABOVE IS FOR DIPLAYING THE TABLE IN THE PAGE


# import subprocess
# from django.shortcuts import render
# from django.http import HttpResponse

# def run_import_script(request):
#     try:
#         # Run the import_from_csv.py script
#         subprocess.run(['python3', 'import_from_csv.py'], check=True)
#         return HttpResponse("Script executed successfully.")
#     except subprocess.CalledProcessError as e:
#         return HttpResponse(f"Error executing script: {e}", status=500)

# def index(request):
#     # Render the dashboard with the button
#     return render(request, 'index.html')


# from rest_framework import viewsets
# from .models import FinancialData
# from .serializers import FinancialDataSerializer
# import pandas as pd

# class FinancialDataViewSet(viewsets.ModelViewSet):
#     queryset = FinancialData.objects.all()
#     serializer_class = FinancialDataSerializer

#     def list(self, request, *args, **kwargs):
#         # Example: Aggregating and normalizing data
#         data = FinancialData.objects.all().values()
#         df = pd.DataFrame(list(data))
        
#         # Example of normalization: Calculating average amount
#         average_amount = df['amount'].mean()
        
#         # Add aggregated data to response
#         response = super().list(request, *args, **kwargs)
#         response.data['average_amount'] = average_amount
#         return response





import subprocess
import os
# from django.shortcuts import render
# from django.http import HttpResponse
# from rest_framework import viewsets
# from .models import FinancialData
# from .serializers import FinancialDataSerializer
# import pandas as pd

# def index(request):
#     # Render the dashboard with the button
#     return render(request, 'index.html')

# def run_import_script(request):
#     script_path = os.path.join(os.path.dirname(__file__), 'import_from_csv.py')
    
#     try:
#         # Run the import_from_csv.py script
#         subprocess.run(['python3', script_path], check=True)
#         return HttpResponse("Script executed successfully.")
#     except subprocess.CalledProcessError as e:
#         return HttpResponse(f"Error executing script: {e}", status=500)

# class FinancialDataViewSet(viewsets.ModelViewSet):
#     queryset = FinancialData.objects.all()
#     serializer_class = FinancialDataSerializer

#     def list(self, request, *args, **kwargs):
#         # Example: Aggregating and normalizing data
#         data = FinancialData.objects.all().values()
#         df = pd.DataFrame(list(data))
        
#         # Example of normalization: Calculating average amount
#         average_amount = df['amount'].mean()
        
#         # Add aggregated data to response
#         response = super().list(request, *args, **kwargs)
#         response.data['average_amount'] = average_amount
#         return response


from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets
from .models import FinancialData
from .serializers import FinancialDataSerializer
import pandas as pd
from rest_framework.response import Response
from rest_framework import status
import subprocess

def index(request):
    return render(request, 'index.html')

def run_import_script(request):
    try:
        subprocess.run(['python3', 'import_from_csv.py'], check=True)
        return HttpResponse("DB Created Successfully    ")
    except subprocess.CalledProcessError as e:
        return HttpResponse(f"Error executing script: {e}", status=500)

class FinancialDataViewSet(viewsets.ModelViewSet):
    queryset = FinancialData.objects.all()
    serializer_class = FinancialDataSerializer

    def list(self, request, *args, **kwargs):
        try:
            # Fetch all financial data
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            data = serializer.data

            # Convert data to DataFrame for aggregation and normalization
            df = pd.DataFrame(data)

            # Check data types and handle normalization
            df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
            df['amount_normalized'] = (df['amount'] - df['amount'].min()) / (df['amount'].max() - df['amount'].min())

            # Aggregate data
            average_amount = df['amount'].mean()
            total_amount_by_category = df.groupby('category')['amount'].sum().to_dict()
            total_amount_by_customer = df.groupby('customer')['amount'].sum().to_dict()
            average_normalized_amount = df['amount_normalized'].mean()

            aggregated_data = {
                'average_amount': average_amount,
                'total_amount_by_category': total_amount_by_category,
                'total_amount_by_customer': total_amount_by_customer,
                'average_normalized_amount': average_normalized_amount
            }

            # Combine the list of data and the aggregated statistics
            response_data = {
                'data': data,
                'aggregated_data': aggregated_data
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            print(f"An error occurred: {e}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
def insights_view(request):
    return render(request, 'insights.html')
from django.shortcuts import render
from django.http import JsonResponse
import json

def generate_insights(data):
    insights = []

    # Example Insight: Category with the highest amount
    category_data = {}
    for item in data:
        category = item['category']
        category_data[category] = category_data.get(category, 0) + item['amount']

    if category_data:
        top_category = max(category_data, key=category_data.get)
        insights.append(f"The category with the highest total amount is '{top_category}' with a total of ${category_data[top_category]:.2f}.")

    # Example Insight: Gender with the highest spending
    gender_data = {}
    for item in data:
        gender = item['gender']
        gender_data[gender] = gender_data.get(gender, 0) + item['amount']

    if gender_data:
        top_gender = max(gender_data, key=gender_data.get)
        insights.append(f"'{top_gender}' is the gender with the highest total spending, amounting to ${gender_data[top_gender]:.2f}.")

    # Example Insight: Top Merchant
    merchant_data = {}
    for item in data:
        merchant = item['merchant']
        merchant_data[merchant] = merchant_data.get(merchant, 0) + item['amount']

    if merchant_data:
        top_merchant = max(merchant_data, key=merchant_data.get)
        insights.append(f"The top merchant based on spending is '{top_merchant}' with a total of ${merchant_data[top_merchant]:.2f}.")

    # Add more insights as needed...

    return insights

def insights_page(request):
    # Retrieve the stored data (this assumes it’s stored in localStorage and passed to the backend)
    aggregated_data = request.GET.get('data', '[]')
    data = json.loads(aggregated_data)

    # Generate insights from the data
    insights = generate_insights(data)

    return render(request, 'insights.html', {'insights': insights})

