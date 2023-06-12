from minizinc import Instance, Model, Solver, types
from utils import convert_solution_string_to_dict

# Specify the path to the MZN file
mzn_file = "CalDep.mzn"

# Specify the path to the DZN file
dzn_file = "input_data.dzn"

gecode = Solver.lookup("gecode")
model = Model()

model.add_file(mzn_file)

model.add_file(dzn_file)

instance = Instance(gecode, model)

result = instance.solve()
print(result.solution)
print(type(result.solution))
print(str(result.solution))


print("ddddddddddddddd ")

convert_solution_string_to_dict(str(result.solution), 4)


print(result.solution.check()) 