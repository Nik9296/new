import sqlite3
from datetime import date

# ------------------ Database Setup ------------------
conn = sqlite3.connect("library.db")
cursor = conn.cursor()

# Create tables
cursor.execute("""
CREATE TABLE IF NOT EXISTS books (
    book_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT,
    qty INTEGER DEFAULT 1
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS issued (
    issue_id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id INTEGER,
    student_name TEXT,
    issue_date TEXT,
    return_date TEXT,
    FOREIGN KEY(book_id) REFERENCES books(book_id)
)
""")
conn.commit()

# ------------------ Functions ------------------
def add_book():
    title = input("Enter Book Title: ")
    author = input("Enter Author Name: ")
    qty = int(input("Enter Quantity: "))
    cursor.execute("INSERT INTO books (title, author, qty) VALUES (?, ?, ?)", (title, author, qty))
    conn.commit()
    print("✅ Book added successfully!")

def view_books():
    cursor.execute("SELECT * FROM books")
    for row in cursor.fetchall():
        print(row)

def search_book():
    title = input("Enter book title to search: ")
    cursor.execute("SELECT * FROM books WHERE title LIKE ?", ('%' + title + '%',))
    data = cursor.fetchall()
    if data:
        for book in data:
            print(book)
    else:
        print("❌ No book found!")

def issue_book():
    book_id = int(input("Enter Book ID: "))
    student = input("Enter Student Name: ")

    # Check if book available
    cursor.execute("SELECT qty FROM books WHERE book_id=?", (book_id,))
    result = cursor.fetchone()

    if result and result[0] > 0:
        issue_date = date.today()
        cursor.execute("INSERT INTO issued (book_id, student_name, issue_date) VALUES (?, ?, ?)",
                       (book_id, student, issue_date))
        cursor.execute("UPDATE books SET qty = qty - 1 WHERE book_id=?", (book_id,))
        conn.commit()
        print("📘 Book issued successfully!")
    else:
        print("❌ Book not available!")

def return_book():
    issue_id = int(input("Enter Issue ID to return: "))
    cursor.execute("SELECT book_id FROM issued WHERE issue_id=?", (issue_id,))
    data = cursor.fetchone()

    if data:
        book_id = data[0]
        return_date = date.today()
        cursor.execute("UPDATE issued SET return_date=? WHERE issue_id=?", (return_date, issue_id))
        cursor.execute("UPDATE books SET qty = qty + 1 WHERE book_id=?", (book_id,))
        conn.commit()
        print("✅ Book returned successfully!")
    else:
        print("❌ Invalid Issue ID!")

def view_issued_books():
    cursor.execute("""
    SELECT issued.issue_id, books.title, issued.student_name, issued.issue_date, issued.return_date
    FROM issued
    JOIN books ON issued.book_id = books.book_id
    """)
    for row in cursor.fetchall():
        print(row)

def delete_book():
    book_id = int(input("Enter Book ID to delete: "))
    cursor.execute("DELETE FROM books WHERE book_id=?", (book_id,))
    conn.commit()
    print("🗑️ Book deleted successfully!")

# ------------------ Menu ------------------
def main():
    while True:
        print("\n===== 📚 LIBRARY MANAGEMENT SYSTEM =====")
        print("1. Add Book")
        print("2. View All Books")
        print("3. Search Book")
        print("4. Issue Book")
        print("5. Return Book")
        print("6. View Issued Books")
        print("7. Delete Book")
        print("8. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            add_book()
        elif choice == '2':
            view_books()
        elif choice == '3':
            search_book()
        elif choice == '4':
            issue_book()
        elif choice == '5':
            return_book()
        elif choice == '6':
            view_issued_books()
        elif choice == '7':
            delete_book()
        elif choice == '8':
            print("👋 Exiting... Have a nice day!")
            break
        else:
            print("❌ Invalid choice! Please try again.")

main()
