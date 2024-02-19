class Library:
    def __init__(self, database_file):
        self.database_file = database_file
        try:
            self.file = open(self.database_file, 'a+')
        except FileNotFoundError:
            print("Database file not found.")

    def __del__(self):
        self.file.close()
        print("Database file closed.")

    def list_books(self):
        self.file.seek(0)
        books = self.file.read().splitlines()
        if books:
            print("List of books:")
            for book in books:
                book_info = book.split(',')
                print(f"- Title: {book_info[0]}, Author: {book_info[1]}, Genre: {book_info[2]}, Pages: {book_info[4]}")
        else:
            print("No books found in the library.")

    def add_book(self):
        title = input("Enter the book title: ")
        author = input("Enter the book author: ")
        genre = input("Enter the genre of the book: ")
        release_year = input("Enter the first release year: ")
        num_pages = input("Enter the number of pages: ")

        book_info = f"{title},{author},{genre},{release_year},{num_pages}\n"  
        self.file.write(book_info)
        print("Book added successfully.")

    def remove_book(self):
        self.file.seek(0)
        books = self.file.readlines()
        if not books:
            print("No books found in the library.")
            return

        title_to_remove = input("Enter the title of the book to remove: ")

        updated_books = []
        removed = False
        for book in books:
            book_info = book.strip().split(',')
            if book_info[0] == title_to_remove:
                removed = True
            else:
                updated_books.append(book)

        if removed:
            with open(self.database_file, 'w') as file:
                file.writelines(updated_books)
            self.remove_ratings_and_comments(title_to_remove)
            print(f"Book '{title_to_remove}' removed successfully.")
        else:
            print(f"Book '{title_to_remove}' not found in the library.")

    def remove_ratings_and_comments(self, title):
        try:
            with open("ratings_comments.txt", "r+") as rc_file:
                lines = rc_file.readlines()
                rc_file.seek(0)
                for line in lines:
                    if not line.startswith(title + ','):
                        rc_file.write(line)
                rc_file.truncate()
        except:
            passthisline = 0

    def rate_book(self):
        title = input("Enter the title of the book to rate: ")
        if not self.is_book_exist(title):
            print(f"No such book with title '{title}'.")
            return
        rating = input("Enter a rating for this book (1-5): ")
        comment = input("Enter a comment for this book: ")
        self.record_rating_and_comment(title, rating, comment)

    def is_book_exist(self, title):
        self.file.seek(0)
        for book in self.file.readlines():
            if book.strip().split(',')[0] == title:
                return True
        return False

    def record_rating_and_comment(self, title, rating, comment):
        with open("ratings_comments.txt", "a") as rc_file:
            rc_file.write(f"{title},{rating},{comment}\n")

    def calculate_average_rating(self, title):
        with open("ratings_comments.txt") as rc_file:
            ratings = []
            for line in rc_file:
                data = line.strip().split(',')
                if data[0] == title:
                    ratings.append(int(data[1]))
            if ratings:
                average_rating = sum(ratings) / len(ratings)
                return average_rating
            else:
                return "No ratings yet."

    def view_average_rating(self, title):
        average_rating = self.calculate_average_rating(title)
        if average_rating != "No ratings yet.":
            print(f"Average rating for '{title}': {average_rating}")
        else:
            print(f"No ratings yet for '{title}'.")

    def view_ratings_and_comments(self, title):
        with open("ratings_comments.txt") as rc_file:
            print(f"Comments and ratings for '{title}':")
            found = False
            for line in rc_file:
                data = line.strip().split(',')
                if data[0] == title:
                    print(f"- Rating: {data[1]}, Comment: {data[2]}")
                    found = True
            if not found:
                print("No comments or ratings yet for this book.")

    def filter_books_by_year(self):
        self.file.seek(0)
        books = self.file.readlines()
        books.sort(key=lambda x: int(x.strip().split(',')[3]), reverse=True)
        print("Books sorted by release year (descending):")
        for book in books:
            book_info = book.strip().split(',')
            print(f"- Title: {book_info[0]}, Author: {book_info[1]}, Release Year: {book_info[3]}")

    def filter_books_by_author(self):
        author = input("Enter the author's name to filter books: ")
        self.file.seek(0)
        books = self.file.readlines()
        found = False
        print(f"Books by author '{author}':")
        for book in books:
            book_info = book.strip().split(',')
            if book_info[1] == author:
                print(f"- Title: {book_info[0]}, Author: {book_info[1]}")
                found = True
        if not found:
            print("No books found by this author.")

    def filter_books_by_genre(self):
        genre = input("Enter the genre to filter books: ")
        self.file.seek(0)
        books = self.file.readlines()
        found = False
        print(f"Books in genre '{genre}':")
        for book in books:
            book_info = book.strip().split(',')
            if book_info[2] == genre:
                print(f"- Title: {book_info[0]}, Author: {book_info[1]}, Genre: {book_info[2]}")
                found = True
        if not found:
            print("No books found in this genre.")

    def filter_books_by_pages(self):
        self.file.seek(0)
        books = self.file.readlines()
        books.sort(key=lambda x: int(x.strip().split(',')[4]), reverse=True)
        print("Books sorted by number of pages:")
        for book in books:
            book_info = book.strip().split(',')
            print(f"- Title: {book_info[0]}, Author: {book_info[1]}, Number of Pages: {book_info[4]}")

    def filter_books_by_average_rating(self):
        with open("ratings_comments.txt") as rc_file:
            book_ratings = {}
            for line in rc_file:
                data = line.strip().split(',')
                title = data[0]
                rating = int(data[1])
                if title in book_ratings:
                    book_ratings[title].append(rating)
                else:
                    book_ratings[title] = [rating]

        average_ratings = {}
        for title, ratings in book_ratings.items():
            average_ratings[title] = sum(ratings) / len(ratings) if ratings else 0

        sorted_books = sorted(average_ratings.items(), key=lambda x: x[1], reverse=True)

        print("Books sorted by average rating:")
        for title, avg_rating in sorted_books:
            print(f"- Title: {title}, Average Rating: {avg_rating}")

    def print_filter_menu(self):
        print(" -- FILTER MENU -- ")
        print("a) Sort Books by Release Year")
        print("b) Filter Books by Author")
        print("c) Sort Books by Number of Pages")
        print("d) Sort Books by Average Rating")
        print("e) Filter Books by Genre")
        print("f) Return to Main Menu")

    def print_menu(self):
        print(" *** MAIN MENU***")
        print("1) List Books")
        print("2) Add Book")
        print("3) Remove Book")
        print("4) Filter Books")
        print("5) Rate a Book")
        print("6) View Average Rating for a Book")
        print("7) View Ratings and Comments for a Book")
        print("8) Quit")

    def run(self):
        while True:
            self.print_menu()
            menu_choice = input("Enter your choice (1/2/3/4/5/6/7/8): ")

            if menu_choice == "1":
                self.list_books()
            elif menu_choice == "2":
                self.add_book()
            elif menu_choice == "3":
                self.remove_book()
            elif menu_choice == "4":
                
                while True:
                    self.print_filter_menu()
                    filter_choice = input("Enter your choice (a/b/c/d/e/f): ")
                    if filter_choice == "a":
                        self.filter_books_by_year()
                    elif filter_choice == "b":
                        self.filter_books_by_author()
                    elif filter_choice == "c":
                        self.filter_books_by_pages()
                    elif filter_choice == "d":
                        self.filter_books_by_average_rating()
                    elif filter_choice == "e":
                        self.filter_books_by_genre()
                    elif filter_choice == "f":
                        break
                    else:
                        print("Invalid choice. Please try again.")
            elif menu_choice == "5":
                self.rate_book()
            elif menu_choice == "6":
                title = input("Enter the title of the book: ")
                self.view_average_rating(title)
            elif menu_choice == "7":
                title = input("Enter the title of the book: ")
                self.view_ratings_and_comments(title)
            elif menu_choice == "8":
                break
            else:
                print("Invalid choice. Please try again.")

        print("You have quitted from the program.")

lib = Library("books.txt")
lib.run()
