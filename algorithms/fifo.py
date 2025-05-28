def fifo_scheduler(processes):
    timeline = []
    current_time = 0
    waiting_times = {}
    executed_processes = []

    for pid, bt, at, pr in sorted(processes, key=lambda x: x[2]):
        if at > current_time:
            current_time = at
        waiting_times[pid] = current_time - at
        for i in range(bt):
            timeline.append((current_time + i, pid))
        current_time += bt
        executed_processes.append((pid, bt, at, pr)) 

    avg_waiting_time = sum(waiting_times.values()) / len(waiting_times)
    return timeline, avg_waiting_time, executed_processes
