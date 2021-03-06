from ecolyzer.ecosystem import Relationship, Ecosystem
from ecolyzer.system import Operation


class CentralSoftwareUsage:
	"""CentralSoftwareUsage"""

	def execute(self, dataaccess):
		ecosystem = dataaccess.query(Ecosystem).first()  # TODO: associate system to ecosystem
		relations = dataaccess.query(Relationship).all()
		to_system = relations[0].to_system
		ecosystem_name = to_system.name
		if ecosystem:
			ecosystem_name = ecosystem.name
		components = []
		source_pos = {}
		paths = {}
		source_ids = []
		source_ids_map = {}
		component_operations = {}

		to_source_files = to_system.source_files
		operations_map = self._get_operations_map(to_source_files,
												 to_system.id, dataaccess)
		dependent_systems_map = {}
		dependent_systems_by_package = {}
		for rel in relations:
			source_id = rel.to_source_file_id
			curr_operation = rel.to_code_element
			dependent_systems_map[rel.from_system.name] = True
			if rel.from_system.name not in dependent_systems_by_package:
				dependent_systems_by_package[rel.from_system.name] = {}
			if rel.to_source_file.path not in dependent_systems_by_package[rel.from_system.name]:
				dependent_systems_by_package[rel.from_system.name][rel.to_source_file.path] = 0
			dependent_systems_by_package[rel.from_system.name][rel.to_source_file.path] += 1
			if source_id in source_pos:
				pos = source_pos[source_id]
				components[pos]['count'] += 1
				components[pos]['total'] += rel.from_code_element_count
				if component_operations[source_id][curr_operation.name]:
					component_operations[source_id][curr_operation.name] = False
					components[pos]['coverage'] += 1
			else:  # enter here just in the first time
				source_pos[source_id] = len(components)
				operations = operations_map[source_id]
				component_operations[source_id] = {}
				for op in operations:
					component_operations[source_id][op.name] = True
				component_operations[source_id][curr_operation.name] = False 
				file_mod = curr_operation.modification	
				info = {
					'id': source_id,
					'source': rel.to_source_file.name,
					'fullpath': rel.to_source_file.fullpath,
					'path': rel.to_source_file.path,
					'system': rel.to_system.name,
					'operations': len(operations),
					'nloc': file_mod.nloc,
					'coverage': 1,
					'count': 1,
					'total': rel.from_code_element_count
				}
				components.append(info)
				paths[rel.to_source_file.path] = 0
				source_ids.append(source_id)
				source_ids_map[source_id] = rel.to_source_file

		sources_without_relation = self._sources_without_relation(source_ids_map, to_source_files)
		sources_without_relation_info = []
		for src in sources_without_relation:
			operations = []
			if src.id in operations_map:
				operations = operations_map[src.id]
			if len(operations) > 0:		
				file_mod = operations[0].modification 
				info = {
					'id': src.id,
					'source': src.name,
					'fullpath': src.fullpath,
					'path': src.path,
					'system': to_system.name,
					'operations': len(operations),
					'nloc': file_mod.nloc,
					'coverage': 0,
					'count': 0,
					'total': 0
				}
				sources_without_relation_info.append(info)
				paths[src.path] = 0
		
		components = components + sources_without_relation_info	

		return {'components': components, 
				'central_software': ecosystem_name,
				'component_paths': paths,
				'dependents_count': len(dependent_systems_map),
				'dependents_by_package': dependent_systems_by_package}	

	def _get_operations_map(self, source_files, system_id, dataaccess):
		operations_map = {}
		for source_file in source_files.values():
			for ce in source_file.code_elements().values():
				if isinstance(ce, Operation):
					if source_file.id not in operations_map:
						operations_map[source_file.id] = []
					operations_map[source_file.id].append(ce)
		return operations_map		

	def _sources_without_relation(self, source_ids_map, source_files):
		sources_without_relation = []
		for source_file in source_files.values():
			if source_file.id not in source_ids_map:
				sources_without_relation.append(source_file)
		return sources_without_relation
