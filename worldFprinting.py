import random  #导入随机模块
import math    #导入数学模块
"""
功能：网格初始化
参数：d表示矩阵的大小
m是行数，n是列数
"""

def InitGrid(m,n):
    grid = [[(x + 1, y + 1) for y in range(n)] for x in range(m)]#利用列表推导式初始化网格
    return grid                         #返回初始化的网格

"""
功能：指定行过滤出可选位置并随机选取一个，作为"警卫"的填入位置
参数： grid：网格矩阵
      rowIndex: 指定矩阵的某一行的序号
      position：已被选的位置
      wrongpoints: 回溯时的排除项列表
"""
def r2(x1, y1, x2, y2):
    r = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
    return r

def resetgrid(pick,gird,backlist):#方便在出现死解时还原表格
    data = []
    data.append((pick[0], pick[1], gird[pick[0]][pick[1]]))
    gird[pick[0]][pick[1]] = (0, 0)
    if (pick[0] - 1 >= 0):
        data.append((pick[0] - 1,pick[1],gird[pick[0] - 1][pick[1]]))
        gird[pick[0] - 1][pick[1]] = (0, 0)  # 上1
        if (pick[1] - 1 >= 0):  # 上1左
            if gird[pick[0] - 1][pick[1] - 1] == (0, 0):pass
            else:
                data.append((pick[0] - 1,pick[1] - 1,gird[pick[0] - 1][pick[1] - 1]))
                gird[pick[0] - 1][pick[1] - 1] = (-1, -1)
        try:  # 上1右
            if gird[pick[0] - 1][pick[1] + 1] == (0, 0):pass
            else:
                data.append((pick[0] - 1,pick[1] + 1,gird[pick[0] - 1][pick[1] + 1]))
                gird[pick[0] - 1][pick[1] + 1] = (-1, -1)
        except:pass
    if (pick[0] - 2 >= 0):  # 上2
        if gird[pick[0] - 2][pick[1]] == (0, 0):pass
        else:
            data.append((pick[0] - 2,pick[1],gird[pick[0] - 2][pick[1]]))
            gird[pick[0] - 2][pick[1]] = (-1, -1)
    try:  # 下1
        data.append((pick[0] + 1,pick[1],gird[pick[0] + 1][pick[1]]))
        gird[pick[0] + 1][pick[1]] = (0, 0)
        try:  # 下1右
            if gird[pick[0] + 1][pick[1] + 1] == (0, 0):pass
            else:
                data.append((pick[0] + 1,pick[1] + 1,gird[pick[0] + 1][pick[1] + 1]))
                gird[pick[0] + 1][pick[1] + 1] = (-1, -1)
        except:pass
    except:pass
    try:  # 下2
        if gird[pick[0] + 2][pick[1]] == (0, 0):pass
        else:
            data.append((pick[0] + 2,pick[1],gird[pick[0] + 2][pick[1]]))
            gird[pick[0] + 2][pick[1]] = (-1, -1)
    except:pass
    if (pick[1] - 1 >= 0):
        data.append((pick[0],pick[1] - 1,gird[pick[0]][pick[1] - 1]))
        gird[pick[0]][pick[1] - 1] = (0, 0)  # 左1
        try:  # 下1左
            if gird[pick[0] + 1][pick[1] - 1] == (0, 0):pass
            else:
                data.append((pick[0] + 1,pick[1] - 1,gird[pick[0] + 1][pick[1] - 1]))
                gird[pick[0] + 1][pick[1] - 1] = (-1, -1)
        except:pass
    if (pick[1] - 2 >= 0):  # 左2
        if gird[pick[0]][pick[1] - 2] == (0, 0):pass
        else:
            data.append((pick[0],pick[1] - 2,gird[pick[0]][pick[1] - 2]))
            gird[pick[0]][pick[1] - 2] = (-1, -1)
    try:# 右1
        data.append((pick[0],pick[1]+1,gird[pick[0]][pick[1] + 1]))
        gird[pick[0]][pick[1] + 1] = (0, 0)
    except:pass
    try:  # 右2
        if gird[pick[0]][pick[1] + 2] == (0, 0):pass
        else:
            data.append((pick[0],pick[1] + 2,gird[pick[0]][pick[1] + 2]))
            gird[pick[0]][pick[1] + 2] = (-1, -1)
    except:pass
    backlist.append(data)

def fill(grid, rowIndex, position, wrongpoints,backlist,backdepth):
    row = grid[rowIndex]  # 取到某行
    optional = []  # 在后续过程中保存本行过滤完的可选位置
    for column in row:  # 遍历本行的每一项
        available = False  # 这个变量标志了该位置是否可用，初始化的时候是True，可用
        if len(position)==0:available = True
        for item in position:  # 遍历已被选的位置 #不能选择已经在警戒范围内的点，满足在任意一条边上，即可选取该点
            if (column[0] != 0 and r2(column[0], column[1], item[0], item[1]) <= 3) and \
                    (column[0] + column[1] == item[0] - 3 + item[1] or column[0] + column[1] == item[0] + 3 + item[1] or column[0] - column[1] == item[0] + 3 - item[1] or column[0] - column[1] == item[0] - 3 - item[1]):
                available = True
        if column[0] == -1 : available = False    # 不能被标记为无法使用
        if column in wrongpoints: available = False  # 不能在死解里面
        if available:  # 该位置可用，添加进可用项列表里
            optional.append(column)

    # 随机挑选位置点，之后判断是否为死解，若为死解返回0
    randomIndex = math.floor(len(optional) * random.random())  # 随机位置点
    if len(optional) != 0:
        pick = optional[randomIndex]  # 挑选位置
        # print("本次wrongpoints:", wrongpoints)
        # print("本次可用点:", pick)
        position.append(pick)  # 把这个位置点添加到可选位置的列表中
        # print("本次position:", position)
        backdepth[rowIndex].append(pick+(len(backdepth[rowIndex])+1,))
        pick = (pick[0]-1,pick[1]-1)
        resetgrid(pick, grid,backlist)
    # else:
    #     print("本次position:", position)
    #     print("第",rowIndex+1,"行无可用点!")
    '''判断是否出现死解'''
    if rowIndex >= 1 :  # 当第n行填完后，发现第n-1行还有未被看守的点，则出现死解
        a = 0
        for i in range(n):
            a = a + sum(gird[rowIndex - 1][i])
        if (a != 0):
            return 0,rowIndex
    if rowIndex == m-1:  # 当最后一行填完后，发现最后一行还有未被看守的点，则出现死解
        a = 0
        for i in range(n):
            a = a + sum(gird[rowIndex][i])
        if (a != 0):
            return 0,rowIndex
    '''判断是否进入下一行，并且是否出现死解'''
    axis_h = 0
    b = []
    for i in range(n):
        if sum(gird[rowIndex][i]) < 0:  # 若该位置为死解,则视为已经标记过了
            b.append(gird[rowIndex][i])
            axis_h = axis_h + 0
        else:
            axis_h = axis_h + sum(gird[rowIndex][i])
    if axis_h > 0:  # 若这一行还有位置没被标记过，则继续在这一行寻找
        row = rowIndex
    else:  # 若这一行全标记完了，则前往下一行
        row = rowIndex+1
    return 1,row

#(-1, -1)代表无法使用，(0, 0)代表已经被守卫勘察

def trace(m,n,gird, row, position, wrongpoints,backlist,backdepth,backtracking):
    while row < m:#循环m行
        # print("============================开始=============================")
        success,row = fill(gird, row, position, wrongpoints[row],backlist,backdepth)#调用fill()函数填入皇后
        if success == 0:# 死解
            # print("~~~~~~~~~~~~~~~~本次死解开始~~~~~~~~~~~~~~~~~")
            if len(position)!=0:
                if position[-1][0] != row+1: # 若不相等，则这一行没有解，死解发生在上一行,否则死解发生在这一行，不用退回
                    row = position[-1][0]-1  # 回退到死解所在行
                deadpoint = position.pop()    # 去掉死解的点
                # print("Position changed:",position)
                deadbackdepth = backdepth[row].pop()
                tracelist = backlist.pop()
                for i in tracelist: # 将死解的点所影响的点还原
                    if len(i)>2:
                        gird[i[0]][i[1]]=i[-1]
                    else:
                        gird[i[0]][i[1]]=i[-1]
                gird[deadpoint[0] - 1][deadpoint[1] - 1] = (-1, -1)  # 在网格中标记死解
                wrongpoints[row].append(deadpoint)  # 将死解的点存入排除项中
                backtracking[row].append(deadbackdepth)
                if len(wrongpoints[row]) > 1:
                    if deadbackdepth[-1] < backtracking[row][-2][2]:
                        if backtracking[row][0][1] == 1:
                            pass
                        else:
                            backtracking[row] = backtracking[row][-1:]
                            for i in wrongpoints[row][:-1]:  # 将标记死解的点还原
                                gird[i[0] - 1][i[1] - 1] = i
                            wrongpoints[row] = wrongpoints[row][-1:]  # 当前一个位置的点重新选取时，后面的排除项就没有意义了，清空
                # print("~~~~~~~~~~~~~~~~~本次死解结束~~~~~~~~~~~~~~~~~")
"""
功能：根据最终结果用网格展示出来
参数：positions: 最终挑选的位置列表
"""
def show(positions,m,n):
    figure = ''#初始化
    for row in range(m):#遍历行
        for line in range(n):#遍历列
            if (row + 1, line + 1) in positions:#判断行列在可选位置上
                figure += 'R '#就在网格中添加R(表示警卫)
            else: figure += '■ '#就在网格中添加方块■
        figure += '\n'#遍历4列之后再换行遍历
    return figure#返回网格

if __name__ == '__main__':
    m=4
    n=4
    if m<n:
        p = m
        m = n
        n = p
    gird = InitGrid(m,n)#初始化mXn网格
    position = []#保存本行过滤完的可选位置的列表
    backdepth = [[] for i in range(m)]
    backtracking = [[] for i in range(m)]
    wrongpoints = [[] for i in range(m)]#回溯mXn网格的列表
    backlist = []
    row = 0#行
    if (m>=5 and n>=3):print("No Solution!")
    else:
        if n==2:
            if m % 2 == 0:print("No Solution!")
            else:
                trace(m, n, gird, row, position, wrongpoints, backlist,backdepth,backtracking)
                print("Finallgird:",gird)
                print("Finallposition:",position)
        elif m == 3 and n == 3:print("No Solution!")
        elif m == 4 and n == 3:print("No Solution!")
        else:
            trace(m, n, gird, row, position, wrongpoints, backlist,backdepth,backtracking)
            print("Finallgird:",gird)
            print("Finallposition:",position)
        print(show(position,m,n))# 调用show()函数展示出网格
