import matplotlib.pyplot as plt

def draw_gantt(processes, timeline, step):
    fig, ax = plt.subplots(figsize=(8, 1 + len(processes) * 0.5))  

    process_ids = sorted(set([p[0] for p in processes]))
    process_row = {pid: i for i, pid in enumerate(process_ids)}
    colors = {}

    for i in range(step):
        t, pid = timeline[i]
        if pid not in colors:
            colors[pid] = f"C{len(colors)}"
        y = 5 + 5 * process_row[pid]  
        ax.broken_barh([(t, 1)], (y, 4), facecolors=colors[pid])
        ax.text(t + 0.1, y + 2, pid, fontsize=6) 

    ax.set_xlim(0, max(t for t, _ in timeline) + 1)
    ax.set_ylim(2, 5 + 5 * len(process_ids))
    ax.set_xlabel("Ciclos", fontsize=8)
    ax.set_yticks([5 + 5 * i + 1.5 for i in range(len(process_ids))])
    ax.set_yticklabels(process_ids, fontsize=7)
    ax.set_title("Diagrama de Gantt", fontsize=10, pad=10)
    ax.tick_params(axis='x', labelsize=7)
    return fig

