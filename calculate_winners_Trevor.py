from form_to_structure import voteInfo

voting = voteInfo("candidate_preference.csv", "test_votes.csv")

print(voting.getVotes())
print(voting.getCandidates())
print(voting.getLengths())