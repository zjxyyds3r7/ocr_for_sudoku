import os

import pic2list
import solveSudoku

if __name__ == '__main__':
    path = 'Screenshot_2023-07-31-10-35-49-14_e39d2c7de19156b0683cd93e8735f348.jpg'
    img = pic2list.getroi(path)
    l, need = pic2list.roi2list(img, 'en')
    r = solveSudoku.solveSudoku(l)

    for i in r:
        print(' '.join(i))
    pic2list.list2pic(img, r, need)
    os.system('text.jpg')
    # print(r)
    pass

