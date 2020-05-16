#yowie zowie
#would get fucked up if at some point no one wins there top choice
import numpy as np
from form_to_structure import voteInfo

def in_list(item, lisp):
    for value in lisp:
        if (value==item):
            return True
    return False

def rev_search_dict(dictionary,value):
    key_list=list(dictionary.keys())
    val_list=list(dictionary.values())
    return key_list[val_list.index(value)]

def winner(votes,position,still_in_it):   
    number_moving_on=2
    length=len(votes[0][position])
    candidate_key={}
    i=0
    for candidate in still_in_it[position]:
        candidate_key[i]=candidate
        i+=1
    ranking=np.zeros(len(candidate_key)).tolist()
    for vote in votes:
        for i in range(0,length):
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
        print("Tie")
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
            print("Tie")
            return "Tie"
        return winner(votes,position,new_still_in_it)

def get_first_winners (votes,candidates):
    first_winners={}
    for position in list(candidates.keys()):
        win=winner(votes,position,candidates)
        first_winners[position]=win
    return first_winners    

def remove_from_preferences (new_real_winners,preferences):
    positions_won=list(new_real_winners.keys())
    candidates_won=list(new_real_winners.values())
    candidates=list(preferences.keys())
    for position in positions_won:
        for candidate in candidates:
            if in_list(position,preferences[candidate]):
                preferences[candidate].remove(position)
    for candidate in candidates_won:
        preferences[candidate]=[]

def remove_from_candidates (new_real_winners,candidates):
    candidates_won=list(new_real_winners.values())
    positions_won=list(new_real_winners.keys())
    positions=list(candidates.keys())
    for candidate in candidates_won:
        for position in positions:
            if in_list(candidate,candidates[position]):
                candidates[position].remove(candidate)
    for position in positions_won:
        candidates.pop(position)

def removal(new_real_winners,preferences,candidates):
    remove_from_preferences (new_real_winners,preferences)
    remove_from_candidates (new_real_winners,candidates)

def real_winner(winners,preferences,real_winners,candidates):
    new_real_winners={}
    for position in list(winners.keys()):
        if winners[position]!="Tie":
            if preferences[winners[position]][0]==position:
                new_real_winners[position]=winners[position]
                name=winners[position]
                winners.pop(position)
                for pos in list(winners.keys()): #if they won anothe position too remove that position from winners
                    if winners[pos]==name:
                        winners.pop(pos)
    real_winners.update(new_real_winners)
    if len(new_real_winners)==0:
        return real_winners #kinda running on assumption that at least someone won their first position, otherwise gets stuck in infinite loop
    else:
        removal(new_real_winners,preferences,candidates)
        return real_winner(winners,preferences,new_real_winners,candidates)

def find_winners(votes,candidates,real_winners,preferences):
    if len(real_winners)==position_number:
        return real_winners
    else:
        winners=get_first_winners(votes,candidates)
        real_winner(winners,preferences,real_winners,candidates)
        return find_winners(votes,candidates,real_winners,preferences)



votes=[{"President":["Trevor","Ryan","Kenton"],"Vice President":["Ryan","Trevor","Kenton"]},{"President":["Ryan","Trevor","Kenton"],"Vice President":["Ryan","Trevor","Kenton"]},{"President":["Kenton","Ryan","Trevor"],"Vice President":["Kenton","Trevor","Ryan"]},{"President":["Trevor","Ryan","Kenton"],"Vice President":["Trevor","Ryan","Kenton"]},{"President":["Ryan","Trevor","Kenton"],"Vice President":["Kenton","Trevor","Ryan"]}]
candidates={"President":["Trevor","Ryan","Kenton"],"Vice President":["Ryan","Trevor","Kenton"]}
preferences={"Trevor":["President","Vice President"],"Kenton":["President","Vice President"],"Ryan":["Vice President","President"]}
position_number=len(candidates)

voting = voteInfo("candidate_preference.csv", "test_votes.csv")

votes=voting.getVotes()
candidates=voting.getCandidates()
preferences=voting.getPreferences()

real_winners={}
find_winners(votes,candidates,real_winners,preferences)
print(real_winners)
