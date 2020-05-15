from form_to_structure import voteInfo

voting = voteInfo("candidate_preference.csv", "test_votes.csv")

print(voting.getVotes())
print(voting.getCandidates())
print(voting.getLengths())

def get_first_winners (votes,candidates):
    first_winners={}
    for position in list(candidates.keys()):
        win=winner(votes,position,candidates)
        first_winners[position]=win
    return first_winners    

def remove_from_preferences (real_winners,preferences):
    positions_won=list(real_winners.keys())
    candidates_won=list(real_winners.values())
    candidates=list(preferences.keys())
    for position in positions_won:
        for candidate in candidates:
            if in_list(position,preferences[candidate]):
                preferences[candidate].remove(position)
    for candidate in candidates_won:
        preferences[candidate]=[]

