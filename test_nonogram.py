import matplotlib.pyplot as plt

# -----------------------------
# 完全解探索関数（先ほどと同じ）
# -----------------------------
def generate_line_possibilities(length, hints):
    if not hints:
        return [[0]*length]
    total_blocks = sum(hints) + len(hints)-1
    if total_blocks > length:
        return []

    spaces = length - sum(hints)
    def distribute_spaces(spaces, n):
        if n == 1:
            yield [spaces]
        else:
            for i in range(spaces+1):
                for rest in distribute_spaces(spaces-i, n-1):
                    yield [i] + rest

    possibilities = []
    for distribution in distribute_spaces(spaces, len(hints)+1):
        line = []
        for pre, block in zip(distribution, hints + [0]):
            line.extend([0]*pre)
            line.extend([1]*block)
        line = line[:length]
        possibilities.append(line)
    return possibilities

def is_valid(solution, col_possibilities):
    for c_idx, col_opts in enumerate(col_possibilities):
        col_so_far = [row[c_idx] for row in solution]
        if not any(opt[:len(col_so_far)] == col_so_far for opt in col_opts):
            return False
    return True

def solve_nonogram_bt(row_hints, col_hints):
    rows, cols = len(row_hints), len(col_hints)
    row_possibilities = [generate_line_possibilities(cols, h) for h in row_hints]
    col_possibilities = [generate_line_possibilities(rows, h) for h in col_hints]

    solution = []
    def backtrack(r):
        if r == rows:
            return True
        for possibility in row_possibilities[r]:
            solution.append(possibility)
            if is_valid(solution, col_possibilities):
                if backtrack(r+1):
                    return True
            solution.pop()
        return False

    if backtrack(0):
        return solution
    else:
        return None

# -----------------------------
# 可視化
# -----------------------------
def visualize_solution(solution):
    plt.figure(figsize=(6,6))
    plt.imshow(solution, cmap='Greys', interpolation='none')
    plt.xticks(range(len(solution[0])))
    plt.yticks(range(len(solution)))
    plt.gca().invert_yaxis()
    plt.show()

# -----------------------------
# ダミーデータ（15x15テスト用）
# -----------------------------
if __name__ == "__main__":
    row_hints = [[1],[3],[5],[7],[8],[8],[8],[9],[10],[11],[11,2],[2,6,1,1],[5,1],[2,1],[2]]
    col_hints = [[3],[5],[3,3],[6,1],[7],[7],[8],[8],[9],[8,1],[11],[8],[5,1],[4,2],[4]]

    solution = solve_nonogram_bt(row_hints, col_hints)

    if solution:
        visualize_solution(solution)
    else:
        print("解は見つかりませんでした")
