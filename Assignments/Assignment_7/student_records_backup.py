import sqlite3

def main():

    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS StudentRecords (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT NOT NULL,
            Age INTEGER NOT NULL,
            Major TEXT NOT NULL
        )
    """)

  
    starting_students = [
        ("Alice Smith", 20, "Computer Science"),
        ("Bob Jones", 21, "Data Science"),
        ("Charlie Brown", 19, "Mathematics"),
        ("Diana Prince", 22, "Physics"),
        ("Evan Wright", 20, "Chemistry")
    ]

    cursor.executemany("""
        INSERT INTO StudentRecords (Name, Age, Major)
        VALUES (?, ?, ?)
    """, starting_students)
    conn.commit()


    print("--- Current Student Records ---")
    cursor.execute("SELECT Name, Age, Major FROM StudentRecords")
    records = cursor.fetchall()
    
    for row in records:
        print(f"Name: {row[0]}, Age: {row[1]}, Major: {row[2]}")
    print("-" * 31)

  
    user_choice = input("\nWould you like to add a new student? (yes/no): ").strip().lower()

    if user_choice == "yes":
        print("\n--- Add New Student ---")
        
        while True:
            name = input("Enter Name: ").strip()
            if name:
                break
            print("Error: Name cannot be empty. Please try again.")

       
        while True:
            age_input = input("Enter Age: ").strip()
            if age_input.isdigit() and int(age_input) > 0:
                age = int(age_input)
                break
            print("Error: Age must be a positive number. Please try again.")

    
        while True:
            major = input("Enter Major: ").strip()
            if major:
                break
            print("Error: Major cannot be empty. Please try again.")

        cursor.execute("""
            INSERT INTO StudentRecords (Name, Age, Major)
            VALUES (?, ?, ?)
        """, (name, age, major))
        conn.commit()
        print(f"\nSuccessfully added {name} to the database!")

     
        print("\n--- Updated Student Records ---")
        cursor.execute("SELECT Name, Age, Major FROM StudentRecords")
        for row in cursor.fetchall():
            print(f"Name: {row[0]}, Age: {row[1]}, Major: {row[2]}")
            
    elif user_choice == "no":
        print("\nNo new student added. Goodbye!")
    else:
        print("\nInvalid choice. Program exiting.")


    conn.close()

if __name__ == "__main__":
    main()
