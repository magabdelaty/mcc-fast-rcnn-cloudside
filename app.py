

__author__ = 'Maged'

import falcon
import netprofile
import upload_manager
import dropBox_upload_manager
import download_manager
import service_discovery
import idle_power_estimate
import object_detection

api = application = falcon.API()

upload_file = upload_manager.Collection("/home/maged/share/Python/Simplicity/files")
upload_dropBox_file = dropBox_upload_manager.Collection("/home/maged/share/Python/Simplicity/files")
download_file = download_manager.Item("/home/maged/share/Python/Simplicity/files")

objDetect = object_detection.Detect("/home/maged/share/Python/Simplicity/files")

netProfileDownImage = netprofile.Item("/home/maged/share/Python/Simplicity/files")
netProfileUpImage = netprofile.Collection("/home/maged/share/Python/Simplicity/files")

serviceDiscovery = service_discovery.Discover("/home/maged/share/Python/Simplicity")
idlePowerEstimate = idle_power_estimate.IdlePowerEstimate()

api.add_route("/files", upload_file)
api.add_route("/files/{name}", download_file)
api.add_route("/object_detection/detect/{name}", objDetect)

api.add_route("/netprofile/{name}", netProfileDownImage)
api.add_route("/netprofile", netProfileUpImage)

api.add_route("/service_discovery", serviceDiscovery)

api.add_route("/idle_power_estimate", idlePowerEstimate)



