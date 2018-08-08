import sys

with open("out.log" , "w") as out:
   with open(sys.argv[1], encoding = "ISO-8859-1" ) as inp:
       c = 0
       for line in inp.readlines():
           if "en.wikipedia" in line:
               out.write(line.split()[2]+"\n")
               c +=1
               if c > 100:
                   break





with open("urls.log", "w") as out:
    with open("out.log", "r") as innp:
       for line in innp.readlines():
           if "http://en.wikipedia.org/w/" in line:
               if "index.php" not in line:
                   line = line.replace("http://en.wikipedia.org/w/", "http://"+sys.argv[2]+"/mediawiki/index.php/")
               else:
                   line = line.replace("http://en.wikipedia.org/w/", "http://"+sys.argv[2]+"/mediawiki/")
               out.write(line)
           elif "http://en.wikipedia.org/wiki/" in line:
               if "index.php" not in line:
                   line = line.replace("http://en.wikipedia.org/wiki/", "http://"+sys.argv[2]+"/mediawiki/index.php/")
               else:
                   line = line.replace("http://en.wikipedia.org/wiki/", "http://"+sys.argv[2]+"/mediawiki/")
               out.write(line)
