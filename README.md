# Simplex algorithm
* Implementation of 'two-phase revised simplex method' in **'Introduction to linear optimization' (Bertsimas, Dimitris, and John N. Tsitsiklis)** which was done in August, 2021 as a part of summer LP study. 


### Description
* main.py: choose the problem instance and run the simplex algorithm
* Simplex.py: 'two-phase revised simplex method' in chapter 3 of the above mentioned book
* Problem_set.pu: generation of LP problem instances including examples in the book


### Example
* Example 3.8
\begin{align*}
    \text{minimize} \quad       &  \sum_{i \in F} \left( t_{i} - h_{i} \right)    \\
    \text{subject to} \quad     &  \sum_{k \in G} x_{ik} = 1, \quad \forall i \in F,  \\
                                &  t_{i} \geq h_{i}, \quad \forall i \in F,\\
                                &  t_{i} + p_{i} - t_{j} \leq M (2-x_{ik}-x_{jk}), \quad \forall i<j,\; \forall i,j\in F,\; \forall k \in G, \\
                                & x_{ik}\in \{0,1\}, \quad \forall i \in F, k \in G,\\
                                & t_{i} \geq 0,\ \quad \forall i \in F.
\end{align*}
