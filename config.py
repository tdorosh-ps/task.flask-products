POSTGRES_USER = 'admin1'
POSTGRES_PASSWORD = 'admin'
POSTGRES_HOST = 'localhost'
POSTGRES_PORT = '5432'
POSTGRES_DATABASE = 'products'

DATABASE_CONNECTION_URI = f'postgresql+psycopg2://' \
                          f'{POSTGRES_USER}:{POSTGRES_PASSWORD}@' \
                          f'{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DATABASE}'