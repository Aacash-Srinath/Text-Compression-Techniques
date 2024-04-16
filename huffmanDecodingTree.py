import heapq
from collections import defaultdict
import os 

 
# to map each character its huffman value
codes = {}

# To store the frequency of character of the input data
freq = defaultdict(int)

# A Huffman tree node
class MinHeapNode:
	def __init__(self, data, freq):
		self.left = None
		self.right = None
		self.data = data
		self.freq = freq

	def __lt__(self, other):
		return self.freq < other.freq
	
	def display(self):
		lines, *_ = self._display_aux()
		for line in lines:
			print(line)

	def _display_aux(self):
		"""Returns list of strings, width, height, and horizontal coordinate of the root."""
		# No child.
		if self.right is None and self.left is None:
			line = '%s' % self.data
			width = len(line)
			height = 1
			middle = width // 2
			return [line], width, height, middle

		# Only left child.
		if self.right is None:
			lines, n, p, x = self.left._display_aux()
			s = '%s' % self.key
			u = len(s)
			first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s
			second_line = x * ' ' + '/' + (n - x - 1 + u) * ' '
			shifted_lines = [line + u * ' ' for line in lines]
			return [first_line, second_line] + shifted_lines, n + u, p + 2, n + u // 2

		# Only right child.
		if self.left is None:
			lines, n, p, x = self.right._display_aux()
			s = '%s' % self.key
			u = len(s)
			first_line = s + x * '_' + (n - x) * ' '
			second_line = (u + x) * ' ' + '\\' + (n - x - 1) * ' '
			shifted_lines = [u * ' ' + line for line in lines]
			return [first_line, second_line] + shifted_lines, n + u, p + 2, u // 2

		# Two children.
		left, n, p, x = self.left._display_aux()
		right, m, q, y = self.right._display_aux()
		s = '%s' % self.data
		u = len(s)
		first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s + y * '_' + (m - y) * ' '
		second_line = x * ' ' + '/' + (n - x - 1 + u + y) * ' ' + '\\' + (m - y - 1) * ' '
		if p < q:
			left += [n * ' '] * (q - p)
		elif q < p:
			right += [m * ' '] * (p - q)
		zipped_lines = zip(left, right)
		lines = [first_line, second_line] + [a + u * ' ' + b for a, b in zipped_lines]
		return lines, n + m + u, max(p, q) + 2, n + u // 2


# utility function to print characters along with
# there huffman value
def printCodes(root, str):
	if root is None:
		return
	if root.data != '$':
		print(root.data, ":", str)
	printCodes(root.left, str + "0")
	printCodes(root.right, str + "1")

# utility function to store characters along with
# there huffman value in a hash table
def storeCodes(root, str):
	if root is None:
		return
	if root.data != '$':
		codes[root.data] = str
	storeCodes(root.left, str + "0")
	storeCodes(root.right, str + "1")

# function to build the Huffman tree and store it
# in minHeap
def HuffmanCodes(size):
	global minHeap
	for key in freq:
		minHeap.append(MinHeapNode(key, freq[key]))
	heapq.heapify(minHeap)
	while len(minHeap) != 1:
		left = heapq.heappop(minHeap)
		right = heapq.heappop(minHeap)
		top = MinHeapNode('$', left.freq + right.freq)
		top.left = left
		top.right = right
		heapq.heappush(minHeap, top)
	storeCodes(minHeap[0], "")

# utility function to store map each character with its
# frequency in input string
def calcFreq(str, n):
	for i in range(n):
		freq[str[i]] += 1

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

# def compress_file(input_file_path, output_file_path):
#     with open(input_file_path, "r") as input_file:
#         text = input_file.read()
#     codes = compress(text)
#     with open(output_file_path, "w") as output_file:
#         for code in codes:
#             output_file.write(str(code) + " ")
		


def write_file(encodedString):
	codeCopy = int(encodedString, 2)
	hexCode = []
	while codeCopy:
		hexCode.insert(0, codeCopy % 256)
		codeCopy //= 256

	k2 = bytes(hexCode)


def read_file():
	with open(r"SampleTextFiles/outout.txt", "rb") as key:
		toDecode = key.read()
	huffCode = "".join([f"{int(bin(i).replace('0b', '')):08d}" for i in list(toDecode)])
	i = 0
	while True:
		i += 1
		if huffCode[i-1]=='1':
			break
	return huffCode[i:]

def print_tree(node, level=0):
	if node != None:
		print_tree(node.right, level + 1)
		print(' ' * 4 * level + '->', node.data)
		print_tree(node.left, level + 1)
	
# Driver code
if __name__ == "__main__":
	minHeap = []
	str = ""
	inputFile = open(r"SampleTextFiles/words200/file1.txt", "r")

	for line in inputFile:
		str += line
	encodedString, decodedString = "", ""
	calcFreq(str, len(str))
	HuffmanCodes(len(str))
	# print("Character With there Frequencies:")
	# for key in sorted(codes):
	# 	print(key, codes[key])

	val = list(codes.values())
	car= list(codes.keys())
	

	tre=''+val[0]+car[0]
	for i in range (1,len(val)):
		fir=val[i-1]
		now=val[i]
		if (len(now)>len(fir)):
			tre+='0'*(len(now)-len(fir))
		tre+=car[i]

	# print(tre)

	cods={}

	i=0
	cod=''
	while(i<len(tre)):
		if(tre[i]=='0'):
			cod+='0'
	
		elif (tre[i]=='1' ):
			i+=1
			cods[tre[i]]=cod

			if (tre[i-1]!='0'):
				
				if (cod[-1]=='0'):
					cod=cod[:-1]+'1'

				while (cod[-1]=='1' and ('0' in cod)):
					cod=cod[:-1]
				
			# print(cod)	


		i+=1
	# print((cods))
	# print((codes))
	# print(codes['s'])
	# print(cods['s'])
	
	with open(r"SampleTextFiles/words200/tre.txt", "w") as key:
		key.write(tre)

	for i in str:
		encodedString += codes[i]

	# print("\nEncoded Huffman data:")
	# print(encodedString)

	write_file('1'+encodedString)

	input_file_size = os.path.getsize(r"SampleTextFiles/words200/file1.txt")
	print("Input file size is: ", input_file_size, "bytes")
	output_file_size = os.path.getsize((r"SampleTextFiles/outout.txt"))
	# print("Output file size is: ", output_file_size, "bytes")
	tree_file_size = os.path.getsize((r"SampleTextFiles/tre.txt"))
	# print("tree file size is: ", tree_file_size, "bytes")
	print("Total Output file size is: ", output_file_size+tree_file_size, "bytes")

	# Function call
	huffCode = read_file()
	decodedString = decode_file(minHeap[0], huffCode)
	# print("\nDecoded Huffman Data:")
	# print(decodedString)


	print(tre)
	print(minHeap)
	minHeap[0].display()