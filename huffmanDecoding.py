import heapq
from collections import defaultdict
import os 
 
# A Huffman tree node
class MinHeapNode:
	def __init__(self, data, freq):
		self.left = None
		self.right = None
		self.data = data
		self.freq = freq

	def __lt__(self, other):
		return self.freq < other.freq
	
# function iterates through the encoded string s
# if s[i]=='1' then move to node->right
# if s[i]=='0' then move to node->left
# if leaf node append the node->data to our output string
def decode_file(root, s):
	ans = ""
	curr = root
	n = len(s)
	for i in range(n):
		if s[i] == '0':
			curr = curr.left
		else:
			curr = curr.right

		# reached leaf node
		if curr.left is None and curr.right is None:
			ans += curr.data
			curr = root
	return ans + '\0'

