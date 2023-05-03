import pandas as pd
import psycopg2

#script to insert data from 1976-2020-house.csv into database


#RETRIEVE FROM CSV PART
# get the data from csv
# read CSV file
df = pd.read_csv('../../ressources/1976-2020-house.csv')


#for each row/line/vote_fact
for index, row in df.iterrows():
    #attribute values of df to the variables used in insert command
    year = row['year']
    state_name = row['state']
    po_code = row['state_po']
    fips_code = row['state_fips']
    cen_code = row['state_cen']
    ic_code = row['state_ic']
    number_district = row['district']
    run_off_vote = row['runoff']
    special_vote = row['special']
    name_person = row['candidate']
    name_party = row['party']
    write_in_candidate = row['writein']
    candidate_vote = row['candidatevotes']
    total_vote = row['totalvotes']
    fusion_ticket_candidate = row['fusion_ticket']

    #FILTER PART
    #modifying data
    #if stage column = PRI then skip this iteration
    if row['stage'] == 'PRI':
        continue
    #if df.('writein') = true then set WRITEIN in column df.('party')
    if row['writein'] == 'true':
        name_party = 'WRITEIN'

    #print(f"{year} {row['stage']} {write_in_candidate}.")

    #INSERT TO DATABASE PART
    # establish a connection to the PostgreSQL database
    conn = psycopg2.connect("host=localhost "
                            "dbname=election "
                            "user=postgres "
                            "password=camille "
                            "port=5432"
                            )

    # create a cursor object to interact with the database
    cur = conn.cursor()

    # execute the SQL query with the tuple as parameters
    cur.execute("INSERT INTO year (year) "
                "VALUES (%s)",
                (year,))
    cur.execute("INSERT INTO state (state_name, po_code, fips_code, cen_code, ic_code) "
                "VALUES (%s, %s, %s, %s, %s)",
                (state_name, po_code, fips_code, cen_code, ic_code))
    """

    conn.commit()
# commit the changes to the database
    cur.execute("INSERT INTO district (number_district, id_state) "
                "VALUES (%s, (SELECT id_state FROM state WHERE state_name = 'ALABAMA'))",
                (number_district,))
    cur.execute("INSERT INTO party (name_party) "
                "VALUES (%s)",
                (name_party,))
    cur.execute("INSERT INTO person (name_person) "
                "VALUES (%s)",
                (name_person,))
    conn.commit()

    cur.execute("INSERT INTO candidate (write_in_candidate, fusion_ticket_candidate, id_party, id_person) "
                "VALUES (%s, %s, (SELECT id_party FROM party WHERE name_party = 'REPUBLICAN'), (SELECT id_person FROM person WHERE name_person = 'LEONARD WILSON'))",
                (write_in_candidate, fusion_ticket_candidate,))
    conn.commit()
    cur.execute("INSERT INTO fait_de_vote (id_district, id_year, id_candidate, candidate_vote, total_vote, run_off_vote, special_vote) "
                "VALUES ((SELECT id_district FROM district WHERE number_district = 4 AND id_state = (SELECT id_state FROM state WHERE state_name = 'ALABAMA')),"
                "        (SELECT id_year FROM year WHERE year = 1976), "
                "        (SELECT id_candidate FROM candidate "
                "               WHERE id_person = (SELECT id_person FROM person WHERE name_person = 'LEONARD WILSON') "
                "               AND id_party = (SELECT id_party FROM party WHERE name_party = 'REPUBLICAN')), "
                "       %s, %s, %s, %s),"
                (candidate_vote, total_vote, run_off_vote, special_vote,))
"""
    conn.commit()

    # close the cursor and the connection
    cur.close()
    conn.close()

#do the insert
"""
    INSERT INTO year (year)
    VALUES (1976);

    INSERT INTO state (state_name, po_code, fips_code, cen_code, ic_code)
    VALUES ('ALABAMA', 'AL', 1, 63, 41);

    INSERT INTO district (number_district, id_state)
    VALUES (4, (SELECT id_state FROM state WHERE state_name = 'ALABAMA'));

    INSERT INTO party (name_party)
    VALUES ('REPUBLICAN');

    INSERT INTO person (name_person)
    VALUES ('LEONARD WILSON');

    INSERT INTO candidate (write_in_candidate, fusion_ticket_candidate, id_party, id_person)
    VALUES (FALSE, FALSE, (SELECT id_party FROM party WHERE name_party = 'REPUBLICAN'), (SELECT id_person FROM person WHERE name_person = 'LEONARD WILSON'));

    INSERT INTO fait_de_vote (id_district, id_year, id_candidate, candidate_vote, total_vote, run_off_vote, special_vote)
    VALUES ((SELECT id_district FROM district WHERE number_district = 4 AND id_state = (SELECT id_state FROM state WHERE state_name = 'ALABAMA')),
    (SELECT id_year FROM year WHERE year = 1976),
    (SELECT id_candidate FROM candidate WHERE id_person = (SELECT id_person FROM person WHERE name_person = 'LEONARD WILSON') AND id_party = (SELECT id_party FROM party WHERE name_party = 'REPUBLICAN')),
    34531, 176022, FALSE, FALSE);
"""


