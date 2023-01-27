
class Node: 

    def __init__ (self, id, pc, pl, is_wall=False):

        self.id = id
        self.pc = pc
        self.pl = pl
        self.is_wall = is_wall
    
    def __str__(self):
        
        return "Node: " + str(self.id) + " Pos: (" + str(self.pc) + "," + str(self.pl) + ")."

    def getId(self):

        return self.id

    def getPl(self):

        return self.pl
    
    def getPc(self):

        return self.pc
    
    def setId(self, id):

        self.id = id
    
    def setPl(self, pl):

        self.pl = pl

    def setPc(self, pc):

        self.pc = pc

    def isWall(self):

        return self.is_wall

    def __eq__(self, other):

        if (other == None):
            
            return False
        
        return self.id == other.id

    def is_equal(self, other):

        if (other == None): 
            
            return False

        return self.pc == other.getPc() and self.pl == other.getPl()

    def __hash__(self):

        return hash(self.id)

    def clone(self):

        return Node(self.id, self.pc, self.pl)
        
        