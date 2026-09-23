# CivicFix AI

## Problem Statement

Many citizens face difficulty reporting civic issues such as potholes, broken streetlights, blocked drains, unsafe public spaces, and sanitation problems. In many cases, complaints are not structured clearly, and local authorities struggle to prioritize urgent issues efficiently.

## Project Objective

CivicFix AI is designed to help citizens report civic problems in a structured way and assist authorities in prioritizing issues based on urgency, category, and department routing. The system uses AI-powered classification to convert raw user complaints into actionable service requests.

## Key Features

- User-friendly civic issue reporting form
- AI-based categorization of complaints
- Severity and urgency detection
- Department-specific routing suggestions
- Complaint summary generation
- SQLite-backed local data storage
- Dashboard for viewing submitted complaints
- Fallback classification logic when external AI services are unavailable

## Technology Stack

- Python
- Streamlit
- SQLite
- Pandas
- python-dotenv
- Google Generative AI SDK

## System Workflow

1. A citizen enters their name, location, and civic issue description.
2. The application validates the submitted details.
3. The complaint is analyzed by the AI engine.
4. The system assigns a category, urgency level, and recommended department.
5. A structured complaint summary is generated.
6. The complaint is stored in the SQLite database.
7. The dashboard displays complaint records and status for review.

## Project Structure

```text
CivicFix-AI/
├── app.py                  # Streamlit application entry point
├── ai_engine.py            # Complaint analysis and AI routing logic
├── database.py            # SQLite database setup and complaint storage
├── requirements.txt       # Python dependencies
├── .gitignore             # Git exclusions for local environment files
├── README.md              # Project overview and usage guide
├── .env                   # Local environment file (not committed)
├── data/
│   └── civicfix.db        # SQLite database file
├── templates/
│   └── index.html         # Legacy template file
└── venv/                  # Local virtual environment (not committed)
```

## How to Run Locally

1. Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Add the required environment variable in your local environment before running the app.

4. Start the application:

```bash
streamlit run app.py
```

5. Open the local Streamlit URL shown in the terminal.

## Future Scope

- Add citizen authentication and role-based access
- Integrate a live government workflow dashboard
- Add geospatial mapping of reported complaints
- Support notifications and status tracking
- Add multilingual complaint submissions
- Connect to a production database and analytics layer
- Expand AI classification with more complaint categories and historical training data

## Deployment Information

This project is structured for deployment on Streamlit Community Cloud.

Recommended deployment practices:

- Keep the application entry point as `app.py`
- Keep dependencies in `requirements.txt`
- Store environment secrets in the deployment platform's secret manager rather than in the repository
- Keep `.env` and local database files out of Git
- Use the SQLite database only for lightweight local or prototype scenarios

For production deployment, consider replacing the local SQLite database with a managed database service and securely managing application secrets.
