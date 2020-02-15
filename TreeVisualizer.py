import tkinter as tk
from win32api import GetSystemMetrics

def TreeDepth(node,depth=0):
    '''
    Helper function which calculates the depth of the tree, starting from the input node
    '''
    if node.children == [None,None]:
        return depth
    else:
        depth1 = TreeDepth(node.children[0],depth+1)
        depth2 = TreeDepth(node.children[1],depth+1)
        return max(depth1,depth2)

class TreeVisualizer():
    '''
    GUI class which draw an interactive Huffman Coding tree
    '''
    def __init__(self,root,screenWidth=None,screenHeight=None):
        self.displayLevels = 4 # number of tree nodes to display on screen
        # window and font sizes adapt to the screen resolution/input parameters
        self.HEIGHT = int(GetSystemMetrics(1)*0.8) if screenHeight==None else screenHeight
        self.WIDTH = int(GetSystemMetrics(0)*0.8) if screenWidth==None else screenWidth
        self.nodeFontSize = int(self.WIDTH/100*1)
        self.treeRoot = root
        # Create GUI:
        self.root = tk.Tk()
        self.root.resizable(False, False)
        self.root.title("Tree Visualizer")
        self.MakeTreeFrame()
        self.root.mainloop()
    def NodeButtonCallback(self,node):
        if node.char==None:
            self.treeRoot=node
            self.SetupCurrentBranches()
    def BackButtonCallback(self):
        for _ in range(self.displayLevels):
            self.treeRoot = self.treeRoot.parent
            if self.treeRoot.parent==None:
                break
        self.SetupCurrentBranches()
    def MakeTreeFrame(self):
        self.dx = int(self.WIDTH/4.1)
        self.dy = int(self.HEIGHT/(self.displayLevels+1.5))
        self.treeCanvas = tk.Canvas(self.root,height=self.HEIGHT,width=self.WIDTH,bg='white')
        self.SetupCurrentBranches()
        self.treeCanvas.pack()
    def SetupCurrentBranches(self):
        self.treeCanvas.delete("all")
        self.MakeTree(0,self.treeRoot,int(self.WIDTH/2),10)
        depthLabel = tk.Label(self.root,text = 'Remaining Depth\n'+str(TreeDepth(self.treeRoot)),bg='dodgerblue1',font=("Calibri",self.nodeFontSize))
        depthLabel = self.treeCanvas.create_window(self.WIDTH-20, 20, anchor=tk.NE, window=depthLabel)
        backButton = tk.Button(self.root, text = 'Back', anchor = tk.N, command=lambda :self.BackButtonCallback(),bg='dodgerblue1',font=("Calibri",self.nodeFontSize))
        backButton = self.treeCanvas.create_window(20, 20, anchor=tk.NW, window=backButton)
    def MakeTree(self,level,node,x,y):
        if level>self.displayLevels or node==None:
            return
        if node.char: buttonText = node.char +'\n' + str(node.value)
        else:         buttonText = node.value
        nodeButton = tk.Button(self.root, text = buttonText, anchor = tk.CENTER,bg="skyblue1",
                           command=lambda :self.NodeButtonCallback(node),width=3,font=("Calibri",self.nodeFontSize))
        nodeButton = self.treeCanvas.create_window(x, y, anchor=tk.N, window=nodeButton,width=self.nodeFontSize*4)
        if node.children!=[None,None]: # as long as there are more children, draw arrows
            y0 = self.nodeFontSize*2
            x1 = x+self.dx/2**level
            x2 = x-self.dx/2**level
            self.treeCanvas.create_line(x, y+y0, x1, y+self.dy, arrow=tk.LAST)
            self.MakeTree(level+1,node.children[0],x1,y+self.dy)
            self.treeCanvas.create_line(x, y+y0, x2, y+self.dy, arrow=tk.LAST)
            self.MakeTree(level+1,node.children[1],x2,y+self.dy)


if __name__=="__main__":
    import HuffmanCoding as hc
    with open("heart_of_darkness.txt", "rb") as f:
        text = f.read()
    text = text.decode()
    textPartial = text[:20000]
    freqDict = hc.GetFrequency(textPartial)
    hctRoot = hc.HuffmanCodingTree(freqDict)
    tv = TreeVisualizer(hctRoot)
    
