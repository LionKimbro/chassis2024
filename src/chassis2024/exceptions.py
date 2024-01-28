# Copyright 2024 Lion Kimbro
# SPDX-License-Identifier: BSD-3-Clause

class Chassis2024Exception(Exception): pass

class ExecutionGraphCycleDetected(Chassis2024Exception): pass

class MultiplePackagesHandlingExecutionGraphNode(Chassis2024Exception): pass

class MultipleDefinitionsOfInterface(Chassis2024Exception): pass

class InterfaceUndefined(Chassis2024Exception): pass

