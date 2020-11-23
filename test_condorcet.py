"""Ranks candidates by the Condorcet method with also unvoted candidates.

For more information, please refer to https://en.wikipedia.org/wiki/Condorcet_method.
"""

__author__ = "Matteo Caorsi"
## I thank Michael G. Parker (http://omgitsmgp.com/) from whom I took the code skeleton

import numpy as np
import pandas as pd
import condorcet

def test_compute_ranks():
    '''A simnple unit test
    '''
    
    # create dataframe
    table = np.asarray([
                        ["b","c","a"],
                        ["c","a","b"],
                        ["c","a","b"],
                        ["b","a","c"],
                        ["d","a","c"],
                        ["d","a","c"]
                        ])
    df = pd.DataFrame(table, columns = ["first_preference","second_preference","third_preference"])
    try:
        # run the classification
        assert condorcet.compute_ranks(df)==[['a', 'c'], ['b'], ['d']]
    except:
        raise ValueError("The method is not working as expected!")

