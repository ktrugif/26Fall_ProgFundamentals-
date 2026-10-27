import sqlite3

# 1. Connect to the database (added quotes around 'library.db')
conn = sqlite3.connect('library.db')
cur = conn.cursor()

# Remove the old table, so this step can be run again.
cur.execute('DROP TABLE IF EXISTS Books')

cur.execute('''
CREATE TABLE Books (
    id INT NOT NULL,
    Title VARCHAR(30) NOT NULL,
    author VARCHAR(30) NOT NULL,
    year INT,
    genre VARCHAR(30),
    copies INT,
    rating INT
)
''')
conn.commit()

print('The library database has been created and the Books table has been added.')

# 2. Fixed single insert (added quotes around text values)
cur.execute("INSERT INTO Books VALUES (1, 'Maya', 'Maya', 2020, 'Biology', 15, 5)")

# 3. List of tuples to insert
Books = [
    (1, 'The Road', 'Cormac McCarthy', 2006, 'Fiction', 250000, 4),
    (2, 'A Visit from the Goon Squad', 'Jennifer Egan', 2010, 'Fiction', 100000, 5),
    (3, 'The Call of The Wild', 'Jack London', 1904, 'Fiction', 50000, 4),
    (4, 'Claws for Alarm: A Mrs. Murphy Mystery', 'Rita Mae Brown', 2022, 'Mystery', 35000, 3.9),
    (5, 'The Wager: A Tale of Shipwreck, Mutiny and Murder', 'David Grann', 2023, 'Nonfiction History', 1000000, 4.1),
    (6, 'Funny Story', 'Emily Henry', 2024, 'Romance', 800000, 4),
    (7, 'The Love Hypothesis', 'Colleen Hoover', 2020, 'Romance', 150000, 4.5),
    (8, 'Get a Life, Chloe Brown', 'Talia Hibbert', 2019, 'Romance', 300000, 5),
    (9, 'Never Smile at Children', 'Lou Marchetti', 1959, 'Mystery', 0, 0)
]

# Note: id starts at 2 or matches your tuple unpacking cleanly
cur.executemany("INSERT INTO Books VALUES (?, ?, ?, ?, ?, ?, ?)", Books)
conn.commit()

print("Books Published after 1990:")
for row in cur.execute('SELECT Title, author FROM Books WHERE year > 1990'):
    print(row)

print("Fiction books with more than two copies:")
for row in cur.execute("SELECT Title, author FROM Books WHERE genre = 'Fiction' AND copies > 2"):
    print(row)

print("Book printed before 1900s or rated 5")
for row in cur.execute("SELECT Title, author FROM Books WHERE year < 1900 OR rating = 5"):
    print(row)

print("Books that are  in the fiction genre ")
for row in cur.execute("SELECT Title, author FROM Books WHERE genre = 'Fiction'"):
    print(row)

    print("Books that are  in the romance genre ")
for row in cur.execute("SELECT Title, author FROM Books WHERE genre = 'Romance'"):
    print(row)

print("Books that are  in the mystery genre ")
for row in cur.execute("SELECT Title, author FROM Books WHERE genre = 'Mystery'"):
    print(row)  

print("Books that are  in the nonfiction history genre ")
for row in cur.execute("SELECT Title, author FROM Books WHERE genre = 'Nonfiction History'"):
    print(row)      

letters = input( "Choose a letter of the alphabet to see all books that start with that letter: " )
for row in cur.execute("SELECT Title, author FROM Books WHERE Title LIKE ?", (letters + '%',)):
    print(row)      
print("\nBooks with no rating:")
for row in cur.execute("SELECT Title, author FROM Books WHERE rating IS NULL OR rating = '' OR rating = 0"):
    print(row)


conn.commit()
conn.close()