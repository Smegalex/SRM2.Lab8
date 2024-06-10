import math
import copy


def basic_checks(matrix: list, vector: list) -> None:
    if not isinstance(matrix, list) or not isinstance(vector, list):
        raise ValueError(
            "Матриця коефіцієнтів і вектор розв'язків мають бути типу list.")
    if len(matrix) != len(vector):
        raise ValueError(
            "Вектор розв'язків має бути такої ж розмірності, що і кількість рядків в матриці коефіцієнтів.")
    if len(matrix) != len(matrix[0]):
        raise ValueError(
            "Матриця коефіцієнтів має бути квадратною для того, щоб існував єдиний розв'язок.")


def join_matrix_and_vector(matrix: list, vector: list) -> list:
    matrix_copy = copy.deepcopy(matrix)
    for i, row in enumerate(matrix_copy):
        row.append(vector[i])

    return matrix_copy

def separate_matrix_and_vector(matrix: list) -> list:
    matrix_copy = copy.deepcopy(matrix)
    vector = []
    for i, row in enumerate(matrix_copy):
        vector.append(row[-1])
        row.pop(-1)

    return matrix_copy, vector


def print_matrix(matrix: list) -> None:
    for row in matrix:
        print(row)


def swap_rows(matrix: list, row1_ind: int, row2_ind: int) -> list:
    buffer = matrix[row1_ind]

    matrix[row1_ind] = matrix[row2_ind]
    matrix[row2_ind] = buffer
    return matrix


def vector_subtraction(vector1: list, vector2: list) -> list:
    result = []
    for i in range(len(vector2)):
        result.append(vector1[i]-vector2[i])
    return result


def gauss_jordan(matrix: list, vector: list) -> list:
    basic_checks(matrix, vector)

    ext_matrix = join_matrix_and_vector(matrix, vector)

    def check_for_zero(matrix: list, col_ind: int) -> matrix:
        non_zero_row_ind = None
        if (matrix[col_ind][col_ind] == 0):
            for ind in range(col_ind, len(matrix)):
                if matrix[ind][col_ind] != 0:
                    non_zero_row_ind = ind
                    break
            if non_zero_row_ind == None:
                raise ValueError("Система не має єдиного розв'язку.")

            # переставляємо рядочки місцями
            matrix = swap_rows(matrix, col_ind, non_zero_row_ind)
        return matrix

    def row_division(row: list) -> list:
        divider = None
        new_row = []
        for el in row:
            if el == 0:
                new_row.append(el)
                continue
            if divider == None:
                new_row.append(1)
                divider = el
                continue
            new_row.append(el/divider)
        return new_row

    def replace_row(row: list, subtractor: list):
        replacement_row = []
        first_nonZero_ind = None
        for ind in range(len(row)):
            if subtractor[ind] == 0:
                replacement_row.append(row[ind])
                continue
            if first_nonZero_ind == None:
                first_nonZero_ind = ind
            replacement_row.append(
                row[ind]-row[first_nonZero_ind]*subtractor[ind])

        return replacement_row

    def get_solutions(ext_matrix: list) -> list:
        vector = []
        for row in ext_matrix:
            vector.append(row[-1])

        return vector

    for col_ind in range(len(matrix)):
        ext_matrix = check_for_zero(ext_matrix, col_ind)
        ext_matrix[col_ind] = row_division(ext_matrix[col_ind])

        for row_ind in range(len(matrix)):
            if row_ind != col_ind:
                ext_matrix[row_ind] = replace_row(
                    ext_matrix[row_ind], ext_matrix[col_ind])

    return get_solutions(ext_matrix)


def zeidel_method(matrix: list, vector: list, error: float, opLim: int = 1000) -> list:
    def find_matrix_norms(matrix: list) -> list:
        columns_sums = [0]*len(matrix)
        for row in matrix:
            for i in range(len(matrix)):
                columns_sums[i] += row[i]
        norm1 = max(columns_sums)

        el_squared_sum = 0
        for row in matrix:
            for el in row:
                el_squared_sum += el ** 2
        norm2 = math.sqrt(el_squared_sum)

        rows_sums = []
        for row in matrix:
            rows_sums.append(sum(row))
        normc = max(rows_sums)

        return [norm1, norm2, normc]

    def find_vector_norms(vector: list) -> list:
        norm1 = sum(vector)
        el_sqr_sum = 0
        for el in vector:
            el_sqr_sum += el**2
        norm2 = math.sqrt(el_sqr_sum)

        normc = max(vector)

        return [norm1, norm2, normc]

    def getC(As: list) -> list:
        C = [[None]*len(As)]*len(As)
        for i in range(len(As)):
            for j in range(len(As)):
                if i >= j:
                    C[i][j] = As[i][j]
        return C

    basic_checks(matrix, vector)
    Bs = []
    for i in range(len(matrix)):
        Bs.append(vector[i]/matrix[i][i])
    As = [[None] * len(matrix) for _ in range(len(matrix))]
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if i == j:
                As[i][j] = 0
            else:
                As[i][j] = - matrix[i][j]/matrix[i][i]
    Xs = Bs

    sufficient = False
    Cnorm = max(find_matrix_norms(getC(As)))
    suddicientNorm = None
    for norm in find_matrix_norms(As):
        if norm < 1:
            print("Достатня умова збіжності методу Зейделя досягнута.")
            sufficient = True
            sufficientnorm = norm
            break
    counter = 0
    while True:

        newXs = [None]*len(matrix)
        for i in range(len(matrix)):
            newXs[i] = Bs[i]
            for j in range(len(matrix)):
                if newXs[j] == None:
                    newXs[i] += As[i][j]*Xs[j]
                else:
                    newXs[i] += As[i][j]*newXs[j]
        # check error
        e = find_vector_norms(vector_subtraction(newXs, Xs))[2]
        if sufficient:
            e = e*(Cnorm/(1-sufficientnorm))
        if e <= error:
            return newXs
        else:
            Xs = newXs
        counter += 1
        if (counter == opLim):
            print(f"Метод Зейделя не збігається за {opLim} операцій.")


if __name__ == "__main__":
    gauss_matrix = [[7.5, -5.5, 0, 0, 0],
                    [26.5, -52.1, 23.5, 0, 0],
                    [0, 26.5, -52.3, 23.5, 0],
                    [0, 0, 26.5, -52.5, 23.5],
                    [0, 0, 0, 26.5, -52.7]]
    gauss_vector = [0.1, 1.2, 1.2, 1.2, -45.565]

    gauss = join_matrix_and_vector(gauss_matrix, gauss_vector)

    print(f"Розширена матриця, яку треба розв'язати методом Гауса-Жордана:")
    print_matrix(gauss)
    print("\nРезультати розв'язання:")
    print(gauss_jordan(gauss_matrix, gauss_vector))

    # zeidel_matrix = [[28, 9, -3, -7],
    #                 [-5, 21, -5, -3],
    #                 [-8, 1, -16, 5],
    #                 [0, -2, 5, 8]]
    # zeidel_vector = [-159, 63, -45, 24]

    # error = 0.01

    # zeidel = join_matrix_and_vector(zeidel_matrix, zeidel_vector)

    # print(f"\n\nРозширена матриця, яку треба розв'язати методом Зейделя:")
    # print_matrix(zeidel)
    # zeidel_result=zeidel_method(zeidel_matrix, zeidel_vector, error)
    # print("\nРезультати розв'язання:")
    # print(zeidel_result)

    # def getMaxElementInColumn(matrix: list, col_ind: int) -> int:
    #     col = []
    #     for row in matrix:
    #         col.append(row[col_ind])
    #     max_num_in_col = float('-inf')
    #     for row_num in range(col_ind, len(matrix)):
    #         if max_num_in_col < col[row_num]:
    #             max_num_in_col = col[row_num]

    #     if max_num_in_col == 0:
    #         raise ValueError("Система не має єдиного розв'язку.")
    #     max_num_in_col_ind = col.index(max_num_in_col)

    #     return max_num_in_col_ind, max_num_in_col

    # max_num_in_col_ind, max_num_in_col = getMaxElementInColumn(
    #     ext_matrix, col_ind)
