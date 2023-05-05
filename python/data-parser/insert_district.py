import pandas as pd


def insert_district():
    df = pd.read_csv("../../ressources/1976-2020-house.csv",
                     dtype={"district": str, "state_fips": str})

    district_data = df[[
        "state_fips",
        "district"
    ]].rename(columns={
        "district": "district_number"
    }).drop_duplicates(keep="first").reset_index().drop(columns="index")

    insert_query = "INSERT INTO district(district_number, id_state) VALUES \n"

    for index, row in district_data.iterrows():
        insert_query += f"\t('{row['district_number']}', (SELECT (id_state) FROM state s WHERE s.fips_code = '{row['state_fips']}')),\n"

    insert_query = insert_query[:-2] + ";"

    print("insert_district() finished")
    return insert_query + "\n" * 3


if __name__ == "__main__":
    district = insert_district()
    with open("../../sql/insert_district.sql", "w") as file:
        file.write(district)
        file.close()
