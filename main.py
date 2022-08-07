import os,json,shutil,zipfile

with open("carsNames.json") as f:
    carNames = json.load(f)


defaltJbeam = """
{
"SKINNAME": {
    "information":{
        "authors":"AUTHOR",
        "name":"NAME",
        "value":1000
    },
    "slotType" : "paint_design",
    "globalSkin" : "SKINNAME"
  },
}
"""

defaltCs = """
singleton Material("CARNAME.skin.SKINNAME")
  {
   mapTo = "CARNAME.skin.SKINNAME";
   colorPaletteMap[2] = "vehicles/CARNAME/SKINNAME/SKINNAME_color.FILETYPE";
   overlayMap[2] = "vehicles/CARNAME/SKINNAME/SKINNAME.FILETYPE";
   diffuseMap[2] = "vehicles/CARNAME/CARNAME_c.FILETYPE";
   specularMap[2] = "vehicles/CARNAME/CARNAME_s.FILETYPE";
   normalMap[2] = "vehicles/CARNAME/CARNAME_n.FILETYPE";
   diffuseMap[1] = "vehicles/CARNAME/CARNAME_d.FILETYPE";
   specularMap[1] = "vehicles/CARNAME/CARNAME_s.FILETYPE";
   normalMap[1] = "vehicles/CARNAME/CARNAME_n.FILETYPE";
   diffuseMap[0] = "vehicles/common/null.FILETYPE";
   specularMap[0] = "vehicles/common/null.FILETYPE";
   normalMap[0] = "vehicles/CARNAME/CARNAME_n.FILETYPE";
   specularPower[0] = "128";
   pixelSpecular[0] = "1";
   specularPower[1] = "32";
   pixelSpecular[1] = "1";
   specularPower[2] = "128";
   pixelSpecular[2] = "1";
   diffuseColor[0] = "1 1 1 1";
   diffuseColor[1] = "1 1 1 1";
   diffuseColor[2] = "1 1 1 1";
   useAnisotropic[0] = "1";
   useAnisotropic[1] = "1";
   useAnisotropic[2] = "1";
   castShadows = "1";
   translucent = "1";
   translucentBlendOp = "None";
   alphaTest = "0";
   alphaRef = "0";
   dynamicCubemap = true; //cubemap = "BNG_Sky_02_cubemap";
   instanceDiffuse[2] = true;
   materialTag0 = "beamng"; materialTag1 = "vehicle";
   };
"""

defaltJson ="""
{
 "CARNAME.skin.SKINNAME" : {
    "name" : "CARNAME.skin.SKINNAME",
    "class" : "Material",
    "persistentId" : "",
    "Stages" : [
      {
        "colorMap" : "vehicles/CARNAME/SKINNAME/SKINNAME_color.FILETYPE",
        "normalMap" : "vehicles/CARNAME/CARNAME_n.FILETYPE",
        "pixelSpecular" : true,
        "specularMap" : "vehicles/common/null.FILETYPE",
        "specularPower" : 128,
        "useAnisotropic" : true
      },
      {
        "colorMap" : "vehicles/CARNAME/CARNAME_d.FILETYPE",
        "normalMap" : "vehicles/CARNAME/CARNAME_n.FILETYPE",
        "pixelSpecular" : true,
        "specularMap" : "vehicles/CARNAME/CARNAME_s.FILETYPE",
        "specularPower" : 32,
        "useAnisotropic" : true
      },
      {
        "colorMap" : "vehicles/CARNAME/CARNAME_c.FILETYPE",
        "instanceDiffuse" : false,
        "normalMap" : "vehicles/CARNAME/CARNAME_n.FILETYPE",
        "pixelSpecular" : true,
        "specularMap" : "vehicles/CARNAME/CARNAME_s.FILETYPE",
        "specularPower" : 64,
        "useAnisotropic" : true
      },
      {}
    ],
    "alphaRef" : 0,
    "dynamicCubemap" : true,
    "mapTo" : "CARNAME.skin.SKINNAME",
    "materialTag0" : "beamng",
    "materialTag1" : "vehicle",
    "translucent" : true,
    "translucentBlendOp" : "None"
  }
}
"""


print("""
██████  ███████  █████  ███    ███ ███    ██  ██████  
██   ██ ██      ██   ██ ████  ████ ████   ██ ██       
██████  █████   ███████ ██ ████ ██ ██ ██  ██ ██   ███ 
██   ██ ██      ██   ██ ██  ██  ██ ██  ██ ██ ██    ██ 
██████  ███████ ██   ██ ██      ██ ██   ████  ██████  
                                                      

░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▒▓▓███▓▒░░░░░░░░░░░░░░░░░
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▓████████▓░░░░░░░░░░░░░░░░
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░██████████▒░░░░░░░░░░░░░░░
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▒▓▒░▓█████████▒░░░░░░░░░░░░░░░
░░░░░░░░░░░░░░░░░░░░░░░░░░░▒▓████▒░▓██████▓▒░░░░░░░░░░░░░░░░
░░░░░░░░░░░░▒▓████████▓▒░░▓██████▓░░░░▒▒▒░▒▒░░░░░░░░░░░░░░░░
░░░░░░░░░░▓██████████████▒░▒██▓▒░░░░░░▒████▓░░░░░░░░░░░░░░░░
░░░░░░░░░▓████████████████▓░░░░░░░░░░░░█████░░░░░░░░░░░░░░░░
░░░░░░░░▓██████████████████▓░░░░░░░░░░░█████░░░░░░░░░░░░░░░░
░░░░░░░░████████████████████░░░░░░░░░░░▓████▒░░░░░░░░░░░░░░░
░░░░░░░░████████████████████░░░░░░░░░░░▒████▓░░░░░░░░░░░░░░░
░░░░░░░░▓██████████████████▒░▒▒░░░░░░░░░▒▒▒▒▒░░░░░░░░░░░░░░░
░░░░░░░░░▓████████████████▒░▒████▓▒░░░░▒▓▓███▓▒▒░░░░░░░░░░░░
░░░░░░░░░░▒▓████████████▓░░▒███████░░▓██████████▓▒░░░░░░░░░░
░░░░░░░░░░░░░▒▓▓▓▓▓▓▓▒▒░░░░░░░▒▓██░░██████████████▒░░░░░░░░░
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▓███████████████░░░░░░░░░
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▓██████████████▓░░░░░░░░░
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░██████████████▒░░░░░░░░░
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▓██████████▓░░░░░░░░░░░
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▒▓▓▓▓▓▓▒░░░░░░░░░░░░░
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░



███████ ██   ██ ██ ███    ██     ███    ███  █████  ██   ██ ███████ ██████  
██      ██  ██  ██ ████   ██     ████  ████ ██   ██ ██  ██  ██      ██   ██ 
███████ █████   ██ ██ ██  ██     ██ ████ ██ ███████ █████   █████   ██████  
     ██ ██  ██  ██ ██  ██ ██     ██  ██  ██ ██   ██ ██  ██  ██      ██   ██ 
███████ ██   ██ ██ ██   ████     ██      ██ ██   ██ ██   ██ ███████ ██   ██ 
                                                                            
by myrccar




""")

skinName = input("enter skin name(no space): ").replace(" ","_")
print("")

#don't ask just know it works
split_appdata = os.getenv('APPDATA').split("\\")
path = split_appdata[0]+"/"+split_appdata[1]+"/"+split_appdata[2]+"/"+split_appdata[3]+"/Local/BeamNG.drive/0.25/mods/unpacked/"+skinName
os.mkdir(path)
path = path+"/vehicles"
os.mkdir(path)

for x in carNames["cars"]:
    print(f'({carNames["cars"].index(x)}) {list(x.keys())[0]}')


carName = input("slect car: ")
carName = carNames["cars"][int(carName)][list(carNames["cars"][int(carName)].keys())[0]]

path += "/"+carName
os.mkdir(path)
path += "/"+skinName
os.mkdir(path)

#copy uv map
shutil.copyfile(f'uvs/{carName}_skin_UVs.png',f'{path}\skin map(export as SKINNAME dot dds).png')
shutil.copyfile(f'uvs/{carName}_skin_UVs.png',f'{path}\skin color(beamng docs) map(export as SKINNAME_color dot dds).png')

#make the .jbeam file
with open(f'{path}\{skinName}.jbeam',"w") as f:
    f.write(defaltJbeam.replace("SKINNAME",skinName).replace("NAME",input("enter name that shows up: ")).replace("AUTHOR",input("enter author: ")))

#get file type .dds/.data
if os.path.exists(f'vehicles/{carName}/{carName}_n.dds'):
  fileType = "dds"
else: fileType = "data"


#make mat.cs/json
if input("materials.cs(old) or materials.json(new) c/j: ") == "c":
    with open(f'{path}\materials.cs',"w") as f:
        f.write(defaltCs.replace("CARNAME",carName).replace("SKINNAME",skinName).replace("FILETYPE",fileType))
else:
    with open(f'{path}\materials.json',"w") as f:
        f.write(defaltJson.replace("CARNAME",carName).replace("SKINNAME",skinName).replace("FILETYPE",fileType))


input("enter to close")
os.system('start '+path)