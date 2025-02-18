#!/usr/bin/python3
"""
Contains the TestDBStorageDocs and TestDBStorage classes
"""

from datetime import datetime
import inspect
import models
from models.engine import db_storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import json
import os
import pep8
import unittest
DBStorage = db_storage.DBStorage
classes = {"Amenity": Amenity, "City": City, "Place": Place,
           "Review": Review, "State": State, "User": User}


class TestDBStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of DBStorage class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.dbs_f = inspect.getmembers(DBStorage, inspect.isfunction)

    def test_pep8_conformance_db_storage(self):
        """Test that models/engine/db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_db_storage(self):
        """Test tests/test_models/test_db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_engine/\
test_db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_db_storage_module_docstring(self):
        """Test for the db_storage.py module docstring"""
        self.assertIsNot(db_storage.__doc__, None,
                         "db_storage.py needs a docstring")
        self.assertTrue(len(db_storage.__doc__) >= 1,
                        "db_storage.py needs a docstring")

    def test_db_storage_class_docstring(self):
        """Test for the DBStorage class docstring"""
        self.assertIsNot(DBStorage.__doc__, None,
                         "DBStorage class needs a docstring")
        self.assertTrue(len(DBStorage.__doc__) >= 1,
                        "DBStorage class needs a docstring")

    def test_dbs_func_docstrings(self):
        """Test for the presence of docstrings in DBStorage methods"""
        for func in self.dbs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestDBStorage(unittest.TestCase):
    """Test the FileStorage class"""
    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_returns_dict(self):
        """Test that all returns a dictionaty"""
        self.assertIs(type(models.storage.all()), dict)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_no_class(self):
        """Test that all returns all rows when no class is passed"""
        state_data = {"name": "Wisconsin"}
        created_state = State(**state_data)
        models.storage.new(created_state)
        models.storage.save()

        session = models.storage.DBStorage.__session
        all_objs = session.query(State).all()

        self.assertTrue(len(all_objs) > 0)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_new(self):
        """test that new adds an object to the database"""
        state_data = {"name": "Chicago"}
        cr_state = State(**state_data)
        models.storage.new(cr_state)

        session = models.storage.DBStorage.__session
        filter_state = session.query(State).filter_by(id=cr_state.id).first()

        self.assertEqual(filter_state.id, cr_state.id)
        self.assertEqual(filter_state.name, cr_state.name)
        self.assertIsNotNone(filter_state)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_save(self):
        """Test that save properly saves objects to file.json"""
        state_data = {"name": "New Mexico"}
        cr_state = State(**state_data)
        models.storage.new(cr_state)
        models.storage.save()

        session = models.storage.__DBStorage.__session
        filtered_state = session.query(State).filter_by(id=cr_state.id).first()

        self.assertEqual(filtered_state.id, cr_state.id)
        self.assertEqual(filtered_state.name, cr_state.name)
        self.assertIsNotNone(filtered_state)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_get(self):
        """Tests method for obtaining an instance for the database storage
        """
        storage = models.storage
        storage.reload()
        state_data = {"name": "Bahamas"}
        created_state = State(**state_data)
        retrieve_state = storage.get(State, created_state.id)
        self.assertEqual(created_state, retrieve_state)
        inexistent_state_id = storage.get(State, 'inexistent_id')
        self.assertEqual(inexistent_id, None)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_count(self):
        """Tests method for obtaining a count of an instance from db storage
        """
        storage = models.storage
        storage.reload()
        state_data = {"name": "Mauritius"}
        created_state = State(**state_data)
        storage.new(created_state)

        city_data = {"name": "Rocky", "state_id": created_state.id}
        created_city = City(**city_data)
        storage.new(created_city)
        storage.save()

        state_event = storage.count(State)
        self.assertEqual(state_event, len(storage.all(State)))

        all_state_occurences = storage.count()
        self.assertEqual(all_state_occurences, len(storage.all()))
