from databaseActions import DatabaseActions, Person



def display_menu():
    print(f"==Database Modification System==")
    print(f"1. Generate Database")
    print(f"2. Add a name")
    print(f"3. Search for a name")
    print(f"4. Update a record")
    print(f"5. Delete a record")
    print(f"6. Exit")

    choice = input("Enter your choice: ")
    return run_menu(choice)

def run_menu(choice: int):
    choice = int(choice)
    if choice == 1:
        answer = input(f"Are you sure you want to generate the database? This will delete any existing data,Estimated time of completion(1hr 30min) (y/n): ")
        if answer.lower() == "y":
            DatabaseActions.generate_database()
            return False
        return False
    elif choice == 2:
        name = input(f"Please enter the name: ")
        sex = input(f"Please enter the person's sex (M/F): ")
        year = input(f"Please enter the person's year of birth: ")
        numbberOfOccurences = input(f"Please enter the number of occurences of {name} in the {year}: ")

        person = Person(None, name, sex, year, numbberOfOccurences)
        DatabaseActions.create_person(person)
        return False
    elif choice == 3:
        name = input(f"Please enter the name to search for: ")
        person = DatabaseActions.get_person_by_name(name)
        if person:
            print(person)
        else:
            print("Person not found.")
        return False
    elif choice == 4:
        id = input(f"Please input a name of id")
        actualPerson = None
        if id.isdigit():
            actualPerson = DatabaseActions.get_person_by_id(int(id))
        else:
            actualPerson = DatabaseActions.get_person_by_name(id)

        if not actualPerson:
            print("Person not found.")
            return False

        name = input(f"Please enter the new name (leave blank to keep current) '{actualPerson.name}': ")
        sex = input(f"Please enter the sex of the person (M/F) (leave blank to keep current) '{actualPerson.sex}': ")
        year = input(f"Please enter the year of birth (leave blank to keep current) '{actualPerson.year}': ")
        numberOfOccurences = input(f"Please enter the new number of occurences (leave blank to keep current) '{actualPerson.numberOfOccurences}': ")

        if name: 
            actualPerson.name = name
        if sex:
            actualPerson.Sex = sex
        if year:
            actualPerson.year = year
        if numberOfOccurences:
            actualPerson.numberOfOccurences = int(numberOfOccurences)

        if actualPerson is not None:
            DatabaseActions.update_person(actualPerson)
        else:
            print("Person not found.")
        return False
    elif choice == 5:
        record = input(f"Please input the name or id of the record you want to delete: ")
        if record.isdigit():
            person = DatabaseActions.delete_person(DatabaseActions.get_person_by_id(int(record)))
        else:
            person = DatabaseActions.delete_person(DatabaseActions.get_person_by_name(record))
        return False
    return True


if __name__ == "__main__":
    while True:
        exit = display_menu()
        if exit:
            break