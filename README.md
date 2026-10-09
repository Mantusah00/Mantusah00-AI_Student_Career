# Advanced Student Career Interest Field Work Project

Features: 12-question survey, top-3 career interest matches, personalized learning roadmaps, dashboard charts, SQLite database, CSV export.

## Run in VS Code (Windows)
Open terminal in the folder containing app.py and run:
`python app.py`
If using the venv in the parent folder: `..\\venv\\Scripts\\python.exe app.py`
Open http://127.0.0.1:5000

If needed: `python -m pip install -r requirements.txt`

Pages: `/` survey, `/dashboard` charts and collected responses, `/export.csv` download data.

Academic note: recommendation scores are weighted interest-match indices, not probabilities or validated career predictions. Collect actual student responses with consent; do not invent research results.
