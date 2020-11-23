"""Ranks candidates by the Condorcet method with also unvoted candidates.

For more information, please refer to https://en.wikipedia.org/wiki/Condorcet_method.
"""

__author__ = "Matteo Caorsi"
## I thank Michael G. Parker (http://omgitsmgp.com/) from whom I took the code skeleton

import numpy as np
from collections import defaultdict

def candidate_names_from_df(df):
    return list(np.unique(df.values.flatten()))

def weighted_ranks_from_df(df):
    weighted_ranks = []
    for row in df.values:
        weighted_ranks.append((list(row),1))
    return weighted_ranks


def _add_remaining_ranks(d, candidate_name, remaining_ranks, weight):
    for other_candidate_name in remaining_ranks:
        d[candidate_name, other_candidate_name] += weight


def _add_ranks_to_d(d, ranks, weight, unvoted_candidates):
    for i, candidate_name in enumerate(ranks):
        remaining_ranks = ranks[i+1:] + unvoted_candidates
        _add_remaining_ranks(d, candidate_name, remaining_ranks, weight)


def _compute_d(weighted_ranks, candidate_names):
    """Computes the d array in the Schulze method.
        
        d[V,W] is the number of voters who prefer candidate V over W.
        
        We consider unvoted candidates as being ranked less than any
        other candidate voted by the voter.
        """
    d = defaultdict(int)
    for ranks, weight in weighted_ranks:
        unvoted_candidates = list(set(candidate_names)-set(ranks))
        #print("unoted:", unvoted_candidates)
        _add_ranks_to_d(d, ranks, weight, unvoted_candidates)
    #print(d)
    return d


def _compute_p(d, candidate_names):
    '''Computes the p array in the Schulze method.
        
        p[V,W] is the strength of the strongest path from candidate V to W.
    '''
    
    # taken directly from wikipedia: https://en.wikipedia.org/wiki/Schulze_method#Implementation
    p = {}
    for candidate_name1 in candidate_names:
        for candidate_name2 in candidate_names:
            if candidate_name1 != candidate_name2:
                # get the value from the d matrix or default it to 0
                strength = d.get((candidate_name1, candidate_name2), 0)
                if strength > d.get((candidate_name2, candidate_name1), 0):
                    p[candidate_name1, candidate_name2] = strength
                else:
                    p[candidate_name1, candidate_name2] = 0

    for candidate_name1 in candidate_names:
        for candidate_name2 in candidate_names:
            if candidate_name1 != candidate_name2:
                for candidate_name3 in candidate_names:
                    if (candidate_name1 != candidate_name3) and (candidate_name2 != candidate_name3):
                        curr_value = p.get((candidate_name2, candidate_name3), 0)
                        new_value = min(
                                        p.get((candidate_name2, candidate_name1), 0),
                                        p.get((candidate_name1, candidate_name3), 0))
                        p[candidate_name2, candidate_name3] = max(curr_value,new_value)
    return p


def _rank_p(candidate_names, p):
    """Ranks the candidates by p."""
    # how many times does a candidate wins against each of the others?
    candidate_wins = defaultdict(list)
    
    for candidate_name1 in candidate_names:
        num_wins = 0
        
        # Compute the number of wins this candidate has over all other candidates.
        for candidate_name2 in candidate_names:
            if candidate_name1 != candidate_name2:
                candidate1_score = p.get((candidate_name1, candidate_name2), 0)
                candidate2_score = p.get((candidate_name2, candidate_name1), 0)
                if candidate1_score > candidate2_score:
                    num_wins += 1
        
        candidate_wins[num_wins].append(candidate_name1)
        #print(candidate_wins)
    sorted_wins = sorted(candidate_wins.keys(), reverse=True)
    return [candidate_wins[num_wins] for num_wins in sorted_wins]


def compute_ranks(df):
    weighted_ranks = weighted_ranks_from_df(df)
    candidate_names = candidate_names_from_df(df)
    #print(candidate_names)
    d = _compute_d(weighted_ranks, candidate_names)
    p = _compute_p(d, candidate_names)
    return _rank_p(candidate_names, p)
