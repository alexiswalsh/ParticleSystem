import rhinoscriptsyntax as rs
from Particle import Particle
from Particle import Attractor
from curveMaker import CurveMaker
import random
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

