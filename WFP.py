"""
功能:网格初始化
参数:d表示矩阵的大小
m是行数，n是列数
"""
def InitGrid(m,n):
    grid = [[0 for y in range(n)] for x in range(m)]#利用列表推导式初始化网格
    return grid                         #返回初始化的网格

"""
功能:指定行过滤出可选位置并随机选取一个，作为"警卫"的填入位置
参数: 
    grid:网格矩阵
    count:记录网格中已经被警戒的数量
    finallcount:作为结束回溯的的判断
"""
def fill(grid ,count,finallcount):
    for i in range(len(grid)):
        if (i-2>=0):#剪枝，将可以判断为死解的选择剪掉
            for j in range(len(grid[0])):
                if grid[i-2][j]==0:
                    return
        for j in range(len(grid[0])):
            if (judge(grid,i,j)):#判断是否可以放警卫
                grid[i][j] = 2
                count = count + 1 + monitors(grid,i,j,1)
                if count==len(grid)*len(grid[0]):
                    finallcount.append(count)
                    return
                fill(grid,count,finallcount)
                try:
                    if finallcount[0]==len(grid)*len(grid[0]):
                        return
                except:pass
                grid[i][j] = 0
                count = count - 1 - monitors(grid,i,j,0)

"""
功能:计算一个警卫监视了几个房间,回溯时将房间移除监视
参数:
    grid:网格矩阵
    i,j:房间所在行列数
    gruad:判断是计入监视还是移除监视
"""
def monitors(grid,i,j,gruad):
    num = 0
    if (i - 1 >= 0):
        grid[i - 1][j] = gruad
        num = num+1
    if (i + 1 < len(grid)):
        grid[i + 1][j] = gruad
        num = num+1
    if (j - 1 >= 0):
        grid[i][j-1] = gruad
        num = num+1
    if (j + 1 < len(grid[0])):
        grid[i][j+1] = gruad
        num = num+1
    return num

"""
功能:判断该房间是否可以放警卫
参数:
    grid:网格矩阵
    i,j:房间所在行列数
"""
def judge(grid,i,j):
    judge = 0
    if (i - 1 < 0 or grid[i - 1][j] == 0):
        judge = judge + 1
    if (i + 1 >= len(grid) or grid[i + 1][j] == 0):
        judge = judge + 1
    if (j - 1 < 0 or grid[i][j - 1] == 0):
        judge = judge + 1
    if (j + 1 >= len(grid[0]) or grid[i][j+1] == 0):
        judge = judge + 1
    if judge == 4:
        return True
    else:return False


"""
功能:根据最终结果用网格展示出来
参数:grid:网格矩阵
"""
def show(grid):
    figure = ''#初始化
    for row in range(len(grid)):#遍历行
        for line in range(len(grid)):#遍历列
            if grid[row][line] ==2:#判断行列在可选位置上
                figure += 'R '#就在网格中添加R(表示警卫)
            else: figure += '■ '#就在网格中添加方块■
        figure += '\n'#遍历n列之后再换行遍历
    return figure#返回网格

if __name__ == '__main__':
    m=4
    n=4
    if m<n:
        p = m
        m = n
        n = p
    count=0
    finallcount=[]
    grid = InitGrid(m,n)#初始化mXn网格
    if (m>=5 and n>=3):print("No Solution!")
    else:
        if n==2:
            if m % 2 == 0:print("No Solution!")
            else:
                fill(grid,count,finallcount)
        elif m == 3 and n == 3:print("No Solution!")
        elif m == 4 and n == 3:print("No Solution!")
        else:
            fill(grid,count,finallcount)
            print("Finallgrid:",grid)
        print(show(grid))# 调用show()函数展示出网格
