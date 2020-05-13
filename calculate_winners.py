#yowie zowie
import numpy as np

def in_list(item, lisp):
    for value in lisp:
        if (value==item):
            return True
    return False

def find_first_winner(votes,position,still_in_it):   
    number_moving_on=2
    length=len(votes[0][position])
    ranking=np.zeros(length).tolist()
    for vote in votes:
        for i in range(0,length-1):
            if (in_list(vote[position][i],still_in_it)):
                choice=vote[position][i]
                ranking[choice]+=1
                break
    scores=ranking.copy()
    scores.sort()
    scores.reverse()
    most=scores[0]
    if most>(len(votes)/2):
        return ranking.index(most)
    else:
        second_most=scores[1]
        while true:
            next=scores[number_moving_on-1]
            if(next==second_most_scores):
                number_moving_on+=1
            else:
                break
        still_in_it=[]
        first=ranking.index(most)
        still_in_it.append(first)
        ranking[first]=0
        for i in range(0,number_moving_on-2):
            second=ranking.index(second_most)
            still_in_it.append(second)
            ranking[second]=0
        find_first_winner(votes,position,still_in_it)


yippee=[{"President":[1,0],"VP":[0,2,1]},{"President":[0,1],"VP":[0,1,2]},{"President":[0,1],"VP":[0,1,2]}]
print(find_first_winner(yippee,"President",[0,1]))

