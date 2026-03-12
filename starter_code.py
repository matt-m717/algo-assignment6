"""
Dynamic Programming Assignment - Longest Common Subsequence
Implement three versions: naive recursive, memoization, and tabulation.
"""

import json
import time


# ============================================================================
# PART 1: NAIVE RECURSIVE SOLUTION
# ============================================================================

def lcs_recursive(seq1, seq2):
    if not seq1 or not seq2:
        return 0

    if seq1[-1] == seq2[-1]:
        return 1 + lcs_recursive(seq1[:-1], seq2[:-1])
    else:
        option1 = lcs_recursive(seq1[:-1], seq2)
        option2 = lcs_recursive(seq1, seq2[:-1])
        return max(option1, option2)

# ============================================================================
# PART 2: MEMOIZATION (TOP-DOWN WITH CACHING)
# ============================================================================

def lcs_memoization(seq1, seq2):
    cache = {}
    i = len(seq1)
    j = len(seq2)

    if (i, j) in cache:
        return cache[(i, j)]

    if not seq1 or not seq2:
        return 0

    if seq1[i-1] == seq2[-1]:
        result = 1 + lcs_recursive(seq1[:-1], seq2[:-1])
    else:
        option1 = lcs_recursive(seq1[:-1], seq2)
        option2 = lcs_recursive(seq1, seq2[:-1])
        result = max(option1, option2)
    cache[(i, j)] = result
    return result

# ============================================================================
# PART 3: TABULATION (BOTTOM-UP WITH TABLE)
# ============================================================================

def lcs_tabulation(seq1, seq2):
    i = len(seq1)
    j = len(seq2)

    table = [[0 for _ in range(j+1)] for _ in range(i+1)]

    for k in range(1, i+1):
        for l in range(1, j+1):
            if seq1[k-1] == seq2[l-1]:
                table[k][l] = 1 + table[k-1][l-1]
            else:
                table[k][l] = max(table[k-1][l], table[k][l-1])
    return table[i][j]

# ============================================================================
# TESTING & TIMING
# ============================================================================

def load_sequence(filename):
    """Load DNA sequence from JSON file."""
    with open(f"sequences/{filename}", "r") as f:
        return json.load(f)


def test_small_cases():
    """Test all implementations on small known cases."""
    print("="*70)
    print("TESTING ON SMALL CASES")
    print("="*70 + "\n")
    
    test_cases = [
        ("AGGTAB", "GXTXAYB", 4),  # LCS: GTAB
        ("ABCDGH", "AEDFHR", 3),   # LCS: ADH
        ("ABC", "AC", 2),           # LCS: AC
        ("", "ABC", 0),             # LCS: empty
    ]
    
    for seq1, seq2, expected in test_cases:
        print(f"Test: '{seq1}' vs '{seq2}'")
        print(f"  Expected LCS length: {expected}")
        
        # Test recursive
        try:
            result = lcs_recursive(seq1, seq2)
            status = "✓ PASS" if result == expected else "✗ FAIL"
            print(f"  Recursive: {result} {status}")
        except Exception as e:
            print(f"  Recursive: ERROR - {str(e)}")
        
        # Test memoization
        try:
            result = lcs_memoization(seq1, seq2)
            status = "✓ PASS" if result == expected else "✗ FAIL"
            print(f"  Memoization: {result} {status}")
        except Exception as e:
            print(f"  Memoization: ERROR - {str(e)}")
        
        # Test tabulation
        try:
            result = lcs_tabulation(seq1, seq2)
            status = "✓ PASS" if result == expected else "✗ FAIL"
            print(f"  Tabulation: {result} {status}")
        except Exception as e:
            print(f"  Tabulation: ERROR - {str(e)}")
        
        print()


def time_recursive():
    """Time the recursive solution on progressively larger inputs."""
    print("\n" + "="*70)
    print("TIMING RECURSIVE SOLUTION")
    print("="*70 + "\n")
    print("WARNING: Recursive solution will become very slow!\n")
    
    sizes = [10, 20, 50]  # Keep small to avoid infinite wait
    
    for size in sizes:
        data = load_sequence(f"dna_{size}.json")
        seq1 = data["sequence1"]
        seq2 = data["sequence2"]
        
        print(f"Sequence length: {size}")
        
        start = time.perf_counter()
        result = lcs_recursive(seq1, seq2)
        elapsed = time.perf_counter() - start
        
        print(f"  LCS length: {result}")
        print(f"  Time: {elapsed:.4f} seconds\n")
        
        if elapsed > 5.0:
            print("  Stopping - recursive is too slow for larger inputs!\n")
            break


def compare_all_approaches():
    """Compare all three approaches on sequences of increasing size."""
    print("\n" + "="*70)
    print("COMPARING ALL APPROACHES")
    print("="*70 + "\n")
    
    sizes = [10, 20, 50, 100, 200, 500, 1000]
    
    print(f"{'Size':<10} {'Recursive':<15} {'Memoization':<15} {'Tabulation':<15}")
    print("-" * 70)
    
    for size in sizes:
        data = load_sequence(f"dna_{size}.json")
        seq1 = data["sequence1"]
        seq2 = data["sequence2"]
        
        times = {"size": size}
        
        # Recursive (skip if too large)
        if size <= 20:
            try:
                start = time.perf_counter()
                lcs_recursive(seq1, seq2)
                times["recursive"] = time.perf_counter() - start
            except:
                times["recursive"] = None
        else:
            times["recursive"] = None
        
        # Memoization
        try:
            start = time.perf_counter()
            lcs_memoization(seq1, seq2)
            times["memoization"] = time.perf_counter() - start
        except:
            times["memoization"] = None
        
        # Tabulation
        try:
            start = time.perf_counter()
            lcs_tabulation(seq1, seq2)
            times["tabulation"] = time.perf_counter() - start
        except:
            times["tabulation"] = None
        
        # Print results
        rec_str = f"{times['recursive']:.4f}s" if times['recursive'] else "Too slow"
        mem_str = f"{times['memoization']:.4f}s" if times['memoization'] else "ERROR"
        tab_str = f"{times['tabulation']:.4f}s" if times['tabulation'] else "ERROR"
        
        print(f"{size:<10} {rec_str:<15} {mem_str:<15} {tab_str:<15}")


if __name__ == "__main__":
    print("DYNAMIC PROGRAMMING ASSIGNMENT - STARTER CODE")
    print("Implement the LCS functions above, then run tests.\n")
    
    # Uncomment these as you complete each part:
    
    test_small_cases()
    # time_recursive()
    # compare_all_approaches()
    
    print("\n⚠ Uncomment the test functions in the main block to run tests!")