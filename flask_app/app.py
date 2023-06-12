from flask import Flask, render_template, request
from utils import solve_problem, solve_problem_from_data_list
from variables import DZN_DATA_FILE

app = Flask(__name__)


@app.route('/', methods=['POST','GET'])
def index():
	if request.method == 'GET': 
		return render_template('index.html')
	
	elif request.method == 'POST': 
		print("-----------------------------------------")
		integer1 = request.form.get('integer1')
		integer2 = request.form.get('integer2')
		integer3 = request.form.get('integer3')

		matrix = []
		for i in range(int(integer1)):
			row = []
			for j in range(int(integer1)):
				key = f'matrix_{i}_{j}'
				value = request.form.get(key)
				row.append(int(value))
			matrix.append(row)

		print(matrix)

		return "hola"


@app.route('/manual-input', methods=['POST','GET'])
def manual_input():
	if request.method == 'GET':
		return render_template("manual_input.html")
	
	elif request.method == 'POST': 
		n_teams = int(request.form.get('n_teams'))
		min = int(request.form.get('Min'))
		max = int(request.form.get('Max'))

		matrix = []
		for i in range(int(n_teams)):
			row = []
			for j in range(int(n_teams)):
				key = f'matrix_{i}_{j}'
				value = request.form.get(key)
				row.append(int(value))
			matrix.append(row)

		print(matrix)

		data_list = [n_teams, min, max, matrix]
		
		solution = solve_problem_from_data_list(data_list)
		num_rows = len(solution['Matriz'])
		num_cols = len(solution['Matriz'][0])

		return render_template("display_results.html", data=solution, num_rows=num_rows, num_cols=num_cols)
	


@app.route('/upload-file', methods=['POST'])
def upload_input_file():

	if request.method == 'POST':

		file = request.files['file']

		solution = solve_problem(file)

		if(solution==None):
			return render_template("unsatisfiable.html")

		num_rows = len(solution['Matriz'])
		num_cols = len(solution['Matriz'][0])

		return render_template("display_results.html", data=solution, num_rows=num_rows, num_cols=num_cols)


if __name__ == "__main__":
	app.run(host='0.0.0.0',debug=True)

