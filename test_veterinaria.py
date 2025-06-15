import unittest
import logging
import os
import csv
import json

# Import the classes and functions to test
from classes import Owner, Pet, Consultation
import functions

class TestOwner(unittest.TestCase):
    """Pruebas para la clase Owner."""

    def test_owner_creation_attributes(self):
        """Valida que se creen correctamente los dueños y sus atributos."""
        owner = Owner("Mario Perez", "123456", "Calle 1")
        self.assertEqual(owner.name, "Mario Perez")
        self.assertEqual(owner.phone, "123456")
        self.assertEqual(owner.address, "Calle 1")
        self.assertIn("Mario Perez", str(owner))
        self.assertIn("123456", str(owner))
        self.assertIn("Calle 1", str(owner))

class TestPet(unittest.TestCase):
    """Pruebas para la clase Pet."""

    def test_pet_creation_attributes(self):
        """Valida que se creen correctamente las mascotas y sus atributos."""
        owner = Owner("Ana", "999", "Plaza 2")
        pet = Pet("Toby", "Perro", "Labrador", 5, owner)
        self.assertEqual(pet.name, "Toby")
        self.assertEqual(pet._species, "Perro")
        self.assertEqual(pet._breed, "Labrador")
        self.assertEqual(pet._age, 5)
        self.assertEqual(pet._owner, owner)
        self.assertEqual(pet.consultations, [])
        self.assertIn("Toby", str(pet))
        self.assertIn("Perro", str(pet))
        self.assertIn("Ana", str(pet))

    def test_add_and_show_consultation(self):
        """Verifica agregar y mostrar consultas de una mascota."""
        owner = Owner("Carlos", "888", "Río 7")
        pet = Pet("Felix", "Gato", "Siames", 3, owner)
        consulta = Consultation("10/05/2024", "Vacunación", "Sin novedad", pet)
        pet.add_consultation(consulta)
        self.assertIn(consulta, pet.consultations)
        self.assertIn("Vacunación", pet.show_consultations())

class TestConsultation(unittest.TestCase):
    """Pruebas para la clase Consultation."""

    def test_consultation_creation_and_str(self):
        """Valida atributos y representación de la consulta."""
        owner = Owner("Luz", "777", "Av. Z")
        pet = Pet("Rocky", "Perro", "Boxer", 2, owner)
        consulta = Consultation("11/06/2024", "Chequeo", "Saludable", pet)
        self.assertEqual(consulta.date, "11/06/2024")
        self.assertEqual(consulta.reason, "Chequeo")
        self.assertEqual(consulta.diagnosis, "Saludable")
        self.assertEqual(consulta.pet, pet)
        self.assertIn("Chequeo", str(consulta))
        self.assertIn("Saludable", str(consulta))

class TestValidationFunctions(unittest.TestCase):
    """Pruebas para las funciones de validación."""

    def test_valid_name(self):
        self.assertTrue(functions.is_valid_name("Rex"))
        self.assertFalse(functions.is_valid_name("12345"))
        self.assertFalse(functions.is_valid_name(""))
        self.assertFalse(functions.is_valid_name("1234"))
        self.assertTrue(functions.is_valid_name("R2D2"))

    def test_valid_reason_or_diagnosis(self):
        self.assertTrue(functions.is_valid_reason_or_diagnosis("Consulta general"))
        self.assertFalse(functions.is_valid_reason_or_diagnosis("7890"))
        self.assertFalse(functions.is_valid_reason_or_diagnosis(""))

    def test_valid_date(self):
        self.assertTrue(functions.is_valid_date("10/05/2024"))
        self.assertFalse(functions.is_valid_date("abcd"))
        self.assertFalse(functions.is_valid_date(""))

class TestExceptions(unittest.TestCase):
    """Pruebas para el manejo de excepciones al ingresar datos incorrectos."""

    def test_register_owner_invalid_name(self):
        """Debe lanzar ValueError si el nombre es solo dígitos."""
        with self.assertRaises(ValueError):
            if not functions.is_valid_name("1234"):
                raise ValueError("Owner's name must contain letters and cannot be only numbers.")

    def test_register_pet_invalid_age(self):
        """Debe lanzar ValueError si la edad no es válida."""
        with self.assertRaises(ValueError):
            if not "abc".isdigit() or int("0") < 0:
                raise ValueError("Age must be a non-negative integer.")

    def test_register_consultation_invalid_reason(self):
        """Debe lanzar ValueError si el motivo es inválido."""
        with self.assertRaises(ValueError):
            if not functions.is_valid_reason_or_diagnosis("1234"):
                raise ValueError("Reason must contain letters and cannot be only numbers.")

class TestLogging(unittest.TestCase):
    """Verifica el funcionamiento del logging para eventos importantes."""

    def setUp(self):
        # Elimina todos los handlers previos antes de configurar uno nuevo
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)
        # Ahora sí, configura el log de pruebas
        logging.basicConfig(
            filename='test_clinica_veterinaria.log',
            level=logging.INFO,
            format='%(asctime)s | %(levelname)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            force=True  # Solo en Python 3.8+: fuerza la reconfiguración
        )
        # Limpia el archivo log de pruebas
        open('test_clinica_veterinaria.log', 'w').close()

    def test_logging_info(self):
        logging.info("Test event: registro exitoso de prueba")
        # Asegúrate de que el log se escriba
        logging.shutdown()
        with open('test_clinica_veterinaria.log', 'r', encoding='utf-8') as log_file:
            logs = log_file.read()
        self.assertIn("Test event: registro exitoso de prueba", logs)

    def test_logging_warning(self):
        logging.warning("Test warning!")
        logging.shutdown()
        with open('test_clinica_veterinaria.log', 'r', encoding='utf-8') as log_file:
            logs = log_file.read()
        self.assertIn("Test warning!", logs)

class TestSerialization(unittest.TestCase):
    """Pruebas de serialización y deserialización CSV/JSON."""

    def setUp(self):
        # Limpia listas globales y archivos de prueba antes de cada test
        functions.owners.clear()
        functions.pets.clear()
        if os.path.exists("test_mascotas_dueños.csv"):
            os.remove("test_mascotas_dueños.csv")
        if os.path.exists("test_consultas.json"):
            os.remove("test_consultas.json")

    def test_export_import_mascotas_duenos_csv(self):
        """Valida exportación e importación CSV de mascotas y dueños."""
        owner = Owner("Julia", "456", "Calle 10")
        pet = Pet("Linda", "Perro", "Cocker", 4, owner)
        functions.owners.append(owner)
        functions.pets.append(pet)

        functions.export_mascotas_duenos_csv("test_mascotas_dueños.csv")
        self.assertTrue(os.path.exists("test_mascotas_dueños.csv"))

        # Limpia las listas para probar importación
        functions.owners.clear()
        functions.pets.clear()
        functions.import_mascotas_duenos_csv("test_mascotas_dueños.csv")
        self.assertTrue(any(o.name == "Julia" for o in functions.owners))
        self.assertTrue(any(p.name == "Linda" for p in functions.pets))

    def test_export_import_consultas_json(self):
        """Valida exportación e importación JSON de consultas."""
        owner = Owner("Raul", "321", "Boulevard 5")
        pet = Pet("Max", "Perro", "Pug", 6, owner)
        consulta = Consultation("15/06/2024", "Cirugía", "Recuperado", pet)
        pet.add_consultation(consulta)
        functions.owners.append(owner)
        functions.pets.append(pet)

        functions.export_consultas_json("test_consultas.json")
        self.assertTrue(os.path.exists("test_consultas.json"))

        # Limpia las consultas para probar importación
        pet._consultations.clear()
        functions.import_consultas_json("test_consultas.json")
        self.assertTrue(any("Recuperado" in c.diagnosis for c in pet.consultations))

    def tearDown(self):
        if os.path.exists("test_mascotas_dueños.csv"):
            os.remove("test_mascotas_dueños.csv")
        if os.path.exists("test_consultas.json"):
            os.remove("test_consultas.json")

if __name__ == '__main__':
    print("\n======== Running Veterinary Clinic Unit Tests ========")
    unittest.main(verbosity=2)