# src/utils.py
import os
import logging
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "debate_log.txt")

logging.basicConfig(
    filename=LOG_FILE,
    filemode="a",
    format="%(asctime)s | %(levelname)s | %(message)s",
    level=logging.INFO
)
console_logger = logging.getLogger("console")
console_logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(message)s"))
console_logger.addHandler(handler)

def log(msg, level="info"):
    if level == "info":
        logging.info(msg)
        console_logger.info(msg)
    elif level == "warning":
        logging.warning(msg)
        console_logger.warning(msg)
    else:
        logging.error(msg)
        console_logger.error(msg)

def now_ts():
    return datetime.utcnow().isoformat() + "Z"

def get_openai_api_key():
    return os.getenv("OPENAI_API_KEY", "").strip()
