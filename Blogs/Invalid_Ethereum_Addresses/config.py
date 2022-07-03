
from dotenv import dotenv_values

config_dict = dotenv_values(".env") 


infura_url = config_dict["INFURA_URL"]


    