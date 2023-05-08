import pandas as pd


def insert_candidate():
    df = pd.read_csv("../../ressources/1976-2020-house.csv")

    candidate_data = df[[
        "candidate",
        "party",
        "writein",
        "fusion_ticket"
    ]].rename(columns={
        "candidate": "person_name",
        "party": "party_name",
    }).drop_duplicates(subset=["person_name", "party_name", "writein"], keep="first").reset_index().drop(
        columns="index")

    global_insert = ""
    no_write_in = True

    insert_query = "INSERT INTO candidate(fusion_ticket, write_in, id_person, id_party)  VALUES \n"
    for index, row in candidate_data.iterrows():

        # if row["writein"]:
        #     party_name = 'WRITE-IN'
        # else:
        #     party_name = str(row["party_name"]).replace("'", "''")
        party_name = str(row["party_name"]).replace("'", "''")

        person_name = str(row["person_name"]).replace("'", "''")

        if person_name == "WRITEIN":
            if not no_write_in:
                continue
            no_write_in = False

        insert_query += f"\t({row['fusion_ticket']}, "
        insert_query += f"{row['writein']}, "
        insert_query += f"(SELECT (id_person) FROM person pe WHERE pe.person_name = '{person_name}'), "

        insert_query += f"(SELECT (id_party) FROM party pa WHERE pa.party_name = '{party_name}')),\n"

        if index % 1000 == 0:
            global_insert += insert_query[:-2] + ";\n\n\n"
            insert_query = "INSERT INTO candidate(fusion_ticket, write_in, id_person, id_party)  VALUES \n"

    global_insert += insert_query[:-2] + ";"

    print("insert_candidate() finished")
    return global_insert + "\n" * 3


if __name__ == "__main__":
    candidate = insert_candidate()
    with open("../../sql/insert_candidate.sql", "w") as file:
        file.write(candidate)
        file.close()
