from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from OTXv2 import OTXv2
import argparse
import get_malicious
import hashlib
from datetime import datetime
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import dns.resolver



API_KEY = 'c5248c5809767e4f30fbfa7e84bd9791178d66563914278982676674962aaf19'
OTX_SERVER = 'https://otx.alienvault.com/'
otx = OTXv2(API_KEY, server=OTX_SERVER)

cred = credentials.Certificate('sparta-project-c3f1f-firebase-adminsdk-g3rjz-c0d341a37a.json')
firebase_admin.initialize_app(cred)

# Initialize Firestore
db = firestore.client()
doc_ref = db.collection('Query').document()

record_types = ["A"]
resolver = dns.resolver.Resolver()
@csrf_exempt
def Check_for_Malicious(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            # Now you can use the data dictionary as needed
            if data.get('type','wrong')=="ip":
                alerts = get_malicious.ip(otx, data.get('value','wrong'))
                now = datetime.now()
                if len(alerts) > 0:
                    data = {
                        'value': data.get('value','wrong'),
                        'type': data.get('type','none'),
                        'isMalicious': False,
                        'date': now
                    }
                    doc_ref.set(data)
                else:
                    now = datetime.now()
                    data = {
                        'value': data.get('value', 'wrong'),
                        'type': data.get('type', 'none'),
                        'isMalicious': True,
                        'date': now
                    }
                    doc_ref.set(data)
            if data.get('type', 'wrong') == "hostname":
                alerts = get_malicious.hostname(otx, data.get('value', 'wrong'))
                if len(alerts) > 0:
                    now = datetime.now()
                    data = {
                        'value': data.get('value', 'wrong'),
                        'type': data.get('type', 'none'),
                        'isMalicious': False,
                        'date': now
                    }
                    doc_ref.set(data)
                else:
                    now = datetime.now()
                    data = {
                        'value': data.get('value', 'wrong'),
                        'type': data.get('type', 'none'),
                        'isMalicious': True,
                        'date': now
                    }
                    doc_ref.set(data)




        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    else:
        return JsonResponse({"error": "Only POST method allowed"}, status=405)

def fetch_50_data(request):
    try:
        # Reference to your Firebase collection
        collection_ref = db.collection('Query')

        # Fetch 50 documents
        documents = collection_ref.order_by('date').limit(50).stream()

        # Extracting data
        data = []
        for doc in documents:
            doc_data = doc.to_dict()
            # Assuming 'date' is a field in your document
            data.append({
                'value': doc_data.get('value', None),
                'type': doc_data.get('type', None),
                'isMalicious': doc_data.get('isMalicious', None),
                'date': doc_data.get('date', None)
            })

        # Return the data as JSON
        return JsonResponse({"data": data})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

def fetch_latest_data(request):
    try:
        # Reference to your Firebase collection
        collection_ref = db.collection('Query')
        request_data = json.loads(request.body)
        value_to_query = request_data.get('value')

        # Fetch 50 documents
        query_ref = collection_ref.where('value', '==', value_to_query)
        docs = query_ref.stream()



        # Extracting data
        data = []
        for doc in docs:
            doc_data = doc.to_dict()
            # Assuming 'date' is a field in your document
            data.append({
                'value': doc_data.get('value', None),
                'type': doc_data.get('type', None),
                'isMalicious': doc_data.get('isMalicious', None),
                'date': doc_data.get('date', None)
            })
        if doc_data.get('value', None)=='hostname':
            target_domain = doc_data.get('value', None)
            record_types = ["A", "AAAA", "CNAME", "MX", "NS", "SOA", "TXT"]
            # Create a DNS resolver
            resolver = dns.resolver.Resolver()
            List = []
            for record_type in record_types:
                # Perform DNS lookup for the specified domain and record type
                try:
                    answers = resolver.resolve(target_domain, record_type)
                except dns.resolver.NoAnswer:
                    continue
                # Print the answers

                for rdata in answers:
                    data.append({record_type: rdata})

        # Return the data as JSON
        return JsonResponse({"data": data},safe=False)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
