from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import spacy
from collections import Counter
import random
from PyPDF2 import PdfReader

# Initialize FastAPI
app = FastAPI()

# Allow CORS for Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the NLP model
nlp = spacy.load("en_core_web_sm")

# Function to process PDF
def process_pdf(file: UploadFile):
    text = ""
    pdf_reader = PdfReader(file.file)
    for page_num in range(len(pdf_reader.pages)):
        text += pdf_reader.pages[page_num].extract_text()
    return text

# Generate MCQs function
def generate_mcqs(text, num_questions=5):
    if not text:
        return []

    doc = nlp(text)
    sentences = [sent.text.strip() for sent in doc.sents if len(sent.text.strip()) > 5]
    sentences = sorted(sentences, key=len, reverse=True)
    num_questions = min(num_questions, len(sentences))
    selected_sentences = sentences[:num_questions]

    mcqs = []
    for sentence in selected_sentences:
        sent_doc = nlp(sentence)
        nouns = [token.text for token in sent_doc if token.pos_ == "NOUN"]
        if len(nouns) < 1:
            continue

        noun_counts = Counter(nouns)
        correct_answer = noun_counts.most_common(1)[0][0]
        question_stem = sentence.replace(correct_answer, "______")

        # Generate distractors
        doc_nouns = list(set([token.text for token in doc if token.pos_ == "NOUN"]))
        distractors = list(set(doc_nouns) - {correct_answer})
        
        # Ensure we have at least 3 distractors
        while len(distractors) < 3:
            random_noun = random.choice(doc_nouns)
            if random_noun not in distractors and random_noun != correct_answer:
                distractors.append(random_noun)
        
        # Shuffle and limit distractors to 3
        random.shuffle(distractors)
        distractors = distractors[:3]
        answer_choices = [correct_answer] + distractors
        random.shuffle(answer_choices)

        # Determine the correct answer position
        correct_option = chr(65 + answer_choices.index(correct_answer))
        mcqs.append({
            "question_stem": question_stem,
            "answer_choices": answer_choices,
            "correct_answer": correct_option,
        })

    return mcqs

@app.post("/generate-mcqs/")
async def generate_mcqs_endpoint(
    files: List[UploadFile] = None,
    num_questions: int = Form(5),
):
    combined_text = ""

    if files:
        for file in files:
            if file.filename.endswith(".pdf"):
                combined_text += process_pdf(file)
            elif file.filename.endswith(".txt"):
                combined_text += (await file.read()).decode("utf-8")

    mcqs = generate_mcqs(combined_text, num_questions=num_questions)
    return {"mcqs": mcqs}
