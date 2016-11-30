import math



def answer(area):

    # your solution here 7s
    sol = []

    
    def rec_answer(sol, n):
        if n == 0:
            return

        s = int(math.pow(int(math.sqrt(n)),2))
        d = n - s
        sol.append(s)

        rec_answer(sol, d)
       
    rec_answer(sol, area)

    return sol

print answer(15324)