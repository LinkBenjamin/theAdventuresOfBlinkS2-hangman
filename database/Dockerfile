FROM mongo:latest

ENV MONGO_INITDB_ROOT_USERNAME=${MONGO_INITDB_ROOT_USERNAME}
ENV MONGO_INITDB_ROOT_PASSWORD=${MONGO_INITDB_ROOT_PASSWORD}

COPY init_mongo.sh /docker-entrypoint-initdb.d/init_mongo.sh
RUN chmod -x /docker-entrypoint-initdb.d/init_mongo.sh

EXPOSE 27017

CMD ["mongod"]