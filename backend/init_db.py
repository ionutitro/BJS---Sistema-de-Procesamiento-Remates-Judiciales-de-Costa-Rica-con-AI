import mysql.connector
from mysql.connector import errorcode

DB_NAME = 'bjs_db'
TABLES = {}
TABLES['remates'] = (
    "CREATE TABLE `remates` ("
    "  `id` int(11) NOT NULL AUTO_INCREMENT,"
    "  `tipo` varchar(50) NOT NULL,"
    "  `descripcion` text,"
    "  `marca` varchar(100),"
    "  `modelo` varchar(100),"
    "  `vin` varchar(100),"
    "  `placa` varchar(50),"
    "  `matricula` varchar(100),"
    "  `precio_base` varchar(100),"
    "  `ubicacion` varchar(255),"
    "  `juzgado` varchar(255),"
    "  `fecha_remate` varchar(100),"
    "  `texto_completo` longtext,"
    "  `fecha_registro` timestamp DEFAULT CURRENT_TIMESTAMP,"
    "  PRIMARY KEY (`id`)"
    ") ENGINE=InnoDB")

def create_database(cursor):
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)

try:
    print("Connecting to MySQL...")
    cnx = mysql.connector.connect(user='root', password='') # Default XAMPP settings
    cursor = cnx.cursor()

    try:
        cursor.execute("USE {}".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Database {} does not exist.".format(DB_NAME))
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            create_database(cursor)
            print("Database {} created successfully.".format(DB_NAME))
            cnx.database = DB_NAME
        else:
            print(err)
            exit(1)

    for table_name in TABLES:
        table_description = TABLES[table_name]
        try:
            print("Creating table {}: ".format(table_name), end='')
            cursor.execute(table_description)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)
        else:
            print("OK")

    cursor.close()
    cnx.close()
    print("Database setup completed.")

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
