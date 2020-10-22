# imports
from can import Candidates_store
from can import Candidate



Candidates = Candidates_store(number_of_candidates=3, number_of_voters=10 , max_utility=1, average_utility=0.5)

Candidates.create()

bla = Candidate(voters=10, max_utility=1, average_utility=0.5)



"""
for i in Candidates.can_dict:
    Candidates.can_dict[i].print_info()
"""


Candidate_1 = Candidate(voters=10, max_utility=1, average_utility=0.5)
Candidate_1.create_hist()
Candidate_1.print_info()

Candidate_1.change_ut(position=3, change=0.3)
Candidate_1.create_hist()
Candidate_1.print_info()

Candidate_1.change_ut(position=3, change=0.5)
Candidate_1.create_hist()
Candidate_1.print_info()







