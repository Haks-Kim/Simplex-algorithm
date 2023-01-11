import numpy as np
import copy
import matplotlib.pyplot as plt

def solve_LP(A, b, c):
    # Auxiliary Problem for Phase1 simplex
    (m, n) = A.shape

    for i in range(m):
        if b[i] < 0:
            A[i, :] = -A[i, :]
            b[i] = -b[i]

    I = np.identity(m)
    W = np.hstack([A, I])
    d = np.hstack([np.zeros(n), np.ones(m)])
    z = np.hstack([np.zeros(n), b])
    B_inv = I
    idx_B = [i for i in range(n, m + n)]

    # Phase 1 problem
    LP1 = Simplex(W, b, d, z, B_inv, idx_B)
    LP1.perform_simplex()

    if round(LP1.cost, 9) != 0:
        LP1.state = 'Infeasible'  # and then terminated'
        LP1.display_status(1)
        return (LP1, None)

    else:
        LP1.drive_out_artificial_variable()

        LP2 = Simplex(LP1.A[:, :n], LP1.b, c, LP1.solution[:n], LP1.B_inv, LP1.idx_B)
        LP2.perform_simplex()
        LP1.display_status(1)
        LP2.display_status(2)
        return (LP1, LP2)


class Simplex:
    def __init__(self, A, b, c, x, B_inv, idx_B):
        # input관련 변수
        self.A = A
        self.A_initial = A
        self.b = b
        self.c = c
        self.x = x
        (self.m, self.n) = self.A.shape
        (self.m_initial,_) = self.A.shape

        # iteration관련 변수
        self.B_inv = B_inv
        self.idx_B = idx_B
        self.idx_N = None
        self.u = None
        self.theta = None

        # result와 관련된 state 변수.
        self.state = "Proceeding"
        self.solution = None
        self.cost = None
        self.solution_trace = [x]
        self.idx_B_trace = [copy.deepcopy(idx_B)]
        self.drive_out_specification = list()

    def reduce_row(self):
        NotImplementedError()

    def perform_simplex(self):
        A = self.A
        b = self.b
        c = self.c

        while True:
            # -----------------------
            # step1 : Initialization
            # -----------------------
            c_B = c[self.idx_B]
            p = (c_B.T @ self.B_inv)
            self.idx_N = set([i for i in range(self.n)]) - set(self.idx_B)  # nonbasic index update

            # -------------------------------------------
            # step2 : Termination - Optimality condition
            # -------------------------------------------
            idx_neg_rc = set()  # indices of negative reduced costs for pivoting
            c_reduced = np.zeros(self.n)
            for i in self.idx_N:
                c_reduced[i] = np.round(c[i] - p.T @ A[:, i],9)

                if c_reduced[i] < 0:
                    idx_neg_rc.add(i)
                    j = i
                    break

            if len(idx_neg_rc) == 0:
                self.state = 'Optimal'
                self.solution = self.x
                self.cost = c @ self.x
                break

            # ----------------------------------------------
            # step3 : Termination - Unboundedness condition
            # ----------------------------------------------
            self.u = self.B_inv @ A[:, j]

            test = 0
            for i in range(self.m):
                test += (self.u[i] <= 0)
                if test == 0:
                    break

            if test == self.m:
                self.state = 'Unbounded'
                break

            # ----------------
            # step4: stepsize
            # ----------------
            self.theta = np.inf
            l = None  # l : exiting variable(basic -> nonbasic)
            theta_list = np.inf * np.ones(self.m)
            for i in range(self.m):
                if self.u[i] > 0:
                    theta_list[i] = self.x[self.idx_B[i]] / self.u[i]

            self.theta = np.min(theta_list)
            for i in range(self.m):
                if theta_list[i] == self.theta:  # 이 안에 smallest subscript rule이 내포됨.
                    if l == None:
                        l = i
                    else:
                        if self.idx_B[i] < self.idx_B[l]:
                            l = i

            # ----------------
            # step5,6: update
            # ----------------
            self.enter_exit_variable(j, l)

    def enter_exit_variable(self, j, l):  # entering idx : j / exiting row idx : l
        self.idx_B[l] = j  # Basic index update
        self.idx_N = set([i for i in range(self.n)]) - set(self.idx_B)  # Nonbasic index update

        # Move to adjacent New BFS
        y = np.zeros(self.n)
        for i in range(self.m):
            if i == l:
                y[self.idx_B[i]] = self.theta
            else:
                y[self.idx_B[i]] = self.x[self.idx_B[i]] - self.theta * self.u[i]
        self.x = y
        self.idx_B_trace.append(copy.deepcopy(self.idx_B))
        self.solution_trace.append(self.x)

        # This is keypoint : Update date B_inv using information. Don't calculate inverse of B directly.
        Q = np.identity(self.m)
        for i in range(self.m):
            if i == l:
                Q[l, l] = 1 / self.u[l]
            else:
                Q[i, l] = -self.u[i] / self.u[l]

        self.B_inv = Q @ self.B_inv

    def drive_out_artificial_variable(self):  # exception error를 추가해야함.
        self.theta = 0
        while len(set(self.idx_B) - set([i for i in range(self.n - self.m)])) != 0:
            artificial_idx_B = min(set(self.idx_B) - set([i for i in range(self.m)]))
            candidate_idx_B = min(set([i for i in range(self.m)]) - set(self.idx_B))

            ((idx,),) = np.where(np.array(self.idx_B) == artificial_idx_B)

            test = 0
            for i in range(self.n - self.m_initial):
                test += ( np.round(self.B_inv[idx, :] @ self.A_initial[:, i],9) != 0)
                if test > 0:
                    break

            if test == 0:
                self.A = self.A[[i for i in range(self.m) if i != idx], :]
                self.b = self.b[[i for i in range(self.m) if i != idx]]
                self.m = self.m - 1
                self.idx_B.remove(artificial_idx_B)
                print("Redundant row {} was eliminated!".format(copy.deepcopy(idx)))
                self.drive_out_specification.append("Redundant row {} was eliminated!".format(idx))

            else:
                self.idx_B[idx] = candidate_idx_B  # Basic index update
                self.drive_out_specification.append("Artifitial basis was driven out : {0} -> {1}".format(artificial_idx_B,candidate_idx_B))

        self.B_inv = np.linalg.inv(self.A[:, self.idx_B])

    def display_status(self, phase):
        if self.state == "Optimal":
            print("[Phase_{}] - result".format(phase))
            print("----------------------")
            print("State    : {0} \nSolution : {1} \nCost     : {2} \nIteration : {3}".format(self.state, np.round(self.solution,3),
                                                                            np.round(self.cost,3),len(self.solution_trace) ))
            print("----------------------")

        if self.state != "Optimal":
            print("[Phase_{}] - result".format(phase))
            print("----------------------")
            print("State    : {0} ".format(self.state))
            print("----------------------")

        if phase == 1:
            for i in self.drive_out_specification:
                print(i)
            print("\n")

    def calc_degeneracy_ratio(self):
        num_zeros = list()
        cost_trace = list()

        for i in self.solution_trace:
            cost_trace.append(self.c@i)

        improvements = [cost_trace[i]-cost_trace[i+1] for i in range(len(cost_trace)-1)]
        num_zero_improvements = np.sum(np.array(improvements)==0)
        return(num_zero_improvements/len(improvements))

    def plot_stepsize_trace(self):
        stepsize_trace = list()
        for i in range(len(self.solution_trace)-1):
            stepsize_trace.append(np.linalg.norm(self.solution_trace[i]-self.solution_trace[i+1]))

        plt.plot(stepsize_trace)
        plt.title("Stepsize trace")
        plt.show()

    def plot_cost_trace(self):
        cost_trace = list()
        for i in self.solution_trace:
            cost_trace.append(self.c@i)

        plt.plot(cost_trace)
        plt.title("Cost trace")
        plt.show()

    def plot_result(self):
        fig, ax = plt.subplots(2,2,figsize=(12,12))

        stepsize_trace = list()
        cost_trace = list()
        for i in range(len(self.solution_trace)-1):
            stepsize_trace.append(np.linalg.norm(self.solution_trace[i]-self.solution_trace[i+1]))
        for i in self.solution_trace:
            cost_trace.append(self.c @ i)

        plt.plot(cost_trace)
        plt.title("Cost trace")
        plt.show()




