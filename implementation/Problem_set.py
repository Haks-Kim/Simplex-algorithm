import numpy as np

def dataset(n):
    '''
    1 : Example3.5 : Standard LP Problem (Feasible)
    2 : Example3.8 : Standard LP Problem (Feasible)
    3 : Exercise 3.17
    4 : Example 5.1
    5 : Example 5.2
    6 : Large-size example
    7,8 : Example in section 3.7
    '''

    # Example3.5 : Standard LP Problem  (OK)
    if n == 1:
        c = np.array([-10,-12,-12,0,0,0])
        A = np.array([[1,2,2,1,0,0],[2,1,2,0,1,0],[2,2,1,0,0,1]])
        b = np.array([20,20,20])
        return((A,b,c))

    # Example3.8 : Standard LP Problem    (OK)
    if n == 2:
        c = np.array([1,1,1,0])
        A = np.array([[1,2,3,0],[-1,2,6,0],[0,4,9,0],[0,0,3,1]])
        b = np.array([3,2,5,1])
        return((A, b, c))

    # Exercise 3.17    (OK -- B_inv 계산시에 roundoff 오차가 조금 발생함)
    if n == 3:
        c = np.array([2,3,3,1,-2])
        A = np.array([[1,3,0,4,1],[1,2,0,-3,1],[-1,-4,3,0,0]])
        b = np.array([2,2,1])
        return((A, b, c))

    # Example 5.1    (OK)
    if n == 4:
        c = np.array([-5,-1,12,0])
        A = np.array([[3,2,1,0],[5,3,0,1]])
        b = np.array([10,16])
        return((A, b, c))

    # Example 5.2
    if n == 5:
        c = np.array([-5,-1,12,0,0])
        A = np.array([[3,2,1,0,0],[5,3,0,1,0],[1,1,0,0,-1]])
        b = np.array([10,16,5])
        return((A, b, c))

    # Big-size instance
    if n == 6:
        (m_, n_)=(100,200)
        c = np.random.randn(n_)
        A = np.random.randn(m_,n_)
        b = np.random.randn(m_)
        return((A,b,c))

    # Section 3.7 Example
    # minimize      -x_{n}
    # subject to    0<=x_{i}<=1
    if n == 7:
        n_ = 10
        c = np.zeros(30)
        c[-1] = -1
        b = np.tile([0, 1], 10)

        for i in range(n_):
            a_row = np.zeros((2,30))
            a_row[0,i] = 1
            a_row[0,i+10] = -1
            a_row[1,i] = 1
            a_row[1,i+20] = 1

            if i == 0:
                A = a_row
            else:
                A = np.vstack([A,a_row])

        return((A,b,c))

    # Section 3.7 Example
    # minimize      -x_{n}
    # subject to    eps<=x_{1}<=1
    #       eps*x_{n-1}<=x_{1}<=1-eps*x_{n-1}
    if n == 8:

        n_ = int(input("Number of variables : "))
        c = np.zeros(3*n_)
        c[n_ -1] = -1

        eps = 0.49
        b = np.tile([0, 1], n_-1)
        b = np.hstack([[eps,1], b])


        for i in range(n_):
            a_row = np.zeros((2, 3*n_))

            if i == 0:
                a_row[0, i] = 1
                a_row[0, i + n_] = -1
                a_row[1, i] = 1
                a_row[1, i + 2*n_] = 1
            else:
                a_row[0,i] = 1
                a_row[0,i-1] = -eps
                a_row[0,i+n_] = -1

                a_row[1,i] = 1
                a_row[1,i-1] = eps
                a_row[1,i+2*n_] = 1

            if i == 0:
                A = a_row
            else:
                A = np.vstack([A,a_row])

        return((A,b,c))

    # Section 3.7 Example
    # minimize      -x_{n}
    # subject to    eps<=x_{1}<=2
    #       eps*x_{n-1}<=x_{1}<=2-eps*x_{n-1}
    if n == 9:

        n_ = int(input("Number of variables : "))
        c = np.zeros(3*n_)
        c[n_ -1] = -1
        eps = 0.99
        b = np.tile([0, 2], n_-1)
        b = np.hstack([[eps,2], b])


        for i in range(n_):
            a_row = np.zeros((2, 3*n_))

            if i == 0:
                a_row[0, i] = 1
                a_row[0, i + n_] = -1
                a_row[1, i] = 1
                a_row[1, i + 2*n_] = 1
            else:
                a_row[0,i] = 1
                a_row[0,i-1] = -eps
                a_row[0,i+n_] = -1

                a_row[1,i] = 1
                a_row[1,i-1] = eps
                a_row[1,i+2*n_] = 1

            if i == 0:
                A = a_row
            else:
                A = np.vstack([A,a_row])

        return((A,b,c))