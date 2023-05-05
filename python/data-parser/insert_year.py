import pandas as pd


def insert_year():
    df = pd.read_csv("../../ressources/1976-2020-house.csv")

    year_data = df[[
        "year"
    ]].rename(columns={
        "year":"year_label"
    }).drop_duplicates(keep="first").reset_index().drop(columns="index")

    insert_query = "INSERT INTO year(year_label) VALUES \n"

    for index, row in year_data.iterrows():
        insert_query += f"\t('{row['year_label']}'),\n"

    insert_query = insert_query[:-2] + ";"

    print("insert_year() finished")
    return insert_query + "\n" * 3


if __name__ == "__main__":
    year = insert_year()
    with open("../../sql/insert_year.sql", "w") as file:
        file.write(year)
        file.close()
