from util import Pair

class PropositionLayer(object):
  # El nivel contiene un conjunto de estados y un conjunto de estados mutex
  
  def __init__(self):
    # Constructor
    self.propositions = set() #Conjunto de todos los estados del nivel
    self.mutexPropositions = set() #Conjunto de los pares de estados que están mutex en el nivel
    
  def addProposition(self, proposition): #Añade el estado al conjunto de estados
    self.propositions.add(proposition)
    
  def removePropositions(self, proposition): #Borra el estado del conjunto de estados
    self.propositions.remove(proposition)
    
  def getPropositions(self): #Devuelve el conjunto de estados

    return self.propositions    
  
  def addMutexProp(self, p1, p2): #Añade el par de estados (p1, p2) al conjunto de estados mutex
    self.mutexPropositions.add(Pair(p1,p2))
  
  def isMutex(self, p1, p2):
    return Pair(p1,p2) in self.mutexPropositions #Devuelve true si el estado p1 y el estado p2 están mutex en el nivel
  
  def getMutexProps(self): #Devuelve el conjunto de estados mutex
    return self.mutexPropositions  
  
  def allPrecondsInLayer(self, action):
	#Devuelve true si todos los estados que son precondiciones de la acción pasada por parámetros existen en esta capa
    actionPre = action.getPre()
    for pre in actionPre:
      if not(pre in self.propositions):
        return False
        
    for i in range(len(actionPre)):
      for j in range(i + 1, len(actionPre)):
        pre1 = actionPre[i]
        pre2 = actionPre[j]
        if Pair(pre1,pre2) in self.mutexPropositions:
          return False
    
    return True

  def __eq__(self, other):
    return (isinstance(other, self.__class__)
      and self.__dict__ == other.__dict__)

  def __ne__(self, other):
    return not self.__eq__(other)
      
