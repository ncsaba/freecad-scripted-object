import os
from setuptools import setup
from setuptools.command.install import install as InstallCommand
from setuptools.command.develop import develop as DevelopCommand
import pkg_resources
import shutil
import subprocess


def copy_macros(req, source_dir, dest_dir):
    for file in pkg_resources.resource_listdir(req, source_dir):
        print file
        source = source_dir + "/" + file
        dest = dest_dir + "/" + file
        if pkg_resources.resource_isdir(req, source):
            if not os.path.isdir(dest):
                os.mkdir(dest)
            copy_macros(req, source, dest)
        else:
            with pkg_resources.resource_stream(req, source) as s, open(dest, "w") as d:
                print s, d
                shutil.copyfileobj(s, d)


def run_after(command):
    """
    Copy the free-cad macros/modules in the macro directory.

    @param command: setuptools command instance, either an InstallCommand or
    DevelopCommand.
    """
    req = pkg_resources.Requirement.parse(command.distribution.get_name())
    if pkg_resources.resource_exists(req, "freecad"):
        # get freecad macro dir
        macrodir = None
        devnull = open(os.devnull, 'w')
        for executable in ["freecadcmd", "FreeCADCmd"]:
            try:
                macrodir = subprocess.check_output([executable, "--get-config", "UserAppData"], stderr=devnull)
                break
            except:
                pass
        if macrodir is None:
            print "FreeCAD macro directory not found, please read the installation instructions !"
            return
        macrodir = macrodir.strip()
        print "Using macrodir:", macrodir
        # recursively copy files/directories to the freecad macro dir
        try:
            copy_macros(req, "freecad", macrodir)
        except Exception, ex:
            print "Error:", ex
            print "Failed copying macros, please read the installation instructions !"


def hookify(command_subclass):
    """
    A decorator for subclasses of setuptools commands that calls an after_run hook.
    """
    original_run = command_subclass.run

    def modified_run(self):
        """
        Call the original run implementation, followed by after_run.
        """
        output = original_run(self)
        run_after(self)
        return output

    # attach the new implementation
    command_subclass.run = modified_run

    # set the same run_after everywhere
    if "run_after" not in command_subclass.__dict__:
        command_subclass.run_after = run_after

    return command_subclass

# Override the "develop" and "install" commands to have the hooks.
@hookify
class CustomDevelopCommand(DevelopCommand):
    pass

@hookify
class CustomInstallCommand(InstallCommand):
    pass


setup(
    name="freecad-scripted-object",
    version="0.0.1",
    description="Simple example of a freecad parametric scripted object",
    author="Csaba Nagy",
    author_email="ncsaba@javampire.com",
    url="https://github.com/ncsaba/freecad-scripted-object",
    packages=[
        "fcso",
    ],
    cmdclass={
        "install": CustomInstallCommand,
        "develop": CustomDevelopCommand,
    },
)
