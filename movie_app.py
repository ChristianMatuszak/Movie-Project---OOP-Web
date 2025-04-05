import random
from colorama import Fore, Style
from rapidfuzz import process
from omdb_api import fetch_movie_data



class MovieApp:
    """
    The MovieApp class encapsulates the core logic for a movie database CLI application.
    It interacts with a storage backend (implementing IStorage) to manage movie records,
    and provides various features such as listing, adding, updating, deleting,
    searching, sorting, filtering, and viewing statistics about movies.
    """
    def __init__(self, storage):
        """
        Initializes the MovieApp with the given storage backend.
        Args:
            storage (IStorage): An instance of a storage class implementing the IStorage interface.
        """
        self._storage = storage


    def _command_list_movies(self):
        """
        Lists all movies stored in the database.
        Displays the movie title, rating, and release year. If no movies exist,
        an appropriate message is shown.
        """
        movies = self._storage.list_movies()
        if not movies:
            print(Fore.RED + "No movies found in the database" + Style.RESET_ALL)
            return

        for titel, data in movies.items():
            print(f"{titel}: {data['rating']} (Released: {data['year']})")

    def _command_add_movie(self):
        """
        Prompts the user for a movie title and fetches movie data from the OMDb API.
        If the movie is found, it is saved to storage with title, year, rating, and poster.
        If not found or the API is unreachable, appropriate feedback is shown.
        """
        title = input("Enter the movie title: ").strip()
        data = fetch_movie_data(title)

        if data:
            self._storage.add_movie(
                title=data["title"],
                year=data["year"],
                rating=data["rating"],
                poster=data["poster"]
            )
            print(
                Fore.GREEN + f"\nMovie '{data['title']}' added successfully." + Style.RESET_ALL)
            self._storage.generate_website()

        else:
            print(
                Fore.RED + "\nFailed to fetch movie data. Please try another title." + Style.RESET_ALL)

    def _command_update_movie(self):
        """
        Prompts the user to update an existing movie's information.
        The user provides a new release year and rating. The updated information is saved in storage.
        """
        title = input("Enter the movie title to update: ")
        year = int(input("Enter the new release year: "))
        rating = float(input("Enter the new rating (1.0 - 10.0): "))
        self._storage.update_movie(title, year, rating)
        print(f"Movie '{title}' updated successfully.")


    def _command_delete_movie(self):
        """
        Prompts the user to delete a movie from the database by title.
        Displays a success message after deletion.
        """
        title = input("Enter the movie title to delete: ")
        self._storage.delete_movie(title)
        print(f"Movie '{title}' deleted successfully.")
        self._storage.generate_website()


    def _command_movie_stats(self):
        """
        Calculates and displays statistics about the movies in the database.

        Statistics include:
            - Average rating
            - Median rating
            - Best-rated movie
            - Worst-rated movie

        If the database is empty, a message is shown.
        """
        movies = self._storage.list_movies()
        if not movies:
            print(Fore.RED + "No movies found in the database" + Style.RESET_ALL)
            return

        ratings = [data['rating'] for data in movies.values()]
        average_rating = sum(ratings) / len(ratings)

        sorted_ratings = sorted(ratings)
        mid = len(sorted_ratings) // 2
        median_rating = (
            sorted_ratings[mid]
            if len(sorted_ratings) % 2
            else (sorted_ratings[mid - 1] + sorted_ratings[mid]) / 2
        )

        best = max(movies.items(), key=lambda x: movies[x]['rating'])
        worst = min(movies.items(), key=lambda x: movies[x]['rating'])

        print(f"Average rating: {average_rating:.2f}")
        print(f"Median rating: {median_rating:.2f}")
        print(f"Best movie: {best[0]} ({best[1]['rating']})")
        print(f"Worst movie: {worst[0]} ({worst[1]['rating']})")


    def _command_random_movie(self):
        """
        Selects and displays a random movie from the database.
        Shows the title, rating, and release year. Displays a message if no movies exist.
        """
        movies = self._storage.list_movies()
        if not movies:
            print(Fore.RED + "No movies found in the database" + Style.RESET_ALL)
            return

        title = random.choice(list(movies.keys()))
        rating = movies[title]['rating']
        year = movies[title]['year']
        print(f"Your movie for tonight: {title}, it's rated {rating}. It was released {year}")


    def _command_search_movie(self):
        """
        Prompts the user to search for a movie using fuzzy matching.
        Displays up to 5 results that match the search term with a score of 75 or higher.
        If no matches are found, a message is displayed.
        """
        movies = self._storage.list_movies()
        if not movies:
            print(Fore.RED + "No movies found in the database" + Style.RESET_ALL)
            return

        query = input("Enter the movie title to search: ").strip().lower()
        matches = process.extract(query, movies.keys(), limit=5)
        relevant = [(title, score) for title, score, _ in matches if score >= 75]

        if relevant:
            print("Found the following matches:")
            for title, _ in relevant:
                data = movies[title]
                print(f"{title}: {data['rating']} (Released: {data['year']})")
            else:
                print(Fore.RED + "No matches found." + Style.RESET_ALL)


    def _command_sort_movies(self):
        """
        Prompts the user to sort movies either by rating (descending) or by year (ascending).
        The sorted movies are displayed with their rating and release year.
        """
        movies = self._storage.list_movies()
        if not movies:
            print(Fore.RED + "No movies found in the database" + Style.RESET_ALL)
            return

        print("\nSort movies by:")
        print("1. Rating (high to low)")
        print("2. Year")
        choice = input("Enter your choice (1 or 2): ").strip()

        if choice == "1":
            sorted_movies = sorted(movies.items(), key=lambda x: x[1]['rating'], reverse=True)
        elif choice == "2":
            sorted_movies = sorted(movies.items(), key=lambda x: x[1]['year'])
        else:
            print(Fore.RED + "Invalid choice." + Style.RESET_ALL)
            return

        for title, data in sorted_movies:
            print(f"{title}: {data['rating']} (Released: {data['year']})")


    def _command_filter_movies(self):
        """
        Filters movies based on user-defined criteria.

        The user can specify:
            - Minimum rating
            - Start year
            - End year

        Only movies matching all criteria are displayed. If no movies match, a message is shown.
        """
        movies = self._storage.list_movies()
        if not movies:
            print(Fore.RED + "No movies found in the database" + Style.RESET_ALL)
            return

        min_rating = input("Enter minimum rating (1.0 - 10.0 or blank for none): ").strip()
        start_year = input("Enter start year (or blank for none): ").strip()
        end_year = input("Enter end year (or blank for none): ").strip()

        min_rating = float(min_rating) if min_rating else None
        start_year = int(start_year) if start_year else None
        end_year = int(end_year) if end_year else None

        filtered_movies = {
            title: data
            for title, data in movies.items()
            if (min_rating is None or data['rating'] >= min_rating)
            and (start_year is None or data['year'] >= start_year)
            and (end_year is None or data['year'] <= end_year)
        }

        if not filtered_movies:
            print(Fore.RED + "No movies match the filter criteria." + Style.RESET_ALL)
            return
        else:
            for title, data in sorted(filtered_movies.items(), key=lambda x: x[1]['year']):
                print(f"{title}: {data['rating']} (Released: {data['year']})")

    def run(self):
        """
        Runs the main loop of the movie application.

        Displays a menu of commands, receives user input, and executes the corresponding
        actions by calling internal methods. The loop continues until the user chooses to exit.
        """
        while True:
            print("\n🎬 " + Fore.CYAN + "Movie Database Menu" + Style.RESET_ALL)
            print(Fore.GREEN + "1." + Style.RESET_ALL + " List movies")
            print(Fore.GREEN + "2." + Style.RESET_ALL + " Add movie")
            print(Fore.GREEN + "3." + Style.RESET_ALL + " Update movie")
            print(Fore.GREEN + "4." + Style.RESET_ALL + " Delete movie")
            print(Fore.GREEN + "5." + Style.RESET_ALL + " Movie statistics")
            print(Fore.GREEN + "6." + Style.RESET_ALL + " Random movie")
            print(Fore.GREEN + "7." + Style.RESET_ALL + " Search movie")
            print(Fore.GREEN + "8." + Style.RESET_ALL + " Sort movies")
            print(Fore.GREEN + "9." + Style.RESET_ALL + " Filter movies")
            print(Fore.GREEN + "10." + Style.RESET_ALL + " Generate website")
            print(Fore.YELLOW + "0." + Style.RESET_ALL + " Exit")

            choice = input("\nEnter your choice (0–10): ").strip()

            if choice == "1":
                self._command_list_movies()
            elif choice == "2":
                self._command_add_movie()
            elif choice == "3":
                self._command_update_movie()
            elif choice == "4":
                self._command_delete_movie()
            elif choice == "5":
                self._command_movie_stats()
            elif choice == "6":
                self._command_random_movie()
            elif choice == "7":
                self._command_search_movie()
            elif choice == "8":
                self._command_sort_movies()
            elif choice == "9":
                self._command_filter_movies()
            elif choice == "10":
                self._storage.generate_website()
            elif choice == "0":
                print(Fore.YELLOW + "\nGoodbye!" + Style.RESET_ALL)
                break
            else:
                print(Fore.RED + "Invalid choice. Please try again." + Style.RESET_ALL)
