"""
Test Cases for Counter Web Service

Create a service that can keep a track of multiple counters
- API must be RESTful - see the status.py file. Following these guidelines, you can make assumptions about
how to call the web service and assert what it should return.
- The endpoint should be called /counters
- When creating a counter, you must specify the name in the path.
- Duplicate names must return a conflict error code.
- The service must be able to update a counter by name.
- The service must be able to read the counter
"""

from unittest import TestCase

# we need to import the unit under test - counter
from src.counter import app

# we need to import the file that contains the status codes
from src import status

class CounterTest(TestCase):
    """Counter tests"""

    def test_create_a_counter(self):
        """It should create a counter"""
        client = app.test_client()
        result = client.post('/counters/foo')
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)

    def setUp(self):
        self.client = app.test_client()

    def test_duplicate_a_counter(self):
        """It should return an error for duplicates"""
        result = self.client.post('/counters/bar')
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        result = self.client.post('/counters/bar')
        self.assertEqual(result.status_code, status.HTTP_409_CONFLICT)

    def test_update_a_counter(self):
        """It should update a counter"""
        result = self.client.post('/counters/updateTest')
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        initialVal = result.json['updateTest']
        updateTest = self.client.put('/counters/updateTest')
        self.assertEqual(updateTest.status_code, status.HTTP_200_OK)
        updateValue = updateTest.json['updateTest']
        self.assertEqual(initialVal + 1, updateValue)

    def test_update_a_bad_counter(self):
        """It should return an error for updating non-existent counter"""
        updateTest = self.client.put('/counters/updateCounter')
        self.assertEqual(updateTest.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_a_counter(self):
        """It should get a counter"""
        result = self.client.post('/counters/newTest')
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        value = self.client.get('/counters/newTest')
        self.assertEqual(value.status_code, status.HTTP_200_OK)
        self.assertEqual(value.json['newTest'], 0)

    def test_get_a_bad_counter(self):
        """It should return an error for getting non-existent counter"""
        updateTest = self.client.get('/counters/badCounter')
        self.assertEqual(updateTest.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_a_counter(self):
        """It should delete a counter"""
        result = self.client.post('/counters/test')
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        deleteCounter = self.client.delete('/counters/test')
        self.assertEqual(deleteCounter.status_code, status.HTTP_204_NO_CONTENT)