import sys
import javalang

class JavaParser():
	"""JavaParser"""
	def parser(self, src):
		sys.setrecursionlimit(10**6) 
		self.tree = javalang.parse.parse(src)

	def extract_operations(self):
		return self._extract_declarations()

	def extract_calls(self):
		return self._extract_invocations() + self._extract_annotations()

	def extract_associations(self):
		return self._extract_imports()

	def _extract_imports(self):
		imports = []
		for path, node in self.tree.filter(javalang.tree.Import):
			imports.append(node.path.replace('.', '/'))		
		return imports

	def _extract_methods(self):
		methods = []
		for path, node in self.tree.filter(javalang.tree.MethodDeclaration):
			modifiers = self._get_method_modifier(node)
			methods.append({'name': node.name, 'modifiers': modifiers})
		return methods

	def _get_method_modifier(self, node):
		modifiers = {}
		for modifier in node.modifiers:
			modifiers[modifier] = modifier

		return modifiers

	def _extract_invocations(self):
		calls = []
		for path, node in self.tree.filter(javalang.tree.MethodInvocation):
			calls.append(node.member)
		return calls	

	def _extract_annotations(self):
		annotations = []
		for path, node in self.tree.filter(javalang.tree.Annotation):
			annotations.append(node.name)
		return annotations

	def _extract_declarations(self):
		declarations = []
		for path, node in self.tree.filter(javalang.tree.Declaration):
			if (isinstance(node, javalang.tree.AnnotationDeclaration)
				or isinstance(node, javalang.tree.MethodDeclaration)):
				modifiers = self._get_method_modifier(node)
				declarations.append({'name': node.name, 'modifiers': modifiers})
		return declarations		