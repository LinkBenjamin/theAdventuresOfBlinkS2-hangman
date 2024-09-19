#!/bin/bash

COLLECTION_EXISTS=$(mongosh --username $MONGO_INITDB_ROOT_USERNAME --password $MONGO_INITDB_ROOT_PASSWORD --authenticationDatabase admin --quiet --eval "db.getSiblingDB('$DB_NAME').getCollectionNames().includes('$COLLECTION_NAME')")

if [ "$COLLECTION_EXISTS" = "false" ]
then
    echo "Collection $COLLECTION_NAME does not exist.  Initializing..."
    mongosh --username $MONGO_INITDB_ROOT_USERNAME --password $MONGO_INITDB_ROOT_PASSWORD --authenticationDatabase admin --eval "db.getSiblingDB('$DB_NAME').createCollection('$COLLECTION_NAME')"
    echo "Collection $COLLECTION_NAME created."
else
    echo "Collection $COLLECTION_NAME already exists."
fi

echo "Mongo initialization script ran" > /tmp/startup_complete.txt