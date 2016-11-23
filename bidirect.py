# -*- coding: utf-8 -*-
import collections
class Node:
    def __init__(self,freq):
        self.left = None
        self.right = None
        self.father = None
        self.freq = freq
    def isLeft(self):
        return self.father.left == self
#create nodes
def createNodes(freqs):
    return [Node(freq) for freq in freqs]
#create Huffman-Tree
def createHuffmanTree(nodes):
    queue = nodes[:]
    while len(queue) > 1:
        queue.sort(key=lambda item:item.freq)
        node_left = queue.pop(0)
        node_right = queue.pop(0)
        node_father = Node(node_left.freq + node_right.freq)
        node_father.left = node_left
        node_father.right = node_right
        node_left.father = node_father
        node_right.father = node_father
        queue.append(node_father)
    queue[0].father = None
    return queue[0]
#Huffman
def huffmanEncoding(nodes,root):
    codes = [''] * len(nodes)
    for i in range(len(nodes)):
        node_tmp = nodes[i]
        while node_tmp != root:
            if node_tmp.isLeft():
                codes[i] = '0' + codes[i]
            else:
                codes[i] = '1' + codes[i]
            node_tmp = node_tmp.father
    return codes
# Treating Frequence words build HuffmanTree,
# return HuffmanCode and a maxLen of the code
def dicHuff (nomFicher):
    dic = {}
    binfile = open(nomFicher, 'rb')
    f = binfile.read()
    for eachmot in f:
        if dic.has_key(eachmot):
            dic[eachmot] += 1
        else:
            dic[eachmot] = 1
    binfile.close()
    nodes = createNodes(dic[eachAlpha] for eachAlpha in dic)
    root = createHuffmanTree(nodes)
    codes = huffmanEncoding(nodes,root)
    print "dic of Frequency: ", dic
    print "codage: ",codes
    res = {}
    maxLen = 0
    i=0
    for ele in dic:
        res[ele]=codes[i]
        if len(codes[i])>maxLen:
            maxLen=len(codes[i])
        i+=1
    return [res,maxLen]

def arrToStr(arr):
    res =""
    for eachmot in arr:
        res +=eachmot
    return res
def severalZero(num):
    res = ""
    for i in range(num):
        res+="0"
    return res
def simulateXor(strA, strB):
    if strA=="1":
        a=True
    else:
        a=False
    if strB=="1":
        b=True
    else:
        b=False
    c= a^b
    if c == True:
        return "1"
    else:
        return "0"

def enCoder (nomFiche):
    huffCode = dicHuff(nomFiche)
    binfile = open(nomFiche, 'rb')
    #getCode
    code =[]
    f = binfile.read()
    for eachmot in f:
        code.append(huffCode[0][eachmot])
    binfile.close()
    #get reversedCode

    reversedCode = []
    for item in code:
        reversedCode.append(item[::-1])

    # print code
    # print reversedCode
    #add 0
    b = arrToStr(code)+severalZero(huffCode[1])
    bb = severalZero(huffCode[1])+arrToStr(reversedCode)

    c = ""
    for i in range(len(b)):
        c+=simulateXor(b[i],bb[i])
    print len(c)
    return [c,huffCode]

def invert_dict(d):
    return dict((v,k) for k,v in d.iteritems())

def simulerXorString (str1, str2):
    res = ""
    for i in range(len(str1)):
        res+=simulateXor(str1[i],str2[i])
    return res


#def decodeOneSign(readed,dict):


def decodeForward(c, huffman):
    dict = invert_dict(huffman[0])
    maxLen = huffman[1]
    pointer = maxLen
    readed = collections.deque(simulerXorString(severalZero(maxLen),c[0:pointer]))
    #print "read:",readed
    decoded = ""
    while (pointer < len(c)-maxLen or len(readed)>maxLen):
        tmp=""
        while (not dict.has_key(tmp)):
            tmp+=readed.popleft()
        newLen = len(tmp)
        decoded += dict[tmp]
        readed.extend(simulerXorString(tmp[::-1],c[pointer:pointer+newLen]))
        #print "read:",readed
        pointer+=newLen
    return decoded

def decodeBackward(c, huffman):
    dict = invert_dict(huffman[0])
    print "inverse dict:",dict
    maxLen = huffman[1]
    pointer = len(c)-maxLen
    readed = collections.deque(simulerXorString(severalZero(maxLen), c[-maxLen:]))
    print "read:",readed
    decoded = ""
    while (pointer > maxLen-1 or len(readed) > maxLen):
        tmp = ""
        while (not dict.has_key(tmp)):
            tmp += readed.pop()
        newLen = len(tmp)
        decoded += dict[tmp]
        s = simulerXorString(tmp, c[pointer - newLen:pointer])
        readed.extendleft(s[::-1])
        pointer -= newLen
    return decoded
if __name__ == '__main__':
    coded = enCoder("test.txt")
    print decodeForward(coded[0],coded[1])
    print decodeBackward(coded[0],coded[1])
