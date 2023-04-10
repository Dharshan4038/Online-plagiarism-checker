def word_overlap_ratio(p1,p2):
    p1 = p1.split()
    p2 = p2.split()
    overlap = set(p1).intersection(set(p2))
    print(len(overlap)/len(p1))
    return len(overlap)/len(p1)