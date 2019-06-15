#!/usr/bin/python
import sys 

from PySide import QtUiTools
from PySide import QtCore
from PySide.QtGui import *

import roslib
import rospy
from std_msgs.msg import String
import termios, tty, os, time

pub = rospy.Publisher('setup_requests', String, queue_size = 1)

class myMenu(QDialog):

	def callback_files(self,data):
		rospy.sleep(0.5)
		msg_data = str(data.data).split(',')
		temp = []
		for x in msg_data:
			x = x.replace(" ","")
			x = x.replace("[","")
			x = x.replace("]","")
			x = x.replace("'","")
			temp.append(x)
		filenames = sorted(temp)
		for x in filenames:
			self.listWidget.addItem(QtWidgets.QListWidgetItem(x))

	def __init__(self):
		super(myMenu,self).__init__()
		filedir = os.path.dirname(os.path.abspath(__file__))
		print filedir
		uiFile_path = os.path.join(filedir,'setup.ui')

                uifile = QtCore.QFile(uiFile_path)
		self.window = QtUiTools.QUiLoader().load(uifile)
		uifile.close()

		rospy.Subscriber("route_file",String,self.callback_files)
		pub.publish("files")
		print "filename request published"

                self.window.findChild(QPushButton, 'save_session').clicked.connect(self.button_save)
                self.window.findChild(QPushButton, 'safepoints').clicked.connect(self.button_safepoints)
                self.window.findChild(QPushButton, 'safepaths').clicked.connect(self.button_safepaths)
                self.window.findChild(QPushButton, 'route').clicked.connect(self.button_route)
                self.window.findChild(QListWidget, 'listWidget').setSelectionMode(QAbstractItemView.SingleSelection)

	def mousePressEvent(self,event):
		super(myMenu, self).mousePressEvent(event)

	def mouseReleaseEvent(self, event):
		super(myMenu, self).mouseReleaseEvent(event)
		self.leftClick = False

	def button_save(self):
		msg = "save_session"
		pub.publish(msg)
		#rospy.sleep(0.2)
		self.close()

	def button_new(self):
		msg = "new_session"
		pub.publish(msg)
		#rospy.sleep(0.2)
		self.close()

	def button_safepoints(self):
		msg = "safepoints"
		pub.publish(msg)
		#rospy.sleep(0.2)
		self.close()
	
	def button_safepaths(self):
		msg = "safepaths"
		pub.publish(msg)
		#rospy.sleep(0.2)
		self.close()
	
	def button_route(self):
		try:
			msg = str(self.window.findChild(QListWidget, 'listWidget').selectedItems()[0].text())
		except:
			msg = "goals_current.yaml"
		print msg
		pub.publish(msg)
		#rospy.sleep(0.2)
		self.close()


if __name__=='__main__':
	rospy.init_node('setup_requestor', anonymous=True)
	app = QApplication(sys.argv)
	window = myMenu()
	window.setWindowTitle('Ubiquity TeleOp Tool Setup')
	window.window.show()
	sys.exit(app.exec_())

