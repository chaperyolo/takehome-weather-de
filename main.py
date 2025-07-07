import os
from config import STATION_ID, API_BASE_URL, DB_PATH

# creating the db directory if it doesnt exist
def create_db_directory():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

def main():
    #Given the small data volume (7 days), pandas is sufficient and efficient for this task.


