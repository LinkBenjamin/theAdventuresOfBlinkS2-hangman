#!/bin/bash

source /env/.env

DB_NAME="hangman"
COLLECTION_NAME="phrases"

COLLECTION_EXISTS=$(mongo --username $MONGO_INITDB_ROOT_USERNAME --password $MONGO_INITDB_ROOT_PASSWORD --authenticationDatabase admin --quiet --eval "db.getSiblingDB('$DB_NAME').getCollectionNames().includes('$COLLECTION_NAME')")

if [ "$COLLECTION_EXISTS" = "false" ]: then
    echo "Collection $COLLECTION_NAME does not exist.  Initializing..."
    mongo --username $MONGO_INITDB_ROOT_USERNAME --password $MONGO_INITDB_ROOT_PASSWORD --authenticationDatabase admin --eval "db.getSiblingDB('$DB_NAME').createCollection('$COLLECTION_NAME')"
    echo "Collection $COLLECTION_NAME created."
else
    echo "Collection $COLLECTION_NAME already exists."
fi