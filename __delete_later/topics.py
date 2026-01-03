"""
Topic Definitions for CS 221
Clear, simple topic information
"""

from typing import Dict
from dataclasses import dataclass


@dataclass
class Topic:
    """Represents a CS 221 topic"""
    name: str
    concept: str  # Brief explanation of the concept
    key_points: list[str]  # Key things students should understand
    

TOPICS: Dict[str, Topic] = {
    'queue': Topic(
        name='Queue',
        concept='A Queue is a First-In-First-Out (FIFO) data structure where elements are added at the back and removed from the front.',
        key_points=[
            'FIFO ordering: first element added is first element removed',
            'Two main operations: enqueue (add to back) and dequeue (remove from front)',
            'Common uses: task scheduling, breadth-first search, handling requests',
            'Java implementation: Queue interface, LinkedList, ArrayDeque'
        ]
    ),
    
    'stack': Topic(
        name='Stack',
        concept='A Stack is a Last-In-First-Out (LIFO) data structure where elements are added and removed from the same end (the top).',
        key_points=[
            'LIFO ordering: last element added is first element removed',
            'Two main operations: push (add to top) and pop (remove from top)',
            'Common uses: undo functionality, function call stack, backtracking',
            'Java implementation: Stack class, Deque interface'
        ]
    ),
    
    'linked-list': Topic(
        name='Linked List',
        concept='A Linked List is a linear data structure where elements (nodes) are connected via pointers, not stored contiguously.',
        key_points=[
            'Each node contains data and a reference to the next node',
            'Dynamic size: can grow or shrink easily',
            'Efficient insertion/deletion at beginning or middle',
            'Java implementation: LinkedList class, custom Node classes'
        ]
    ),
    
    'binary-search': Topic(
        name='Binary Search',
        concept='Binary Search is an efficient algorithm for finding an element in a sorted array by repeatedly dividing the search space in half.',
        key_points=[
            'Only works on sorted data',
            'O(log n) time complexity - much faster than linear search',
            'Repeatedly compares with middle element and eliminates half',
            'Java implementation: Arrays.binarySearch(), custom recursive/iterative'
        ]
    ),
    
    'recursion': Topic(
        name='Recursion',
        concept='Recursion is when a method calls itself to solve a problem by breaking it into smaller subproblems.',
        key_points=[
            'Must have a base case to stop recursion',
            'Each recursive call works on a smaller version of the problem',
            'Common uses: tree traversal, divide-and-conquer algorithms',
            'Stack overflow risk if base case is wrong or never reached'
        ]
    )
}


def get_topic(topic_key: str) -> Topic:
    """Get a topic by key"""
    if topic_key not in TOPICS:
        raise ValueError(f"Topic '{topic_key}' not found. Available: {list(TOPICS.keys())}")
    return TOPICS[topic_key]


def get_all_topic_names() -> list[str]:
    """Get list of all topic keys"""
    return list(TOPICS.keys())
