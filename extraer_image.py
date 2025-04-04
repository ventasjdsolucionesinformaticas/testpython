import os
import fdb

# Connection parameters
db_path = '/firebird/data/mekano.fdb'
user = 'SYSDBA'
password = 'masterkey'

# Connect to the database
try:
    con = fdb.connect(
        dsn=db_path,
        user=user,
        password=password
    )

    # Cursor to interact with the database
    cur = con.cursor()

    # SQL query to select the BLOB field
    query = "SELECT CODREFERENCIA, FOTO FROM REFERENCIAS_FOTOS"

    # Execute the query
    cur.execute(query)

    # Fetch all results
    rows = cur.fetchall()

    # Ensure output directory exists
    output_dir = 'images'
    os.makedirs(output_dir, exist_ok=True)

    # Process each row and write the BLOB to a file
    for row in rows:
        codreferencia = row[0].strip()
        blob_data = row[1]

        if blob_data:
            if hasattr(blob_data, 'read'):
                blob_bytes = blob_data.read()
            else:
                blob_bytes = blob_data

            output_file_path = os.path.join(output_dir,f'{codreferencia}.jpg')

            # Write the BLOB bytes to a file
            with open(output_file_path, 'wb') as file:
                file.write(blob_bytes)

            print(f"BLOB data for CODREFERENCIA {codreferencia} has been written to {output_file_path}")

    # Close the cursor and connection
    cur.close()
    con.close()

except fdb.fbcore.DatabaseError as e:
    print(f"Database error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")