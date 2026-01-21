from collections import defaultdict
import heapq

def compress_text(text: str, k: int) -> str:
    if not text or k <= 0:
        return text
    
    n = len(text)
    c = list(text)
    p = [-1] * n
    nx = list(range(1, n)) + [-1]
    for i in range(1, n):
        p[i] = i - 1
    
    h = 0
    t = ord('A')
    
    # Efficient pair tracking
    cnt = defaultdict(int)
    pos_heaps = defaultdict(list)
    at_pos = {}
    
    def add_pair(i):
        j = nx[i]
        if j == -1:
            return
        pr = (c[i], c[j])
        cnt[pr] += 1
        heapq.heappush(pos_heaps[pr], i)
        at_pos[i] = pr
    
    def del_pair(i):
        if i in at_pos:
            cnt[at_pos[i]] -= 1
            del at_pos[i]
    
    def get_first(pr):
        while pos_heaps[pr]:
            pos = pos_heaps[pr][0]
            if pos in at_pos and at_pos[pos] == pr:
                return pos
            heapq.heappop(pos_heaps[pr])
        return None
    
    # Init
    i = h
    while i != -1:
        add_pair(i)
        i = nx[i]
    
    for _ in range(k):
        # Find best
        bp, bc, bf = None, 0, n
        
        for pr in list(cnt.keys()):
            if cnt[pr] >= 2:
                f = get_first(pr)
                if f is not None and (cnt[pr] > bc or (cnt[pr] == bc and f < bf)):
                    bp, bc, bf = pr, cnt[pr], f
        
        if not bp:
            break
        
        nc = chr(t)
        t += 1
        
        # Merge directly without collecting
        i = h
        lm = -1
        
        while i != -1:
            if i in at_pos and at_pos[i] == bp and i != lm:
                j = nx[i]
                pi = p[i]
                nj = nx[j]
                
                # Remove
                if pi != -1:
                    del_pair(pi)
                del_pair(i)
                if j != -1:
                    del_pair(j)
                
                # Merge
                c[i] = nc
                nx[i] = nj
                if nj != -1:
                    p[nj] = i
                
                lm = j
                
                # Add
                if pi != -1:
                    add_pair(pi)
                add_pair(i)
                
                i = nj
            else:
                i = nx[i]
    
    # Result
    r = []
    i = h
    while i != -1:
        r.append(c[i])
        i = nx[i]
    
    return ''.join(r)

