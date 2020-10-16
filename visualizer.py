from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
import random
from PathfindingViualizer import run

#' Heap sort
def heapify(lst,i,n):
    l = (2 * i) + 1
    r = (2 * i) + 2
    largest = i
    if(l < n and lst[l] > lst[largest]):
        largest = l

    if(r < n and lst[r] > lst[largest]):
        largest = r

    if(largest != i):
        lst[i],lst[largest] = lst[largest],lst[i]
        yield lst
        yield from heapify(lst,largest,n)
    yield lst

def heap_sort(lst,n):
    for i in range((n//2)-1,-1,-1):
        yield from heapify(lst,i,n)

    for i in range(n - 1,-1,-1):
        lst[i],lst[0] = lst[0],lst[i]
        yield lst
        yield from heapify(lst,0,i)


#' Insertion Sort
def insertion_sort(lst,n):
    for i in range(1,n):
        m = lst[i]
        j = i - 1
        while j >= 0 and m < lst[j]:
            lst[j + 1] = lst[j]
            j -= 1
        lst[j + 1] = m
        yield(lst)


#' Merge Sort
def merge(lst,m,r,l):
    lenn1,lenn2 = m-l+1,r-m
    leftarr, rightarr = [],[]

    for i in range(0,lenn1):
        leftarr.append(lst[l+i])
    for j in range(0,lenn2):
        rightarr.append(lst[m+1+j])

    i,j,k  = 0,0,l
    while(i < lenn1 and j < lenn2):
        if(leftarr[i] <= rightarr[j]):
            lst[k] = leftarr[i]
            i += 1
        else:
            lst[k] = rightarr[j]
            j += 1
        k += 1
        yield lst

    while(i < lenn1):
        lst[k] = leftarr[i]
        k += 1
        i += 1

    while(j < lenn2):
        lst[k] = rightarr[j]
        k += 1
        j += 1


def merge_sort(lst,l,r):
    if(l < r):
        m = (l + r) // 2
        yield from merge_sort(lst,l,m)
        yield from merge_sort(lst,m+1,r)
        yield from merge(lst,m,r,l)
    yield lst

#' Quick Sort
def partition(lst,l,h):
    pivot = lst[h]
    i,j = l - 1,0
    for j in range(l,h):
        if lst[j] < pivot:
            i = i + 1
            lst[i],lst[j] = lst[j],lst[i]
        yield lst
    lst[i + 1],lst[h] = lst[h],lst[i + 1]
    return (i + 1)

def quick_sort(lst,l,h):
    if(l < h):
        pi = yield from partition(lst,l,h)
        yield from quick_sort(lst,l,pi - 1)
        yield from quick_sort(lst,pi + 1,h)
    yield lst

#'Bubble_sort
def bubble_sort(n,lst):
    for i in range(n):
        for j in range(n- i - 1):
            if(lst[j] > lst[j + 1]):
                lst[j],lst[j + 1] = lst[j + 1],lst[j]
            yield lst


#'Selection sort
def selection_sort(lst,n):
    for i in range(n):
        min = i
        for j in range(i + 1,n):
            if(lst[min] > lst[j]):
                lst[min],lst[j] = lst[j],lst[min]
            yield(lst)

if __name__ == '__main__':
    print('Menu\n'
          '1)To Visualize Sorting\n'
          '2)To Visualize Searching\n'
          '3)To Visualize Path-Finding Algorithms')
    ch = int(input('Enter your choice:'))
    if(ch == 1):
        print("1)To visualize individually\n"
              "2)To Comapare the Visualization\n"
              "3)Exit")
        ch = int(input('Enter your choice:'))
        if(ch==1):

            n = int(input('Enter the number of integer in list (b\w) 100 - 300 (recommended): '))
            title = ''
            a = [x + 1 for x in range(n)]
            random.shuffle(a)

            print("1)Bubble Sort\n"
                   "2)Insertion Sort\n"
                   "3)Selection Sort\n"
                   "4)Merge Sort\n"
                   "5)Quick Sort\n"
                   "6)Heap Sort: ")
            method = input('Enter your choice:')
            if method == '1':
                title = 'Bubble Sort'
                g = bubble_sort(n, a)

            elif method == '2':
                title = 'Insertion Sort'
                g = insertion_sort(a, n)

            elif method == '3':
                title = 'Selection Sort'
                g = selection_sort(a, n)

            elif method == '4':
                title = 'Merge Sort'
                g = merge_sort(a, 0, n - 1)

            elif method == '5':
                title = 'Quick Sort'
                g = quick_sort(a, 0, n - 1)

            elif method == '6':
                title = 'Heap Sort'
                g = heap_sort(a, n)

            else:
                exit(0)

            fig, ax = plt.subplots()
            ax.set_title(title)

            plt_bar = ax.bar(range(len(a)), a, align='edge') #' bar plot returns list of bars
            ax.set_xlim(0,n)
            ax.set_ylim(0, int(1.07 * n))

            text = ax.text(0.02, 0.95, "", transform=ax.transAxes)
            iteration = [0]

            #' Main code
            #' The below code is continuously called by the funcanimation
            def update_fig(g, bars, iteration): #' Instead of a we can use any var name but it will instanciated as new variable
                for bar, val in zip(bars, g):
                    bar.set_height(val)
                iteration[0] += 1
                text.set_text('No. of iterations: {}'.format(iteration))

            anim = FuncAnimation(fig, func=update_fig, fargs=(plt_bar, iteration), frames = g ,interval=1,
                                 repeat=False)
            plt.show()

        elif(ch == 2):
            n = int(input('Enter the number of integer in list (b\w) 100 - 300 (recommended): '))
            b = []
            title = ''
            title1 = ''
            a = [x + 1 for x in range(n)]
            random.shuffle(a)
            for ele in a:
                b.append(ele)

            print("choose 1 algorithm\n"
                    "1)Bubble Sort\n"
                    "2)Insertion Sort\n"
                    "3)Selection Sort\n"
                    "4)Merge Sort\n"
                    "5)Quick Sort\n"
                    "6)Heap Sort: ")
            method1 = input('Enter your choice:')

            if method1 == '1':
                title = 'Bubble Sort'
                g1 = bubble_sort(n, a)

            elif method1 == '2':
                title = 'Insertion Sort'
                g1 = insertion_sort(a, n)

            elif method1 == '3':
                title = 'Selection Sort'
                g1 = selection_sort(a, n)

            elif method1 == '4':
                title = 'Merge Sort'
                g1 = merge_sort(a, 0, n - 1)

            elif method1 == '5':
                title = 'Quick Sort'
                g1 = quick_sort(a, 0, n - 1)

            elif method1 == '6':
                title = 'Heap Sort'
                g1 = heap_sort(a, n)

            else:
                exit(0)

            print("choose 2 algorithm\n"
                    "1)Bubble Sort\n"
                    "2)Insertion Sort\n"
                    "3)Selection Sort\n"
                    "4)Merge Sort\n"
                    "5)Quick Sort\n"
                    "6)Heap Sort: ")
            method2 = input('Enter your choice:')

            if method2 == '1':
                title1 = 'Bubble Sort'
                g2 = bubble_sort(n, b)

            elif method2 == '2':
                title1 = 'Insertion Sort'
                g2 = insertion_sort(b, n)

            elif method2 == '3':
                title1 = 'Selection Sort'
                g2 = selection_sort(b, n)

            elif method2 == '4':
                title1 = 'Merge Sort'
                g2 = merge_sort(b, 0, n - 1)

            elif method2 == '5':
                title1 = 'Quick Sort'
                g2 = quick_sort(b, 0, n - 1)

            elif method2 == '6':
                title1 = 'Heap Sort'
                g2 = heap_sort(b, n)

            else:
                exit(0)

            fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, sharex=True)
            ax1.set_title(title)
            ax2.set_title(title1)
            plt_bar1 = ax1.bar(range(len(a)), a, align='edge')  # ' bar plot returns list of bars
            plt_bar2 = ax2.bar(range(len(b)), b, align='edge')
            ax1.set_xlim(0, n)
            ax1.set_ylim(0, int(1.07 * n))
            ax2.set_xlim(0, n)
            ax2.set_ylim(0, int(1.07 * n))

            text1 = ax1.text(0.02, 0.90, "", transform=ax1.transAxes)
            text2 = ax2.text(0.02, 0.90, "", transform=ax2.transAxes)
            iteration1 = [0]
            iteration2 = [0]

            def update_fig1(g1, bar1,iteration1):
                for bar, val in zip(bar1, g1):
                    bar.set_height(val)
                iteration1[0] += 1
                text1.set_text('No. of iterations: {}'.format(iteration1))

            def update_fig2(g2, bar2,iteration2):
                for bar, val in zip(bar2, g2):
                    bar.set_height(val)
                iteration2[0] += 1
                text2.set_text('No. of iterations: {}'.format(iteration2))

            anim2 = FuncAnimation(fig, func=update_fig2, fargs=(plt_bar2, iteration2), frames=g2, interval=1, repeat=False)
            anim1 = FuncAnimation(fig, func=update_fig1, fargs=(plt_bar1, iteration1), frames=g1, interval=1, repeat=False)
            plt.show()

        else:
            exit()

    elif(ch == 2):
        print('Menu\n'
              '1)Linear Search\n'
              '2)Binary Search')

        ch = int(input('Enter your choice: '))
        if(ch == 1):
            n = int(input('Enter the number of integers: '))
            a = [x + 1 for x in range(n)]
            random.shuffle(a)
            key = int(input('Enter the key to be searched: '))
            fig, ax1 = plt.subplots()
            plt_bar = ax1.bar(range(len(a)),a, align='edge',color='#4666FF')
            ax1.set_xlim(0, n)
            ax1.set_ylim(0, int(1.07 * n))
            ax1.set_title('Linear Search (Sorted/Unsorted List)')
            i = [0]

            def update_fig(plt_bar):
                if(i[0] >= 1):
                    r = plt.Rectangle(xy=(i[0] - 1,0), width=0.8, height= a[i[0] - 1], fc = '#4666FF')
                    ax1.add_patch(r)
                r = plt.Rectangle(xy=(i[0],0), width=0.8, height= a[i[0]], fc = 'red')
                ax1.add_patch(r)
                if(a[i[0]] == key):
                    r = plt.Rectangle(xy=(i[0],0), width=0.8, height= a[i[0]], fc = 'green')
                    ax1.add_patch(r)
                    return
                i[0] += 1

            anim = FuncAnimation(fig, func=update_fig ,frames=plt_bar, interval=100)

            plt.show()

        elif(ch == 2):
            n = int(input('Enter the number of integers: '))
            a = [x + 1 for x in range(n)]
            l,r = [0], [n - 1]
            key = int(input('Enter the key to be searched: '))
            fig, ax1 = plt.subplots()
            plt_bar = ax1.bar(range(len(a)),a, align='edge',color='#4666FF')
            ax1.set_title('Binary Search (Sorted Lists only)')
            def update_fig(plt_bar):
                mid = (l[0]+r[0])//2
                if(mid == key):
                    p = plt.Rectangle(xy=(mid,0), width=0.8, height=a[mid], color='green')
                    ax1.add_patch(p)
                    return
                elif(mid > key):
                    p = plt.Rectangle(xy=(mid,0), width=0.8, height=a[mid], color='red')
                    ax1.add_patch(p)
                    r[0] = mid
                else:
                    p = plt.Rectangle(xy=(mid,0), width=0.8, height=a[mid], color='red')
                    ax1.add_patch(p)
                    l[0] = mid

            anim = FuncAnimation(fig, func=update_fig ,frames=plt_bar, interval=700, repeat=False)

            plt.show()

        else:
            exit()

    elif(ch == 3):
        run()

    else:
        exit()
