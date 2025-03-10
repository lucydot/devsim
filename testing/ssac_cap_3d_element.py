# Copyright 2013 Devsim LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# cap device to test displacement current at contact
import devsim
import test_common

device="test"
region="bulk"
devsim.load_devices(file='3dtetmesh.msh')
#c=3.9*8.85e-14*(6e-2*6e-2)/6e-2

###
### Set parameters on the region
###
devsim.set_parameter(device=device, region=region, name="Permittivity", value=3.9*8.85e-14)

###
### Create the Potential solution variable
###
devsim.node_solution(device=device, region=region, name="Potential")

###
### Creates the Potential@n0 and Potential@n1 edge model
###
devsim.edge_from_node_model(device=device, region=region, node_model="Potential")

###
### Electric field on each edge, as well as its derivatives with respect to
### the potential at each node
###
devsim.edge_model(device=device, region=region, name="ElectricField",
                  equation="(Potential@n0 - Potential@n1)*EdgeInverseLength")

devsim.edge_model(device=device, region=region, name="ElectricField:Potential@n0",
                  equation="EdgeInverseLength")

devsim.edge_model(device=device, region=region, name="ElectricField:Potential@n1",
                  equation="-EdgeInverseLength")

###
### Model the D Field
###
devsim.element_model(device=device, region=region, name="DField",
                  equation="Permittivity*ElectricField")

devsim.element_model(device=device, region=region, name="DField:Potential@en0",
                  equation="diff(Permittivity*ElectricField, Potential@n0)")

devsim.element_model(device=device, region=region, name="DField:Potential@en1",
                  equation="-DField:Potential@en0")

devsim.element_model(device=device, region=region, name="DField:Potential@en2",
                  equation="0")

devsim.element_model(device=device, region=region, name="DField:Potential@en3",
                  equation="0")

###
### Create the bulk equation
###
devsim.equation(device=device, region=region, name="PotentialEquation", variable_name="Potential",
                element_model="DField", variable_update="default")

# the topbias is a circuit node, and we want to prevent it from being overridden by a parameter
devsim.set_parameter(device=device, region=region, name="botbias", value=0.0)

for name, equation in (
    ("topnode_model", "Potential - topbias"),
  ("topnode_model:Potential", "1"),
  ("topnode_model:topbias", "-1"),
  ("botnode_model", "Potential - botbias"),
  ("botnode_model:Potential", "1"),
):
    devsim.node_model(device=device, region=region, name=name, equation=equation)

# attached to circuit node
devsim.contact_equation(device=device, contact="top", name="PotentialEquation",
                        node_model="topnode_model", element_charge_model="DField", circuit_node="topbias")
# attached to ground
devsim.contact_equation(device=device, contact="bot", name="PotentialEquation",
                        node_model="botnode_model", element_charge_model="DField")

#
# Voltage source
#
devsim.circuit_element(name="V1", n1=1,         n2=0, value=1.0, acreal=1.0)
devsim.circuit_element(name="R1", n1="topbias", n2=1, value=1e3)

#
devsim.solve(type="dc", absolute_error=1.0, relative_error=1e-10, maximum_iterations=30)
#
print(devsim.get_contact_charge(device=device, contact="top", equation="PotentialEquation"))
print(devsim.get_contact_charge(device=device, contact="bot", equation="PotentialEquation"))
#
devsim.solve(type="ac", frequency=1e-3)
test_common.print_ac_circuit_solution()
devsim.solve(type="ac", frequency=1e10)
test_common.print_ac_circuit_solution()
devsim.solve(type="ac", frequency=1e15)
test_common.print_ac_circuit_solution()

#for i in devsim.get_element_model_values(device=device, region=region, name="DField"):
#  print(i)
#
#ec = devsim.get_edge_model_values(device=device, region=region, name="EdgeCouple")
#devsim.element_model(device=device, region=region, name="eindex", equation="edge_index")
#ei = [int(x) for x in devsim.get_element_model_values(device=device, region=region, name="eindex")]
#eec = devsim.get_element_model_values(device=device, region=region, name="ElementEdgeCouple")
#ec_compare=[0.0]*len(ec)
#for q, v in zip(ei, eec):
#  #print(q,v)
#  ec_compare[q] += v
#
#for q,v in zip(ec, ec_compare):
#  print(q,v)
