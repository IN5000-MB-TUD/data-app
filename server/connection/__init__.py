import logging

from server.connection import mongo

# Setup logging
log = logging.getLogger(__name__)

log.info("Connecting to MongoDB...")
mo = mongo.Mongo()
