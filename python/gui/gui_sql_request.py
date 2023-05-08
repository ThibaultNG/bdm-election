from flask import Flask, request, render_template
from gevent.pywsgi import WSGIServer
from map_congressional_district import generate_map
from python.gui.graph import generate_graph_image
from python.gui.table import generate_table

# import CSS file
app = Flask(__name__, static_folder='static', template_folder='templates')

print("http://localhost:5000")


@app.route('/', methods=['GET'])
def index():

        # if check_kennedy_before_print :
        #     with open('kennedy.json', 'r') as json_file:
        #         json_data = json.load(json_file)
        #         names = json_data['names']
        #         tmp_results = results
        #         results = []
        #         for tmp_result in tmp_results:
        #             print(tmp_result)
        #             if tmp_result[7] in names:
        #                 results.append(tmp_result)
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



@app.route('/custom-query', methods=['GET'])
def custom_query():
    sql_query = request.form["query"]
    col_names, results = generate_table(sql_query)
    return render_template('result.html', col_names=col_names, results=results)


@app.route('/map', methods=['GET'])
def choropleth_map():
    generate_map()

    return render_template('map.html')


if __name__ == '__main__':
    # Debug/Development
    # app.run(debug=True, host="0.0.0.0", port="5000")
    # Production

    http_server = WSGIServer(('', 5000), app)
    http_server.serve_forever()
