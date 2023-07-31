def solveSudoku(board):
    """
    解数独 抄的力扣题解啊
    https://leetcode.cn/problems/sudoku-solver/solutions/414120/jie-shu-du-by-leetcode-solution/
    :param board: 二维数组,数字或者留空的.
    :return: 解好的二维数组
    """

    def dfs(pos: int):
        nonlocal valid
        if pos == len(spaces):
            # 遍历完了
            valid = True
            return

        i, j = spaces[pos]
        for digit in range(9):
            # 从0遍历到8也就是 1-9
            if line[i][digit] == column[j][digit] == block[i // 3][j // 3][digit] == False:
                # 如果这个格子可以填入digit
                line[i][digit] = column[j][digit] = block[i // 3][j // 3][digit] = True
                board[i][j] = str(digit + 1)
                # 那么就填入
                dfs(pos + 1)
                # 递归查找下一位
                line[i][digit] = column[j][digit] = block[i // 3][j // 3][digit] = False
                # 回溯到当前递归层时要把这个重置为false
            if valid:
                return

    line = [[False] * 9 for _ in range(9)]
    column = [[False] * 9 for _ in range(9)]
    block = [[[False] * 9 for _a in range(3)] for _b in range(3)]
    valid = False
    spaces = list()

    for i in range(9):
        for j in range(9):
            if board[i][j] == ".":
                spaces.append((i, j))
                # 空白格加入 spaces
            else:
                digit = int(board[i][j]) - 1
                line[i][digit] = column[j][digit] = block[i // 3][j // 3][digit] = True
                # 说明第i行 第j列和ij所对应的格子已经有这个数字了
    dfs(0)
    return board
