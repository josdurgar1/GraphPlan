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
    "*** YOUR CODE HERE ***"
    return self.initialState
    
  def isGoalState(self, state):
    """
    Hint: you might want to take a look at goalStateNotInPropLayer function
    """
    "*** YOUR CODE HERE ***"
    return goalStateNotInPropLayer(self, state)
    
  def getSuccessors(self, state):
    """   
    For a given state, this should return a list of triples, 
    (successor, action, stepCost), where 'successor' is a 
    successor to the current state, 'action' is the action
    required to get there, and 'stepCost' is the incremental 
    cost of expanding to that successor, 1 in our case.
    You might want to this function:
    For a list / set of propositions l and action a,
    a.allPrecondsInList(l) returns true if the preconditions of a are in l
    """
    self._expanded += 1
    "*** YOUR CODE HERE ***"
    """"successor= 
    action="""
    successors = []
    for a in self.actions:
      # Check if all preconditions of action a are in current state
      if not a.isNoOp() and a.allPrecondsInList(state):  
        # If action a adds a proposition, add it to state  
        successor = state + [p for p in a.getAdd() if p not in state]
        # Get rid of propositions action a deletes from state
        successor = [p for p in successor if p not in a.getDelete()]
   
        # Stepcost is 1
        successors.append((successor, a, 1))
    return successors

  def getCostOfActions(self, actions):
    return len(actions)
    
  def goalStateNotInPropLayer(self, propositions):
    """
    Helper function that returns true if all the goal propositions 
    are in propositions
    """
    for goal in self.goal:
      if goal not in propositions:
        return True
    return False

  def createNoOps(self):
    """
    Creates the noOps that are used to propagate propositions from one layer to the next
    """
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
  """
  The heuristic value is the number of layers required to expand all goal propositions.
  If the goal is not reachable from the state your heuristic should return float('inf')  
  A good place to start would be:
  propLayerInit = PropositionLayer()          #create a new proposition layer
  for prop in state:
    propLayerInit.addProposition(prop)        #update the proposition layer with the propositions of the state
  pgInit = PlanGraphLevel()                   #create a new plan graph level (level is the action layer and the propositions layer)
  pgInit.setPropositionLayer(propLayerInit)   #update the new plan graph level with the the proposition layer
  """
  "*** YOUR CODE HERE ***"
  level = 0
  propLayerInit = PropositionLayer()
  # Add all propositions in current state to proposition layer
  for p in state:
    propLayerInit.addProposition(p)

  pgInit = PlanGraphLevel()
  pgInit.setPropositionLayer(propLayerInit)
  # Graph is a list of PlanGraphLevel objects
  graph = []
  graph.append(pgInit)

  # While goal state is not in proposition layer, keep expanding
  while problem.goalStateNotInPropLayer(graph[level].getPropositionLayer().getPropositions()):
    # If the graph has not changed between expansions, we should halt
    if isFixed(graph, level):
      return float('inf')
    level += 1
    pgNext = PlanGraphLevel()
    # Expand without mutex (relaxed version of problem)
    pgNext.expandWithoutMutex(graph[level-1])
    graph.append(pgNext)

  return level  


def levelSum(state, problem):
  """
  The heuristic value is the sum of sub-goals level they first appeared.
  If the goal is not reachable from the state your heuristic should return float('inf')
  """
  "*** YOUR CODE HERE ***"
    
  
def isFixed(Graph, level):
  """
  Checks if we have reached a fixed point,
  i.e. each level we'll expand would be the same, thus no point in continuing
  """
  if level == 0:
    return False  
  return len(Graph[level].getPropositionLayer().getPropositions()) == len(Graph[level - 1].getPropositionLayer().getPropositions())  
      
if __name__ == '__main__':
  import sys
  import time
  if len(sys.argv) != 1 and len(sys.argv) != 4:
    print("Usage: PlanningProblem.py domainName problemName heuristicName(max, sum or zero)")
    exit()
  domain = 'dwrDomain.txt'
  problem = 'dwrProblem.txt'
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
    print("Plan found with %d actions in %.2f seconds" % (len(plan), elapsed))
  else:
    print("Could not find a plan in %.2f seconds" %  elapsed)
  print("Search nodes expanded: %d" % prob._expanded)
