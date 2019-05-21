import unittest
import os
import json
from app import create_app, db


class BucketlistTestCase(unittest.TestCase):
	"""This class represents the bucketlist test case"""

	def setUp(self):
		"""Define test variables and initialize app."""
		self.app = create_app(config_name="testing")
		self.client = self.app.test_client
		self.bucketlist = { 'name': 'Go to Alagoinhas for vacation' }

		# binds the app to the current context
		with self.app.app_context():
			# create all tables
			db.create_all()


	def test_bucketlist_creation(self):
		"""Test API can create a bucketlist (POST request)."""
		res = self.client().post('/bucketlists/', data=self.bucketlist)
		self.assertEqual(res.status_code, 201)
		self.assertIn('Go to Alagoinhas', str(res.data))


	def test_api_can_get_all_bucketlists(self):
		"""Test API can get all bucketlists (GET request)."""
		res = self.client().post('/bucketlists/', data=self.bucketlist)
		self.assertEqual(res.status_code, 201)

		res = self.client().get('/bucketlists/')
		self.assertEqual(res.status_code, 200)
		self.assertIn('Go to Alagoinhas', str(res.data))


	def test_api_can_get_bucketlist_by_id(self):
		"""Test API can get a single bucketlist by using it's id."""
		postRes = self.client().post('/bucketlists/', data=self.bucketlist)
		self.assertEqual(postRes.status_code, 201)
		
		insertedID = json.loads(postRes.data.decode('utf-8').replace("'", "\""))['id']

		res = self.client().get('/bucketlists/{}'.format(insertedID))
		self.assertEqual(res.status_code, 200)
		self.assertIn('Go to Alagoinhas', str(res.data))


	def test_bucketlist_can_be_edited(self):
		"""Test API can edit an existing bucketlist. (PUT request)"""
		rv = self.client().post('/bucketlists/', data={ 'name': 'P = NP' })
		self.assertEqual(rv.status_code, 201)

		res = self.client().put(
			'/bucketlists/1',
			data={ 'name': 'P != NP' }
		)
		self.assertEqual(res.status_code, 200)

		result = self.client().get('/bucketlists/1')
		self.assertIn('!=', str(result.data))


	def test_bucketlist_deletion(self):
		"""Test API can delete an existing bucketlist. (DELETE request)"""
		rv = self.client().post('/bucketlists/', data={ 'name': 'P = NP' })
		self.assertEqual(rv.status_code, 201)

		res = self.client().delete('/bucketlists/1')
		self.assertEqual(res.status_code, 200)

		result = self.client().get('/bucketlists/1')
		self.assertEqual(result.status_code, 404)


	def tearDown(self):
		"""teardown all initialized variables"""
		with self.app.app_context():
			# drop all tables
			db.session.remove()
			db.drop_all()


# Make the tests executable
if __name__ == "__main__":
	unittest.main()


