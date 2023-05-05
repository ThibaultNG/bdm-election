import pandas as pd


def insert_person():
    df = pd.read_csv("../../ressources/1976-2020-house.csv")

    person_data = df[[
        "candidate"
    ]].rename(columns={
        "candidate": "person_name"
    }).drop_duplicates(keep="first").reset_index().drop(columns="index")

    insert_query = "INSERT INTO person(person_name) VALUES \n"

    for index, row in person_data.iterrows():
        name = row['person_name'].replace("'","''")
        insert_query += f"\t('{name}'),\n"

    insert_query = insert_query[:-2] + ";"

    print("insert_person() finished")
    return insert_query + "\n" * 3


if __name__ == "__main__":
    person = insert_person()
    with open("../../sql/insert_person.sql", "w") as file:
        file.write(person)
        file.close()
