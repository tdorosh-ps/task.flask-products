import csv
import psycopg2

from config import POSTGRES_USER, POSTGRES_PASSWORD, \
    POSTGRES_HOST, POSTGRES_PORT, POSTGRES_DATABASE


def csv_parse():
    try:
        connection = psycopg2.connect(user=POSTGRES_USER, password=POSTGRES_PASSWORD,
                                      host=POSTGRES_HOST, port=POSTGRES_PORT,
                                      database=POSTGRES_DATABASE)
        cursor = connection.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS product ( "
            "id serial PRIMARY KEY, "
            "title varchar(255) NOT NULL, "
            "asin varchar(10) NOT NULL UNIQUE); "
            
            "CREATE TABLE IF NOT EXISTS review ( "
            "id serial PRIMARY KEY, "
            "asin varchar(10) NOT NULL, "
            "title varchar(255) NOT NULL, "
            "body text NOT NULL, "
            "product_id integer REFERENCES product(id)); "
        )
    except Exception as error:
        print('An error was occurred while connecting db.', error)
    else:
        try:
            reviews_file = open(r'csv_source/Reviews.csv')
            products_file = open(r'csv_source/Products.csv')
        except Exception as error:
            print('An error was occurred while reading files.', error)
        else:
            try:
                reviews_reader = csv.reader(reviews_file, delimiter=',')
                products_reader = csv.reader(products_file, delimiter=',')
                review_insert_query = """INSERT INTO review(asin, title, body) VALUES (%s, %s, %s);"""
                product_insert_query = """INSERT INTO product(title, asin) VALUES (%s, %s);"""
                counter = 0
                for row in reviews_reader:
                    if counter == 0:
                        counter += 1
                        continue
                    cursor.execute(review_insert_query, row)
                counter = 0
                for row in products_reader:
                    if counter == 0:
                        counter += 1
                        continue
                    cursor.execute(product_insert_query, row)
                connection.commit()
            except Exception as error:
                print('An error was occurred while writing data to db.', error)
            else:
                try:
                    cursor.execute("SELECT * from review;")
                    review_data = cursor.fetchall()
                    cursor.execute("SELECT * from product;")
                    product_data = cursor.fetchall()
                except Exception as error:
                    print('An error was occurred while reading data from db.', error)
                else:
                    product_review_insert_query = """UPDATE review SET product_id=(%s) WHERE id=(%s);"""
                    try:
                        for review_row in review_data:
                            for product_row in product_data:
                                if review_row[1] == product_row[2]:
                                    cursor.execute(product_review_insert_query, (product_row[0], review_row[0]))
                        connection.commit()
                    except Exception as error:
                        print('An error was occurred while writing foreign keys to review table.', error)
                    else:
                        print('data writing was finished successfully')
            finally:
                reviews_file.close(), products_file.close()
    finally:
        if connection:
            cursor.close()
            connection.close()


if __name__ == '__main__':
    csv_parse()
