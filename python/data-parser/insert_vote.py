import pandas as pd


def insert_vote():
    df = pd.read_csv("../../ressources/1976-2020-house.csv",
                     dtype={"district": str, "state_fips": str})

    vote_data = df[[
        "year",
        "state_fips",
        "district",
        "runoff",
        "special",
        "candidate",
        "writein",
        "party",
        "candidatevotes",
        "totalvotes",
    ]].rename(columns={
        "district": "district_number"
    }).reset_index().drop(columns="index")

    insert_query = "INSERT INTO vote_fact(id_district, id_year, id_candidate, candidate_vote, total_vote, " \
                   "run_off_election, special_election) VALUES \n "

    global_insert = ""

    for index, row in vote_data.iterrows():
        # if row["writein"]:
        #     party_name = 'WRITE-IN'
        # else:
        #     party_name = str(row["party"]).replace("'", "''")
        party_name = str(row["party"]).replace("'", "''")
        person_name = str(row["candidate"]).replace("'", "''")

        if row["special"]:
            continue
        if row["runoff"]:
            continue

        run_off = str(row['runoff'])
        if run_off == 'nan':
            run_off = False

        insert_query += f"\t((SELECT (id_district) FROM district d JOIN state s ON d.id_state = s.id_state WHERE d.district_number = '{row['district_number']}' AND s.fips_code = '{row['state_fips']}'),"
        insert_query += f"\t(SELECT (id_year) FROM year y WHERE y.year_label = {row['year']}), "

        insert_query += f"\t(SELECT (id_candidate) FROM candidate WHERE id_person = (SELECT (id_person) FROM person WHERE person_name = '{person_name}') AND id_party = (SELECT (id_party) FROM party WHERE party_name = '{party_name}') AND write_in = {row['writein']}), "
        insert_query += f"\t{row['candidatevotes']}, "
        insert_query += f"\t{row['totalvotes']}, "
        insert_query += f"\t{run_off}, "
        insert_query += f"\t{row['special']}),\n"

        if index % 1000 == 0:
            global_insert += insert_query[:-2] + ";\n\n\n"
            insert_query = "INSERT INTO vote_fact(id_district, id_year, id_candidate, candidate_vote, total_vote, " \
                           "run_off_election, special_election) VALUES \n "

    global_insert += insert_query[:-2] + ";"

    print("insert_vote() finished")
    return global_insert + "\n" * 3
    # return insert_query[:-2] + ";"


if __name__ == "__main__":
    vote = insert_vote()
    with open("../../sql/insert_vote.sql", "w") as file:
        file.write(vote)
        file.close()
