import json, os, re
D=os.path.join(os.path.dirname(os.path.abspath(__file__)),'docs'); os.makedirs(D,exist_ok=True)
CAT={'ЗВУК':'sound','СВЕТ':'light','ВИДЕО —':'video','ВИДЕОСЪЕМКА':'cam','DJ':'dj','СПЕЦЭФФЕКТЫ':'sfx','БЭКЛАЙН':'dj','СВЯЗЬ':'comm','КОММУТАЦИЯ':'power','ЭЛЕКТРИКА':'power'}
# (regex, L, W, H, kg, stackable)
DIMS=[
 (r'J8/J12',115,60,45,65,1),(r'V8/V12',100,55,45,50,1),(r'J-SUB',135,80,70,120,1),(r'J-INFRA',135,95,85,150,0),(r'\bM4\b',70,55,40,35,1),(r'V-SUB',100,75,70,80,1),(r'KS28',140,70,58,85,0),
 (r'CHR15|B205D',70,45,45,25,1),(r'D80|D12|R70|PX10|PX5|FP14000',60,55,20,20,1),(r'DM7',120,80,45,70,0),(r'Rio3224',60,55,35,30,1),(r'DM3|MG10|Tio1608',60,50,30,15,1),
 (r'стойка',100,15,15,3,1),(r'барабан',60,40,30,10,1),(r'Shure AD4Q|Axient|SLXD4D|PSM300|UA8',55,45,25,12,1),(r'Shure|Sennheiser|DPA|Neumann',35,25,15,2,1),
 (r'Follow Spot',130,50,60,60,0),(r'TOURIST|BEAM|WASH|H1L',60,45,60,32,1),(r'STROBE',70,35,30,12,1),(r'LED BAR|Wall Washer|Laser',110,25,20,9,1),(r'BLINDER',50,30,30,10,1),(r'LPAR',35,30,25,5,1),
 (r'grandMA2$|Avolites',130,80,45,70,0),(r'Wing',90,70,35,35,1),(r'NPU|ArtNet|Distributor|Splitter',55,45,20,10,1),
 (r'^TV \d',180,30,110,40,0),(r'1000 x 500',120,60,18,21,1),(r'500 x 500',60,60,15,10,1),(r'500 x 250',60,35,15,6,1),(r'TV.*[Ss]tand',180,30,30,25,1),(r'проектор',80,70,45,70,0),
 (r'Resolume|NovaStar|Coolview|ATEM|Feelworld',60,50,25,15,1),
 (r'Sony|Blackmagic Pocket|URSA',60,45,35,12,1),(r'Amaran|Nanlite',70,40,35,10,1),
 (r'Pioneer|Allen|Akai',60,50,25,10,1),
 (r'UGY',80,60,60,50,0),(r'Mirror ball',120,120,120,30,0),(r'H-4000S|H-3000|DHZ|H-9|Haze|[Ff]og',70,45,45,25,1),(r'Sparkular',50,45,35,25,1),(r'CO₂ Jet',50,30,30,10,1),(r'DMX fan',60,60,40,20,1),(r'Баллон',30,30,150,70,0),
 (r'Stratocaster|Jazz Bass|CD-60|G310',120,45,15,8,1),(r'PDP',100,80,80,60,0),(r'Marshall|Champion|Laney',60,40,50,25,1),
 (r'Hollyland|Walkie',40,30,15,4,1),(r'TrueCON|PowerCON|XLR',40,30,10,1,1),
 (r'Power Distributions',60,50,40,35,1),(r'генератор',400,150,200,3000,0),(r'Бак',150,100,100,120,0),
 (r'Stage structure',200,200,20,100,1),(r'Stage Deck',200,100,15,45,1),(r'Box corner',50,50,50,20,1),(r'Mojo',120,100,110,50,1),(r'Chain hoist',60,45,60,58,1),
 (r'Truss 40',300,40,40,30,1),(r'Truss 30|Ферма квадрат',300,30,30,22,1),(r'Fan barrier',200,30,110,25,1),(r'Base collar',15,15,10,1,1),(r'Cable Protector',90,50,8,15,1),
 (r'J/V-Frame',150,60,40,60,1),(r'LED-экрана',120,30,20,20,1),(r'лебедками',60,50,40,30,1),
]
writes=[]
for i,line in enumerate(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'equip.tsv'),encoding='utf8')):
    sub,name,qty,rate,value,amort=line.rstrip('\n').split('\t')
    cat='other'
    for k,v in CAT.items():
        if sub.startswith(k): cat=v
    if sub=='КОНСТРУКЦИИ':
        cat='rig' if re.search(r'Truss|hoist|Frame|Рама|лебед|Ферма',name) else 'stage'
    dm=None
    for rx,L,W,H,kg,st in DIMS:
        if re.search(rx,name): dm=(L,W,H,kg,st); break
    assert dm, name
    iid='eq-%03d'%(i+1)
    pub={'id':iid,'name':name,'cat':cat,'sub':sub.title() if sub.isupper() else sub,'qty':int(qty),'repair':0,'L':dm[0],'W':dm[1],'H':dm[2],'kg':dm[3],'stackable':bool(dm[4]),'loc':'','serials':'','note':'','dimsEst':True,'src':'Google Таблица «Тай - прайс, парк и амортизация»'}
    fin={'rate':int(rate or 0),'value':int(value or 0),'amort':int(amort or 0)}
    for coll,doc,data in (('items',iid,pub),('fin','item-'+iid,fin)):
        f='%s/%s-%s.json'%(D,coll,doc); json.dump(data,open(f,'w'),ensure_ascii=False)
        writes.append({'op':'set','collection':coll,'doc_id':doc,'file_path':f})
json.dump(writes,open(os.path.join(D,'..','writes.json'),'w'),ensure_ascii=False)
print(len(writes))
