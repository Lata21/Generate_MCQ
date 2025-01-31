
# MCQ Generator Application

This project provides an MCQ (Multiple-Choice Question) generator application with a **FastAPI** backend and a **Streamlit** frontend. The application processes uploaded PDF or text files to extract meaningful sentences and generate MCQs with a question stem, answer choices, and the correct answer.

## Features

- **Backend**:
  - Built with FastAPI for generating MCQs.
  - Handles multiple file uploads (`.pdf` or `.txt`).
  - Leverages spaCy for natural language processing.
- **Frontend**:
  - Streamlit-based user interface.
  - Allows users to upload files, specify the number of questions, and view generated MCQs in a clean format.

## Requirements

- Python 3.9 or higher
- FastAPI
- Streamlit
- PyPDF2
- spaCy
- A spaCy language model (`en_core_web_sm`)

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Set up a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
   ```

3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Download the spaCy language model:
   ```bash
   python -m spacy download en_core_web_sm
   ```

## Running the Application

### 1. Start the Backend (FastAPI)
Run the backend server:
```bash
uvicorn main:app --reload
```

The backend will be accessible at [http://127.0.0.1:8000](http://127.0.0.1:8000).

### 2. Start the Frontend (Streamlit)
Run the frontend:
```bash
streamlit run front.py
```

The frontend will be accessible at [http://localhost:8501](http://localhost:8501).

## API Endpoints (Backend)

### POST `/generate-mcqs/`

**Description**: Generates MCQs from uploaded files.

**Parameters**:
- `files`: A list of `.pdf` or `.txt` files to process.
- `num_questions`: The number of MCQs to generate (default is 5).

**Response Example**:
```json
{
  "mcqs": [
    {
      "question_stem": "The Cold War ______ witnessed a space race between the United States and the Soviet Union.",
      "answer_choices": ["race", "era", "space", "landing"],
      "correct_answer": "A"
    }
  ]
}
```

## Project Structure

- **Backend**:
  - `main.py`: FastAPI code for processing files and generating MCQs.
- **Frontend**:
  - `front.py`: Streamlit UI for file upload and MCQ display.
- **Other Files**:
  - `requirements.txt`: Lists project dependencies.
  - `README.md`: Documentation for the project.

## Future Enhancements

- Improve distractor generation with advanced NLP techniques.
- Add support for `.docx` files.
- Allow exporting MCQs to `.csv` or `.json`.

## License

This project is licensed under the MIT License.
