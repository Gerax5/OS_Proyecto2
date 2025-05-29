def srtf_scheduler(processes):
    n = len(processes)
    processes = sorted(processes, key=lambda x: x[2])  

    remaining_bt = {pid: bt for pid, bt, _, _ in processes}
    arrival_map = {pid: at for pid, _, at, _ in processes}
    original_map = {pid: (pid, bt, at, pr) for pid, bt, at, pr in processes}
    completed = set()

    time = 0
    timeline = []
    waiting_times = {}
    executed_processes = []

    while len(completed) < n:
        available = [(pid, remaining_bt[pid]) for pid in remaining_bt if arrival_map[pid] <= time and pid not in completed]
        if available:
            pid, _ = min(available, key=lambda x: x[1])
            timeline.append((time, pid))

            remaining_bt[pid] -= 1
            if remaining_bt[pid] == 0:
                completed.add(pid)
                waiting_times[pid] = time + 1 - original_map[pid][1] - arrival_map[pid]  
                executed_processes.append(original_map[pid])
        else:
            timeline.append((time, "idle"))
            pass

        time += 1

    avg_waiting_time = sum(waiting_times.values()) / n
    return timeline, avg_waiting_time, executed_processes
