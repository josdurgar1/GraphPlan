from action import Action
from actionLayer import ActionLayer
from util import Pair
from proposition import Proposition
from propositionLayer import PropositionLayer

class PlanGraphLevel(object):
	#Clase para representar un nivel en el graphplan
	
	independentActions = []
	actions = []
	props = []
	
	@staticmethod
	def setIndependentActions(independentActions):
		PlanGraphLevel.independentActions = independentActions
	
	@staticmethod	
	def setActions(actions):
		PlanGraphLevel.actions = actions
	
	@staticmethod		
	def setProps(props):
		PlanGraphLevel.props = props	 
	
	def __init__(self):
		#Constructor
		self.actionLayer = ActionLayer() #Ver actionLayer.py
		self.propositionLayer = PropositionLayer() #Ver propositionLayer.py
	
	def getPropositionLayer(self):
		return self.propositionLayer
	
	def setPropositionLayer(self, propLayer):
		self.propositionLayer = propLayer	
	
	def getActionLayer(self):
		return self.actionLayer
	
	def setActionLayer(self, actionLayer):
		self.actionLayer = actionLayer
	
	def updateActionLayer(self, previousPropositionLayer):
		#Actualiza las acciones dadas en el anterior nivel (ver propositionLayer.py)
		allActions = PlanGraphLevel.actions
		for a in allActions:
			if previousPropositionLayer.allPrecondsInLayer(a):
				self.actionLayer.addAction(a)
	
	def updateMutexActions(self, previousLayerMutexProposition):
		#Actualiza las acciones mutex
		currentLayerActions = self.actionLayer.getActions()
		for a_i in currentLayerActions:
			for a_j in currentLayerActions:
				if a_i != a_j and mutexActions(a_i, a_j, previousLayerMutexProposition):
					if Pair(a_i,a_j) not in self.actionLayer.mutexActions:
						self.actionLayer.addMutexActions(a_i,a_j)
	
	def updatePropositionLayer(self):
		#Actualiza los estados del nivel actual
		currentLayerActions = self.actionLayer.getActions()
		for a in currentLayerActions:
			for p in a.getAdd():
				if p not in self.propositionLayer.getPropositions():
					self.propositionLayer.addProposition(p)
				p.addProducer(a)
	
	def updateMutexProposition(self):
		#Actualiza los estados mutex del nivel actual
		currentLayerPropositions = self.propositionLayer.getPropositions()
		currentLayerMutexActions =	self.actionLayer.getMutexActions()
		for p_i in currentLayerPropositions:
			for p_j in currentLayerPropositions:
				if p_i != p_j and mutexPropositions(p_i,p_j,currentLayerMutexActions):
					if Pair(p_i,p_j) not in self.propositionLayer.mutexPropositions:
						self.propositionLayer.mutexPropositions.append(Pair(p_i,p_j)) 
	
	def expand(self, previousLayer):
		#Expande el grafo
		previousPropositionLayer = previousLayer.getPropositionLayer()
		previousLayerMutexProposition = previousPropositionLayer.getMutexProps()

		self.updateActionLayer(previousPropositionLayer) 
		self.updateMutexActions(previousLayerMutexProposition)

		self.updatePropositionLayer()
		self.updateMutexProposition()
	
	def expandWithoutMutex(self, previousLayer):
		previousLayerProposition = previousLayer.getPropositionLayer()
		self.updateActionLayer(previousLayerProposition)
		self.updatePropositionLayer()

def mutexActions(a1, a2, mutexProps):
	#Compueba si a1 y a2 tienen efectos inconsistentes o interfieren
	if Pair(a1,a2) not in PlanGraphLevel.independentActions:
		return True

	#Cogemos las precondiciones de las dos acciones
	pre1 = a1.getPre()
	pre2 = a2.getPre()

	#Comprobamos que a1 y a2 tienen precondiciones mutex
	for p1 in pre1:
		for p2 in pre2:
			if Pair(p1, p2) in mutexProps:
				return True

	return False

def mutexPropositions(prop1, prop2, mutexActions):
	prod1 = prop1.getProducers()
	prod2 = prop2.getProducers()
	for a1 in prod1:
		for a2 in prod2:
			if Pair(a1,a2) not in mutexActions:
				return False
	return True
