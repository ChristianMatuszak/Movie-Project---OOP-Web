from storage.storage_json import StorageJson
from storage.storage_csv import StorageCsv

TEST_FILE_JSON = "test_data.json"
TEST_FILE_CSV = "test_data.csv"

def reset_test_file(path):
    """
    Clears the contents of the given test file to ensure a clean test environment.

    Args:
        path (str): The file path to be reset (JSON or CSV).
    """
    with open(path, "w", encoding="utf-8") as f:
        if path.endswith(".json"):
            f.write("{}")
        elif path.endswith(".csv"):
            f.write("title,rating,year,poster\n")

# --------------------
# Tests for StorageJson
# --------------------

def test_json_add_movie():
    """
    Tests adding a movie to JSON storage.
    Verifies the movie is stored with correct title, year, rating, and poster.
    """
    reset_test_file(TEST_FILE_JSON)
    storage = StorageJson(TEST_FILE_JSON)
    storage.add_movie("Test Movie", 2024, 9.0, "http://example.com/poster.jpg")

    movies = storage.list_movies()
    assert "Test Movie" in movies
    assert movies["Test Movie"]["year"] == 2024
    assert movies["Test Movie"]["rating"] == 9.0
    assert movies["Test Movie"]["poster"] == "http://example.com/poster.jpg"

def test_json_update_movie():
    """
    Tests updating a movie in JSON storage.
    Verifies the updated year and rating are correctly saved.
    """
    reset_test_file(TEST_FILE_JSON)
    storage = StorageJson(TEST_FILE_JSON)
    storage.add_movie("Update Movie", 2000, 7.0, "http://example.com/poster.jpg")
    storage.update_movie("Update Movie", 2024, 8.5)

    updated = storage.list_movies()["Update Movie"]
    assert updated["rating"] == 8.5
    assert updated["year"] == 2024
    assert updated["poster"] == "http://example.com/poster.jpg"

def test_json_delete_movie():
    """
    Tests deleting a movie from JSON storage.
    Verifies the movie no longer exists in the stored data.
    """
    reset_test_file(TEST_FILE_JSON)
    storage = StorageJson(TEST_FILE_JSON)
    storage.add_movie("Delete Me", 2010, 6.5, "http://example.com/poster.jpg")
    storage.delete_movie("Delete Me")

    movies = storage.list_movies()
    assert "Delete Me" not in movies

def test_json_list_movies():
    """
    Tests listing multiple movies from JSON storage.
    Verifies both movies exist with correct titles.
    """
    reset_test_file(TEST_FILE_JSON)
    storage = StorageJson(TEST_FILE_JSON)
    storage.add_movie("Movie A", 1999, 7.1, "http://example.com/a.jpg")
    storage.add_movie("Movie B", 2001, 8.2, "http://example.com/b.jpg")

    movies = storage.list_movies()
    assert len(movies) == 2
    assert "Movie A" in movies
    assert "Movie B" in movies

# --------------------
# Tests for StorageCsv
# --------------------

def test_csv_add_movie():
    """
    Tests adding a movie to CSV storage.
    Verifies the movie is stored with correct title, year, and rating.
    """
    reset_test_file(TEST_FILE_CSV)
    storage = StorageCsv(TEST_FILE_CSV)
    storage.add_movie("CSV Movie", 2020, 8.0, "http://example.com/poster.jpg")

    movies = storage.list_movies()
    assert "CSV Movie" in movies
    assert movies["CSV Movie"]["year"] == 2020
    assert movies["CSV Movie"]["rating"] == 8.0

def test_csv_update_movie():
    """
    Tests updating a movie in CSV storage.
    Verifies the updated year and rating are correctly saved.
    """
    reset_test_file(TEST_FILE_CSV)
    storage = StorageCsv(TEST_FILE_CSV)
    storage.add_movie("CSV Update", 2011, 7.2, "http://example.com/poster.jpg")
    storage.update_movie("CSV Update", 2012, 9.1)

    updated = storage.list_movies()["CSV Update"]
    assert updated["year"] == 2012
    assert updated["rating"] == 9.1

def test_csv_delete_movie():
    """
    Tests deleting a movie from CSV storage.
    Verifies the movie no longer exists in the stored data.
    """
    reset_test_file(TEST_FILE_CSV)
    storage = StorageCsv(TEST_FILE_CSV)
    storage.add_movie("CSV Delete", 1995, 6.0, "http://example.com/poster.jpg")
    storage.delete_movie("CSV Delete")

    movies = storage.list_movies()
    assert "CSV Delete" not in movies

def test_csv_list_movies():
    """
    Tests listing multiple movies from CSV storage.
    Verifies both movies exist with correct titles.
    """
    reset_test_file(TEST_FILE_CSV)
    storage = StorageCsv(TEST_FILE_CSV)
    storage.add_movie("CSV A", 2000, 7.5, "http://example.com/a.jpg")
    storage.add_movie("CSV B", 2005, 8.5, "http://example.com/b.jpg")

    movies = storage.list_movies()
    assert len(movies) == 2
    assert "CSV A" in movies
    assert "CSV B" in movies