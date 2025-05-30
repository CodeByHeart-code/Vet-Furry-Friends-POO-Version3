import functions
import logging

def show_menu():
    print("\n=== Veterinary Clinic - Main Menu ===")
    print("1. Register pet")
    print("2. Register consultation")
    print("3. List pets")
    print("4. View consultation history of a pet")
    print("5. Import/Export Data")
    print("6. Exit")

def main():
    logging.info("Application started.")
    # Cargar datos al inicio
    functions.import_all()
    try:
        while True:
            show_menu()
            option = input("Select an option: ").strip()
            if option == "1":
                functions.register_pet()
            elif option == "2":
                functions.register_consultation()
            elif option == "3":
                functions.list_pets()
            elif option == "4":
                functions.view_pet_history()
            elif option == "5":
                functions.show_export_import_menu()
            elif option == "6":
                # Guardar datos al salir
                functions.export_all()
                print("Goodbye!")
                logging.info("Application closed by user.")
                break
            else:
                print("Invalid option. Please try again.")
                logging.warning(f"Invalid menu option selected: {option}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        logging.error(f"Unexpected error in main loop: {e}")
        # Guardar datos en caso de excepción
        functions.export_all()

if __name__ == "__main__":
    main()