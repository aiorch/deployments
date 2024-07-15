QDRANT_OPTS='-v $(pwd)/qdrant_storage'
docker run -p 6333:6333 -p 6334:6334 $QDRANT_OPTS qdrant/qdrant
