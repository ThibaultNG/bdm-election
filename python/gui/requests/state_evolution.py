from python.gui.requests.table import generate_table
import plotly.express as px
import pandas as pd


def state_evolution():
    state_evolution_query = """
        SELECT y.year_label, s.state_name, p.party_name, COUNT(*) AS seat_number
        FROM (
          SELECT vf.id_year, vf.id_district, MAX(vf.candidate_vote) AS elected_vote_count
          FROM vote_fact vf
          GROUP BY vf.id_year, vf.id_district
        ) AS elected
        JOIN vote_fact vf ON vf.id_year = elected.id_year 
            AND vf.id_district = elected.id_district 
            AND vf.candidate_vote = elected.elected_vote_count
        JOIN candidate c ON vf.id_candidate = c.id_candidate
        JOIN party p ON c.id_party = p.id_party
        JOIN year y ON vf.id_year = y.id_year
        JOIN district d ON vf.id_district = d.id_district
        JOIN state s ON d.id_state = s.id_state
        GROUP BY y.year_label, s.state_name, p.party_name
    """

    col_names, results = generate_table(state_evolution_query)

    df = pd.DataFrame(data=results, columns=col_names)
    df = df[df["party_name"].isin(["DEMOCRAT", "REPUBLICAN"])]

    def compare(x):
        if x.size == 0:
            return 0
        elif x.size == 4:
            if x.iloc[0]["party_name"] == "DEMOCRAT":
                return 1
            return -1
        elif x.size == 8:
            if x.iloc[0]["party_name"] == "DEMOCRAT":
                if x.iloc[0]["seat_number"] == x.iloc[1]["seat_number"]:
                    return 0
                elif x.iloc[0]["seat_number"] > x.iloc[1]["seat_number"]:
                    return 1
                return -1
            else:
                if x.iloc[0]["seat_number"] == x.iloc[1]["seat_number"]:
                    return 0
                elif x.iloc[0]["seat_number"] > x.iloc[1]["seat_number"]:
                    return -1
                return 1

    df = df.groupby(["year_label", "state_name"]).apply(lambda x: compare(x)).to_frame(name="number_of_states")

    democrat = df.groupby("year_label").apply(lambda x: x[x["number_of_states"] == 1].count()).reset_index()
    equal = df.groupby("year_label").apply(lambda x: x[x["number_of_states"] == 0].count()).reset_index()
    republican = df.groupby("year_label").apply(lambda x: x[x["number_of_states"] == -1].count()).reset_index()

    democrat["party"] = "DEMOCRAT"
    equal["party"] = "EQUAL"
    republican["party"] = "REPUBLICAN"

    number_of_state_by_party = pd.concat([democrat, republican, equal], ignore_index=True)

    fig = px.line(
        data_frame=number_of_state_by_party,
        x="year_label",
        y="number_of_states",
        color="party",
        labels={"year_label": "Année", "number_of_states": "Nombre d'états", "party": "Parti politique"},
        markers=True,
    )

    president_df = pd.read_csv("../../../ressources/presidents.csv")


    president_df[["Start Year", "End Year"]] = president_df["Years In Office"].str.split("-", expand=True).astype(int)
    president_df["Background Color"] = president_df["Party"].map({"Democratic": "blue", "Republican": "red"})

    # Creates shapes with the color of the party of the president + president name label
    for _, row in president_df.iterrows():
        party_color = row["Background Color"]
        start_year = row["Start Year"]
        end_year = row["End Year"]
        fig.add_shape(
            editable=False,
            type="rect",
            xref="x",
            yref="paper",
            x0=start_year,
            y0=0,
            x1=end_year,
            y1=1,
            fillcolor=party_color,
            opacity=0.1,
            layer="below",
            line=dict(width=0),
            label={
                "text": row["President Name"],
                "textposition": "top left",
                "textangle": 20
            }
        )

    # fig.show()

    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)

    fig.write_html(file="../templates/state_evolution_div.html", full_html=False)

    print("State evolution finished")


if __name__ == "__main__":
    state_evolution()
