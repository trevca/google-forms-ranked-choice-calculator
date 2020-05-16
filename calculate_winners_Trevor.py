from form_to_structure import voteInfo
# get winners round one

def reset_votes(needed_positions, eligible_candidates):
    vote_count = {i: {} for i in needed_positions}
    for pos in vote_count:
        for person in eligible_candidates[pos]:
            vote_count[pos][person] = 0
    return(vote_count)

def count_votes(needed_positions, eligible_candidates, votes):
    vote_count = reset_votes(needed_positions, eligible_candidates) # makes an empty vote count
    for vote in votes:
        for position in needed_positions:
            l = [cand for cand in vote_count[position]]
            for wanted_person in vote[position]:
                if(wanted_person in l):
                    vote_count[position][wanted_person] += 1
                    break
    
    return vote_count

def vote_and_rank(needed_positions, eligible_candidates, votes):
    vc = count_votes(needed_positions, eligible_candidates, votes)
    final_board = {}
    round_2 = {}
    for position in vc:
        ordered = sorted(vc[position], key=vc[position].__getitem__)
        length = len(ordered)
        ordered.reverse()
        top = vc[position][ordered[0]] # top number of votes
        num_votes = len(votes)
        if top > num_votes/2 or length < 2: # majority
            final_board[position] = ordered[0]
        else:
            round_2[position] = ordered[0:2]
    return(final_board, round_2)

def assign_positions(needed_positions, eligible_candidates, votes):
    confirmed, round_2 = vote_and_rank(needed_positions, eligible_candidates, votes)
    next_positions = round_2.keys()
    confirmed_next, round_2_next = vote_and_rank(next_positions, round_2, votes)
    for pos in confirmed_next:
        confirmed[pos] = confirmed_next[pos]
    if len(round_2_next.keys()) > 0:
        print("second round tie?")
    return(confirmed)

def remove_duplicates(board):
    seen = {}
    multiple_wins = {}
    for position in board:
        if (board[position] in seen):
            keys = multiple_wins.keys()
            if not(board[position] in keys):
                multiple_wins[board[position]] = [seen[board[position]]]
            multiple_wins[board[position]].append(position)
        else:
            seen[board[position]] = position

    for person in multiple_wins:
        seen.pop(person)
    return(seen, multiple_wins)

def voting_round(needed_positions, eligible_candidates, preferences, votes):
    board = assign_positions(needed_positions, eligible_candidates, votes)
    seen, multiple_wins = remove_duplicates(board)

    already_done = list(seen.keys())

    for candidate in multiple_wins:
        desired_roles = preferences[candidate]
        for position in desired_roles:
            if (position in multiple_wins[candidate]):
                seen[candidate] = position
                already_done.append(candidate)
                break

    filled_positions = list(seen.values())
    next_positions = []
    for pos in needed_positions:
        if not(pos in filled_positions):
            next_positions.append(pos)
    return (seen, next_positions)

def vote(positions, candidates, preferences, votes):
    curr_board, next_pos = voting_round(positions, candidates, preferences, votes)
    while len(curr_board) < 10:
        # update positions and candidates
        next_candidates = candidates.copy()
        for position in list(curr_board.values()):
            if (position in list(next_candidates.keys())):
                next_candidates.pop(position)
        for position in next_candidates:
            for person in next_candidates[position]:
                if (person in list(curr_board.keys())):
                    next_candidates[position].remove(person)
        next_board, next_pos = voting_round(list(next_candidates.keys()), next_candidates, preferences, votes)
        for val in next_board:
            curr_board[val] = next_board[val]
    return(curr_board)

voting = voteInfo("candidate_preference.csv", "test_votes.csv")
candidates = voting.getCandidates()
votes = voting.getVotes()
preferences = voting.getPreferences()
positions = list(voting.getLengths().keys())
final = vote(positions, candidates, preferences, votes)
print(final)