from java.io import FileInputStream
import java.lang
import os
import string

composite_path=sys.argv[1]
configplan_path=sys.argv[2]

sca_deployComposite("http://soaLB.test.com:7777",composite_path,configplan=configplan_path,partition="TEST",overwrite=true,user="weblogic",password="")

