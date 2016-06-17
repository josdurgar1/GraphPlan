from util import Pair
import copy
from propositionLayer import PropositionLayer
from planGraphLevel import PlanGraphLevel
from action import Action
from Parser import Parser

class GraphPlan(object):
	#Clase para inicizalizar y ejecutar el algoritmo graphplan

	def __init__(self,domain, problem):
		#Constructor de la clase
		self.independentActions = set()
		self.noGoods = []
		self.graph = []
		p = Parser(domain, problem)
		self.actions, self.propositions = p.parseActionsAndPropositions() #Listado de todas las acciones y estados
		self.initialState, self.goal = p.pasreProblem()	#El estado iniacial y el objetivo (que son una lista de estados)
		self.createNoOps() #Crea el noOps que se usa para propagar estados de una capa a la siguiente
		self.independent() #Crea el listado de acciones independent y actualiza self.independentActions
		PlanGraphLevel.setIndependentActions(self.independentActions)
		PlanGraphLevel.setActions(self.actions)
		PlanGraphLevel.setProps(self.propositions)
 
		
	def graphPlan(self): 
		#El algoritmo graphplan en sí
		
		#Inicialización
		initState = self.initialState
		level = 0
		self.noGoods = []
		self.noGoods.append([])
		
		#Crea la primera capa del grafo, que no consiste más que en el estado inicial
		propLayerInit = PropositionLayer()
		for prop in initState:
			propLayerInit.addProposition(prop)
		pgInit = PlanGraphLevel()
		pgInit.setPropositionLayer(propLayerInit)
		self.graph.append(pgInit)
		
		#Mientras que la capa no contiene todos los estados del estado final buscado (o están mutex) continuamos expandiendo el grafo
		while self.goalStateNotInPropLayer(self.graph[level].getPropositionLayer().getPropositions()) or \
				self.goalStateHasMutex(self.graph[level].getPropositionLayer()):
			if self.isFixed(level):
				return None	#Si llegamos aquí paramos porque significa que hemos llegado a un fixed point en el grafo, así que no podemos hacer nada más
				
			self.noGoods.append([])
			level = level + 1 #Actualizamos el nivel
			pgNext = PlanGraphLevel() #Crea un nuevo objeto GraphPlan
			pgNext.expand(self.graph[level - 1]) #Llama a la función expandir
			self.graph.append(pgNext) #Une el nuevo nivel generado con el graphplan
		
			sizeNoGood = len(self.noGoods[level])
		
		plan = self.extract(self.graph, self.goal, level) #Intentamos hallar un plan (si todos los estados objetivos están en este nivel y no están mutex)
		while(plan is None): #Hacemos esto mientras no podemos encontrar un plan
			level = level + 1 
			self.noGoods.append([])
			pgNext = PlanGraphLevel() #Crea el próximo nivel del grafo
			pgNext.expand(self.graph[level - 1]) #Y ahora lo expande
			self.graph.append(pgNext)
			plan = self.extract(self.graph, self.goal, level) #Intentamos econtrar el plan
			if (plan is None and self.isFixed(level)): #Si fallamos y encontramos un punto un fixed point
				if sizeNoGood == len(self.noGoods[level]): #Si el tamaño de noGood no cambia significa que hemos fallado y no hay plan
					return None
				sizeNoGood = len(self.noGoods[level]) #Si no, significa que aún podemos encontrar el plan y actualizamos el tamaño de noGood
		return plan
	 

	def extract(self, Graph, subGoals, level):
		#Método que se utiliza para intentar extraer un plan atendiendo al objetivo
		
		if level == 0:
			return []
		if subGoals in self.noGoods[level]:
			return None
		plan = self.gpSearch(Graph, subGoals, [], level)
		if plan is not None:
			return plan
		self.noGoods[level].append([subGoals])
		return None
		 
	def gpSearch(self, Graph, subGoals, plan, level):
		if subGoals == []:
			newGoals = []
			for action in plan:
				for prop in action.getPre():
					if prop not in newGoals:
						newGoals.append(prop)						
			newPlan = self.extract(Graph, newGoals, level - 1)
			if newPlan is None:
				return None
			else:
				return newPlan + plan
		
		prop = subGoals[0]
		providers = []
		for action1 in [act for act in Graph[level].getActionLayer().getActions() if prop in act.getAdd()]:
			noMutex = True
			for action2 in plan:
				if Pair(action1, action2) not in self.independentActions:
					noMutex = False
					break
			if noMutex:
				providers.append(action1)
		for action in providers:
			newSubGoals = [g for g in subGoals if g not in action.getAdd()]
			planClone = list(plan)
			planClone.append(action)
			newPlan = self.gpSearch(Graph, newSubGoals, planClone, level)
			if newPlan is not None:
				return newPlan
		return None
		
	
	def goalStateNotInPropLayer(self, propositions):
		#Función auxiliar que recibe una lista de estados y devuelve true si no están todas los estados finales en la lista
		for goal in self.goal:
			if goal not in propositions:
				return True
		return False	
	
	def goalStateHasMutex(self, propLayer):
		#Función auxiliar que comprueba que los estados del objetivo no están mutex en el nivel actual del grafo
		for goal1 in self.goal:
			for goal2 in self.goal:
				if propLayer.isMutex(goal1,goal2):
					return True
		return False
	
	def isFixed(self, level):
		#Comprueba si hemos encontrado un fixed point, es decir, si por ejemplo expandimos el grafo y el resultado que obtenemos es el mismo, por lo tanto no tendría sentido seguir
		if level == 0:
			return False
		
		if len(self.graph[level].getPropositionLayer().getPropositions()) == len(self.graph[level - 1].getPropositionLayer().getPropositions()) and \
			len(self.graph[level].getPropositionLayer().getMutexProps()) == len(self.graph[level - 1].getPropositionLayer().getMutexProps()):
			return True
		return False	
	
	def createNoOps(self):
		for prop in self.propositions:
			name = prop.name
			precon = []
			add = []
			precon.append(prop)
			add.append(prop)
			delete = []
			act = Action(name,precon,add,delete, True)
			self.actions.append(act)
			prop.addProducer(act)
	 
	def independent(self):
		#Crea un set de acciones independientes
		for i in range(len(self.actions)):
			for j in range(i + 1,len(self.actions)):
				act1 = self.actions[i]
				act2 = self.actions[j]
				if independentPair(act1,act2):
					self.independentActions.add(Pair(act1,act2)) 

	def isIndependent(self, a1, a2):
		return Pair(a1,a2) in self.independentActions	
	
	
	def noMutexActionInPlan(self, plan, act, actionLayer):
		#Función auxiliar que usamos cuando intentamos hallar un plan, devuelve true si no hay estados mutex en el plan
		for planAct in plan:
			if actionLayer.isMutex(Pair(planAct,act)):
				return False
		return True	

def independentPair(a1, a2):
	#Devuelve true si las actiones no tienen efectos inconsistentes la una con la otra
	if a1 == a2:
		return True
	for p in a1.getDelete():
		if a2.isPreCond(p) or a2.isPosEffect(p):
			return False
	for p in a2.getDelete():
		if a1.isPreCond(p) or a1.isPosEffect(p):
			return False
	return True

if __name__ == '__main__':	
	import sys
	import time
	
	domain = 'domain.txt'
	problem = 'problem.txt'
	
	gp = GraphPlan(domain, problem)
	start = time.clock()
	plan = gp.graphPlan()
	elapsed = time.clock() - start
	if plan is not None:
		print("Encontrado un plan con %d acciones en %.2f segundos" % (len([act for act in plan if not act.isNoOp()]), elapsed))
	else:
		print("No se pudo encontrar un plan satisfactorio en %.2f segundos" %	elapsed)
