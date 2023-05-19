import plotly.express as px
import pandas as pd
import geopandas as gpd

from python.gui.table import generate_table


def generate_seat_map(chosen_year):
    # Congressional district / County relationship
    df_congressional_districts = pd.read_csv('../../../ressources/tab20_cd11820_county20_natl.csv',
                                             dtype={"GEOID_CD118_20": str, "GEOID_COUNTY_20": str},
                                             delimiter="|")

    # Cleaning data to keep stcd (State+Congressional District, example : 0101) and county fips code
    df_congressional_districts = df_congressional_districts.drop(columns=[
        "OID_CD118_20",
        "NAMELSAD_CD118_20",
        "AREALAND_CD118_20",
        "AREAWATER_CD118_20",
        "MTFCC_CD118_20",
        "FUNCSTAT_CD118_20",
        "OID_COUNTY_20",
        "NAMELSAD_COUNTY_20",
        "AREALAND_COUNTY_20",
        "AREAWATER_COUNTY_20",
        "MTFCC_COUNTY_20",
        "CLASSFP_COUNTY_20",
        "FUNCSTAT_COUNTY_20",
        "AREALAND_PART",
        "AREAWATER_PART"
    ]).rename(columns={"GEOID_CD118_20": "stcd", "GEOID_COUNTY_20": "fips"})

    # Geographical data of all counties
    gdf_counties = gpd.read_file('../../../ressources/geojson-counties.json')

    # Merge the geographical data to have the congressional districts of each county
    gdf_congressional_districts = gdf_counties.merge(df_congressional_districts, left_on="id", right_on='fips',
                                                     how='left')

    # Merge counties using the stcd => To have a map of congressional districts
    gdf_congressional_districts_dissolved = gdf_congressional_districts.dissolve(by="stcd")

    number_of_seats_by_party_query = f"""
        SELECT y.year_label, p.party_name, s.fips_code, d.district_number, s.state_name
        FROM (
          SELECT vf.id_year, vf.id_district, MAX(vf.candidate_vote) AS max_vote
          FROM vote_fact vf
          GROUP BY vf.id_year, vf.id_district
        ) AS max_votes
        JOIN vote_fact vf ON vf.id_year = max_votes.id_year AND vf.id_district = max_votes.id_district AND vf.candidate_vote = max_votes.max_vote
        JOIN candidate c ON vf.id_candidate = c.id_candidate
        JOIN party p ON c.id_party = p.id_party
        JOIN year y ON vf.id_year = y.id_year
        JOIN district d ON d.id_district = vf.id_district
        JOIN state s ON d.id_state = s.id_state
        WHERE y.year_label = {chosen_year}
    """

    col_names, results = generate_table(number_of_seats_by_party_query)

    df = pd.DataFrame(columns=col_names, data=results)

    def generate_stcd(row):
        st = row["fips_code"]
        cd = row["district_number"][1:]
        if len(st) == 1:
            st = "0" + st

        if st + cd == "3000":
            return "3001"
        return st + cd

    df["stcd"] = df.apply(lambda x: generate_stcd(x), axis=1)

    montana_1 = df[df["stcd"] == "3001"]

    montana_2 = montana_1.copy()
    montana_2["stcd"] = "3002"

    df = pd.concat([df, montana_2], ignore_index=True)

    # Show the map
    fig = px.choropleth(df, geojson=gdf_congressional_districts_dissolved, locations='stcd', color='party_name',
                        color_continuous_scale="Viridis",
                        range_color=(0, 15),
                        scope="usa",
                        labels={
                            'party_name': 'Parti politique',
                            "state_name": "État",
                            "district_number": "Numéro de district"
                        },
                        hover_data=["state_name", "district_number", "party_name"]
                        )
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0}, height=700)
    # fig.show()

    fig.write_html(f"../templates/map/{chosen_year}_map_div.html")

    print(chosen_year, "map generation finished")


if __name__ == "__main__":
    for year in range(1976, 2021, 2):
        generate_seat_map(year)
