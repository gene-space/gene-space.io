#### FLOWER FUNCTIONS ####
def removeSeed(string):
    pos = string.find(' (seed)')
    if pos > -1:
        string = string[0:pos]
    return string

def removeIsland(string):
    pos = string.find(' (island)')
    if pos > -1:
        string = string[0:pos]
    return string

def findSeednIsland(string):
    val = 'Hybrid'
    if string.find(' (seed)') > -1:
        val = "Seed"    
    elif string.find(' (island)') > -1:
        val = "Island"
    return val

def num_str2tup(num_str):
    tup = [int(num_str[0]), int(num_str[4]), int(num_str[8])]
    return tup

def tup2num_str(tup):
    num_str = []
    for n in range(0,len(tup)):
        num_str += [str(int(tup[n]))]
    num_str = ' - '.join(num_str)
    return num_str

def convertNumericToBinary(parentNumeric):
    parentBinary = [None]*len(parentNumeric)
    for n in range(0,len(parentNumeric)):
        if parentNumeric[n] == 0:
            parentBinary[n] = '00'
        elif parentNumeric[n] == 1:
            parentBinary[n] = '01'
        elif parentNumeric[n] == 2:
            parentBinary[n] = '11'
    return parentBinary

def convertBinaryToNumeric(parentBinary):
    parentNumeric = [None]*len(parentBinary)
    for n in range(0,len(parentBinary)):
        parentNumeric[n] = str(int(parentBinary[n][0]) + int(parentBinary[n][1]))
    return parentNumeric

def getChildren(par1, par2):    
    # return the children as dictionary with the (string) numeric genes as keys, and the probability as the value
    par1 = convertNumericToBinary(par1)
    par2 = convertNumericToBinary(par2)
    genes1 = {}; genes2 = {}; genes3 = {}        
    total1 = 0; total2 = 0; total3 = 0        
    for n in range(0,2):
        for m in range(0,2):
            gen1 = par1[0][m] + par2[0][n]
            gen2 = par1[1][m] + par2[1][n]
            gen3 = par1[2][m] + par2[2][n]            
            if gen1 in genes1.keys():
                genes1[gen1] = genes1[gen1] + 1
            elif gen1 not in genes1.keys():
                genes1[gen1] = 1            
            if gen2 in genes2.keys():
                genes2[gen2] = genes2[gen2] + 1
            elif gen2 not in genes2.keys():
                genes2[gen2] = 1            
            if gen3 not in genes3.keys():
                genes3[gen3] = 1
            else:
                genes3[gen3] = genes3[gen3] + 1
            total1 = total1 + 1; total2 = total2 + 1; total3 = total3 + 1
    genes1['Total'] = total1
    genes2['Total'] = total2
    genes3['Total'] = total3
    children = {}
    for key1 in genes1.keys():
        for key2 in genes2.keys():
            for key3 in genes3.keys():
                if key1 != 'Total' and key2 != 'Total' and key3 != 'Total':
                    tupleNumeric = convertBinaryToNumeric([key1, key2, key3])
                    codeNumeric = tupleNumeric[0] + ' - ' + tupleNumeric[1] + ' - ' + tupleNumeric[2]
                    prob = genes1[key1]/genes1['Total'] * genes2[key2]/genes2['Total'] * genes3[key3]/genes3['Total']
                    if codeNumeric in children.keys():
                        children[codeNumeric] = children[codeNumeric] + prob
                    else:
                        children[codeNumeric] = prob
    return children
                    
def btr_purp(color):
    if color == 'purple':
        color = 'mediumpurple'        
    return color