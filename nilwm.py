
from Xlib import X, XK
from Xlib.display import display
import subprocess
import click
from time import strftime
from Preferences import preferences

def log(s):
    print(s)

class wm(object):
    "Main wm class"
    def __init__(self):
        self.windows = []
        self.display = Display()
        self.window = {
            'current': None,
            'active': None,
            'root': self.display.screen().root            
        }
        self.area = {
            'width': self.window['root'].get_geometry().width,
            'height': self.window['root'].get_geometry().height
        }
        self.window['root'].change_attributes(event_mask = X.SubstructureRedirectMask)

    def loop(self):
        self.focus()
        self.events()

    def destroy(self, event):
        try:
            self.window['active'].destroy()
            self.windows.remove(self.window['active'])
            self.window['active'] = None
        except:
            log('No focused window!')

    def focus(self):
        window = self.display.screen().root.query_pointer().child
        if window != 0:
            self.window['active'] = window

    def events(self):
        ignores = [3, 33, 34, 23]
        if self.display.pending_events() > 0:
            event = self.display.next_event()
        else:
            return
        if event.type == X.MapRequest:
            self.map(event)
        elif event.type == X.KeyPress():
            self.key(event)
        elif event.type in ignores:
            log('Ignoring event')
        else:
            log('Unhandled event')

    def map(self, event):
        self.windows.append(event.window)
        self.window['active'] = event.window
        event.window.map()

    def key(self, event):
        if event.detail in self.t:
            self.run(preferences.applicationDefaults.terminal)
        if event.detail in self.x:
            self.destroy(event)
        else:
            log('Unhandled key event')

    def run(self, applicationInfo):
        try:
            name = applicationInfo['name']
            command = applicationInfo['command']
        except:
            raise ValueError
        try:
            log('Running ' + name)
            subprocess.Popen(command)
        except BaseException as e:
            log('Failed to launch :' + command)
            log(str(e))

    def close(self):
        self.display.close()
        
if __name__ == '__main__':
    _wm = wm()
    while True:
        try:
            wm.loop()
        except KeyboardInterrupt:
            _wm.close()
