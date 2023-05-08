import json

from flask import Flask, request, render_template
from gevent.pywsgi import WSGIServer
from python.gui.graph import generate_graph_image
from python.gui.table import generate_table

# import CSS file
app = Flask(__name__, static_folder='static', template_folder='templates')

print("http://localhost:5000")


@app.route('/', methods=['GET'])
def index():
    sql_query = "SELECT * FROM state"
    col_names, results = generate_table(sql_query)
    return render_template('index.html', col_names=col_names, results=results)

@app.route('/persons', methods=['GET'])
def persons():
    sql_query = "SELECT * FROM person"
    col_names, results = generate_table(sql_query)
    return render_template('result.html', col_names=col_names, results=results)


@app.route('/year', methods=['GET'])
def year():
    sql_query = "SELECT * FROM year"
    col_names, results = generate_table(sql_query)
    return render_template('result.html', col_names=col_names, results=results)


@app.route('/candidates', methods=['GET'])
def candidates():
    sql_query = "SELECT * FROM candidate JOIN party p on candidate.id_party = p.id_party JOIN person p2 on " \
                "p2.id_person = candidate.id_person "
    col_names, results = generate_table(sql_query)
    return render_template('result.html', col_names=col_names, results=results)


@app.route('/candidate-by-name', methods=['GET'])
def candidate_by_name():
    sql_query = f"""
                SELECT vf.*, p.person_name
                FROM vote_fact vf
                JOIN candidate c ON vf.id_candidate = c.id_candidate
                JOIN person p ON c.id_person = p.id_person
                WHERE p.person_name ILIKE '%' || '{request.args['input-name']}' || '%';
            """
    col_names, results = generate_table(sql_query)
    if str(request.args['input-name'].lower()) == 'kennedy':
        with open('kennedy.json', 'r') as json_file:
            json_data = json.load(json_file)
            names = json_data['names']
            tmp_results = results
            results = []
            for tmp_result in tmp_results:
                print(tmp_result)
                if tmp_result[7] in names:
                    results.append(tmp_result)
    return render_template('result.html', col_names=col_names, results=results)

@app.route('/evolve-vote-1', methods=['GET'])
def evolve_vote_1():
    sql_query = f"""
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
                                        s.state_name = '{request.args['input-state']}'
                            ) AS subquery
                        GROUP BY
                            subquery.year_label
                    ) AS total_votes ON y.year_label = total_votes.year_label
                WHERE
                        s.state_name = '{request.args['input-state']}'
                GROUP BY
                    s.state_name,
                    pa.party_name,
                    total_votes.total_vote_all_districts,
                    y.year_label
                ORDER BY pa.party_name asc, y.year_label asc;
            """
    col_names, results = generate_table(sql_query)
    if request.args['input-party'] != "":
        generate_graph_image(results, request.args['input-state'], request.args['input-party'])
        return render_template('graph.html', col_names=col_names, results=results)

    return render_template('result.html', col_names=col_names, results=results)



@app.route('/custom-query', methods=['POST'])
def custom_query():
    sql_query = request.form["query"]
    col_names, results = generate_table(sql_query)
    return render_template('result.html', col_names=col_names, results=results)


@app.route("/map", methods=["GET"])
def choropleth_map():
    # generate_map()
    with open("templates/map_div.html", "r", encoding="utf-8") as file:
        map_fig = file.read()
        file.close()

    return render_template("figure.html", figure=map_fig)


@app.route("/trend", methods=["GET"])
def graph():
    with open("templates/seats_graph_div.html", "r", encoding="utf-8") as file:
        seats_graph_div = file.read()
        file.close()

    with open("templates/vote_share_graph_div.html", "r", encoding="utf-8") as file:
        vote_share_graph_div = file.read()
        file.close()

    with open("templates/state_evolution_div.html", "r", encoding="utf-8") as file:
        state_evolution = file.read()
        file.close()

    return render_template(
        "trend.html",
        seat_evolution=seats_graph_div,
        vote_share_evolution=vote_share_graph_div,
        state_evolution=state_evolution
    )


@app.route("/write-in", methods=["GET"])
def write_in_scores():

    all_winners_query = """
        SELECT y.year_label, s.state_name, p.person_name
        FROM vote_fact vf
        JOIN year y ON vf.id_year = y.id_year
        JOIN district d ON vf.id_district = d.id_district
        JOIN candidate c ON vf.id_candidate = c.id_candidate
        JOIN person p ON c.id_person = p.id_person
        JOIN party pa ON pa.id_party = c.id_party
        JOIN state s ON s.id_state = d.id_state
        WHERE (vf.id_year, vf.id_district, vf.candidate_vote) IN (
            SELECT id_year, id_district, MAX(candidate_vote)
        FROM vote_fact
        GROUP BY id_year, id_district
        ) AND c.write_in = True;
    """

    winner_col_names, winner_results = generate_table(all_winners_query)

    winner_col_names = ["Année", "État", "Nom"]

    best_scores_query = """
        SELECT y.year_label, s.state_name, p.person_name, vf.candidate_vote, vf.total_vote
        FROM vote_fact vf
        JOIN year y ON vf.id_year = y.id_year
        JOIN district d ON vf.id_district = d.id_district
        JOIN candidate c ON vf.id_candidate = c.id_candidate
        JOIN person p ON c.id_person = p.id_person
        JOIN party pa ON pa.id_party = c.id_party
        JOIN state s ON s.id_state = d.id_state
        WHERE c.write_in = True AND p.person_name <> 'WRITEIN'
        ORDER BY vf.candidate_vote DESC
    """

    best_score_col_names, best_score_results = generate_table(best_scores_query)
    best_score_col_names = ["Année", "État", "Nom", "Nombre de votes"]

    winner_names = [row[2] for row in winner_results]

    best_score_results = [list(row) for row in best_score_results]

    for bs_row in best_score_results:
        if bs_row[2] in winner_names:
            bs_row[4] = True
        else:
            bs_row[4] = False

    return render_template(
        "write_in_scores.html",
        winner_col_names=winner_col_names,
        winner_results=winner_results,
        best_score_col_names=best_score_col_names,
        best_score_results=best_score_results
    )


if __name__ == '__main__':
    # Debug/Development
    # app.run(debug=True, host="0.0.0.0", port="5000")
    # Production

    http_server = WSGIServer(('', 5000), app)
    http_server.serve_forever()
