import sqlite3
from datetime import datetime
import os



# ==========================
# DATABASE SETUP
# ==========================

connection = sqlite3.connect("feedback.db")
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS feedback(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    reference TEXT,
    name TEXT,
    email TEXT,
    school TEXT,
    year TEXT,
    feedback_type TEXT,
    category TEXT,
    message TEXT,
    date TEXT
)
""")

connection.commit() 
def generate_reference():

    cursor.execute("SELECT COUNT(*) FROM feedback")

    count = cursor.fetchone()[0] + 1

    return f"FB-{count:04d}"
def student_portal():

    print("\n" + "="*60)
    print("               STUDENT PORTAL")
    print("="*60)

    while True:
        name = input("Enter your name: ").strip()
        if name != "":
            break
        print("Name cannot be empty.")

    while True:
        email = input("Enter your email: ").strip()

        if "@" in email and "." in email:
            break

        print("Invalid email.")

    schools = {
        "1":"SCES",
        "2":"SIMS",
        "3":"STH",
        "4":"SBS"
    }

    print("\nChoose School")
    print("1. SCES")
    print("2. SIMS")
    print("3. STH")
    print("4. SBS")

    while True:

        school_choice = input("Choice : ")

        if school_choice in schools:
            school = schools[school_choice]
            break

        print("Invalid choice.")

    if school == "SCES":
        years=["1","2","3","4","5"]
    else:
        years=["1","2","3","4"]

    print("\nChoose Year")

    for year in years:
        print(f"{year}. Year {year}")

    while True:

        year=input("Choice : ")

        if year in years:
            break

        print("Invalid Year.")

    print(f"\nHey {name}! 😊")

    print("\nWould you like to leave a:")

    print("1. Suggestion")
    print("2. Complaint")

    while True:

        choice=input("Choice : ")

        if choice=="1":
            feedback_type="Suggestion"
            break

        elif choice=="2":
            feedback_type="Complaint"
            break

        print("Invalid choice.")

    print("\nChoose Category")

    print("1. Education")
    print("2. Injustice")
    print("3. Sanitation")

    while True:

        category_choice=input("Choice : ")

        if category_choice=="1":
            category="Education"
            break

        elif category_choice=="2":
            category="Injustice"
            break

        elif category_choice=="3":
            category="Sanitation"
            break

        print("Invalid choice.")

    print("\nType your feedback below.")

    message=input("> ")

    reference=generate_reference()

    date=datetime.now().strftime("%d/%m/%Y %H:%M")

    cursor.execute("""
    INSERT INTO feedback
    VALUES(NULL,?,?,?,?,?,?,?,?,?)
    """,(reference,
         name,
         email,
         school,
         year,
         feedback_type,
         category,
         message,
         date))

    connection.commit()

    print("\n"+"="*60)
    print("SUBMISSION SUCCESSFUL")
    print("="*60)

    print(f"Reference Number : {reference}")

    print("\nThank you",name+"!")

    print("Your message has been received successfully.")

    print("A response will be delivered within 14 days.")

    input("\nPress ENTER to return to the menu...") 
    
def administrator_portal():

    password = input("\nEnter Administrator Password: ")

    if password != "admin123":
        print("Incorrect password!")
        input("\nPress ENTER to return...")
        return

    while True:

        print("\n" + "=" * 60)
        print("          ADMINISTRATOR PORTAL")
        print("=" * 60)

        print("1. View All Feedback")
        print("2. Search Feedback")
        print("3. Statistics")
        print("4. Generate Summary")
        print("5. Delete Feedback")
        print("6. Logout")

        choice = input("\nChoice: ")

        if choice == "1":

            cursor.execute("""
            SELECT reference,
                   name,
                   school,
                   feedback_type,
                   category,
                   date
            FROM feedback
            """)

            rows = cursor.fetchall()

            if len(rows) == 0:
                print("\nNo feedback found.")

            else:

                print()

                for row in rows:

                    print("=" * 60)
                    print("Reference :", row[0])
                    print("Student   :", row[1])
                    print("School    :", row[2])
                    print("Type      :", row[3])
                    print("Category  :", row[4])
                    print("Date      :", row[5])

            input("\nPress ENTER...")

        elif choice == "6":
            break
        elif choice == "2":

            print("\nSEARCH MENU")
            print("1. Search by Name")
            print("2. Search by School")
            print("3. Search by Category")
            print("4. Search by Reference")

            search_choice = input("\nChoice: ")

            if search_choice == "1":

                keyword = input("Enter Name: ")

                cursor.execute("""
                SELECT * FROM feedback
                WHERE name LIKE ?
                """, ('%' + keyword + '%',))

            elif search_choice == "2":

                keyword = input("Enter School: ")

                cursor.execute("""
                SELECT * FROM feedback
                WHERE school LIKE ?
                """, ('%' + keyword + '%',))

            elif search_choice == "3":

                keyword = input("Enter Category: ")

                cursor.execute("""
                SELECT * FROM feedback
                WHERE category LIKE ?
                """, ('%' + keyword + '%',))

            elif search_choice == "4":

                keyword = input("Reference Number: ")

                cursor.execute("""
                SELECT * FROM feedback
                WHERE reference=?
                """, (keyword,))

            else:
                print("Invalid Choice.")
                continue

            rows = cursor.fetchall()

            if len(rows) == 0:
                print("\nNo results found.")

            else:
                for row in rows:

                    print("=" * 60)
                    print("Reference :", row[1])
                    print("Student   :", row[2])
                    print("Email     :", row[3])
                    print("School    :", row[4])
                    print("Year      :", row[5])
                    print("Type      :", row[6])
                    print("Category  :", row[7])
                    print("Message   :", row[8])
                    print("Date      :", row[9])

            input("\nPress ENTER...")

        elif choice == "3":

            print("\n" + "=" * 60)
            print("SYSTEM STATISTICS")
            print("=" * 60)

            cursor.execute("SELECT COUNT(*) FROM feedback")
            total = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM feedback WHERE feedback_type='Suggestion'")
            suggestions = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM feedback WHERE feedback_type='Complaint'")
            complaints = cursor.fetchone()[0]

            print(f"\nTotal Feedback : {total}")
            print(f"Suggestions    : {suggestions}")
            print(f"Complaints     : {complaints}")

            print("\nSchools")

            for school in ["SCES", "SIMS", "STH", "SBS"]:
                cursor.execute("SELECT COUNT(*) FROM feedback WHERE school=?", (school,))
                print(f"{school:<10}{cursor.fetchone()[0]}")

            print("\nCategories")

            for category in ["Education", "Injustice", "Sanitation"]:
                cursor.execute("SELECT COUNT(*) FROM feedback WHERE category=?", (category,))
                print(f"{category:<15}{cursor.fetchone()[0]}")

            input("\nPress ENTER...")
            export = input("\nExport report? (Y/N): ")

            if export.upper()=="Y":

              export_report()

        elif choice == "4":
            print("\n" + "=" * 60)
            print("SUMMARY REPORT")
            print("=" * 60)

            categories = ["Education", "Injustice", "Sanitation"]

            for category in categories:

                print(f"\n{category.upper()}")
                print("-" * 40)

                # Complaints
                print("\nComplaints:")

                cursor.execute("""
                SELECT message
                FROM feedback
                WHERE category=? AND feedback_type='Complaint'
                """, (category,))

                complaints = cursor.fetchall()

                if complaints:

                   for complaint in complaints:
                       print("•", complaint[0])

                else:
                  print("None")

               # Suggestions
                print("\nSuggestions:")

                cursor.execute("""
                SELECT message
                FROM feedback
                WHERE category=? AND feedback_type='Suggestion'
                 """, (category,))

                suggestions = cursor.fetchall()

                if suggestions:

                  for suggestion in suggestions:
                      print("•", suggestion[0])

                else:
                   print("None")

                print("\n" + "-" * 60)

            input("\nPress ENTER...")

        elif choice == "5":
                reference = input("\nEnter Reference Number: ")

                cursor.execute("""
                SELECT reference,name
                FROM feedback
                WHERE reference=?
                 """,(reference,))

                row = cursor.fetchone()

                if row is None:

                  print("\nReference not found.")

                else:

                  print("\nFound:")

                  print("Reference :",row[0])

                  print("Student :",row[1])

                  confirm=input("\nDelete this feedback? (Y/N): ")

                  if confirm.upper()=="Y":

                     cursor.execute("""
                     DELETE FROM feedback
                      WHERE reference=?
                      """,(reference,))

                     connection.commit()

                     print("\nFeedback deleted successfully.")

                  else:

                    print("\nDeletion cancelled.")

        input("\nPress ENTER...")

    else:
        print("\nInvalid choice.")
    
def export_report():

    file = open("Summary_Report.txt","w")

    file.write("STRATHMORE FEEDBACK SUMMARY\n")
    file.write("="*40+"\n\n")

    categories=["Education","Injustice","Sanitation"]

    for category in categories:

        file.write(category+"\n")
        file.write("-"*30+"\n")

        cursor.execute("""
        SELECT feedback_type,message
        FROM feedback
        WHERE category=?
        """,(category,))

        rows=cursor.fetchall()

        if len(rows)==0:

            file.write("No feedback.\n\n")

        else:

            for row in rows:

                file.write(f"[{row[0]}] {row[1]}\n")

            file.write("\n")

    file.close()

    print("\nSummary_Report.txt created successfully.")

def main_menu():
 while True:

     print("\n" + "=" * 55)
     print("     STRATHMORE FEEDBACK MANAGEMENT SYSTEM")
     print("=" * 55)

     print("1. Student Portal")
     print("2. Administrator Portal")
     print("3. Exit")

     choice = input("\nChoose an option: ")

     if choice == "1":
            student_portal()

     elif choice == "2":
            administrator_portal()

     elif choice == "3":
            print("\nThank you for using the system.")
            break

     else:
            print("\nInvalid choice.")

main_menu()

connection.close() 