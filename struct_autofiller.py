class Type:
    def __init__(self, name, size = 0):
        self.name = name
        if name == "float" or name == "int" or name == "uint32_t" or name == "int32_t" or name == "WORD":
            size = 4
        elif name == "bool" or name == "char" or name == "uint8_t" or name == "int8_t" or name == "byte":
            size = 1
        elif name == "uint64_t" or name == "int64_t" or name == "double" or name == "DWORD":
            size = 8
        elif name == "uint16_t" or name == "int16_t":
            size = 2
        elif name == "JunkType" or name == "void*" or name == "char*":
            size = size
        else:
            print("Warning unknown type: " + name + " size: " + str(size) + " bytes")
        self.size = size

class StructVal:
    def __init__(self, name, type, offset):
        self.name = name
        self.type = type
        self.offset = offset

    def __str__(self):
        return self.name + " " + self.type.name + " " + str(self.offset)
    

class Structure:
    junkTypeStr = "JunkType"
    junkTypeAlias = "__JUNK"

    def __init__(self, name, vals):
        self.name = name
        self.vals = vals

    def __str__(self):
        s = "struct " + self.name + "{\n"
        for val in self.vals:
            if val.type.name != "JunkType":
                s += "\t" + val.type.name + " " + val.name + "; // " + hex(val.offset) + "\n"
            else:
                s += "\t" + Structure.junkTypeStr + " " + val.name + "[" + str(val.type.size) + "];\n"
        s += "};\n"
        return s


def autofill(set, structName,size = -1):
    i = 0
    jnkstr = Structure.junkTypeAlias

    struct = []

    while i < size or len(set) > 0:
        begin = i
        while i != set[0].offset:
            i+=1

        if(i != begin):
            struct.append(StructVal(jnkstr + str(hex(begin)), Type(Structure.junkTypeStr, i - begin), begin))

        val = set[0]
        i += val.type.size
        struct.append(val)
        set = set[1:]
        
    return struct

playerOffsets = [
    StructVal("vTable", Type("uint32_t"), 0x0),
    StructVal("timeAlive", Type("float"), 0x3C),
    StructVal("xSpeed", Type("float"), 0x94),
    StructVal("ySpeed", Type("float"), 0x98),
    StructVal("zSpeed", Type("float"), 0x9C),
    StructVal("xPos", Type("float"), 0xA0),
    StructVal("yPos", Type("float"), 0xA4),
    StructVal("zPos", Type("float"), 0xA8),
    StructVal("m_iTeamNum", Type("uint8_t"), 0xF4),
    StructVal("hps", Type("int"), 0x100),
    StructVal("height", Type("float"), 0x110),
    StructVal("longitude", Type("float"), 0x12C),
    StructVal("latitude", Type("float"), 0x130),
    StructVal("boneMatrix", Type("uint32_t"), 0x26A8),
    StructVal("m_flFlashMaxAlpha", Type("float"), 0x1046C),
    StructVal("iGlowIndex", Type("uint8_t"), 0x10488),
]

glowingManager = [
    StructVal("r", Type("float"), 0x8),
    StructVal("g", Type("float"), 0xC),
    StructVal("b", Type("float"), 0x10),
    StructVal("a", Type("float"), 0x14),
    StructVal("m_bRenderWhenOccluded", Type("bool"), 0x28),
    StructVal("m_bRenderWhenUnoccluded", Type("bool"), 0x29),
    StructVal("m_bFullBloomRender", Type("bool"), 0x2A),
    StructVal("m_nFullBloomStencilTestValue", Type("int"), 0x2C),
    StructVal("m_nNextFreeSlot", Type("int"), 0x38),
]

playerFilled = autofill(playerOffsets, "Player")
playerStruct = Structure("Player", playerFilled)
print(playerStruct)

glowingFilled = autofill(glowingManager, "GlowingObject")
glowingStruct = Structure("GlowingObject", glowingFilled)
print(glowingStruct)
