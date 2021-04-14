import os
import pymongo


def get_db_collection():
    dbClientUri = os.getenv('MONGO_DB_CONNECTION_STRING')
    databaseName = os.getenv('MONGO_DB_DATABASE_NAME')
    collectionName = 'collection'

    dbClient = pymongo.MongoClient(dbClientUri)
    db = dbClient[databaseName]
    return db[collectionName]
