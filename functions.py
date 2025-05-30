import logging
import csv
import json
import os
from classes import Owner, Pet, Consultation

# Configuración del logging
logging.basicConfig(
    filename='clinica_veterinaria.log',
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Listas para almacenar objetos Owner y Pet
owners = []
pets = []

def is_valid_name(value):
    """Valida que el valor no sea solo numérico y tenga sentido como nombre."""
    return value and not value.isdigit() and any(char.isalpha() for char in value)

def is_valid_reason_or_diagnosis(value):
    """Valida que el motivo o diagnóstico no sea solo numérico, no esté vacío y tenga letras."""
    return value and not value.isdigit() and any(char.isalpha() for char in value)

def is_valid_date(value):
    """Valida que la fecha no esté vacía, no sea solo números y que tenga formato básico."""
    return value and not value.isdigit() and any(char.isdigit() for char in value) and not any(char.isalpha() for char in value)

def register_owner():
    """Registra un nuevo dueño y lo agrega a la lista de dueños. Maneja errores de entrada y los deja en el log."""
    print("=== Register Owner ===")
    try:
        name = input("Owner's name: ").strip()
        if not is_valid_name(name):
            logging.warning(f"Nombre de dueño inválido ingresado: '{name}'")
            raise ValueError("Owner's name must contain letters and cannot be only numbers.")

        phone = input("Phone: ").strip()
        if not phone or phone.isalpha():
            logging.warning(f"Teléfono inválido ingresado: '{phone}'")
            raise ValueError("Phone must be a non-empty number.")

        address = input("Address: ").strip()
        if not address:
            logging.warning("Dirección vacía ingresada.")
            raise ValueError("Address cannot be empty.")

        owner = Owner(name, phone, address)
        owners.append(owner)
        print("Owner successfully registered.")
        logging.info(f"Owner registered: {owner}")
        return owner
    except ValueError as ve:
        print(f"Input error: {ve}")
        logging.warning(f"Input error in register_owner: {ve}")
    except Exception as e:
        print(f"Error registering owner: {e}")
        logging.error(f"Exception in register_owner: {e}")


def find_owner_by_name(name):
    """Busca un dueño por nombre."""
    for o in owners:
        if o.name.lower() == name.lower():
            return o
    return None


def register_pet():
    """Registra una nueva mascota y la asigna a un dueño, validando entradas y logueando errores."""
    print("=== Register Pet ===")
    try:
        name = input("Pet's name: ").strip()
        if not is_valid_name(name):
            logging.warning(f"Nombre de mascota inválido ingresado: '{name}'")
            raise ValueError("Pet's name must contain letters and cannot be only numbers.")

        species = input("Species: ").strip()
        if not is_valid_name(species):
            logging.warning(f"Especie inválida ingresada: '{species}'")
            raise ValueError("Species must contain letters and cannot be only numbers.")

        breed = input("Breed: ").strip()
        if not is_valid_name(breed):
            logging.warning(f"Raza inválida ingresada: '{breed}'")
            raise ValueError("Breed must contain letters and cannot be only numbers.")

        age_input = input("Age: ").strip()
        if not age_input.isdigit() or int(age_input) < 0:
            logging.warning(f"Edad inválida ingresada: '{age_input}'")
            raise ValueError("Age must be a non-negative integer.")
        age = int(age_input)

        owner_name = input("Owner's name: ").strip()
        if not is_valid_name(owner_name):
            logging.warning(f"Nombre de dueño inválido ingresado: '{owner_name}'")
            raise ValueError("Owner's name must contain letters and cannot be only numbers.")

        owner = find_owner_by_name(owner_name)
        if not owner:
            print("Owner not found. Please register them first.")
            logging.warning(f"Attempted to register pet for non-existent owner: {owner_name}")
            owner = register_owner()
            if not owner:
                logging.error("Pet registration aborted due to failed owner registration.")
                return

        pet = Pet(name, species, breed, age, owner)
        pets.append(pet)
        print("Pet successfully registered.")
        logging.info(f"Pet registered: {pet}")
    except ValueError as ve:
        print(f"Input error: {ve}")
        logging.warning(f"Input error in register_pet: {ve}")
    except Exception as e:
        print(f"Error registering pet: {e}")
        logging.error(f"Exception in register_pet: {e}")


def find_pet_by_name(name):
    """Busca una mascota por nombre."""
    for p in pets:
        if p.name.lower() == name.lower():
            return p
    return None


def register_consultation():
    """Registra una consulta veterinaria para una mascota específica, validando entradas y logueando errores."""
    print("=== Register Consultation ===")
    try:
        pet_name = input("Pet's name: ").strip()
        if not is_valid_name(pet_name):
            logging.warning(f"Nombre de mascota inválido ingresado para consulta: '{pet_name}'")
            raise ValueError("Pet's name must contain letters and cannot be only numbers.")
        pet = find_pet_by_name(pet_name)
        if not pet:
            print("Pet not found, please register it first.")
            logging.warning(f"Attempted to register consultation for non-existent pet: {pet_name}")
            return
        date = input("Date of consultation: ").strip()
        if not is_valid_date(date):
            logging.warning(f"Fecha inválida ingresada: '{date}'")
            raise ValueError("Date must not be only numbers, cannot be empty and should contain digits and separators (e.g. 10/05/2024).")
        reason = input("Reason: ").strip()
        if not is_valid_reason_or_diagnosis(reason):
            logging.warning(f"Motivo inválido ingresado: '{reason}'")
            raise ValueError("Reason must contain letters and cannot be only numbers.")
        diagnosis = input("Diagnosis: ").strip()
        if not is_valid_reason_or_diagnosis(diagnosis):
            logging.warning(f"Diagnóstico inválido ingresado: '{diagnosis}'")
            raise ValueError("Diagnosis must contain letters and cannot be only numbers.")
        consultation = Consultation(date, reason, diagnosis, pet)
        pet.add_consultation(consultation)
        print("Consultation successfully registered.")
        logging.info(f"Consultation registered for pet {pet.name}: {consultation}")
    except ValueError as ve:
        print(f"Input error: {ve}")
        logging.warning(f"Input error in register_consultation: {ve}")
    except Exception as e:
        print(f"Error registering consultation: {e}")
        logging.error(f"Exception in register_consultation: {e}")


def list_pets():
    """Muestra todas las mascotas registradas y sus dueños."""
    print("=== List of Pets ===")
    if not pets:
        print("No pets registered.")
        logging.info("Attempted to list pets but none registered.")
    for p in pets:
        print(p)
        print("-" * 40)


def view_pet_history():
    """Muestra el historial de consultas de una mascota específica."""
    print("=== Consultation History ===")
    try:
        pet_name = input("Pet's name: ").strip()
        pet = find_pet_by_name(pet_name)
        if pet:
            print(pet.show_consultations())
            logging.info(f"Consultation history viewed for pet {pet_name}")
        else:
            print("Pet not found.")
            logging.warning(f"Consultation history requested for non-existent pet: {pet_name}")
    except Exception as e:
        print(f"Error viewing pet history: {e}")
        logging.error(f"Exception in view_pet_history: {e}")


##############################
# SERIALIZACIÓN Y DESERIALIZACIÓN
##############################

def export_mascotas_duenos_csv(filename='mascotas_dueños.csv'):
    """
    Guarda la información de mascotas y dueños en un archivo CSV.
    Cada fila contiene: pet_name, species, breed, age, owner_name, owner_phone, owner_address
    """
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            # Cabecera
            writer.writerow(['pet_name', 'species', 'breed', 'age', 'owner_name', 'owner_phone', 'owner_address'])
            for pet in pets:
                writer.writerow([
                    pet.name,
                    pet._species,
                    pet._breed,
                    pet._age,
                    pet._owner.name,
                    pet._owner.phone,
                    pet._owner.address
                ])
        logging.info(f"Exported pets and owners to CSV: {filename}")
        print(f"Data exported to {filename}")
    except Exception as e:
        logging.error(f"Error exporting to CSV {filename}: {e}")
        print(f"Error exporting to CSV: {e}")

def import_mascotas_duenos_csv(filename='mascotas_dueños.csv'):
    """
    Carga la información de mascotas y dueños desde un archivo CSV.
    Valida duplicados y consistencia.
    """
    try:
        if not os.path.exists(filename):
            logging.warning(f"File {filename} does not exist. No data imported.")
            return

        with open(filename, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Verificar si el dueño ya existe
                owner = find_owner_by_name(row['owner_name'])
                if not owner:
                    owner = Owner(row['owner_name'], row['owner_phone'], row['owner_address'])
                    owners.append(owner)
                # Verificar si la mascota ya existe
                pet = find_pet_by_name(row['pet_name'])
                if not pet:
                    pet = Pet(
                        row['pet_name'],
                        row['species'],
                        row['breed'],
                        int(row['age']),
                        owner
                    )
                    pets.append(pet)
        logging.info(f"Imported pets and owners from CSV: {filename}")
        print(f"Data imported from {filename}")
    except Exception as e:
        logging.error(f"Error importing from CSV {filename}: {e}")
        print(f"Error importing from CSV: {e}")

def export_consultas_json(filename='consultas.json'):
    """
    Guarda el historial de consultas en un archivo JSON.
    Estructura:
    [
        {
            "pet_name": ...,
            "consultations": [
                {"date": ..., "reason": ..., "diagnosis": ...},
                ...
            ]
        },
        ...
    ]
    """
    try:
        data = []
        for pet in pets:
            consultas_list = []
            for consulta in pet.consultations:
                consultas_list.append({
                    'date': consulta.date,
                    'reason': consulta.reason,
                    'diagnosis': consulta.diagnosis
                })
            data.append({
                'pet_name': pet.name,
                'consultations': consultas_list
            })
        with open(filename, 'w', encoding='utf-8') as jsonfile:
            json.dump(data, jsonfile, ensure_ascii=False, indent=4)
        logging.info(f"Exported consultations to JSON: {filename}")
        print(f"Consultations exported to {filename}")
    except Exception as e:
        logging.error(f"Error exporting consultations to JSON {filename}: {e}")
        print(f"Error exporting consultations to JSON: {e}")

def import_consultas_json(filename='consultas.json'):
    """
    Carga el historial de consultas desde un archivo JSON.
    Valida consistencia de mascotas.
    """
    try:
        if not os.path.exists(filename):
            logging.warning(f"File {filename} does not exist. No consultations imported.")
            return

        with open(filename, 'r', encoding='utf-8') as jsonfile:
            data = json.load(jsonfile)
            for item in data:
                pet = find_pet_by_name(item['pet_name'])
                if pet:
                    for consulta_data in item['consultations']:
                        # Evitar duplicados
                        exists = any(
                            c.date == consulta_data['date'] and
                            c.reason == consulta_data['reason'] and
                            c.diagnosis == consulta_data['diagnosis']
                            for c in pet.consultations
                        )
                        if not exists:
                            consulta = Consultation(
                                consulta_data['date'],
                                consulta_data['reason'],
                                consulta_data['diagnosis'],
                                pet
                            )
                            pet.add_consultation(consulta)
                else:
                    logging.warning(f"Consultation import found pet not in memory: {item['pet_name']}")
        logging.info(f"Imported consultations from JSON: {filename}")
        print(f"Consultations imported from {filename}")
    except Exception as e:
        logging.error(f"Error importing consultations from JSON {filename}: {e}")
        print(f"Error importing consultations from JSON: {e}")

def export_all():
    """Guarda toda la información (mascotas, dueños y consultas) en los archivos recomendados."""
    export_mascotas_duenos_csv()
    export_consultas_json()

def import_all():
    """Carga toda la información desde los archivos recomendados."""
    import_mascotas_duenos_csv()
    import_consultas_json()


# MENÚ DE IMPORTACIÓN/EXPORTACIÓN OPCIONAL
def show_export_import_menu():
    print("\n=== Data Import/Export Menu ===")
    print("1. Export all data")
    print("2. Import all data")
    print("3. Export pets and owners (CSV)")
    print("4. Import pets and owners (CSV)")
    print("5. Export consultations (JSON)")
    print("6. Import consultations (JSON)")
    print("0. Back to main menu")

    option = input("Select an option: ").strip()
    if option == "1":
        export_all()
    elif option == "2":
        import_all()
    elif option == "3":
        export_mascotas_duenos_csv()
    elif option == "4":
        import_mascotas_duenos_csv()
    elif option == "5":
        export_consultas_json()
    elif option == "6":
        import_consultas_json()
    elif option == "0":
        return
    else:
        print("Invalid option.")
        logging.warning(f"Invalid import/export menu option selected: {option}")

# NOTA IMPORTANTE:
# - Al iniciar la aplicación, llama a import_all() para cargar datos si existen.
# - Al finalizar la aplicación (antes de salir), llama a export_all() para guardar datos actuales.
# - Puedes llamar show_export_import_menu() desde el menú principal para dar acceso manual según se requiera.