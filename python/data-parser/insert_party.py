import pandas as pd


def insert_party():
    df = pd.read_csv("../../ressources/1976-2020-house.csv")

    party_data = df[[
        "party",
    ]].rename(columns={
        "party": "party_name"
    }).drop_duplicates(keep="first").reset_index().drop(columns="index")

    insert_query = "INSERT INTO party(party_name) VALUES "

    for index, row in party_data.iterrows():
        party_name = str(row['party_name']).replace("'", "''")
        insert_query += f"\t('{party_name}'),\n"

    insert_query = insert_query[:-2] + ";"

    print("insert_party() finished")
    return insert_query + "\n" * 3


if __name__ == "__main__":
    party = insert_party()
    with open("../../sql/insert_party.sql", "w") as file:
        file.write(party)
        file.close()
