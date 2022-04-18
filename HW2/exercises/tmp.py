import numpy as np 

print("Example 1")

A = np.array([
  [4,0,0,0,1],
  [0,3,1,1,0],
  [0,1,4,0,0],
  [0,1,0,4,0],
  [1,0,0,0,4]
]) 
A_inverted = np.linalg.inv(A)
trace = np.trace(A_inverted)

for i in range(A_inverted.shape[0]):
  R = 0
  for j in range(A_inverted.shape[1]):
    R = R + A_inverted[i][j]
  
  centrality = 1 / (A_inverted[i][i] + (trace - 2 * R) )
  print(i + 1, centrality, (A_inverted[i][i] + (trace - 2 * R)), 2 * R)
  
print(A_inverted, trace)

print("Example 2")

A = np.array([
  [14,0,-5,-5,1],
  [0,6,1,1,-4],
  [-5,1,15,-2,-4],
  [-4,1,-2,12,-1],
  [1,-4,-4,-1,12]
]) 
A_inverted = np.linalg.inv(A)
trace = np.trace(A_inverted)

for i in range(A_inverted.shape[0]):
  R = 0
  for j in range(A_inverted.shape[1]):
    R = R + A_inverted[i][j]
  
  centrality = 1 / (A_inverted[i][i] + (trace - 2 * R) / 5 )
  print(i + 1, centrality, (A_inverted[i][i] + (trace - 2 * R)), 2 * R)
  
print(A_inverted, trace)

print("Example 3")

A = np.array([
  [2,0,1,1],
  [0,7,-4,1],
  [1,-4,8,-1],
  [1,1,-1,3]
]) 
A_inverted = np.linalg.inv(A)
trace = np.trace(A_inverted)

for i in range(A_inverted.shape[0]):
  R = 0
  for j in range(A_inverted.shape[1]):
    R = R + A_inverted[i][j]
  
  centrality = 1 / (A_inverted[i][i] + (trace - 2 * R) / 4 )
  print(i + 1, centrality, (A_inverted[i][i] + (trace - 2 * R)), 2 * R)
  
print(A_inverted, trace)