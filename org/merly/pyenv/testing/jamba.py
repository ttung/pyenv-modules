import pyenv

class Module(pyenv.Module):
    def __init__(self, name):
        pyenv.Module.__init__(self, name)


    def preload(self, env):
        return []


    def load(self, env, shell):
        shell.add_shell_variable('jamba', 'juice')


    def unload(self, env, shell):
        shell.remove_shell_variable('jamba')
