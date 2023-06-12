import pymzn
import datetime
from minizinc import Instance, Model, Solver
from werkzeug.datastructures import FileStorage
from typing import List
from variables import MZN_MODEL_FILE, DZN_DATA_FILE


def read_input_data_from_txt(file: FileStorage):

    file_data = file.read().decode('utf-8')
    file_data = file_data.strip().split('\n')

    output = []
    matrix = []
    for id, line in enumerate(file_data):
        
        if(id<3):
            num = line.strip()
            output.append(int(num))
        else:
            arr = line.strip().split()
            temp = []
            for num in arr:
                temp.append(int(num))
            
            matrix.append(temp)

    output.append(matrix)

    return output
    


def convert_input_data_list_to_dict(data: List):
    output = {}
    output['n'] = data[0]
    output['Min'] = data[1]
    output['Max'] = data[2]
    output['D'] = data[3]

    return output
     

def input_list_data_to_dzn(data: List, output_file: str):

    data_dict = convert_input_data_list_to_dict(data)
    pymzn.dict2dzn(objs=data_dict, fout=output_file)


def get_mzn_model_solution(mzn_file:str, dzn_file: str):
    gecode = Solver.lookup("chuffed")
    
    model = Model()
    model.add_file(mzn_file)
    model.add_file(dzn_file)

    instance = Instance(gecode, model)

    timeout = datetime.timedelta(minutes=2)

    result = instance.solve(timeout=timeout)

    return result.solution


def solve_problem(input_file: FileStorage):
    
    data = read_input_data_from_txt(input_file)
    input_list_data_to_dzn(data, DZN_DATA_FILE)
    
    solution = str( get_mzn_model_solution(MZN_MODEL_FILE, DZN_DATA_FILE) )

    if solution=='None':
        return None
    else:        
        solution_dict = convert_solution_string_to_dict(solution, data[0])
        return solution_dict




def convert_solution_string_to_dict(solution_str: str, n: int):
    # Split the string into key-value pairs
    key_value_pairs = solution_str.split(",", 1)

    data_dict = {}

    for pair in key_value_pairs:
        # Split each pair into key and value
        key, value = pair.split(":")

        # Strip any whitespace from the key and value
        key = key.strip()
        value = value.strip()

        # Check if the value is a list
        if "[" in value and "]" in value:
            # Extract the list elements and convert them to integers                        
            temp = [int(num) for num in value[1:-1].split(",")]

            value = [temp[i:i+n] for i in range(0, len(temp), n)]

        # Assign the key-value pair to the dictionary
        data_dict[key] = value


    return data_dict



def solve_problem_from_data_list(data_list: List):

    input_list_data_to_dzn(data_list, DZN_DATA_FILE)

    solution = str( get_mzn_model_solution(MZN_MODEL_FILE, DZN_DATA_FILE) )

    if solution=='None':
        return None
    else:        
        solution_dict = convert_solution_string_to_dict(solution, data_list[0])
        return solution_dict


