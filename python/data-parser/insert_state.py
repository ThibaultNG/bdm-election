import pandas as pd


def insert_state():
    df = pd.read_csv("../../ressources/1976-2020-house.csv")

    state_data = df[[
        "state",
        "state_po",
        "state_fips",
        "state_cen",
        "state_ic"
    ]].rename(columns={
        "state": "state_name",
        "state_po": "po_code",
        "state_fips": "fips_code",
        "state_cen": "cen_code",
        "state_ic": "ic_code"
    }).drop_duplicates(keep="first").reset_index().drop(columns="index")

    insert_query = "INSERT INTO state(state_name, po_code, fips_code, cen_code, ic_code) VALUES \n"

    for index, row in state_data.iterrows():
        insert_query += f"\t('{row['state_name']}','{row['po_code']}','{row['fips_code']}','{row['cen_code']}','{row['ic_code']}'),\n"

    insert_query = insert_query[:-2] + ";"

    print("insert_state() finished")
    return insert_query + "\n" * 3


if __name__ == "__main__":
    state = insert_state()
    with open("../../sql/insert_state.sql", "w") as file:
        file.write(state)
        file.close()