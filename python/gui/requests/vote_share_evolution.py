from python.gui.table import generate_table
import plotly.express as px
import pandas as pd


def vote_share_evolution():
    vote_share_evolution_query = """
        SELECT y.year_label, p.party_name, SUM(vf.candidate_vote) AS party_votes
        FROM vote_fact vf
        JOIN year y ON vf.id_year = y.id_year
        JOIN candidate c ON vf.id_candidate = c.id_candidate
        JOIN party p ON c.id_party = p.id_party
        WHERE c.id_party < 3
        GROUP BY y.year_label, p.party_name
        ORDER BY y.year_label
    """
    col_names, results = generate_table(vote_share_evolution_query)

    df = pd.DataFrame(data=results, columns=col_names)

    df_total_vote = df.groupby("year_label").sum("party_votes").rename(columns={"party_votes": "total_votes"})

    df = df.merge(df_total_vote, left_on="year_label", right_on="year_label", how="left")
    df["share"] = df["party_votes"] / df["total_votes"]

    df.sort_values(by="party_votes")

    fig = px.line(
        data_frame=df,
        x="year_label",
        y="share",
        color="party_name",
        labels={"year_label": "Année", "party_name": "Partis politiques", "party_votes": "", "share": "Part des votes"},
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

    fig.write_html(file="../templates/vote_share_graph_div.html", full_html=False)

    print("Vote share evolution finished")


if __name__ == "__main__":
    vote_share_evolution()
