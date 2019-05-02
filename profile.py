"""
Profile for starting up a single machine. Can select hardware and image.
"""
import re

import geni.aggregate.cloudlab as cloudlab
import geni.portal as portal
import geni.rspec.emulab as emulab
import geni.rspec.pg as pg
import geni.urn as urn

# Portal context is where parameters and the rspec request is defined.
pc = portal.Context()

# The possible set of base disk-images that this cluster can be booted with.
# The second field of every tupule is what is displayed on the cloudlab
# dashboard.
images = [ ("UBUNTU14-64-STD", "Ubuntu 14.04"),
           ("UBUNTU16-64-STD", "Ubuntu 16.04"),
           ("urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU16-64-STD:45", "Ubuntu 16.04:45") ]

# The possible set of node-types this cluster can be configured with. Currently 
# only m510 machines are supported.
hardware_types = [ ("m510", "m510 (CloudLab Utah, 8-Core Intel Xeon D-1548)"),
                   ("m400", "m400 (CloudLab Utah, 8-Core 64-bit ARMv8)"),
                   ("d430", "d430 (Emulab, 8-Core Intel Xeon E5-2630v3)") ]

pc.defineParameter("image_str", "Disk Image URN", 
        portal.ParameterType.STRING, "", None,
        "URN of specific disk image to use. If blank, uses option selected in menu above.")

pc.defineParameter("image_opt", "Disk Image",
        portal.ParameterType.IMAGE, images[2], images,
        "Specify the base disk image that all the nodes of the cluster " +\
        "should be booted with.")

pc.defineParameter("hardware_type_opt", "Hardware Type",
       portal.ParameterType.NODETYPE, hardware_types[0], hardware_types)

pc.defineParameter("hardware_type_str", "Hardware Type", 
        portal.ParameterType.STRING, "", None,
        "Specific hardware type to use. If blank, uses option selected in menu above.")

params = pc.bindParameters()

# Create a Request object to start building the RSpec.
request = pc.makeRequestRSpec()

node = request.RawPC("master")
if (params.hardware_type_str != ""):
    node.hardware_type = params.hardware_type_str
else:
    node.hardware_type = params.hardware_type

if (params.image_str != ""):
    node.disk_image = params.image_str
else:
    node.disk_image = urn.Image(cloudlab.Utah, "emulab-ops:%s" % params.image)

# Generate the RSpec
pc.printRequestRSpec(request)
