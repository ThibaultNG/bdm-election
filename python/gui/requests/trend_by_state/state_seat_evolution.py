from python.gui.requests.table import generate_table
import plotly.express as px
import pandas as pd


def get_state_seat_evolution_graph(selected_state):
    number_of_seats_by_party_query = f"""
        SELECT y.year_label, p.party_name, COUNT(*) AS seat_count
        FROM (
          SELECT vf.id_year, vf.id_district, MAX(vf.candidate_vote) AS max_vote
          FROM vote_fact vf
          GROUP BY vf.id_year, vf.id_district
        ) AS max_votes
        JOIN vote_fact vf ON vf.id_year = max_votes.id_year AND vf.id_district = max_votes.id_district AND vf.candidate_vote = max_votes.max_vote
        JOIN candidate c ON vf.id_candidate = c.id_candidate
        JOIN party p ON c.id_party = p.id_party
        JOIN year y ON vf.id_year = y.id_year
        JOIN district d on d.id_district = vf.id_district
        JOIN state s2 on d.id_state = s2.id_state
        WHERE s2.state_name = '{selected_state}'
        GROUP BY y.year_label, p.party_name
    """

    col_names, results = generate_table(number_of_seats_by_party_query)

    df = pd.DataFrame(data=results, columns=col_names)

    fig = px.line(
        data_frame=df,
        x="year_label",
        y="seat_count",
        color="party_name",
        labels={"year_label": "Année", "party_name": "Partis politiques", "seat_count": "Nombre de sièges"},
        markers=True
    )

    president_df = pd.read_csv("../../ressources/presidents.csv")


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
    # fig.write_html(file="../templates/state/seats_graph_div.html", full_html=False)

    print("Seat evolution finished")
    return fig.to_html(full_html=False)


if __name__ == "__main__":
    get_state_seat_evolution_graph("MINNESOTA")
