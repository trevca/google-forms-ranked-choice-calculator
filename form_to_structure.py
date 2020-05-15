import numpy as np
import pandas as pd

class voteInfo:
    def __init__(self, candidate_info_path, vote_info_path):
        candidate_raw = pd.read_csv(candidate_info_path).to_numpy()
        self.candidates = {}
        for candidate in candidate_raw:
            self.candidates[candidate[0]] = []
            self.candidates[candidate[0]].append(candidate[1])
            self.candidates[candidate[0]].append(candidate[2])
            self.candidates[candidate[0]].append(candidate[3])

        self.lengths = {"President": 1, "Vice President": 1, "Corporate Liaison": 6, "Secretary": 9, "Treasurer": 3, "UC Liaison": 2, 
          "Director of Community Service": 3, "Director of Outreach": 2, "Director of Public Relations": 5, "Webmaster": 3}
        self.votes = []

        votes_data = pd.read_csv(vote_info_path).drop("Timestamp",1).drop("Email Address",1).to_numpy()
        for vote in votes_data:
            dictionary = {}
            currPartition = 0
            nextPartition = 0
            for position in self.lengths:
                currPartition = nextPartition
                nextPartition += self.lengths[position]
                dictionary[position] = vote[currPartition:nextPartition].tolist()
            self.votes.append(dictionary)

    def getVotes(self):
        return self.votes

    def getCandidates(self):
        return self.candidates

    def getLengths(self):
        return self.lengths

    