import psycopg2


def generate_table(sql_query):
    # create a connection to the database
    # conn = psycopg2.connect("""
    #         host=127.0.0.1
    #         port=5432
    #         dbname=election
    #         user=postgres
    #         password=camille
    #         """)

    conn = psycopg2.connect("""
            host=127.0.0.1
            port=5432
            dbname=bdm-election
            user=postgres
            password=admin
            """)

    # create a cursor object
    cur = conn.cursor()

    # execute the SQL query
    cur.execute(sql_query)

    # fetch the results
    results = cur.fetchall()

    # Get the column names
    col_names = [desc[0] for desc in cur.description]

    # close the cursor and connection
    cur.close()
    conn.close()

    return col_names, results
