import heapq
from collections import defaultdict

def compress_text(text: str, k: int) -> str:
    """
    Re-Pair compression with Priority Queue optimization.
    
    Uses:
    - Linked list via arrays (next[], prev[], char[])
    - Hash map for O(1) pair lookup
    - Max heap for O(log n) best pair retrieval
    
    Time: O(k * n log n)
    Space: O(n)
    """
    if not text or k <= 0:
        return text
    
    n = len(text)
    char = list(text)
    prev = [-1] * n
    next_arr = [-1] * n
    
    # Initialize linked list
    for i in range(n):
        if i > 0:
            prev[i] = i - 1
        if i < n - 1:
            next_arr[i] = i + 1
    
    head = 0
    new_token_ord = ord('A')
    
    for iteration in range(k):
        # Track pairs with their positions
        pair_data = defaultdict(lambda: {'count': 0, 'positions': [], 'first_pos': float('inf')})
        
        # Count all pairs
        i = head
        while i != -1:
            j = next_arr[i]
            if j != -1:
                pair = (char[i], char[j])
                pair_data[pair]['count'] += 1
                pair_data[pair]['positions'].append(i)
                if i < pair_data[pair]['first_pos']:
                    pair_data[pair]['first_pos'] = i
            i = next_arr[i]
        
        if not pair_data:
            break
        
        # Build max heap (negate count for max heap using min heap)
        # Heap elements: (-count, first_pos, pair)
        heap = []
        for pair, data in pair_data.items():
            if data['count'] >= 2:  # Only consider pairs appearing 2+ times
                heapq.heappush(heap, (-data['count'], data['first_pos'], pair))
        
        # No valid pairs found
        if not heap:
            break
        
        # Get best pair (highest count, then leftmost position)
        neg_count, first_pos, best_pair = heapq.heappop(heap)
        best_count = -neg_count
        
        # Create new token
        new_char = chr(new_token_ord)
        new_token_ord += 1
        
        # Replace all non-overlapping occurrences
        i = head
        while i != -1:
            j = next_arr[i]
            if j != -1 and char[i] == best_pair[0] and char[j] == best_pair[1]:
                # Merge i and j
                char[i] = new_char
                next_j = next_arr[j]
                next_arr[i] = next_j
                if next_j != -1:
                    prev[next_j] = i
                i = next_j  # Skip to avoid overlap
            else:
                i = next_arr[i]
    
    # Build result
    result = []
    i = head
    while i != -1:
        result.append(char[i])
        i = next_arr[i]
    
    return ''.join(result)


def run_tests():
    """20 comprehensive test cases"""
    test_cases = [
        # Cases 1-4: Basic Sanity Checks
        ("ababcababc", 2, "BcBc"),
        ("aaaaa", 1, "AAa"),
        ("aabbcc", 1, "aabbcc"),
        ("abcabc", 1, "AcAc"),
        
        # Cases 5-8: Edge Cases
        ("abcdefg", 1, "abcdefg"),
        ("aa", 1, "aa"),
        ("aaaa", 2, "AA"),
        ("aaaaaa", 2, "BA"),
        
        # Cases 9-12: Recursive Patterns
        ("abababab", 2, "BB"),
        ("aabbaabb", 2, "BbBb"),
        ("xyzxyzxyz", 1, "AzAzAz"),
        ("mississippi", 1, "mAsAsippi"),
        
        # Cases 13-16: Complex Patterns
        ("banana", 2, "bAAa"),
        ("bookkeeper", 2, "bookkeeper"),
        ("ab" * 50, 1, "A" * 50),
        ("abc" * 30, 1, "Ac" * 30),
        
        # Cases 17-20: Stress Tests
        ("aaabbb", 2, "AaBb"),
        ("aabbaa", 1, "AbbA"),
        ("abcdefgh" * 10, 1, "Acdefgh" * 10),
        ("aabbccdd" * 10, 3, "Cccdd" * 10),
    ]
    
    print("="*80)
    print("Re-Pair Compression with Priority Queue - 20 Test Cases")
    print("="*80)
    
    passed = 0
    failed = 0
    failed_tests = []
    
    for i, (text, k, expected) in enumerate(test_cases, 1):
        result = compress_text(text, k)
        is_pass = (result == expected)
        
        if is_pass:
            passed += 1
            print(f"Test {i:2d}: ✓ PASS")
        else:
            failed += 1
            failed_tests.append(i)
            display_text = text if len(text) <= 50 else text[:50] + "..."
            print(f"Test {i:2d}: ✗ FAIL")
            print(f"  Input:    '{display_text}' (k={k})")
            print(f"  Expected: '{expected}'")
            print(f"  Got:      '{result}'")
            print()
    
    print("="*80)
    print(f"Results: {passed}/20 passed, {failed}/20 failed")
    if failed_tests:
        print(f"Failed tests: {failed_tests}")
    else:
        print("🎉 All tests passed!")
    print("="*80)
    
    return passed == 20


if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1)