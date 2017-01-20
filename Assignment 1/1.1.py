
from collections import deque
from Container import Container
from Node import Node




def search(searchType,basenode, array):
	numnodes=0
	frontier=Container(searchType)
	exploredSet=[]
	solutionPath=[]
	frontier.add(basenode)

	while (not (frontier.empty())):
		#print (frontier.size())
		activeNode=frontier.remove() #remove only one node from frontier or pop out the element in the queue/stack?
		# check if its a at the posiiton of a goal and remove it from the list if so
		#print(activeNode.goalCoordinates)
		#print(activeNode.coordinates)

		#print (activeNode in exploredSet)

		if(not (activeNode.coordinates,activeNode.goalCoordinates) in exploredSet):
			if (len(activeNode.goalCoordinates)==1):	
				if(activeNode.goalCoordinates[0]==activeNode.coordinates):
					# print (activeNode.goalCoordinates)
					# print (activeNode.coordinates)
					solutionPath.append(activeNode)
					return (solutionPath,numnodes)

			for i,val in enumerate(activeNode.goalCoordinates):
				if(val==activeNode.coordinates):
					solutionPath.append(activeNode)
					activeNode.goalCoordinates.remove(val)
			
			


			exploredSet.append((activeNode.coordinates,activeNode.goalCoordinates))
			numnodes+=1
			xcoord,ycoord=activeNode.coordinates #tuple's y starts from 0?
			
			if ((xcoord-1>=0 ) and  (array[ycoord][xcoord-1]!='%')):#openArray (y,x)
				#print ("hi1")
				childNode1=Node(activeNode,(xcoord-1,ycoord),activeNode.goalCoordinates) #use dictionary to find if childNode1 is in explored or frontier
				if((not frontier.find(childNode1)) and (not (childNode1.coordinates,childNode1.goalCoordinates) in exploredSet)):
					frontier.add(childNode1)
					
					#print ("hi1")

			if ((xcoord+1<len(array[0])) and  (array[ycoord][xcoord+1]!='%')):
				#print ("hi1")
				childNode1=Node(activeNode,(xcoord+1,ycoord),activeNode.goalCoordinates) #use dictionary to find if childNode1 is in explored or frontier
				if((not frontier.find(childNode1)) and (not (childNode1.coordinates,childNode1.goalCoordinates)  in exploredSet)):
					frontier.add(childNode1)

				
					#print ("hi2")

			if (ycoord-1>=0 ) and  (array[ycoord-1][xcoord]!='%') :
				#print ("hi1")
				childNode1=Node(activeNode,(xcoord,ycoord-1),activeNode.goalCoordinates) #use dictionary to find if childNode1 is in explored or frontier
				if((not frontier.find(childNode1)) and (not (childNode1.coordinates,childNode1.goalCoordinates)  in exploredSet) ):
					frontier.add(childNode1)
					
					#print ("hi3")

			if (ycoord+1<len(array) ) and  (array[ycoord+1][xcoord]!='%') :
				#print ("hi1")
				childNode1=Node(activeNode,(xcoord,ycoord+1),activeNode.goalCoordinates) #use dictionary to find if childNode1 is in explored or frontier
				if((not frontier.find(childNode1)) and (not (childNode1.coordinates,childNode1.goalCoordinates)  in exploredSet)):
					frontier.add(childNode1)
					
					#print ("hi4")

	return None










# mediumMazefile = open('mediumMaze.txt',  'r+')	#open the files using r+ for read write
# bigMazefile = open('bigMaze.txt',  'r+')
# openMazefile = open('openMaze.txt',  'r+')	
# #process files and store them in arrays
# mediumString = mediumMazefile.read()
# bigString = bigMazefile.read()
# openString = openMazefile.read()
# mediumHeight =21
# mediumWidth = 41
# mediumArray = [None]*mediumHeight
# for i in range(mediumHeight):
# 	mediumArray[i]=[None]*mediumWidth
# for i in range(mediumHeight):
# 	for j in range(mediumWidth):
# 			mediumArray[i][j]=mediumString[i*mediumWidth+j+i]
# openHeight =20
# openWidth = 37
# openArray = [None]*openHeight
# for i in range(openHeight):
# 	openArray[i]=[None]*openWidth
# for i in range(openHeight):
# 	for j in range(openWidth):
# 			openArray[i][j]=openString[i*openWidth+j+i]
# bigHeight =41
# bigWidth = 41
# bigArray = [None]*bigHeight
# for i in range(bigHeight):
# 	bigArray[i]=[None]*bigWidth
# for i in range(bigHeight):
# 	for j in range(bigWidth):
# 			bigArray[i][j]=bigString[i*bigWidth+j+i]


# #*********************  2.2 ***************************************

# mediumSearchfile = open('mediumSearch.txt',  'r+')	#open the files using r+ for read write
# smallSearchfile = open('smallSearch.txt',  'r+')
# tinySearchfile = open('tinySearch.txt',  'r+')	
# #process files and store them in arrays
# mediumSearchString = mediumSearchfile.read()
# smallSearchString = smallSearchfile.read()
# tinySearchString = tinySearchfile.read()
# mediumSearchHeight =13
# mediumSearchWidth = 49
# mediumSearchArray = [None]*mediumSearchHeight
# for i in range(mediumSearchHeight):
# 	mediumSearchArray[i]=[None]*mediumSearchWidth
# for i in range(mediumSearchHeight):
# 	for j in range(mediumSearchWidth):
# 			mediumSearchArray[i][j]=mediumSearchString[i*mediumSearchWidth+j+i]
# tinySearchHeight =9
# tinySearchWidth = 9
# tinySearchArray = [None]*tinySearchHeight
# for i in range(tinySearchHeight):
# 	tinySearchArray[i]=[None]*tinySearchWidth
# for i in range(tinySearchHeight):
# 	for j in range(tinySearchWidth):
# 			tinySearchArray[i][j]=tinySearchString[i*tinySearchWidth+j+i]
# smallSearchHeight =13
# smallSearchWidth = 30
# smallSearchArray = [None]*smallSearchHeight
# for i in range(smallSearchHeight):
# 	smallSearchArray[i]=[None]*smallSearchWidth
# for i in range(smallSearchHeight):
# 	for j in range(smallSearchWidth):
# 			smallSearchArray[i][j]=smallSearchString[i*smallSearchWidth+j+i]





#swap out 0 for dfs 1 for bfs 2 for greedy 3 for a*  
#swap out bigArray for medium and hardcoded values or uncomment whats  below

#************** medium ************************

# GoalList1=[]
# type=3
# for i in range(tinySearchHeight):
# 	for j in range(tinySearchWidth):
# 		if(tinySearchArray[i][j]=='.'):
# 			GoalList1.append((j,i))

# root = Node(None, (7,1), GoalList1)
# (path,numbernodes) = search(type, root, tinySearchArray)
# charc=chr(ord('1'))
# print (numbernodes)
# pathcost=0
# for i,child in enumerate(path):
# 	pathcost+=child.pathcost
# print(pathcost)

# for i,child in enumerate(path):
# 	while (child!=None):
# 		x,y=child.coordinates
# 		if (tinySearchArray[y][x]!='.' and tinySearchArray[y][x]==' '):
# 			tinySearchArray[y][x]=charc
# 		child=child.parent
# 	charc=chr(ord(charc) + 1)
# 	if (charc>'9'):
# 		charc='a'

# tinySearchSolution=open('tinySearchSolutionAstar.txt', 'w+')

# for i in range(tinySearchHeight):
# 	for j in range(tinySearchWidth):
# 		tinySearchSolution.write(tinySearchArray[i][j])
# 	tinySearchSolution.write('\n')
# tinySearchSolution.close()


# for i in range(mediumSearchHeight):
# 	for j in range(mediumSearchWidth):
# 		if(mediumSearchArray[i][j]=='.'):
# 			GoalList1.append((j,i))

# root = Node(None, (7,1), GoalList1)
# (path,numbernodes) = search(type, root, mediumSearchArray)
# charc=chr(ord('1'))
# print (numbernodes)
# pathcost=0
# for i,child in enumerate(path):
# 	pathcost+=child.pathcost
# print(pathcost)

# for i,child in enumerate(path):
# 	while (child!=None):
# 		x,y=child.coordinates
# 		if (mediumSearchArray[y][x]!='.' and mediumSearchArray[y][x]==' '):
# 			mediumSearchArray[y][x]=charc
# 		child=child.parent
# 	charc=chr(ord(charc) + 1)
# 	if (charc>'9'):
# 		charc='a'

# mediumSearchSolution=open('mediumSearchSolutionAstar.txt', 'w+')

# for i in range(mediumSearchHeight):
# 	for j in range(mediumSearchWidth):
# 		mediumSearchSolution.write(mediumSearchArray[i][j])
# 	mediumSearchSolution.write('\n')
# mediumSearchSolution.close()

# for i in range(smallSearchHeight):
# 	for j in range(smallSearchWidth):
# 		if(smallSearchArray[i][j]=='.'):
# 			GoalList1.append((j,i))

# root = Node(None, (7,1), GoalList1)
# (path,numbernodes) = search(type, root, smallSearchArray)
# charc=chr(ord('1'))
# print (numbernodes)
# pathcost=0
# for i,child in enumerate(path):
# 	pathcost+=child.pathcost
# print(pathcost)

# for i,child in enumerate(path):
# 	while (child!=None):
# 		x,y=child.coordinates
# 		if (smallSearchArray[y][x]!='.' and smallSearchArray[y][x]==' '):
# 			smallSearchArray[y][x]=charc
# 		child=child.parent
# 	charc=chr(ord(charc) + 1)
# 	if (charc>'9'):
# 		charc='a'

# smallSearchSolution=open('smallSearchSolutionAstar.txt', 'w+')

# for i in range(smallSearchHeight):
# 	for j in range(smallSearchWidth):
# 		smallSearchSolution.write(smallSearchArray[i][j])
# 	smallSearchSolution.write('\n')
# smallSearchSolution.close()


#**********************************************************************

# #*********************  extra ***************************************

# # extracreditfile = open('extracredit.txt',  'r+')	#open the files using r+ for read write

# # #process files and store them in arrays
# # extracreditString = extracreditfile.read()

# # extracreditHeight =17
# # extracreditWidth = 28
# # extracreditArray = [None]*extracreditHeight
# # for i in range(extracreditHeight):
# # 	extracreditArray[i]=[None]*extracreditWidth
# # for i in range(extracreditHeight):
# # 	for j in range(extracreditWidth):
# # 			extracreditArray[i][j]=extracreditString[i*extracreditWidth+j+i]





# extrafile = open('extracredit.txt',  'r+')	
# #process files and store them in arrays

# extraString = extrafile.read()

# extraHeight =17
# extraWidth = 28
# extraArray = [None]*extraHeight
# for i in range(extraHeight):
# 	extraArray[i]=[None]*extraWidth
# for i in range(extraHeight):
# 	for j in range(extraWidth):
# 			extraArray[i][j]=extraString[i*extraWidth+j+i]









# # GoalList1=[]
# # type=3
# # for i in range(extracreditHeight):
# # 	for j in range(extracreditWidth):
# # 		if(extracreditArray[i][j]=='.'):
# # 			GoalList1.append((j,i))

# # root = Node(None, (14,11), GoalList1)
# # (path,numbernodes) = search(type, root, extracreditArray)
# # charc=chr(ord('1'))
# # print (numbernodes)
# # pathcost=0
# # for i,child in enumerate(path):
# # 	pathcost+=child.pathcost
# # print(pathcost)

# # for i,child in enumerate(path):
# # 	while (child!=None):
# # 		x,y=child.coordinates
# # 		if (extracreditArray[y][x]!='.' and extracreditArray[y][x]==' '):
# # 			extracreditArray[y][x]=charc
# # 		child=child.parent
# # 	charc=chr(ord(charc) + 1)
# # 	if (charc>'9'):
# # 		charc='a'






# extraSolution=open('extraSolutionAstar.txt', 'w+')

# for i in range(extraHeight):
# 	for j in range(extraWidth):
# 		extraSolution.write(extraArray[i][j])
# 	extraSolution.write('\n')
# extraSolution.close()



# #swap out 0 for dfs 1 for bfs 2 for greedy 3 for a*  
# #swap out bigArray for medium and hardcoded values or uncomment whats  below
#*****************************************************************************















   #newNode=node(parent, (22,2), (11,19))


#root=Node(None,(39,19),[(1,1)])
#path=search(3,root, mediumArray)


#root = Node(None, (21,1), [(10,18)])
#path = search(3, root, openArray)







# mediumSolution=open('mediumSolution.txt', 'w+')
# for i in range(mediumHeight):
# 	for j in range(mediumWidth):
# 			mediumSolution.write(mediumArray[i][j])
# 	mediumSolution.write('\n')

# openSolution=open('openSolution.txt', 'w+')
# for i in range(openHeight):
# 	for j in range(openWidth):
# 			openSolution.write(openArray[i][j])
# 	openSolution.write('\n')





#********************************************************
type=0





#swap out 0 for dfs 1 for bfs 2 for greedy 3 for a*  
#swap out bigArray for medium and hardcoded values or uncomment whats  below
# root = Node(None, (1,39), [(39,39)])
# (path,numbernodes) = search(type, root, bigArray)
# print (path.pathcost)
# print (numbernodes)
# while (path!=None):
# 	x,y=path.coordinates

# 	bigArray[y][x]='.'
# 	path=path.parent
# bigSolution=open('bigSolutionAstar.txt', 'w+')

# for i in range(bigHeight):
# 	for j in range(bigWidth):
# 			bigSolution.write(bigArray[i][j])
# 	bigSolution.write('\n')
# bigSolution.close()


#************************************************
# mediumArray1=mediumArray


# root = Node(None, (39,19), [(1,1)])
# (path,numbernodes) = search(type, root, mediumArray)
# print (path.pathcost)
# print (numbernodes)
# while (path!=None):
# 	x,y=path.coordinates
# 	mediumArray[y][x]='.'
# 	path=path.parent
# mediumSolution=open('mediumSolutionAstar.txt', 'w+')
# for i in range(mediumHeight):
# 	for j in range(mediumWidth):
# 			mediumSolution.write(mediumArray[i][j])
# 	mediumSolution.write('\n')
# mediumSolution.close()



# #**********************************************
# openArray1=openArray

# root = Node(None, (21,1), [(10,18)])
# (path,numbernodes) = search(3, root, openArray)
# print (path.pathcost)
# print (numbernodes)
# while (path!=None):
# 	x,y=path.coordinates
	
# 	openArray[y][x]='.'
# 	path=path.parent
# openSolution=open('openSolutionAstar.txt', 'w+')
# for i in range(openHeight):
# 	for j in range(openWidth):
# 			openSolution.write(openArray[i][j])
# 	openSolution.write('\n')


extracreditfile.close()
# mediumMazefile.close()
# bigMazefile.close()
# openMazefile.close()

# #******************************************************
# mediumSearchfile.close()
# smallSearchfile.close()
# tinySearchfile.close()
