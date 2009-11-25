#!/usr/bin/env python

""" General Functions to help music playing and composition"""

def gcd(a, b):
    """Return greatest common divisor using Euclid's Algorithm."""
    while b:      
        a, b = b, a % b
    return a

def lcm(a, b):
    """Return lowest common multiple."""
    return a * b // gcd(a, b)

def lcm_many(*args):
    """Return lcm of args."""   
    return reduce(lcm, args)

