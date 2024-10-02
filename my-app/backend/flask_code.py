from flask import Flask, request, jsonify
from flask_cors import CORS
from main import fetch_papers, chat_with_pdfs, summarize_file, fetch_relevant_keywords, extract_keywords  # Ensure these functions return valid responses
from analyze_ts import extract_popular_keywords
from pygithub import getTopics, searchRepos
from PyPDF2 import PdfReader
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
CORS(app)

# Define a folder to store uploaded PDF files
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/api/chat-with-pdf', methods=['POST', 'GET'])
def chat_with_pdf():
    try:
        # Check if the request contains a file
        if 'file' not in request.files:
            return jsonify({"error": "No file part"}), 400

        pdf_file = request.files['file']  # Fetch the file

        if pdf_file.filename == '':
            return jsonify({"error": "No selected file"}), 400    

        # Parse additional data like the user's question
        user_query = request.form.get('question')  # Use form, not json here

        # Check if the query is provided
        if not user_query:
            return jsonify({"error": "No question provided"}), 400

        # Process the file and query (You can add your logic here)
        response_message = chat_with_pdfs(user_query)  # Add file processing if needed
        print(response_message)

        return jsonify({"response": response_message}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Route to handle fetching papers based on the user's prompt
@app.route('/api/send-prompt', methods=['POST', 'GET'])
def send_prompt():
    data = request.json
    user_prompt = data.get('prompt')

    # Check if the prompt is provided
    if not user_prompt:
        return jsonify({"error": "Prompt is required."}), 400

    try:
        # Process the prompt as needed
        response_message = fetch_papers(user_prompt)

        # Check if the response message is valid
        if response_message is None:
            return jsonify({"error": "No response from fetch_papers"}), 500
        
        # Return the response as JSON
        return jsonify({"response": response_message}), 200

    except Exception as e:
        # If any error occurs, catch it and return an error message
        return jsonify({"error": str(e)}), 500
    
@app.route('/api/summarize-pdf', methods=['POST', 'GET'])
def summarize_pdf():
    # Check if any file is provided in the request
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    files = request.files.getlist('file')  # Handle multiple files if needed

    if not files:
        return jsonify({"error": "No file uploaded"}), 400

    # Process each file
    summaries = []
    for file in files:
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400

        # Save the uploaded file to the server
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Call the summarize function (assumed to be implemented in summarize_pdf_module)
        try:
            summary = summarize_file(file_path)
            summaries.append(summary)
        except Exception as e:
            return jsonify({"error": f"Error processing file: {str(e)}"}), 500

    # Combine summaries if multiple files are uploaded
    final_summary = "\n\n".join(summaries)

    # Return the summarized content as a JSON response
    return jsonify({"response": final_summary}), 200

# Route to handle fetching papers based on the user's prompt
@app.route('/api/recommend-ts', methods=['POST', 'GET'])
def recommend_ts():
    data = request.json
    user_prompt = data.get('prompt')

    # Check if the prompt is provided
    if not user_prompt:
        return jsonify({"error": "Prompt is required."}), 400

    try:
        # Process the prompt as needed
        keywords = extract_keywords(user_prompt)
        response = fetch_relevant_keywords(keywords)

        response = searchRepos(response) #repo-data
        keyword_popularity = extract_popular_keywords(response)

        popular_keywords = keyword_popularity.most_common(10)
    
        # Check if the response message is valid
        if len(response) == 0:
            return jsonify({"error": "No response from pygithub"}), 500
        
        # Return the response as JSON
        return jsonify({"response": popular_keywords}), 200

    except Exception as e:
        # If any error occurs, catch it and return an error message
        return jsonify({"error": str(e)}), 500

# Main entry point for running the Flask app
if __name__ == '__main__':
    app.run(debug=True, port=8080)
