import logging
import os
from datetime import datetime

# Specify the absolute path for the log directory
LOG_DIR = r"C:\Users\Samya\PycharmProjects\Elephant-Tusk-Classification\log"

# Ensure the log directory exists
os.makedirs(LOG_DIR, exist_ok=True)

# Create a unique log file name based on the current datetime
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
LOG_FILE_PATH = os.path.join(LOG_DIR, LOG_FILE)

# Configure logging
logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[ %(asctime)s ] %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
