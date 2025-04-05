import csv
import os

from colorama import Fore, Style

from storage.istorage import IStorage

class StorageCsv(IStorage):
    """
    StorageCsv implements the IStorage interface using a CSV file.
    It supports basic CRUD operations for movies with title, year, rating, and poster URL.
    """

    def __init__(self, filename):
        self.filename = filename

    def list_movies(self):
        """
        Returns all stored movies from the CSV file as a dictionary.

        Returns:
            dict: Movie titles as keys and dictionaries with year, rating, and poster as values.
        """
        movies = {}
        try:
            with open(self.filename, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    movies[row['title']] = {
                        'rating': float(row['rating']),
                        'year': int(row['year']),
                        'poster': row.get('poster', '')
                    }
        except FileNotFoundError:
            pass
        return movies

    def add_movie(self, title, year, rating, poster):
        """
        Adds a new movie to the CSV file.

        Args:
            title (str): Movie title.
            year (int): Release year.
            rating (float): IMDb rating.
            poster (str): Poster URL.
        """
        movies = self.list_movies()
        movies[title] = {
            'year': year,
            'rating': rating,
            'poster': poster
        }
        self._save_movies(movies)

    def delete_movie(self, title):
        """
        Deletes a movie from the CSV file by title.

        Args:
            title (str): Movie title to delete.
        """
        movies = self.list_movies()
        if title in movies:
            del movies[title]
            self._save_movies(movies)

    def update_movie(self, title, year, rating):
        """
        Updates the year and rating of a movie.
        Poster remains unchanged.

        Args:
            title (str): Movie title to update.
            year (int): New release year.
            rating (float): New IMDb rating.
        """
        movies = self.list_movies()
        if title in movies:
            movies[title]['year'] = year
            movies[title]['rating'] = rating
            self._save_movies(movies)

    def _save_movies(self, movies):
        """
        Saves the entire movie dictionary to the CSV file.

        Args:
            movies (dict): Dictionary of movies to write.
        """
        with open(self.filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['title', 'rating', 'year', 'poster']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for title, data in movies.items():
                writer.writerow({
                    'title': title,
                    'rating': data['rating'],
                    'year': data['year'],
                    'poster': data.get('poster', '')
                })

    def generate_website(self, output_dir="website"):
        """
        Generates a static HTML website of the movie list using a template.

        Args:
            output_dir (str): Directory where the website files are located.
        """
        movies = self.list_movies()
        grid_html = ""
        for title, data in movies.items():
            grid_html += f'''
            <div class="movie">
                <img class="movie-poster" src="{data['poster']}">
                <div class="movie-title">{title}</div>
                <div class="movie-year">{data['year']}</div>
                <div class="movie-rating">{data['rating']}</div>
            </div>
            '''

        try:
            with open(os.path.join(output_dir, "index_template.html"), "r", encoding="utf-8") as template_file:
                template = template_file.read()

            page = template.replace("__TEMPLATE_TITLE__", "My Movie App")
            page = page.replace("__TEMPLATE_MOVIE_GRID__", grid_html)

            with open(os.path.join(output_dir, "index.html"), "w", encoding="utf-8") as output_file:
                output_file.write(page)

            print(Fore.GREEN + "\nWebsite was generated successfully." + Style.RESET_ALL)

        except FileNotFoundError:
            print(Fore.RED + "\nTemplate file not found." + Style.RESET_ALL)
        except Exception as e:
            print(Fore.RED + f"\nAn error occurred while generating the website: {e}" + Style.RESET_ALL)