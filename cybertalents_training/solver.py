def BytePadding(x):
  Z = [0x3,0x5,0x7,0xb,0xd,0x11,0x13,0x17,0x1D,0x1F,0x25,0x29,0x2B,0x2F,0x35,0x3B,0x3D,0x43,0x47,0x49,0x4F,0x53,0x59,0x61,0x65,0x67,0x6B,0x6D,0x71,0x7F,0x83,0x89,0x8B,0x95,0x97,0x9D,0x0A3,0xA7]
  return Z[x]
def ischr(a1):
  return a1 > 96 and a1 <= 122;
def ischr_(a1):
  return a1 > 96 and a1 <= 122 or a1 > 64 and a1 <= 90;
def isNum(a1):
  return ischr_(a1) and ischr(a1) ^ 1
def Enc(usrinpt):
  usrinpt = bytearray(usrinpt)
  out = bytearray()
  for i in range(len(usrinpt)):
    chrUsrInpt = usrinpt[i]
    newChrInpt = chrUsrInpt + BytePadding(i)
    if (ischr(chrUsrInpt)):
      v4 = 0x7A
    else:
      v4 = 0x5A if (isNum(chrUsrInpt)) else chrUsrInpt
    while (newChrInpt > v4):
      newChrInpt -=0x1A
    if chrUsrInpt == ord('{'):
      _out = "}"
    elif chrUsrInpt == ord('}'):
      _out = "{"
    else:
      _out = newChrInpt if (ischr_(chrUsrInpt)) else chrUsrInpt
    if _out != "":
      out.append(_out)
  return out

flag = "IQHR}nxio_vtvk_aapbijsr_vnxwbbmm{"
Found = ""
search = ""
for char in flag:
  search += char
  for i in range(0xff):
    if Enc( Found+chr(i) ) ==  search:
      Found += chr(i)
print Found
