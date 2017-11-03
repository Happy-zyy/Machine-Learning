minSupport = 3   # 最小支持度


class treeNode:
    def __init__(self, nameValue, numOccur, parentNode):
        self.name = nameValue
        self.count = numOccur
        self.nodeLink = None
        self.parent = parentNode
        self.children = {}

    def inc(self, numOccur):
        self.count += numOccur



def loadSimpDat():
    simpDat = [['r', 'z', 'h', 'j', 'p'],
               ['z', 'y', 'x', 'w', 'v', 'u', 't', 's'],
               ['z'],
               ['r', 'x', 'n', 'o', 's'],
               ['y', 'r', 'x', 'z', 'q', 't', 'p'],
               ['y', 'r', 'x', 'z', 'q', 't', 'p'],
               ['y', 'z', 'x', 'e', 'q', 's', 't', 'm']]
    return simpDat


def createInitSet(dataSet):
    retDict = {}
    for trans in dataSet:
        if frozenset(trans) in retDict:
            retDict[frozenset(trans)] += 1
        else:
            retDict[frozenset(trans)] = 1
    return retDict

def createTree(dataSet):
    headerTable = {}
    for item in dataSet:  #第一次遍历：构造所有项出现次数的字典
        for e in item:
            headerTable[e] = dataSet[item] + headerTable.get(e,0)

    tmpList = []
    for key in headerTable.keys():     # 剔除非频繁项
        if headerTable[key] < minSupport:
            tmpList.append(key)
    for key in tmpList:
        del(headerTable[key])
    freqItemSet = set(headerTable.keys())

    if len(freqItemSet) == 0:return None,None

    for k in headerTable:  # 增加一个数据项，用于存放指向相似元素项指针
        headerTable[k] = [headerTable[k],None]
    retTree = treeNode('Null Set', 1, None)  # 根节点

    # 第二次遍历数据集，创建FP树
    for tranSet, count in dataSet.items():
        localD = {} # 对一个项集tranSet，记录其中每个元素项的全局频率，用于排序
        for item in tranSet:
            if item in freqItemSet:
                localD[item] = headerTable[item][0] # 注意这个[0]，因为之前加过一个数据项
        if len(localD) > 0:
            print(localD)
            orderedItems = [v[0] for v in sorted(localD.items(), key=lambda p: (-p[1],p[0]))] # 排序 按（值降序，值升序）排序
            print(orderedItems)
            updateTree(orderedItems, retTree, headerTable,count) # 更新FP树
    return retTree, headerTable


def updateTree(items, inTree, headerTable, count):
    if items[0] in inTree.children:
        # 有该元素项时计数值+count
        inTree.children[items[0]].inc(count)
    else:
        # 没有这个元素项时创建一个新节点
        inTree.children[items[0]] = treeNode(items[0], count, inTree)
        # 更新头指针表或前一个相似元素项节点的指针指向新节点
        if headerTable[items[0]][1] == None:
            headerTable[items[0]][1] = inTree.children[items[0]]
        else:
            updateHeader(headerTable[items[0]][1], inTree.children[items[0]])

    if len(items) > 1:
        # 对剩下的元素项迭代调用updateTree函数
        updateTree(items[1:], inTree.children[items[0]], headerTable, count)

def updateHeader(nodeToTest, targetNode):
    while (nodeToTest.nodeLink != None):
        nodeToTest = nodeToTest.nodeLink
    nodeToTest.nodeLink = targetNode


def findPrefixPath(lefeNode):  #
    condPats = {}
    while lefeNode != None:
        prefixPath = []
        ascendTree(lefeNode,prefixPath)
        if len(prefixPath) > 1:
            condPats[frozenset(prefixPath[1:])] = lefeNode.count
        lefeNode = lefeNode.nodeLink
    return condPats

def ascendTree(lefeNode,prefixPath):
    while lefeNode.parent != None:
        prefixPath.append(lefeNode.name)
        lefeNode = lefeNode.parent

def mineTree(headerTable, preFix, freqItemList):
    bigL = [v[0] for v in sorted(headerTable.items(), key=lambda p: p[1][0])]
    for basePat in bigL:
        newFreqSet = preFix.copy()
        newFreqSet.add(basePat)
        freqItemList.append(newFreqSet)
        basePatConPats = findPrefixPath(headerTable[basePat][1])
        _,myHead = createTree(basePatConPats)
        if myHead != None:
            mineTree(myHead,newFreqSet,freqItemList)

def fpGrowth():
    initSet = createInitSet(loadSimpDat())
    myFPtree, myHeaderTab = createTree(initSet)
    freqItems = []
    mineTree(myHeaderTab, set([]), freqItems)
    print(freqItems)


fpGrowth()


