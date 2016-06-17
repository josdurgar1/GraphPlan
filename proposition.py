class Proposition(object):

  def __init__(self,name):
    #Constructor
    self.name = name #El nombre del estado, como cadena
    self.producers = [] #Lista de todas las acciones en el nivel actual que tienen este estado en su lista de estados a añadir si se efectúa la acción
    
  def getName(self):
    return self.name
  
  def getProducers(self):
    return self.producers

  def setProducers(self, producers):
    self.producers = producers
  
  def addProducer(self, producer):
      self.producers.append(producer)  
  
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
