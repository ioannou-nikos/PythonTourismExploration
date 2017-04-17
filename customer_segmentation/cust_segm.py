import pandas as pd 
# http://blog.yhat.com/posts/customer-segmentation-python-rodeo.html
# Ofers data
df_offers = pd.read_excel("./WineKMC.xlsx", sheetname=0)
df_offers.columns = ["offer_id", "campaign", "varietal", "min_qty", "discount", 
                    "origin", "past_peak"]

# Transaction data
df_transactions = pd.read_excel("./WineKMC.xlsx", sheetname=1)
df_transactions.columns = ['customer_name', 'offer_id']
df_transactions['n'] = 1

# Join the offers and transactions table
df = pd.merge(df_offers, df_transactions)
# Create a pivot table which gives us the number that each customer responded
# to a given offer
matrix = df.pivot_table(index=['customer_name'], columns=['offer_id'], values='n')
# a little tidying up. Fill the NA values with 0 and make the index into a column
matrix = matrix.fillna(0).reset_index()
# save a list of the 0/1 columns for later use
x_cols = matrix.columns[1:]
# Now use the KMeans from scikit-learn. Take 5 clusters because we use the rule of thumb
# that rows must be 7x the number of clusters at least
from sklearn.cluster import KMeans
cluster = KMeans(n_clusters=5)
matrix['cluster'] = cluster.fit_predict(matrix[matrix.columns[2:]])
# Know show the value counts
matrix.cluster.value_counts()

# Know use ggplot to plot the result into a histogram
from ggplot import *
ggplot(matrix, aes(x='factor(cluster)')) + geom_bar() + xlab("Cluster") + ylab("Customers\n(# in cluster)")

# VISUALIZING THE CLUSTERS
# Use of Principal Component Analysis (PCA) from sklearn
from sklearn.decomposition import PCA
pca = PCA(n_components=2)
matrix['x'] = pca.fit_transform(matrix[x_cols])[:,0]
matrix['y'] = pca.fit_transform(matrix[x_cols])[:,1]
matrix = matrix.reset_index()
customer_clusters = matrix[['customer_name', 'cluster', 'x', 'y']]
customer_clusters.head()

# Create the scatter plot
df = pd.merge(df_transactions, customer_clusters)
df = pd.merge(df_offers, df)
ggplot(df, aes(x='x', y='y', color='cluster')) + \
    geom_point(size=75) + \
    ggtitle("Customers Grouped by Cluster")

# Draw the centers of each cluster which is stored in KMeans instance in variable cluster_centers_
cluster_centers = pca.transform(cluster.cluster_centers_)
cluster_centers = pd.DataFrame(cluster_centers, columns=['x', 'y'])
cluster_centers['cluster'] = range(0, len(cluster_centers))