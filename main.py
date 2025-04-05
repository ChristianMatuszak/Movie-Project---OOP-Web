from colorama import Fore, Style
from storage.storage_csv import StorageCsv
from movie_app import MovieApp

def main():
    """
    Entry point for the movie database application.
    Initializes the storage backend and starts the MovieApp.
    """
    storage = StorageCsv("data.csv")  # or "john.json", etc.
    app = MovieApp(storage)
    app.run()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(Fore.RED + "\nProgram terminated by user." + Style.RESET_ALL)
