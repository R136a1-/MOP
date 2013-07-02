import os
import string
header = """Universe   = vanilla
Executable = run_mkpsf.sh
getenv     = True
notify_user = jjkavelaars@nrc-cnrc.gc.ca
notification = Complete
should_transfer_files = YES
transfer_input_files = /home/jkavelaars/.ssl/cadcproxy.pem
when_to_transfer_output = ON_EXIT
transfer_output_files = /dev/null
RunAsOwner = True
#on_exit_remove = (ExitCode == 0)

Requirements = VMType =?= "MOP"  && \
               Arch == "x86_64" && \
	       Memory >= 4000 && \
               Cpus >= 1 

+VMLoc         = "http://www.cadc-ccda.hia-iha.nrc-cnrc.gc.ca/data/pub/vospace/jkavelaars/MOP.img.gz"
+VMMem         = "4096"
+VMCPUCores    = "1"
+VMStorage     = "20"
"""
print header

task = "./scripts/prep.sh"

import vos
c = vos.Client()
for line in c.listdir('vos:OSSOS/dbimages'):
  fileId=line.strip()
  logName = "%s" %(fileId)
  print  "Arguments = %s %s %s" % (task, fileId, fileId)
  print  "Queue"
  print  ""
