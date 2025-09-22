import random

# Dictionary of Quantum Gates
gateDict = {
    "H": [[1, 1], [1, -1]],
    "cNot": [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]]
}


# Quantum Gate Functions
class Gate():

  @staticmethod
  def cNot(state1, state2):
    stateTensored = tensorProduct(state1, state2)
    finalState = matrixMultiplier(stateTensored
    , gateDict.get("cNot"))
    finalState = flattenList(finalState)
    qStatePair = tensorFactor(finalState)
    return qStatePair

  @staticmethod
  def Hadamard(qbitAmt):
    matrix = gateDict["H"]
    for _ in range(qbitAmt - 1):
      matrix = tensorProduct(matrix, gateDict["H"])
    return matrix


# Operation Functions
def flattenList(unflatList):
  flattenedList = []
  if isinstance(unflatList, int):
    return [unflatList]
  elif not isinstance(unflatList, list):
    raise ValueError("flattenList: Input must be a list or an integer.")

  for elem in unflatList:
    if isinstance(elem, list):
      flattenedList += flattenList(elem)
    else:
      flattenedList.append(elem)

  return flattenedList


def tensorFactor(vector4D):
  if vector4D == [1, -1, -1, 1]:
    vector2D3 = [1, -1]
    cbit = [1, -1]
  else:
    vector2D3 = [vector4D[0], vector4D[1]]
    cbit = [1, 1]

  return vector2D3, cbit


def tensorProduct(matrix1, matrix2):
  if isinstance(matrix1, int):
    matrix1 = [[matrix1]]
  elif isinstance(matrix1[0], int):
    matrix1 = [matrix1]

  if isinstance(matrix2, int):
    matrix2 = [[matrix2]]
  elif isinstance(matrix2[0], int):
    matrix2 = [matrix2]

  rows1, cols1 = len(matrix1), len(matrix1[0])
  rows2, cols2 = len(matrix2), len(matrix2[0])

  result = [[0 for _ in range(cols1 * cols2)] for _ in range(rows1 * rows2)]

  for i in range(rows1):
    for j in range(cols1):
      for m in range(rows2):
        for n in range(cols2):
          result[i * rows2 + m][j * cols2 + n] = matrix1[i][j] * matrix2[m][n]

  return result


def matrixMultiplier(matrix1, matrix2):
  rowsMatrix1 = len(matrix1)
  colsMatrix1 = len(matrix1[0])

  colsMatrix2 = len(matrix2[0])

  result = [[0 for j in range(colsMatrix2)] for i in range(rowsMatrix1)]

  for i in range(rowsMatrix1):
    for j in range(colsMatrix2):
      for k in range(colsMatrix1):
        result[i][j] += matrix1[i][k] * matrix2[k][j]

  return result


# Measure Functions
def measure(state):
  amplitudes = [item[0] if isinstance(item, list) else item for item in state]
  probabilities = [abs(amplitude)**2 for amplitude in amplitudes]
  outcomeIndex = random.choices(range(len(state)), weights=probabilities)[0]
  collapsedState = [0] * len(state)
  collapsedState[outcomeIndex] = 1
  return collapsedState


# Algorithm Functions
def ufParity(stateArray, ansBit, a):
  if a == 1:
    stateArray, ansBit = Gate.cNot(stateArray, ansBit)
    
  stateArray = flattenList(stateArray)
  return stateArray, ansBit


def bvAlgorithm(n):
  if n <= 0:
    raise ValueError("bvAlgorithm: n must be a positive integer.")

  stateArray = []
  for _ in range(n):
    stateArray.append([[1, 0]])

  ansBit = [[1, -1]]
  print("Initialization: ", stateArray)

  for i in range(n):
    stateArray[i] = matrixMultiplier(stateArray[i], Gate.Hadamard(1))
  print("\nFirst Hadamard: ", stateArray)

  a = [random.randint(0, 1) for _ in range(n)]
  print("\nRandom a: ", a)

  for i in range(n):
    stateArray[i], ansBit = ufParity(stateArray[i], ansBit, a[i])
  print("\nAfter Uf Parity: ", stateArray)

  for i in range(n):
    stateArray[i] = matrixMultiplier([stateArray[i]], Gate.Hadamard(1))
  print("\nSecond Hadamard: ", stateArray)

  measuredState = stateArray[0][0]
  for i in range(n - 1):
    measuredState = tensorProduct(measuredState, stateArray[i + 1])
  print("\nMeasured state: ", measuredState)

  return measure(measuredState[0]) if n >= 2 else measure(measuredState)


# Main Execution
numQbits = 2
print(f'\nAnswer = {bvAlgorithm(numQbits)}')