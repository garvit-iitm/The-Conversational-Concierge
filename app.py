from flask import Flask, render_template, request, jsonify ,session
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from google import genai
import os
from PyPDF2 import PdfReader

app = Flask(__name__)

client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    # Handle PDF or text
    if file.filename.endswith(".pdf"):
        reader = PdfReader(file)
        content = ""
        for page in reader.pages:
            content += page.extract_text() or ""
    else:
        content = file.read().decode('utf-8')

    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
    prompt = PromptTemplate(
        input_variables=["content"],
        template="""Given the following content, generate 5 relevant questions 
        that a user might want to ask:
        Content: {content}
        
        Generate only 5 questions, numbered 1-5."""
    )
    chain = LLMChain(llm=llm, prompt=prompt)
    questions = chain.run(content=content)

    return jsonify({"questions": questions})

if __name__ == "__main__":
    app.run(debug=True, port=8080)
    
