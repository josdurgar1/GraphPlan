from util import Pair

class ActionLayer(object):
  """
  A class for an ActionLayer in a level of the graph.
  The layer contains a set of actions (action objects) and a set of mutex actions (Pair objects)
  """

  def __init__(self):
    """
    Constructor
    """
    self.actions = set() #Conjunto de todas las acciones en el nivel
    self.mutexActions = set() #Conjunto de los pares de acciones mutex en el nivel
    
  def addAction(self, act): #Añade la acción al conjunto de acciones
    self.actions.add(act)
    
    
  def removeActions(self, act): #Borra la acción del conjunto de acciones
    self.actions.remove(act)
    
  def getActions(self): #Devuelve el conjunto de acciones
    return self.actions
  
  def getMutexActions(self): #Devuelve las acciones mutex

    return self.mutexActions
    
  def addMutexActions(self, a1, a2): #Añade un par de acciones al conjunto de acciones mutex
    self.mutexActions.add(Pair(a1,a2))
  
  
  def isMutex(self, Pair):
	#Devuelve true si el conjuto de acciones están mutex en el nivel
    return Pair in self.mutexActions
  
  def effectExists(self, prop):
	#Devuelve true si al menos una de las acciones del nivel actual tiene el estado en su lista de estado a añadir
    for act in self.actions:
      if prop in act.getAdd():
        return True
    return False
  
  def __eq__(self, other):
    return (isinstance(other, self.__class__)
      and self.__dict__ == other.__dict__)

  def __ne__(self, other):
    return not self.__eq__(other)
