from abc import ABC, abstractmethod

class IStorage(ABC):
    """
    Interface for movie storage backends.
    Defines the standard methods required to manage a movie collection,
    such as listing, adding, deleting, and updating movies.
    """

    @abstractmethod
    def list_movies(self):
        """
        Retrieves all stored movies.
        Returns:
            dict: A dictionary where keys are movie titles (str), and values
                  are dictionaries with 'year' (int) and 'rating' (float).
        """
        pass

    @abstractmethod
    def add_movie(self, title, year, rating, poster):
        """
        Adds a new movie to the storage.
        Args:
            title (str): The movie title.
            year (int): The release year.
            rating (float): The movie rating.
            poster (str): The URL of the movie poster.
        """
        pass

    @abstractmethod
    def delete_movie(self, title):
        """
        Deletes a movie from the storage by title.
        Args:
            title (str): The title of the movie to be removed.
        """
        pass

    @abstractmethod
    def update_movie(self, title, year, rating):
        """
        Updates the rating of an existing movie.
        Args:
            title (str): The title of the movie to update.
            year (int): The new release year.
            rating (float): The new rating value.
        """
        pass
