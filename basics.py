# imports
from can import Candidate

default_voters = 10
default_max_utility = 1
default_average_utility = 0.5


Candidate_1 = Candidate(voters=default_voters, max_utility=default_max_utility, average_utility=default_average_utility)
Candidate_1.create_hist()
Candidate_1.print_info()

Candidate_1.change_ut(position=3, change=0.3)
Candidate_1.create_hist()
Candidate_1.print_info()

Candidate_1.change_ut(position=3, change=0.5)
Candidate_1.create_hist()
Candidate_1.print_info()







