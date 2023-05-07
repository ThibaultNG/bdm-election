import os
from flask import Flask, request, render_template
from gevent.pywsgi import WSGIServer

from python.gui.table import generate_table

# import CSS file
app = Flask(__name__, static_folder='static', template_folder='templates')

# Set the FLASK_ENV environment variable to "production"
os.environ['FLASK_ENV'] = 'production'

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

    return render_template('index.html')


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


@app.route('/custom-query', methods=['GET'])
def custom_query():
    sql_query = request.form["query"]
    col_names, results = generate_table(sql_query)
    return render_template('result.html', col_names=col_names, results=results)


@app.route('/map', methods=['GET'])
def choropleth_map():
    return render_template('html_map.html')


if __name__ == '__main__':
    # Debug/Development
    # app.run(debug=True, host="0.0.0.0", port="5000")
    # Production

    http_server = WSGIServer(('', 5000), app)
    http_server.serve_forever()
