
from aiservice import call_llm, intent_classifer
from kb_service.similarity_search import similarity_search
from flask import Flask, request,jsonify
from flask_cors import CORS
from kb_service.pdf_extraction import extract_pdf_to_txt
from kb_service.Embedding import create_kb
from contants import set_system_instruction
from utils import extractJSON
import uuid
import os

app = Flask(__name__)
CORS(app)

app.config['UPLOAD_FOLDER'] = 'kb_upload/'
app.config['MAX_CONTENT_LENGTH'] = 1024*1024*100

@app.route('/health', methods=['GET'])
def health():
    return {
        "status" : "Works!"
    }, 200


@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    if  "message" in data.keys():
        message = data.get("message")
        if message != None and message != "":
            intent_response = intent_classifer(message)
            if intent_response.get('intent') == "general":
                llm_response = call_llm(message)
                return {
                    "message" : f"{llm_response}",
                    "status" : 200
                }, 200
            else:
                try:
                    datas = similarity_search(message,top_k=10)
                    context = ""
                    for data in datas:
                        context += data[0]
                        context += ".  \n"
                        system_instruction = set_system_instruction(context, message)
                        llm_response = call_llm(message, system_instruction)
                        responseJSON = extractJSON(llm_response)
                        summary = responseJSON.get("summary")
                        return {
                            "message" : summary,
                            "status" : 200
                        }, 200
                except Exception as err:
                    return {
                            "message" : "Something Went Wrong",
                            "error" : str(err),
                            "status" : 500
                        }, 500
        else:
            return {
                "message" : "No Message Found in the Payload",
                "status" : 200
            }, 200
    else:
        return {
            "message" : "BAD Request",
            "status" : 400
        }, 400
        
@app.route('/upload', methods=['POST'])
def upload_file():
    """
    Handle single file upload.
    Expects 'files' as a multi-part form field (even for single file).
    """
    try:
        print(request.files)
        # Check if file was uploaded
        if 'files' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['files']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Secure the filename and create unique name
        filename = file.filename
        unique_filename = f"{uuid.uuid4()}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        
        # Save the file
        file.save(filepath)

        text_data = extract_pdf_to_txt(filepath, f'kb_info/{unique_filename}.txt')
        print("KB Builiding is Started")
        create_kb(data=text_data)
        print("KB Builiding is Completed")
        # Return success response
        return jsonify({
            'message': 'File uploaded successfully',
            'file_info': {
                'original_name': file.filename,
                'stored_name': unique_filename,
                'size': os.path.getsize(filepath)
            }
        }), 201
        
    except Exception as e:
        return jsonify({'error': 'Internal server error during upload' + str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)