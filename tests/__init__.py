import os, sys

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, "src",))

# Don't write .pyc files
sys.dont_write_bytecode = True

# Load the .env file
from dotenv import load_dotenv
load_dotenv()