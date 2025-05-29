def round_robin_scheduler(processes, quantum):
    processes = sorted(processes, key=lambda x: x[2])  
    n = len(processes)
    remaining_bt = {pid: bt for pid, bt, _, _ in processes}
    arrival_time = {pid: at for pid, _, at, _ in processes}
    original_map = {pid: (pid, bt, at, pr) for pid, bt, at, pr in processes}

    queue = [] 
    timeline = []
    time = 0
    waiting_times = {}
    finished = set()
    executed_processes = []
    index = 0  

    while len(finished) < n:
        while index < n and processes[index][2] <= time:
            queue.append(processes[index][0])
            index += 1

        if not queue:
            # timeline.append((time, "idle"))
            time += 1
            continue

        pid = queue.pop(0) 
        bt_left = remaining_bt[pid]
        exec_time = min(quantum, bt_left)

        for _ in range(exec_time):
            timeline.append((time, pid))
            time += 1
            while index < n and processes[index][2] <= time:
                queue.append(processes[index][0])
                index += 1

        remaining_bt[pid] -= exec_time
        if remaining_bt[pid] == 0:
            finished.add(pid)
            turnaround_time = time - arrival_time[pid]
            waiting_times[pid] = turnaround_time - original_map[pid][1]
            executed_processes.append(original_map[pid])
        else:
            queue.append(pid)  

    avg_waiting_time = sum(waiting_times.values()) / n
    return timeline, avg_waiting_time, executed_processes
