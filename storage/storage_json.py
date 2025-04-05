import json
from storage.istorage import IStorage

class StorageJson(IStorage):
    """
    StorageJson implements the IStorage interface using a JSON file.
    It allows storing and retrieving movies with title, year, rating, and poster URL.
    """

    def __init__(self, filename):
        """
        Initializes the JSON storage with the specified filename.

        Args:
            filename (str): Path to the JSON file for storing movie data.
        """
        self.filename = filename

    def list_movies(self):
        """
        Returns all stored movies as a dictionary.

        Returns:
            dict: Movie titles as keys and dictionaries with year, rating,
                  and poster as values.
        """
        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def add_movie(self, title, year, rating, poster):
        """
        Adds a new movie to the JSON storage.

        Args:
            title (str): Movie title.
            year (int): Release year.
            rating (float): IMDb rating.
            poster (str): URL to the movie poster.
        """
        movies = self.list_movies()
        movies[title] = {
            "year": year,
            "rating": rating,
            "poster": poster
        }
        self._save_movies(movies)

    def delete_movie(self, title):
        """
        Deletes a movie from the JSON storage.

        Args:
            title (str): Title of the movie to delete.
        """
        movies = self.list_movies()
        if title in movies:
            del movies[title]
            self._save_movies(movies)

    def update_movie(self, title, year, rating):
        """
        Updates the year and rating of an existing movie.
        Poster remains unchanged.

        Args:
            title (str): Title of the movie to update.
            year (int): New release year.
            rating (float): New IMDb rating.
        """
        movies = self.list_movies()
        if title in movies:
            movies[title]["year"] = year
            movies[title]["rating"] = rating
            self._save_movies(movies)

    def _save_movies(self, movies):
        """
        Saves the current movie dictionary to the JSON file.

        Args:
            movies (dict): Dictionary of movie data to be saved.
        """
        with open(self.filename, 'w', encoding='utf-8') as file:
            json.dump(movies, file, indent=4)
