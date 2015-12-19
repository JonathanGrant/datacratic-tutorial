user_ids = []
subreddit_ids = []
subreddit_to_id = {}
i=0
with open("reddituserpostingbehavior.csv", 'r') as f:
    for line in f:
        for sr in line.rstrip().split(",")[1:]: 
            if sr not in subreddit_to_id: 
                subreddit_to_id[sr] = len(subreddit_to_id)
            user_ids.append(i)
            subreddit_ids.append(subreddit_to_id[sr])
        i+=1
  
import numpy as np
from scipy.sparse import csr_matrix 

rows = np.array(subreddit_ids)
cols = np.array(user_ids)
data = np.ones((len(user_ids),))
num_rows = len(subreddit_to_id)
num_cols = i

# the code above exists to feed this call
adj = csr_matrix( (data,(rows,cols)), shape=(num_rows, num_cols) )
print adj.shape
print ""

# now we have our matrix, so let's gather up a bit of info about it
users_per_subreddit = adj.sum(axis=1).A1
subreddits = range(len(subreddit_to_id))
for sr in subreddit_to_id:
    subreddits[subreddit_to_id[sr]] = sr
subreddits = np.array(subreddits)

from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import normalize

svd = TruncatedSVD(n_components=100)
embedded_coords = normalize(svd.fit_transform(adj), norm = 'l1')
print embedded_coords.shape

pd.DataFrame(np.cumsum(svd.explained_variance_ratio_)).plot(figsize=(13,8))