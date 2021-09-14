def main():
    import os
    

    path_to_file=os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "rpsenv", "Scripts", "activate_this.py"))


    #path_to_file = os.path.join(os.path.dirname(os.path.realpath(__file__)),'rpsenv', 'Scripts', 'activate_this.py')
    #os.chdir(path_to_file)
    #path_to_file=path_to_file+"\\rpsenv\Scripts\\activate_this.py"

    #print("file path is", path_to_file)
    exec(compile(open(path_to_file, "rb").read(), path_to_file, 'exec'), dict(__file__=path_to_file))

    #exec(compile(open(str(path_to_file)).read(), path_to_file, 'exec'))
    #exec(open(str(path_to_file)).read())
    