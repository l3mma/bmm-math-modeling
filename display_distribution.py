from pointGen import *
import plotly.express as px

df = pd.DataFrame(points_inside, columns=['x', 'y', 'z'])
fig = px.scatter_3d(df, x = df['x'], y = df['y'], z = df['z'])
fig.update_traces(marker=dict(size=5))
fig.show()