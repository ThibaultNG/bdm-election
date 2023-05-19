from python.gui.requests.table import generate_table
import plotly.express as px
import pandas as pd


def vote_share_evolution_by_state_query(state):
    vote_share_evolution_by_state_query = \
        f"""
                SELECT
                    s.state_name,
                    pa.party_name,
                    round(cast(SUM(vf.candidate_vote) as decimal) / cast(total_vote_all_districts as decimal),2) as "vote_part",
                    SUM(vf.candidate_vote) AS party_vote_all_districts,
                    total_vote_all_districts,
                    y.year_label
                FROM
                    vote_fact vf
                        JOIN district d ON vf.id_district = d.id_district
                        JOIN state s ON d.id_state = s.id_state
                        JOIN year y ON vf.id_year = y.id_year
                        JOIN candidate c ON vf.id_candidate = c.id_candidate
                        JOIN person pe ON c.id_person = pe.id_person
                        JOIN party pa ON c.id_party = pa.id_party
                        JOIN (
                        SELECT
                            SUM(subquery.total_vote) AS total_vote_all_districts,
                            subquery.year_label
                        FROM
                            (
                                SELECT DISTINCT
                                    d.id_district,
                                    total_vote,
                                    y.year_label
                                FROM
                                    vote_fact vf
                                        JOIN district d ON vf.id_district = d.id_district
                                        JOIN state s ON d.id_state = s.id_state
                                        JOIN year y ON vf.id_year = y.id_year
                                WHERE
                                        s.state_name = '{state}'
                            ) AS subquery
                        GROUP BY
                            subquery.year_label
                    ) AS total_votes ON y.year_label = total_votes.year_label
                WHERE
                        s.state_name = '{state}'
                GROUP BY
                    s.state_name,
                    pa.party_name,
                    total_votes.total_vote_all_districts,
                    y.year_label
                ORDER BY pa.party_name asc, y.year_label asc;
    """
    col_names, results = generate_table(vote_share_evolution_by_state_query)
    df = pd.DataFrame(data=results, columns=col_names)
    fig = px.line(
        data_frame=df,
        x="year_label",
        y="vote_part",
        color="party_name",
        labels={"year_label": "Année", "party_name": "Partis politiques", "vote_part": "Part des votes"},
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

    #fig.show()
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)

    fig.write_html(file="../templates/vote_share_by_state_graph_div.html", full_html=False)

    print("Vote share by state evolution finished")


if __name__ == "__main__":
    vote_share_evolution_by_state_query("MINNESOTA")

