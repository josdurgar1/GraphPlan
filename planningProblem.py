from util import Pair
import copy
from propositionLayer import PropositionLayer
from planGraphLevel import PlanGraphLevel
from Parser import Parser
from action import Action

try:
  from search import SearchProblem
  from search import aStarSearch

except:
  from  CPF.search import SearchProblem
  from  CPF.search import aStarSearch

class PlanningProblem():
  def __init__(self, domain, problem):
    """
    Constructor
    """
    p = Parser(domain, problem)
    self.actions, self.propositions = p.parseActionsAndPropositions()	  # list of all the actions and list of all the propositions                                            
    self.initialState, self.goal = p.pasreProblem() 				            # the initial state and the goal state are lists of propositions                                            
    self.createNoOps() 											                            # creates noOps that are used to propagate existing propositions from one layer to the next
    PlanGraphLevel.setActions(self.actions)
    PlanGraphLevel.setProps(self.propositions)
    self._expanded = 0
   
    
  def getStartState(self):
    """ Devuelve el estado inicial """
    return self.initialState
    
  def isGoalState(self, state):
    """ Comprueba si es estado final """
    for p in self.goal:
      if p not in state:
        return False
    return True
    
  def getSuccessors(self, state):
    """ Para un estado dado, esto debe devolver una lista de tres valores,
    (successor, action, stepCost), donde 'successor' es un sucesor para el
    estado actual, 'action' es la acción requerida para llegar allí,
    y 'stepCost' es el costo incremental de ampliar hasta el sucesor,
    1 en nuestro caso. """
    self._expanded += 1
    successors = []
    for a in self.actions:
      # Comprueba si todas las condiciones previas de acción están en el estado actual
      if not a.isNoOp() and a.allPrecondsInList(state):  
        # Si la acción se suma a una proposición, se añade al estado
        successor = state + [p for p in a.getAdd() if p not in state]
        # Deshacerse de las proposiciones y acciones que se han borrado del estado
        successor = [p for p in successor if p not in a.getDelete()]
   
        # El costo siempre suma 1
        successors.append((successor, a, 1))
    return successors

  def getCostOfActions(self, actions):
    return len(actions)
    
  def goalStateNotInPropLayer(self, propositions):
    """ Devuelve verdadero si todas las proposiciones de
    meta están en las proposiciones """
    for goal in self.goal:
      if goal not in propositions:
        return True
    return False

  def createNoOps(self):
    """ Crea los bucles que se utilizan para propagar
    proposiciones de una capa a la siguiente """
    for prop in self.propositions:
      name = prop.name
      precon = []
      add = []
      precon.append(prop)
      add.append(prop)
      delete = []
      act = Action(name,precon,add,delete, True)
      self.actions.append(act)  
      
def maxLevel(state, problem):
  """ El valor de la heurística es el número de capas
  necesarias para expandir todas las proposiciones de gol.
  Si el objetivo no es alcanzable desde el estado de su
  heurística debe volver float('inf') """
  level = 0
  propLayerInit = PropositionLayer()
  # Añadir todas las proposiciones en el estado actual en la propositionLayer
  for p in state:
    propLayerInit.addProposition(p)

  pgInit = PlanGraphLevel()
  pgInit.setPropositionLayer(propLayerInit)
  # El Grafo es una lista de objetos PlanGraphLevel
  graph = []
  graph.append(pgInit)

  # Mientras que el estado objetivo no está en la capa proposición, seguimos expandiendolo
  while problem.goalStateNotInPropLayer(graph[level].getPropositionLayer().getPropositions()):
    # Si el grafo no ha cambiado entre expansiones, lo detenemos.
    if isFixed(graph, level):
      return float('inf')
    level += 1
    pgNext = PlanGraphLevel()
    # Expandir sin mutex (versión relajada de problema)
    pgNext.expandWithoutMutex(graph[level-1])
    graph.append(pgNext)

  return level  


def levelSum(state, problem):
  """ El valor heurístico es la suma de los sub-objetivos de
  nivel de su primera aparición. Si el objetivo no es
  alcanzable desde el estado de su heurística debe volver float ('inf')"""
    
  
def isFixed(Graph, level):
  """ Comprueba si hemos llegado a un punto fijo, es decir,
  si cada nivel que vamos a ampliar es el mismo, no tiene
  sentido continuar """
  if level == 0:
    return False  
  return len(Graph[level].getPropositionLayer().getPropositions()) == len(Graph[level - 1].getPropositionLayer().getPropositions())  
      
if __name__ == '__main__':
  import sys
  import time
  if len(sys.argv) != 1 and len(sys.argv) != 4:
    print("Usage: PlanningProblem.py domainName problemName heuristicName(max, sum or zero)")
    exit()
  domain = 'domain.txt'
  problem = 'problem.txt'
  heuristic = lambda x,y: 0
  if len(sys.argv) == 4:
    domain = str(sys.argv[1])
    problem = str(sys.argv[2])
    if str(sys.argv[3]) == 'max':
      heuristic = maxLevel
    elif str(sys.argv[3]) == 'sum':
      heuristic = levelSum
    elif str(sys.argv[3]) == 'zero':
      heuristic = lambda x,y: 0
    else:
      print("Usage: PlanningProblem.py domainName problemName heuristicName(max, sum or zero)")
      exit()

  prob = PlanningProblem(domain, problem)
  start = time.clock()
  plan = aStarSearch(prob, heuristic)  
  elapsed = time.clock() - start
  if plan is not None:
    print("Plan encontrado con %d acciones en %.2f segundos" % (len(plan), elapsed))
  else:
    print("No se pudo encontrar un plan en %.2f seconds" %  elapsed)
  print("Nodos de búsqueda expandidos: %d" % prob._expanded)
