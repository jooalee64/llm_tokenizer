"""
Re-Pair Compression Algorithm - Production-Ready Implementation
=================================================================
- Linked list via arrays (next[], prev[], char[])
- Hash map for O(1) pair lookup
- Priority queue (max heap) for O(log n) operations
- Handles large inputs efficiently (up to 1M characters)

Time Complexity: O(k * n log n) where k = iterations, n = string length
Space Complexity: O(n)
"""

import heapq
from collections import defaultdict


class PairInfo:
    """Stores information about a character pair"""
    def __init__(self, pair, count=0, first_pos=float('inf')):
        self.pair = pair
        self.count = count
        self.first_pos = first_pos
        self.active = True  # Track if this entry is still valid
    
    def __lt__(self, other):
        # For max heap: higher count wins, then lower position
        if self.count != other.count:
            return self.count > other.count  # Reverse for max heap
        return self.first_pos < other.first_pos


def compress_text(text: str, k: int) -> str:
    """
    Compress text using Re-Pair algorithm with heap optimization.
    
    Args:
        text: Input string of lowercase letters (1 ≤ len ≤ 10^6)
        k: Number of merge operations (1 ≤ k ≤ 26)
    
    Returns:
        Compressed string after k operations
    """
    if not text or k <= 0:
        return text
    
    n = len(text)
    
    # Linked list arrays
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
    
    # Main compression loop
    for iteration in range(k):
        # Step 1: Count all pairs and build heap
        pair_map = {}  # Maps pair tuple -> PairInfo object
        heap = []
        
        i = head
        while i != -1:
            j = next_arr[i]
            if j != -1:
                pair = (char[i], char[j])
                
                if pair not in pair_map:
                    pair_map[pair] = PairInfo(pair, 0, i)
                
                pair_info = pair_map[pair]
                pair_info.count += 1
                if i < pair_info.first_pos:
                    pair_info.first_pos = i
            
            i = next_arr[i]
        
        # Add pairs with count >= 2 to heap
        for pair_info in pair_map.values():
            if pair_info.count >= 2:
                heapq.heappush(heap, pair_info)
        
        # Step 2: Get best pair from heap
        if not heap:
            break  # No valid pairs found
        
        best_info = heapq.heappop(heap)
        best_pair = best_info.pair
        
        # Step 3: Create new token
        new_char = chr(new_token_ord)
        new_token_ord += 1
        
        # Step 4: Replace all non-overlapping occurrences
        i = head
        while i != -1:
            j = next_arr[i]
            if j != -1 and char[i] == best_pair[0] and char[j] == best_pair[1]:
                # Merge positions i and j
                char[i] = new_char
                
                # Remove j from linked list
                next_j = next_arr[j]
                next_arr[i] = next_j
                
                if next_j != -1:
                    prev[next_j] = i
                
                # Skip to avoid overlap
                i = next_j
            else:
                i = next_arr[i]
    
    # Build final result
    result = []
    i = head
    while i != -1:
        result.append(char[i])
        i = next_arr[i]
    
    return ''.join(result)


def compress_text_verbose(text: str, k: int, verbose=False):
    """
    Version with detailed logging for debugging.
    """
    if not text or k <= 0:
        return text
    
    n = len(text)
    char = list(text)
    prev = [-1] * n
    next_arr = [-1] * n
    
    for i in range(n):
        if i > 0:
            prev[i] = i - 1
        if i < n - 1:
            next_arr[i] = i + 1
    
    head = 0
    new_token_ord = ord('A')
    
    if verbose:
        print(f"\nInitial text: {text}")
        print(f"Iterations: {k}")
        print("="*60)
    
    for iteration in range(k):
        # Count pairs
        pair_map = {}
        heap = []
        
        i = head
        while i != -1:
            j = next_arr[i]
            if j != -1:
                pair = (char[i], char[j])
                if pair not in pair_map:
                    pair_map[pair] = PairInfo(pair, 0, i)
                pair_info = pair_map[pair]
                pair_info.count += 1
                if i < pair_info.first_pos:
                    pair_info.first_pos = i
            i = next_arr[i]
        
        for pair_info in pair_map.values():
            if pair_info.count >= 2:
                heapq.heappush(heap, pair_info)
        
        if not heap:
            if verbose:
                print(f"Iteration {iteration + 1}: No pairs with count >= 2. Stopping.")
            break
        
        best_info = heapq.heappop(heap)
        best_pair = best_info.pair
        new_char = chr(new_token_ord)
        new_token_ord += 1
        
        if verbose:
            print(f"\nIteration {iteration + 1}:")
            print(f"  Best pair: '{best_pair[0]}{best_pair[1]}' (count={best_info.count}, pos={best_info.first_pos})")
            print(f"  New token: '{new_char}'")
        
        # Replace
        i = head
        replacements = 0
        while i != -1:
            j = next_arr[i]
            if j != -1 and char[i] == best_pair[0] and char[j] == best_pair[1]:
                char[i] = new_char
                next_j = next_arr[j]
                next_arr[i] = next_j
                if next_j != -1:
                    prev[next_j] = i
                i = next_j
                replacements += 1
            else:
                i = next_arr[i]
        
        # Get current state
        current = []
        i = head
        while i != -1:
            current.append(char[i])
            i = next_arr[i]
        
        if verbose:
            print(f"  Replacements: {replacements}")
            print(f"  Result: {''.join(current)}")
    
    result = []
    i = head
    while i != -1:
        result.append(char[i])
        i = next_arr[i]
    
    if verbose:
        print(f"\nFinal result: {''.join(result)}")
        print("="*60)
    
    return ''.join(result)


def run_tests():
    """Run all 20 test cases"""
    test_cases = [
        ("ababcababc", 2, "BcBc"),
        ("aaaaa", 1, "AAa"),
        ("aabbcc", 1, "aabbcc"),
        ("abcabc", 1, "AcAc"),
        ("abcdefg", 1, "abcdefg"),
        ("aa", 1, "aa"),
        ("aaaa", 2, "AA"),
        ("aaaaaa", 2, "BA"),
        ("abababab", 2, "BB"),
        ("aabbaabb", 2, "BbBb"),
        ("xyzxyzxyz", 1, "AzAzAz"),
        ("mississippi", 1, "mAsAsippi"),
        ("banana", 2, "bAAa"),
        ("bookkeeper", 2, "bookkeeper"),
        ("ab" * 50, 1, "A" * 50),
        ("abc" * 30, 1, "Ac" * 30),
        ("aaabbb", 2, "AaBb"),
        ("aabbaa", 1, "AbbA"),
        ("abcdefgh" * 10, 1, "Acdefgh" * 10),
        ("aabbccdd" * 10, 3, "Cccdd" * 10),
    ]
    
    print("="*80)
    print("Re-Pair Compression - Heap-Optimized Implementation")
    print("="*80)
    
    passed = 0
    failed = 0
    
    for i, (text, k, expected) in enumerate(test_cases, 1):
        result = compress_text(text, k)
        is_pass = (result == expected)
        
        if is_pass:
            passed += 1
            print(f"Test {i:2d}: ✓ PASS")
        else:
            failed += 1
            display = text if len(text) <= 50 else text[:50] + "..."
            print(f"Test {i:2d}: ✗ FAIL")
            print(f"  Input:    '{display}' (k={k})")
            print(f"  Expected: '{expected}'")
            print(f"  Got:      '{result}'")
            
            # Show detailed trace for failed test
            print(f"\n  Detailed trace:")
            compress_text_verbose(text, k, verbose=True)
    
    print("="*80)
    print(f"Results: {passed}/20 passed, {failed}/20 failed")
    print("="*80)
    
    return passed == 20


def stress_test():
    """Test with large inputs to verify efficiency"""
    print("\nRunning stress tests...")
    print("-" * 60)
    
    import time
    
    test_cases = [
        ("a" * 10000, 10, "10k 'a' characters"),
        ("ab" * 5000, 5, "10k alternating 'ab'"),
        ("abc" * 3333, 3, "~10k 'abc' pattern"),
    ]
    
    for text, k, description in test_cases:
        start = time.time()
        result = compress_text(text, k)
        elapsed = time.time() - start
        
        print(f"{description}:")
        print(f"  Input length: {len(text)}")
        print(f"  Output length: {len(result)}")
        print(f"  Time: {elapsed:.4f}s")
        print(f"  Compression: {100 * (1 - len(result)/len(text)):.1f}%")
        print()


if __name__ == "__main__":
    # Run standard tests
    success = run_tests()
    
    # Run stress tests
    stress_test()
    
    exit(0 if success else 1)