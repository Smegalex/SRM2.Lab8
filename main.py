from sympy.abc import x
from lab6 import gauss_jordan, separate_matrix_and_vector, zeidel_method


def create_x_range(x_start: float, x_end: float, h: float) -> list:
    h_multiplier = 1
    while (not (h % 1 == 0)):
        h_multiplier = h_multiplier / 10
        h = h * 10

    start_multiplier = 1
    while (not (x_start % 1 == 0)):
        start_multiplier = start_multiplier / 10
        x_start = x_start * 10

    end_multiplier = 1
    while (not (x_end % 1 == 0)):
        end_multiplier = end_multiplier / 10
        x_end = x_end * 10

    x_multiplier = 1
    if (start_multiplier > end_multiplier):
        x_start = x_start * (start_multiplier / end_multiplier)
        x_multiplier = end_multiplier
    else:
        x_end = x_end * (end_multiplier / start_multiplier)
        x_multiplier = start_multiplier

    multiplier = 1
    if (h_multiplier > x_multiplier):
        h = h * (h_multiplier / x_multiplier)
        multiplier = x_multiplier
    else:
        x_end = x_end * (x_multiplier / h_multiplier)
        x_start = x_start * (x_multiplier / h_multiplier)
        multiplier = h_multiplier

    x_end = int(x_end)
    x_start = int(x_start)
    h = int(h)

    x_range = [i * multiplier for i in range(x_start, x_end+h, h)]
    return x_range


def find_limit(limit: float | dict, k: int, h: float, N: int) -> dict | float:
    if (isinstance(limit, float)):
        return {f"y{k}": 1, "=": limit}

    returnable = {}

    if (k == N):
        returnable = {f"y{k}": limit["y'"]/h,
                      f"y{k-1}": -1*(limit["y'"]/h), "=": limit["="]}
    elif (k == 0):
        returnable = {"y1": limit["y'"]/h, "y0": -
                      1*(limit["y'"]/h), "=": limit["="]}

    returnable[f"y{k}"] += limit["y"]

    return returnable


def dict_equation_to_list(equation: dict, N: int) -> list:
    returnable = [0]*(N+2)
    for key, value in equation.items():
        if key == "=":
            returnable[-1] = value
            continue
        key = int(key.replace("y", ""))
        returnable[key] = value
    return returnable


def form_system(inside_pattern: dict, left_limit: dict | float, right_limit: dict | float, x_range: list, N: int) -> list:
    system = []
    substitutions = {}

    if len(list(left_limit.values())) == 1:
        substitutions["y0"] = list(left_limit.values())[0]
        system.append(left_limit)
    else:
        system.append(left_limit)
    if len(list(right_limit.values())) == 1:
        substitutions[f"y{N}"] = list(right_limit.values())[0]
        system.append(right_limit)
    else:
        system.append(right_limit)

    pattern_order = ["yk-1", "yk", "yk+1"]
    for i in range(1, N):
        new_equation = {"=": inside_pattern["="]}
        for j, k in enumerate(range(i-1, i+2)):
            # if f"y{k}" in substitutions:
            #     new_equation["="] += -1*substitutions[f"y{k}"]*inside_pattern[pattern_order[j]]
            # else:
            inside = inside_pattern[pattern_order[j]]
            if (not isinstance(inside, float)):
                new_equation[f"y{k}"] = inside.subs(x, x_range[i])
            else:
                new_equation[f"y{k}"] = inside

        system.append(new_equation)
    system = [dict_equation_to_list(i, N) for i in system]
    return system


def limit_difference(equation: dict, left_limit: float | dict, right_limit: float | dict, x_left: float, x_right: float, h: float):
    x_range = create_x_range(x_left, x_right, h)

    inside_ys = {"yk+1": 0, "yk": 0, "yk-1": 0, "=": equation["="]}

    # Заміна похідних різницевими аналогами
    inside_ys["yk+1"] += equation["y''"]/(h**2)
    inside_ys["yk"] += -2*equation["y''"]*(1/(h**2))
    inside_ys["yk-1"] += equation["y''"]/(h**2)

    inside_ys["yk+1"] += equation["y'"]/(h*2)
    inside_ys["yk-1"] += -1*(equation["y'"]/(h*2))

    inside_ys["yk"] += equation["y"]

    N = int((x_right-x_left)/h)

    left_limit = find_limit(left_limit, 0, h, N)
    right_limit = find_limit(right_limit, N, h, N)

    system = form_system(inside_ys, left_limit, right_limit, x_range, N)
    matrix, vector = separate_matrix_and_vector(system)
    return gauss_jordan(matrix, vector)


if __name__ == "__main__":
    equation = {"y''": 1, "y'": -0.6, "y": -x, "=": 1.2}
    left_limit = {"y'": -1.1, "y": 2, "=": 0.1}
    right_limit = 1.99
    h = 0.2
    x_left = 1.9
    x_right = 2.9
    solutions = limit_difference(
        equation, left_limit, right_limit,  x_left, x_right, h)
    print("Маємо крайову задачу:")
    print(equation["y''"], 'y" + (', equation["y'"],
          ")y' + (", equation["y"], ")y = ", equation["="])
    print(left_limit["y'"], "y'(", x_left, ") + (",
          left_limit["y"], ")y(", x_left, ") = ", left_limit['='])
    print("y(", x_right, ") = ", right_limit)
    print(f"h = {h}\n")
    print("Розв'язки:")
    print(solutions)
