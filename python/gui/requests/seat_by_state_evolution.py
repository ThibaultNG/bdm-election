from python.gui.table import generate_table
import plotly.express as px
import pandas as pd


def seat_by_state_evolution_query(state):
    number_of_seats_by_party_query = """
        SELECT s.state_name, y.year_label, p.party_name, COUNT(*) AS seat_count
        FROM (
          SELECT vf.id_year, vf.id_district, MAX(vf.candidate_vote) AS max_vote
          FROM vote_fact vf
          GROUP BY vf.id_year, vf.id_district
        ) AS max_votes
        JOIN vote_fact vf ON vf.id_year = max_votes.id_year AND vf.id_district = max_votes.id_district AND vf.candidate_vote = max_votes.max_vote
        JOIN candidate c ON vf.id_candidate = c.id_candidate
        JOIN party p ON c.id_party = p.id_party
        JOIN year y ON vf.id_year = y.id_year
        JOIN district d on vf.id_district = d.id_district
        JOIN state s on d.id_state = s.id_state
        GROUP BY s.state_name, y.year_label, p.party_name
    """

    col_names, results = generate_table(number_of_seats_by_party_query)

    df = pd.DataFrame(data=results, columns=col_names)

    df = df.loc[df['state_name'] == "MINNESOTA"]

    fig = px.line(
        data_frame=df,
        x="year_label",
        y="seat_count",
        color="party_name",
        labels={"year_label": "Année", "party_name": "Partis politiques", "seat_count": "Nombre de sièges"},
        markers=True
    )
    #fig.show()

    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)
    fig.write_html(file="templates/seat_by_state_graph_div.html", full_html=False)

    print("Seat by state evolution finished")
if __name__ == "__main__":
    seat_by_state_evolution_query("MINNESOTA")