import plotly.express as px
import pandas as pd
import geopandas as gpd


def generate_map():
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

    # Random values for all congressional districts
    df = pd.read_csv("../../../ressources/rdm-data.csv",
                     dtype={"stcd": str},
                     delimiter=";")

    # Show the map
    fig = px.choropleth(df, geojson=gdf_congressional_districts_dissolved, locations='stcd', color='rdm',
                        color_continuous_scale="Viridis",
                        range_color=(0, 15),
                        scope="usa",
                        labels={'rdm': 'Ma donnée'}
                        )
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0}, height=700)
    # fig.show()

    # fig.write_html("templates/map.html")
    fig.write_html("templates/map_div.html", full_html=False)

    print("map generation finished")


if __name__ == "__main__":
    generate_map()
