def sjf_scheduler(processes):
    processes = sorted(processes, key=lambda x: x[2])
    n = len(processes)
    remaining = processes[:]
    timeline = []
    current_time = 0
    waiting_times = {}
    executed_processes = []

    while remaining:
        available = [p for p in remaining if p[2] <= current_time]
        if available:
            next_process = min(available, key=lambda x: x[1])
            pid, bt, at, pr = next_process
            for t in range(current_time, current_time + bt):
                timeline.append((t, pid))
            waiting_times[pid] = current_time - at
            current_time += bt
            remaining.remove(next_process)
            executed_processes.append(next_process)
        else:
            current_time += 1

    avg_waiting_time = sum(waiting_times.values()) / n
    return timeline, avg_waiting_time, executed_processes
