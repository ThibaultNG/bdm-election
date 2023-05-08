import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('Qt5Agg')

def generate_graph_image(results, state, party):
    x=[]
    y=[]
    for row in results:
        if row[0] == state and row[1] == party:
            x.append(row[2])
            y.append(row[5])

    plt.figure(figsize=(14,7),
               facecolor='white')
    # Set the x-axis and y-axis ticks every 2 years
    ax = plt.gca()
    ax.set_xticks(range(min(y), max(y) + 1, 2))
    ax.set_yticks(x)

    plt.plot(y, x)
    plt.ylabel("ratio de la part des votes (1= le partie a tous les votes dans cet état)")
    plt.xlabel("année ")
    plt.title(f"Graph for state {state} and party {party}")

    plt.savefig('static/graph1.png')

    plt.title(f"Graph(grid) for state {state} and party {party}")
    plt.grid(True)
    plt.grid(True, color='gray', linestyle=':')

    plt.savefig('static/graph2.png')