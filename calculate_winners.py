#yowie zowie
import numpy as np

def in_list(item, lisp):
    for value in lisp:
        if (value==item):
            return True
    return False

def rev_search_dict(dictionary,value):
    key_list=list(dictionary.keys())
    val_list=list(dictionary.values())
    return key_list[val_list.index(value)]

def find_first_winner(votes,position,still_in_it):   
    number_moving_on=2
    length=len(votes[0][position])
    candidate_key={}
    i=0
    for candidate in still_in_it[position]:
        candidate_key[i]=candidate
        i+=1
    ranking=np.zeros(len(candidate_key)).tolist()
    for vote in votes:
        for i in range(0,length-1):
            if in_list(vote[position][i],still_in_it[position]):
                choice_name=vote[position][i]
                choice_index=rev_search_dict(candidate_key,choice_name)
                ranking[choice_index]+=1
                break
    scores=ranking.copy()
    scores.sort()
    scores.reverse()
    most=scores[0]
    if most>(len(votes)/2):
        return candidate_key.get(ranking.index(most))
    elif len(still_in_it[position])==2:
        return "Tie"
    else:
        second_most=scores[1]
        nexxt=scores[number_moving_on]
        while nexxt==second_most:
            number_moving_on+=1
            if (len(scores)-1)>=number_moving_on:
                nexxt=scores[number_moving_on]
            else:
                break
        new_still_in_it={position:[]}
        first=ranking.index(most)
        ranking[first]=0
        first=candidate_key[first]
        new_still_in_it[position].append(first)
        for i in range(0,number_moving_on-1):
            second=ranking.index(second_most)
            ranking[second]=0
            second=candidate_key[second]
            new_still_in_it[position].append(second)
        if len(still_in_it[position])==len(new_still_in_it[position]):
            return "Tied"
        return find_first_winner(votes,position,new_still_in_it)


votes=[{"President":["Trevor","Ryan","Kenton"]},{"President":["Ryan","Trevor","Kenton"]},{"President":["Kenton","Ryan","Trevor"]},{"President":["Trevor","Ryan","Kenton"]},{"President":["Ryan","Trevor","Kenton"]}]
candidates={"President":["Trevor","Ryan","Kenton"]}
print(find_first_winner(votes,"President",candidates))

