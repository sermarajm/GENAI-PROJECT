import json

def extractJSON(response):
    try:
        start_ind = response.find('{')
        end_ind = response.rfind('}') 
        return json.loads(response[start_ind : end_ind + 1])
    except Exception as err:
        print(err)
        return response