
import rhinoscriptsyntax as rs
from Particle import Particle
from Particle import Attractor
from curveMaker import CurveMaker
import random as r
import Rhino

def main():
    #boxs = rs.ObjectsByName("box")
    #min = rs.ObjectsByName("min")
    #max = rs.ObjectsByName("max")
    
    box = rs.GetBox(prompt1="select box")
    
    attrPointIn = rs.GetObjects("select attractors",1)
    attrs = []
    for a in attrPointIn:
        point = rs.coerce3dpoint(a)
        attrs.append(Attractor(point, -2, 10))
    
    minPoint = box[0]
    maxPoint = box[6]
    
    size = 5.0
    location = [0,0,0]
    vel = [0,0,0]
    acc = [0,0,0]
    
    particles = []
    boundingBox = Rhino.Geometry.BoundingBox(minPoint,maxPoint)
    for i in range(0,500):
        x = random.uniform(minPoint[0],maxPoint[0])
        y = random.uniform(minPoint[1],maxPoint[1])
        z = random.uniform(maxPoint[2],maxPoint[2])
        
        acc = random.uniform(-.01,-0.5)
        #size = random.uniform(.008,0.9)
        tempParticle = Particle(size, [x,y,z], vel, [0,0,acc])
        tempParticle.setBoundingBox(boundingBox)
        particles.append(tempParticle)
    
    for i in range(0,100):
            loop(particles, attrs)
    
    curves = [] 
    for particle in particles:
        curve = particle.drawCurve()
        if curve !=0 :
            curves.append(curve)
    
    for curve in curves:
        idx = random.randint(0,len(curves)-1)
        curve2 = curves[idx]
        #if(curve != curve2):
            #curveMaker = CurveMaker (curve, curve2, 20)
            #curveMaker.drawLinesBetweenCurves()
    
    
    print"finished"

def GeneratePointFromCurve(inputCrv,distance,angle,threshold):
    #generates a point off of a curve of a line
    #returns list: [ point , vector ] 
    crvDomain = rs.CurveDomain(inputCrv)
    ptParam = ((crvDomain[1]-crvDomain[0])/2)+crvDomain[0]
    crvPt = rs.EvaluateCurve(inputCrv,ptParam)
    curveTan = rs.CurveTangent(inputCrv,ptParam)
    cPlane = rs.PlaneFromNormal(crvPt,curveTan)
    rotVec = rs.VectorRotate(curveTan,r.uniform(angle-threshold,angle+threshold),cPlane[1])
    newVec = rs.VectorRotate(rotVec,r.uniform(0,360),curveTan)
    newVec = rs.VectorUnitize(newVec)
    tailVec = rs.VectorScale(newVec,tailDist)
    baseVec = rs.VectorScale(newVec,distance)
    headVec = rs.VectorScale(newVec,headDist)
    newPt = rs.PointAdd(crvPt,baseVec)

    newBranch = Branch(crvPt,baseVec,[newPt,headVec],[crvPt,rs.VectorReverse(tailVec)])
    objList.append(newBranch)
    return [newPt,baseVec]
def GeneratePointFromPoint(inputPt,prevVec,distance,angle,threshold):
    cPlane = rs.PlaneFromNormal(inputPt,prevVec)
    rotVec = rs.VectorRotate(prevVec,r.uniform(angle-threshold,angle+threshold),cPlane[1])
    newVec = rs.VectorRotate(rotVec,r.uniform(0,360),prevVec)
    newVec = rs.VectorUnitize(newVec)
    tailVec = rs.VectorScale(newVec,tailDist)
    baseVec = rs.VectorScale(newVec,distance)
    headVec = rs.VectorScale(newVec,headDist)
    newPt = rs.PointAdd(inputPt,baseVec)
    newBranch = Branch(inputPt,baseVec,[newPt,headVec],[inputPt,rs.VectorReverse(tailVec)])
    objList.append(newBranch)
    return [newPt,baseVec]



class Branch():


    def __init__(self, BASE,VECTOR, HEAD, TAIL):
        self.base = BASE
        #vector list: previous vector,currentvector
        self.vec = VECTOR
        #self.bounds = BOUNDS
        #self.bPts = BRANCHPOINTS
        self.head = HEAD
        self.tail = TAIL
        #self.gen = GEN
        
    def grow(self):
        p1 = self.head[0]
        p2 = rs.PointAdd(self.head[0],self.head[1])
        rs.AddLine(p1,p2)
        p1 = self.tail[0]
        p2 = rs.PointAdd(self.tail[0],self.tail[1])
        rs.AddLine(p1,p2)
#create the Branching
def update():
    for i in range (0, len(objList)):
        objList[i].grow()
#def generateHair():
    

def main():
    startCrv = rs.GetObject("select start Curve",4)
    if startCrv is None:
        print "curve Fail"
        return 
        
    divPts = rs.DivideCurve(startCrv,divCount)
    paramList = []
    for i in range (0,len(divPts)):
        cP = rs.CurveClosestPoint(startCrv,divPts[i])
        paramList.append(cP)
    divCrv = rs.SplitCurve(startCrv,paramList)
    
    for i in range (0,len(divCrv)):
        branchPt = GeneratePointFromCurve(divCrv[i],dist,90,20)
        rs.AddLine(rs.CurveMidPoint(divCrv[i]),branchPt[0])
        
        treeLoop(0,maxBranch,branchPt)
            
def treeLoop(currentGen,maxGen,prevPt):
    if currentGen < maxGen:
        newPt = GeneratePointFromPoint(prevPt[0],prevPt[1],dist,45,10)
        rs.AddLine(prevPt[0],newPt[0])
        treeLoop(currentGen+1,maxGen,newPt)
    else:
        return
            
objList = []




divCount = 15
maxBranch = 4
dist = 5
headDist = 5
tailDist = 3




rs.EnableRedraw(False)
main()
update()
rs.EnableRedraw(True)




def loop(particles, attractor):
    rs.EnableRedraw(False)
    drawPoints = []
    for particle in particles:
        applyRepel(particle,attractor)
        particle.update()
        tempPoint = particle.draw()
        if tempPoint:
            drawPoints.append(tempPoint)
    rs.EnableRedraw(True)
    rs.EnableRedraw(False)
    rs.DeleteObjects(drawPoints)


def applyRepel(particle, attractors):
    for attr in attractors:
        attrVector = attr.attract(particle)
        if attrVector:
            particle.applyForce(attrVector)
        

def drawSphere(particles):
    for particle in particles:
        tempPoint = particle.draw()
        if tempPoint:
            rs.AddSphere(rs.coerce3dpoint(tempPoint),particle._size)

if(__name__ == "__main__"):
    main()

