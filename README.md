# condorcet-method
This repo implements the Schulze method, a Condorcet-type election method. Please refer to [Wikipedia](https://en.wikipedia.org/wiki/Schulze_method) for all the mathematical details.

## How to run the method

__1. Prepare your data__

The first step is to import your data in a dataframe. The structure has to be the following:
 - Each voter has to correspond to a line
 - Each row contains, ordered from the left to the right columns, the preferences of the voter
 - Each entry corresponds to the name of teh candidates: make sure not to make spelling mistakes
 
 To see a concrete example, have a look at [Run_ranking.ipynb](https://github.com/giotto-ai/condorcet-method/blob/main/Run_ranking.ipynb).
 
 __2. Run the election method to discover the winning candidates__
 
 To run the model once the dataframe `df` is ready, it is just one line:
 ```
condorcet.compute_ranks(df) 
```
As in the example in the notebook, the output is a list of lists, where the position of the inner list corresponds to the ranking and if the inner lists are longer than one element, it is because there is a tie.

__3. Dive deeper__

You can extract the *d[V,W]* and *p[V,W]* matrices with the methods:
 - `condorcet._compute_d(weighted_ranks, candidate_names)`
 - `condorcet._compute_p(dmat, candidate_names)`
 
To extract the candidate names and the weighted ranks to be input to the above methods, please use:
 - `weighted_ranks = condorcet.weighted_ranks_from_df(df)`
 - `candidate_names = condorcet.candidate_names_from_df(df)`
 
 ## Code tests
 
 The [Wikipedia example](https://en.wikipedia.org/wiki/Schulze_method#Example) is reproduced in the example notebook and all the entries of the *p* and *d* matrices match the original ones.
 
 A short unit test can be run with the command `pytest` once in the repo root folder. To run the test, pytest is required. You can install it with `pip install pytest`.
