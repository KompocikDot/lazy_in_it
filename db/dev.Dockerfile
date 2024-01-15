FROM postgres:16.1-alpine3.19

COPY ./scripts/create_multiple_psql_db.sh /docker-entrypoint-initdb.d
