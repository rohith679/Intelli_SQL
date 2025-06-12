
# IntelliSQL Streamlit App

This is a Streamlit app that converts English questions into SQL queries using Google Gemini API and interacts with a SQLite database of student records.

---

## Features

- Dynamic SQLite database initialization on first run
- Stores and queries student information
- Clean, neon-red themed UI built with Streamlit
- Uses Google Gemini API for natural language to SQL translation

---

## Getting Started

### Prerequisites

- Python 3.7+
- Streamlit
- `google-generativeai` package
- SQLite3 (comes bundled with Python)

### Installation

1. Clone the repo

```bash
git clone https://github.com/rohith679/Intelli_SQL.git
cd Intelli_SQL
```

2. Create a virtual environment (optional but recommended)

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Set up your `.env` file with your Gemini API key

```
API_KEY=your_google_gemini_api_key_here
```

---

## Usage

Run the app locally:

```bash
streamlit run app.py
```

- On first run, the app will create a `data.db` SQLite database and populate it with student data automatically.
- You can then enter English questions, which will be converted to SQL queries and executed on the database.

---

## File Structure

```
IntelliSQL/
│
├── app.py             # Main Streamlit app
├── data.db            # database file
├── sql.py             # Database initialization script
├── requirements.txt   # Python dependencies
├── .gitignore         # To ignore data.db and other files
├── README.md          # This file
└── .env               # API keys (not uploaded to repo)


```

---

## Notes

- Make sure to add `data.db` in `.gitignore` to avoid pushing the database file.
- Keep your API keys secure and do not upload `.env` to GitHub.

---

## License

This project is licensed under the MIT License.

---
