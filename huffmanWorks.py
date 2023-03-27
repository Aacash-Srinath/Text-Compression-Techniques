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


# utility function to print characters along with
# their huffman value
def printCodes(root, str):
    if root is None:
        return
    if root.data != '$':
        print(root.data, ":", str)
    printCodes(root.left, str + "0")
    printCodes(root.right, str + "1")


# utility function to store characters along with
# their huffman value in a hash table
def storeCodes(root, str):
    if root is None:
        return
    if root.data != '$':
        codes[root.data] = str
    storeCodes(root.left, str + "0")
    storeCodes(root.right, str + "1")


# function to build the Huffman tree and store it
# in minHeap
def HuffmanCodes():
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
def calcFreq(str):
    for i in str:
        freq[i] += 1


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

    with open("output.txt", "wb") as key:
        key.write(k2)


def read_file():
    with open("output.txt", "rb") as key:
        toDecode = key.read()
    huffCode = "".join([f"{int(bin(i).replace('0b', '')):08d}" for i in list(toDecode)])
    i = 0
    while True:
        i += 1
        if huffCode[i - 1] == '1':
            break
    return huffCode[i:]


# Driver code
if __name__ == "__main__":
    minHeap = []
    inputFile = "SampleTextFiles/words200/file1.txt"
    with open(inputFile, 'r') as file:
        str = file.read()

    encodedString, decodedString = "", ""
    calcFreq(str)
    HuffmanCodes()
    # print("Character With their Frequencies:")
    # for key in sorted(codes):
    #     print(key, codes[key])

    for i in str:
        encodedString += codes[i]

    # print("\nEncoded Huffman data:")
    # print(encodedString)

    write_file('1' + encodedString)

    input_file_size = os.path.getsize(inputFile)
    print("Input file size is: ", input_file_size, "bytes")
    output_file_size = os.path.getsize('output.txt')
    print("Output file size is: ", output_file_size, "bytes")

    # Function call
    huffCode = read_file()
    decodedString = decode_file(minHeap[0], huffCode)
    # print("\nDecoded Huffman Data:")
    # print(decodedString)
