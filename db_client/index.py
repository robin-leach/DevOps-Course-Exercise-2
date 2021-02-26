import os
import pymongo


def get_db_collection():
    dbClientUri = f"mongodb+srv://{os.getenv('MONGO_DB_USER_NAME')}:{os.getenv('MONGO_DB_PASSWORD')}@cluster0.g6ify.mongodb.net/database?retryWrites=true&w=majority"
    databaseName = os.getenv('MONGO_DB_DATABASE_NAME')
    collectionName = 'collection'

    dbClient = pymongo.MongoClient(dbClientUri)
    db = dbClient[databaseName]
    return db[collectionName]
