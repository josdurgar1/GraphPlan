class Action(object):
  """
  The action class is used to define operators.
  Each action has a list of preconditions, an "add list" of positive effects,
  a "delete list" for negative effects, and the name of the action.
  Two actions are considered equal if they have the same name.
  """
  
  def __init__(self, name, pre, add, delete, isNoOp = False):
    #Constructor
    self.pre = pre #Lista de las precondiciones
    self.add = add #Lista de los estados que se añadirán si se aplica la acción
    self.delete = delete #Lista de los estados que se borrarán después de aplicar la acción
    self.name = name #El nombre de la acción
    self.noOp = isNoOp #True si la acción es noOp
    
  def getPre(self):
    return self.pre
  
  def getAdd(self):
    return self.add
  
  def getDelete(self):
    return self.delete
  
  def getName(self):
    return self.name
  
  def isPreCond(self, prop):
    return prop in self.pre
  
  
  def isPosEffect(self, prop): 
	#True si el estado tiene un efecto positivo sobre la acción
    return prop in self.add
  
  def isNegEffect(self, prop):
    #True si el estado tiene un efecto, esta vez, negativo sobre la acción
    return prop in self.delete

  def allPrecondsInList(self, propositions):
	#Devuelve true si todos las precondiciones de la acción están en la lista de estados
    for pre in self.pre:
      if pre not in propositions:
        return False
    return True
    
  def isNoOp(self):
    return self.noOp
  
  def __eq__(self, other):
    return (isinstance(other, self.__class__)
      and self.name == other.name)

  def __str__(self):
    return self.name
  
  def __ne__(self, other):
    return not self.__eq__(other)
    
  def __lt__(self, other):
    return self.name < other.name 
    
  def __hash__(self):
    return hash(self.name)
