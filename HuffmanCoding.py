#Huffman Coding - Greedy Algorithm
from functools import reduce

def SortDictionary(dictionary):
    '''Sort a dictionary by values'''
    return {k: v for k, v in sorted(dictionary.items(), key=lambda item: item[1])}

def GetFrequency(data):
    '''
    This function takes a text data string and creates a frequency dictionary
    of the form 
    Input: character string
    Output: a dictionary of the form {character:frequency}
    '''
    freqDict = {}
    for c in data:
        if c not in freqDict:
            freqDict[c] = 1
        else:
            freqDict[c]+=1
    return freqDict


class Node():
    '''
    The Huffman Tree consists of these nodes, which contain both the frequency and character (if available)
    '''
    def __init__(self,value=None,char=None):
        self.value = value
        self.char = char
        self.parent = None
        self.children = [None, None]
    def Connect2(self,n1,n2):
        '''
        This function connects two children nodes n1,n2 to the current node.
        For consistency with other functions, n2.value must be greater or equal than n1.value
        '''
        assert(n2.value>=n1.value)
        self.value = n1.value+n2.value
        n1.parent ,n2.parent= self, self
        self.children = [n1,n2]

def HuffmanCodingTree(freqDict):
    '''
    This function builds a Huffman Coding tree of Nodes
    Input: dictionary of the form {character:frequency}
    Output: root node of the tree
    '''
    leafNodesList=[] # This list stores leaf nodes, which contain characters
    internalNodesList=[] # This list stores internal nodes, which serve as parents to other nodes
    sortedDictionary = SortDictionary(freqDict) # The dictionary must be sorted (lower values first)
    for k,v in sortedDictionary.items():
        leafNodesList.append(Node(v,k))

    while True:
        if not leafNodesList and len(internalNodesList)==1:
            # When only one last node is left in the internal nodes array, that is the root of the tree
            root = internalNodesList[0]
            return root

        # Create a list of candidates for lowest values - 2 at most from each list (internal/leaf)
        # A 'candidate' stores a node and its respective list
        candidates = []
        for i in internalNodesList[:2]:
            candidates.append([i,internalNodesList])
        for j in leafNodesList[:2]:
            candidates.append([j,leafNodesList])
        candidates.sort(key= lambda x: x[0].value) # Sort the candidates by value - lowest first
        # Keep the 2 candidates with the lowest values, then pop them out of their respective lists
        n1 = candidates[0][0]
        candidates[0][1].pop(0)
        n2 = candidates[1][0]
        candidates[1][1].pop(0)
        # Create a parent node (internal) to the candidates and put it last in the internal list
        # This keeps the internal list also sorted (ascending) since the 2 child values summed are larger at every iteration 
        newNode = Node()
        newNode.Connect2(n1,n2)
        internalNodesList.append(newNode)
    
def MakeCodesDict(node,code,codesDict):
    '''
    This regression function creates a Huffman encoding dictionary out of a tree
    Input:
        node - current node in tree (initially the root)
        code - encoding up to current place in tree
        codesDict - Huffman encoding dictionary (initially an empty dictionary)
    
    '''
    if node.children == [None,None]:
        codesDict[node.char]=code
    else:
        MakeCodesDict(node.children[0],code+'0',codesDict) # traveling to the smaller value add 0
        MakeCodesDict(node.children[1],code+'1',codesDict) # traveling to the larger value add 1
        
def EncodeText(text,codesDict):
    '''
    This function encodes a given text, using the provided encoding dictionary
    Input:
        text: a string
        codesDict: (Huffman) encoding dictionary
    Output: encoded text, a string of '1's and '0's
    '''
    encoded = ''
    for c in text:
        encoded+=codesDict[c]
    return encoded

def DecodeText(text,hctRoot):
    '''
    This function decodes a Huffman encoded text, using the respective Huffman tree
    Input:
        text: a string of '1's and '0' encoded with a dictionary created from the provided tree
        hct: Huffman Coding Tree root node
    Output: decoded text string
    '''
    decoded = ''
    currentNode = hctRoot
    for n in text:
        currentNode = currentNode.children[int(n)]
        if currentNode.children ==[None,None]:
            decoded+=currentNode.char
            currentNode = hctRoot
    return decoded
if __name__ =="__main__":
    with open("heart_of_darkness.txt", "rb") as f:
        text = f.read()

    text = text.decode()

    compList = []

    chars = list(range(1000,15000,500))
    for n in chars:
        textPartial = text[:n]
        binText = bin(reduce(lambda x, y: 256*x+y, (ord(c) for c in textPartial), 0))

        freqDict = GetFrequency(textPartial)
        hctRoot = HuffmanCodingTree(freqDict)

        codesDict = {}
        MakeCodesDict(hctRoot,'',codesDict)

        huffmanText = EncodeText(textPartial,codesDict)


        decoded = DecodeText(huffmanText,hctRoot)
            
        compression = ( 1-(len(huffmanText)/len(binText)) )*100
        compList.append(compression)

        print('Compression = {:.1f}%'.format(compression)) 

    import matplotlib.pyplot as plt

    plt.figure()
    plt.plot(chars,compList)
    plt.grid(True)
    plt.xlabel('Characters'); plt.ylabel('Compression Rate (%)')
    plt.show(block=False)
