import os
import psycopg2
from flask import Flask, request, render_template, redirect, url_for
from gevent.pywsgi import WSGIServer
import json

# import CSS file
app = Flask(__name__, static_folder='static')

# Set the FLASK_ENV environment variable to "production"
os.environ['FLASK_ENV'] = 'production'



@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        checkKennedyBeforePrint = False
        # Check if a button was clicked
        if request.form.get('button1') == 'Afficher la liste des personnes':
            sql_query = "SELECT * FROM person"
        elif request.form.get('button2') == 'Afficher la liste des années':
            sql_query = "SELECT * FROM year"
        elif request.form.get('button3') == 'Afficher la liste des candidats avec nom des personnes et des parties':
            sql_query = "SELECT * FROM candidate JOIN party p on candidate.id_party = p.id_party JOIN person p2 on p2.id_person = candidate.id_person"
        elif request.form.get('button4') == 'Afficher la liste des candidats avec pour nom de famille : ':
            sql_query = f"""
                SELECT vf.*, p.person_name
                FROM vote_fact vf
                JOIN candidate c ON vf.id_candidate = c.id_candidate
                JOIN person p ON c.id_person = p.id_person
                WHERE p.person_name ILIKE '%' || '{request.form.get('input4')}' || '%';
            """
            if 'kennedy' in str(request.form.get('input4')).lower():
                checkKennedyBeforePrint = True
        else:
            # If no button was clicked, execute the SQL query from the form
            sql_query = request.form['query']

        # create a connection to the database
        conn = psycopg2.connect("""
            host=localhost
            port=5432
            dbname=election
            user=postgres
            password=camille
            """)

        # create a cursor object
        cur = conn.cursor()

        # execute the SQL query
        cur.execute(sql_query)

        # fetch the results
        results = cur.fetchall()

        # Get the column names
        col_names = [desc[0] for desc in cur.description]

        # close the cursor and connection
        cur.close()
        conn.close()

        if checkKennedyBeforePrint :
            with open('kennedy.json', 'r') as json_file:
                json_data = json.load(json_file)
                names = json_data['names']
                tmp_results = results
                results = []
                for tmp_result in tmp_results:
                    print(tmp_result)
                    if tmp_result[7] in names:
                        results.append(tmp_result)

        if len(results) == 1:
            # If the result contains only one row, render the table
            #print("in if ")
            return render_template('result.html', col_names=col_names, results=results)

        else:
            #print("in else, c'est là qu'il doit y avoir les autres affichages genre map_congressional_district.py")
            return render_template('result.html', col_names=col_names, results=results)
            # If the result contains more than one row, render the map
            #return render_template('map.html', results=results)#un render map ou un lancement de script peu importe

    # if the request method is GET, display the form
    return render_template('index.html')

if __name__ == '__main__':
    # Debug/Development
    # app.run(debug=True, host="0.0.0.0", port="5000")
    # Production
    http_server = WSGIServer(('', 5000), app)
    http_server.serve_forever()
