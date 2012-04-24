class MyLogger
   
    def __init__(self, logfile_location):
        self.logfile = open(logfile_location,"w");
        
    def print(message)
        self.logfile.write('%s\n' % message)