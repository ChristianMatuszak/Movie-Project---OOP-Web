# 🎬 Movie Database CLI App

A Python command-line movie manager that uses the [OMDb API](https://www.omdbapi.com/) to fetch real movie data and optionally generate a static website from your personal movie collection.

---

## 🚀 Features

- Add movies by title using OMDb API
- Store movies in JSON or CSV format
- Display movie statistics (average, median, best, worst)
- Search, sort, filter movies
- Delete movies from the collection
- Generate a movie website (`index.html`) with poster images
- Fully tested with `pytest`

---

## 🗂️ Project Structure

```plaintext
Movie_Project_OOP+Web/
├── data/
│   ├── data.csv                # CSV database (default storage)
│   └── data.json               # JSON database (if using JSON storage)
├── storage/
│   ├── istorage.py             # Interface for all storage types
│   ├── storage_json.py         # JSON-based storage implementation
│   └── storage_csv.py          # CSV-based storage implementation
├── tests/
│   ├── test_data.csv           # CSV test data
│   ├── test_data.json          # JSON test data
│   ├── test_storage.py         # Unit tests for storage
│   └── test_omdb_fetch.py      # Unit test for OMDb API fetching
├── website/
│   ├── index_template.html     # Website HTML template
│   ├── style.css               # Website styling
│   └── index.html              # Generated HTML output
├── .env                        # Stores OMDb API key (excluded from Git)
├── .gitignore
├── main.py                     # App entry point
├── movie_app.py                # CLI application logic
├── omdb_api.py                 # OMDb API integration logic
├── README.md                   # This file
└── requirements.txt            # Required dependencies
```

## ⚙️ Setup & Installation

### 1. Clone the repository

```bash
git clone https://github.com/ChristianMatuszak/Movie-Project---OOP-Web.git
cd Movie-Project---OOP-Web
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up your OMDb API key

Create a .env file in the root directory and insert your key like this:
```env
OMDB_API_KEY=your_api_key_here
```
You can get your API key for free from http://www.omdbapi.com.
