import logging
import os
from datetime import datetime
import os.path

file_name=f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
logs_folder_path=os.path.join(os.getcwd(),"logs",file_name)
os.makedirs(logs_folder_path,exist_ok=True)

LOG_FILE_PATH=os.path.join(logs_folder_path,file_name)

logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[%(asctime)s] %(lineno)d %(name)s %(levelname)s %(message)s",
    level=logging.INFO,
)