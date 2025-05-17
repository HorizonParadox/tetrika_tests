def merge_intervals(intervals: list[tuple[int, int]]) -> list[tuple[int, int]]:
    if not intervals:
        return []
    intervals = sorted(intervals, key=lambda x: x[0])
    merged = [intervals[0]]
    for curr_start, curr_end in intervals[1:]:
        last_start, last_end = merged[-1]
        if curr_start <= last_end:
            merged[-1] = (last_start, max(last_end, curr_end))
        else:
            merged.append((curr_start, curr_end))
    return merged


def clip_intervals(intervals: list[int], lesson_start: int, lesson_end: int) -> list[tuple[int, int]]:
    clipped = []
    for i in range(0, len(intervals), 2):
        s, e = intervals[i], intervals[i + 1]
        # обрезаем по уроку
        s_clipped = max(s, lesson_start)
        e_clipped = min(e, lesson_end)
        if s_clipped < e_clipped:
            clipped.append((s_clipped, e_clipped))
    return clipped


def appearance(intervals: dict[str, list[int]]) -> int:
    lesson_start, lesson_end = intervals['lesson']

    pupil_raw = clip_intervals(intervals['pupil'], lesson_start, lesson_end)
    tutor_raw = clip_intervals(intervals['tutor'], lesson_start, lesson_end)
    pupil = merge_intervals(pupil_raw)
    tutor = merge_intervals(tutor_raw)

    i, j = 0, 0
    total = 0
    while i < len(pupil) and j < len(tutor):
        a_start, a_end = pupil[i]
        b_start, b_end = tutor[j]
        start = max(a_start, b_start)
        end = min(a_end, b_end)
        if start < end:
            total += end - start
        if a_end < b_end:
            i += 1
        else:
            j += 1
    return total