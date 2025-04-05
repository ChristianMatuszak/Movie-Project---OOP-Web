from omdb_api import fetch_movie_data

def test_fetch_inception():
    data = fetch_movie_data("Inception")
    assert data is not None
    assert data["title"] == "Inception"
    assert isinstance(data["year"], int)
    assert isinstance(data["rating"], float)
    assert data["poster"].startswith("http")
