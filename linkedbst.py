"""
File: linkedbst.py
Author: Ken Lambert
"""
import random
import time
from math import log
from abstractcollection import AbstractCollection
from bstnode import BSTNode
from linkedstack import LinkedStack


class LinkedBST(AbstractCollection):
    """An link-based binary search tree implementation."""

    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._root = None
        AbstractCollection.__init__(self, sourceCollection)

    # Accessor methods
    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""

        def recurse(node, level):
            string = ""
            if node is not None:
                string += recurse(node.right, level + 1)
                string += "| " * level
                string += str(node.data) + "\n"
                string += recurse(node.left, level + 1)
            return string

        return recurse(self._root, 0)

    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right is not None:
                    stack.push(node.right)
                if node.left is not None:
                    stack.push(node.left)

    def preorder(self):
        """Supports a preorder traversal on a view of self."""
        return None

    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        lyst = list()

        def recurse(node):
            if node is not None:
                recurse(node.left)
                lyst.append(node.data)
                recurse(node.right)

        recurse(self._root)
        return iter(lyst)

    def postorder(self):
        """Supports a postorder traversal on a view of self."""
        return None

    def levelorder(self):
        """Supports a levelorder traversal on a view of self."""
        return None

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) is not None

    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""

        current_node = self._root

        while current_node is not None:
            if item == current_node.data:
                return current_node.data
            elif item < current_node.data:
                current_node = current_node.left
            else:
                current_node = current_node.right
        return None

    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    def add(self, item):
        """Adds item to the tree."""

        if self.isEmpty():
            self._root = BSTNode(item)
            self._size += 1
            return

        current_node = self._root
        parent = None
        direction = None

        while current_node is not None:
            parent = current_node
            if item < current_node.data:
                current_node = current_node.left
                direction = 'L'
            else:
                current_node = current_node.right
                direction = 'R'

        new_node = BSTNode(item)
        if direction == 'L':
            parent.left = new_node
        else:
            parent.right = new_node

        self._size += 1

    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if not item in self:
            raise KeyError("Item not in tree.""")

        # Helper function to adjust placement of an item
        def remove_helper(top):
            # Replace top's datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top's left subtree
            #       has been removed
            # Post: top.data = maximum value in top's left subtree
            parent = top
            current_node = top.left
            while not current_node.right is None:
                parent = current_node
                current_node = current_node.right
            top.data = current_node.data
            if parent == top:
                top.left = current_node.left
            else:
                parent.right = current_node.left

        # Begin main part of the method
        if self.isEmpty():
            return None

        # Attempt to locate the node containing the item
        item_removed = None
        pre_root = BSTNode(None)
        pre_root.left = self._root
        parent = pre_root
        direction = 'L'
        current_node = self._root
        while not current_node is None:
            if current_node.data == item:
                item_removed = current_node.data
                break
            parent = current_node
            if current_node.data > item:
                direction = 'L'
                current_node = current_node.left
            else:
                direction = 'R'
                current_node = current_node.right

        # Return None if the item is absent
        if item_removed is None:
            return None

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximium node in the left subtree
        if not current_node.left is None \
                and not current_node.right is None:
            remove_helper(current_node)
        else:

            # Case 2: The node has no left child
            if current_node.left is None:
                new_child = current_node.right

                # Case 3: The node has no right child
            else:
                new_child = current_node.left

                # Case 2 & 3: Tie the parent to the new child
            if direction == 'L':
                parent.left = new_child
            else:
                parent.right = new_child

        # All cases: Reset the root (if it hasn't changed no harm done)
        #            Decrement the collection's size counter
        #            Return the item
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = pre_root.left
        return item_removed

    def replace(self, item, new_item):
        """
        If item is in self, replaces it with newItem and
        returns the old item, or returns None otherwise."""
        probe = self._root
        while probe is not None:
            if probe.data == item:
                old_data = probe.data
                probe.data = new_item
                return old_data
            elif probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None

    def height(self):
        '''
        Return the height of tree
        :return: int
        '''
        def height1(top: BSTNode):
            '''
            Helper function
            :param top:
            :return:
            '''
            if top is None:
                return -1
            right_top = height1(top.right)
            left_top = height1(top.left)
            return 1 + max(right_top, left_top)
        if self._root is None:
            return 0
        return height1(self._root)

    def is_balanced(self):
        '''
        Return True if tree is balanced
        :return:
        '''
        def count_vert(top: BSTNode):
            if top is None:
                return 0
            return 1 + count_vert(top.left) + count_vert(top.right)

        return 2 * log(count_vert(self._root)+1, 2) - 1 > self.height()

    def range_find(self, low, high):
        '''
        Returns a list of the items in the tree, where low <= item <= high."""
        :param low:
        :param high:
        :return:
        '''
        res = []
        def append_vert(top: BSTNode, low, high):
            if low <= top.data <= high:
                res.append(top)
            if top.left is not None:
                append_vert(top.left, low, high)
            if top.right is not None:
                append_vert(top.right, low, high)
        append_vert(self._root, low, high)
        return [elem.data for elem in res]

    def rebalance(self, inorder = None):
        '''
        Rebalances the tree.
        :return:
        '''
        if inorder is None:
            inorder = list(self.inorder())
        self.clear()
        def divide_tree(lst):
            if lst:
                len_lst = len(lst)
                top_ind = len_lst//2
                self.add(lst[top_ind])
                divide_tree(lst[:top_ind])
                divide_tree(lst[1+top_ind:])
        return divide_tree(inorder)

    def successor(self, item: int):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        def successor1(top):
            if top is None:
                return None
            if top.data > item:
                left_top = successor1(top.left)
                if left_top is not None:
                    return left_top
                return top
            return successor1(top.right)
        res = successor1(self._root)
        return res.data if res is not None else res

    def predecessor(self, item):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        def predecessor1(top):
            if top is None:
                return None
            if top.data < item:
                right_top = predecessor1(top.right)
                if right_top is not None:
                    return right_top
                return top
            return predecessor1(top.left)
        res = predecessor1(self._root)
        return res.data if res is not None else res

    def demo_bst(self, path):
        """
        Demonstration of efficiency binary search tree for the search tasks.
        :param path:
        :type path:
        :return:
        :rtype:
        """
        with open(path, 'r', encoding='utf-8') as file:
            words = file.readlines()
        words_num = len(words)
        words_to_find = []
        for _ in range(10000):
            ind = random.randint(0, words_num-1)
            words_to_find.append(words[ind])

        print(f'Test start\nSearch time(in seconds) for 10000 random words in list/\
tree with {words_num} elements\n')
        start = time.time()
        for word in words_to_find:
            if word in words:
                continue
        end = time.time()
        print('List:', round(end-start, 2))

        sorted_tree = LinkedBST(words)
        rebalanced_tree = LinkedBST()
        rebalanced_tree.rebalance(words)
        unsorted_tree = LinkedBST()
        while words:
            ind = random.randint(0, len(words)-1)
            unsorted_tree.add(words[ind])
            words.pop(ind)

        start = time.time()
        for word in words_to_find:
            sorted_tree.find(word)
        end = time.time()
        print('Sorted binary search tree:', round(end-start, 2))

        start = time.time()
        for word in words_to_find:
            unsorted_tree.find(word)
        end = time.time()
        print('Unsorted binary search tree:', round(end-start, 2))

        start = time.time()
        for word in words_to_find:
            rebalanced_tree.find(word)
        end = time.time()
        print('Rebalanced binary search tree:',round(end-start, 2))
        print('\nTest end')


if __name__ == '__main__':
    tree = LinkedBST()
    tree.demo_bst('words50k.txt')
