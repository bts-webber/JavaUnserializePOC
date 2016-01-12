import requests
from sys import argv
from string import find,strip

"""object格式：http://url:port"""
class CheckApp(object):
    def __init__(self,target):
        self.target = target

    def CheckWeblogic(self,target):
        try:
            content=requests.get(target+"/console")
        except:
            return False
        if find(content,"管理控制台")!=-1:
            return True
        else:
            return False

    def CheckJboss(self,target):
        try:
            content=requests.get(target+"/invoker/JMXInvokerServlet").content
        except:
            return False
        if content[0:21]=="\xac\xed\x00\x05sr\x00$org.jboss.inv":
            return True
        else:
            return False

    def Check(self,target):
        try:
            c=requests.get(target)
        except:
            print "Target open failed,continue......"
            return False
        app=c.headers["X-Powered-By"]
        content=c.content
        c.close()
        for a in app:
            if find(a,"Servlet")!=-1 and find(a,"JSP")!=-1:
                print "Web App is Weblogic"
                if self.CheckWeblogic(content):
                    print "Target is checkable"
                    return "Weblogic"
                else:
                    print "Target is no checkable"
                    return False
                break
            elif find(a,"JBoss-")!=-1 and find(a,"Servlet")!=-1:
                print "Web App is Jboss"
                if self.CheckJboss(target):
                    print "Target is checkable"
                    return "Jboss"
                else:
                    print "Target is not checkable"
                    return False
                break
        print "Target is not Weblogic/Jboss,continue......"
        return False

class CheckVulnerability(target):
    def __init__(self,target):
        self.target=target

    def CheckWeblogic(self,target):
        pass

    def CheckJboss(self,target):
        pass

def CheckGo(target):
    print ">>>>>>>>>>>>>>>Go Checking:"+target+"<<<<<<<<<<<<<<<"
    checkapp=CheckApp(target).Check(target)
    if checkapp==False:
        return False
    elif checkapp=="Weblogic":
        checkvulnerability=CheckVulnerability(target).CheckWeblogic(target)
        if checkvulnerability==True:
            return checkapp
        else:
            return False
    elif checkapp=="Jboss":
        checkvulnerability=CheckVulnerability(target).CheckJboss(target)
        if checkvulnerability==True:
            return checkapp
        else:
            return False
    print ">>>>>>>>>>>>>>>Checking Finished"+"<<<<<<<<<<<<<<<"

def main():
    result={"weblogic":[],"jboss":[]}
    if len(argv)>1:
        a=argv[1]
    else:
        try:
            a=raw_input("Enter staring URL(http://hotsname:port):")
        except:
            a=""
    if not a:
        return
    elif a[:6]=="http://":
        return
    else:
        try:
            f_target=open(a,"r")
            f_result=open("result.txt","w")
        except:
            print "Open File failed"
            return
        while True:
            l=f_target.readline().strip()
            result=CheckGo(l)
            if result==False:
                continue
            elif result=="Weblogic":
                result["weblogic"].append(l)
            elif result=="Jboss":
                result["jboss"].append(l)
        f_result.write(result)
        f_result.close()
        f_target.close()

if __name__=="_main__":
    main()



