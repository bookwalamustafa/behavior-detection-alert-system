import platform
import os

class AlertSystem:
    def trigger_alert(self):
        if platform.system() == 'Windows':
            duration = 1000
            freq = 440
        else:
            os.system('say "Alert"')