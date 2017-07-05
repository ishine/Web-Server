from pymongo import MongoClient
from bson.objectid import ObjectId
import config


class Car:
	def __init__(self, client):
		#client = MongoClient(config.address, config.port)
		self.db = client[config.dbname]
		self.car_collection = self.db.car_collection

	def create(self, data):
		carId = self.car_collection.insert(data)
		data['id'] = carId
		return data

	def retrieve(self, data):
		car = self.car_collection.find_one({'_id': ObjectId(data['id'])})
		car['id'] = str(car['_id'])
		del car['_id']
		return car

	def update(self, data):
		car = self.car_collection.find_one({'_id': ObjectId(data['id'])})
		if car != None:
			for key in data:
				if key != 'id': car[key] = data[key]
			self.car_collection.save(car)
			car['id'] = str(car['_id'])
			del car['_id']
		return car

	def delete(self, data):
		self.car_collection.remove({'_id': ObjectId(data['id'])})


if __name__ == '__main__':
	client = MongoClient(config.address, config.port)
	collection = Car(client)
	result = collection.create({'carPlate': '123456'})
	print collection.retrieve({'id': result['id']})
	print collection.update({'id': result['id'], 'carPlate': '654321'})
	collection.delete({'id': result['id']})