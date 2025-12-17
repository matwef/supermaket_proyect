import os
from dotenv import load_dotenv


load_dotenv()


SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")


PRODUCTS_TABLE = "products"
EMPLOYEES_TABLE = "employees"
CLIENTS_TABLE = "clients"
SALES_TABLE = "sales"
USUARIOS_TABLE = "usuarios"


WINDOW_BG = "#f5f5f5"
MENU_BG = "#e0e0e0"
BUTTON_COLOR = "#4CAF50"
BUTTON_ACTIVE = "#45a049"


if not SUPABASE_URL or not SUPABASE_KEY:
    raise Exception("Variables de entorno de Supabase faltantes")