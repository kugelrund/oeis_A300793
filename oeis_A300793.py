"""Functions for calculating entries of OEIS A300793

Functions for calculating entries of the sequence a(n), where a(n) is the n-th
derivative of arcsinh(1/x) at x=1 times (-2)^n/sqrt(2) for n >= 1. See
https://oeis.org/A300793.

A call of the form 'python oeisA300793.py [n]' prints the first n entries of
the sequence.
"""


def get_next_row_b(current_row):
    """Calculates the next row of b, given a current row of b

    Given a current row of the helper values b for the proven recursive
    formula for OEIS A300793 (https://oeis.org/A300793/a300793_2.pdf), this
    function calculates the next row of said values b.

    Args:
        current_row (list): A row of b, i.e. b(j,:)
    Returns:
        list: The next row b(j+1,:).
    """
    n = len(current_row)
    new_row = []
    new_row.append(-current_row[0] * n)
    for j in range(1, n):
        new_row.append(current_row[j] * (2*j - n) +
                       current_row[j-1] * (2*j - 3*n - 1))
    new_row.append(current_row[n-1] * (2*n - 3*n - 1))
    return new_row


def get_a_until(num):
    """Calculates a given number of entries of OEIS A300793

    Calculates a given number of entries with the proven recursive
    formula https://oeis.org/A300793/a300793_2.pdf.

    Args:
        num (int): The number of entries that shall be calculated.
    Returns:
        list: A list with the first 'num' entries of OEIS A300793.
    """
    b = [-1]
    a = []
    for n in range(1, num + 1):
        sign = (-1)**n
        a.append(sign * sum(b))
        b = get_next_row_b(b)
    return a


def get_unproven_a_until(num):
    """Calculates a given number of unproven entries for OEIS A300793

    Calculates a given number of entries of the recursive formula proposed by
    Martin Rubey (see https://oeis.org/A300793). The formula is assumed to give
    the sequence OEIS A300793, but this is yet to be proven.

    Args:
        num (int): The number of entries that shall be calculated.
    Returns:
        list: A list with the first 'num' entries of the recursive formula
              proposed by Martin Rubey.
    """
    if num <= 0:
        return []
    elif num == 1:
        return [1]
    elif num == 2:
        return [1, 3]
    a = [1, 3, 13]
    for n in range(3, num):
        # note the index shift in n due to python indexing starting at 0, while
        # the indexing in the definition of the sequence starts at 1
        a.append(4 * (n - 1)**2 * (n - 2) * a[n - 3] -
                 2 * (3*n - 2) * (n - 1) * a[n - 2] +
                 (4*n - 1) * a[n - 1])
    return a


if __name__ == "__main__":
    """Called from the command line with 'python oeisA300793.py [n]'. Prints the
    first n entries of OEIS A300793 and verifies the validity of the unproven
    formula up to that n.
    """
    import sys

    num = int(sys.argv[1])
    a = get_a_until(num)
    a_unproven = get_unproven_a_until(num)
    assert len(a) == len(a_unproven)

    for i in range(len(a)):
        print("a({0})={1}".format(i+1, a[i]))
        assert a[i] == a_unproven[i]
