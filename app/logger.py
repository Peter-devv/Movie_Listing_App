import logging

PAPERTRAIL_HOST = "logs2.papertrailapp.com"
PAPERTRAIL_PORT = 43906

handler = logging.handlers.SysLogHandler(address=(PAPERTRAIL_HOST, PAPERTRAIL_PORT))
# formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s")
# handler.setFormatter(formatter)

logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
    handlers=[handler]
)

def get_logger(name):
    logger = logging.getLogger(name)
    return logger